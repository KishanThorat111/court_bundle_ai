import csv, os
from difflib import SequenceMatcher

GOLD_CSV   = "data/processed/gold_index.csv"
UPLOAD_DIR = "data/uploads"
OUT_CSV    = "data/processed/matched_files.csv"

# Load gold entries
gold_entries = []
with open(GOLD_CSV, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        gold_entries.append((int(row["order"]), row["title"].lower().strip()))

# List uploaded PDFs (excluding the index page)
uploads = [
    f for f in os.listdir(UPLOAD_DIR)
    if f.lower().endswith(".pdf") and not f.lower().startswith("1-")
]

def clean_filename(fname):
    name = os.path.splitext(fname)[0]
    name = name.replace("_", " ").replace("-", " ").lower()
    # remove leading number token (e.g. "2 claim form" → "claim form")
    parts = name.split()
    return " ".join(parts[1:]) if parts and parts[0].isdigit() else name

with open(OUT_CSV, "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)
    writer.writerow(["order", "gold_title", "matched_filename", "score"])

    for order, gold_title in gold_entries:
        # 1) Try a direct prefix match
        prefix = f"{order}-"
        direct = [f for f in uploads if f.lower().startswith(prefix)]
        if direct:
            writer.writerow([order, gold_title, direct[0], "1.00"])
            continue

        # 2) Fallback to fuzzy match
        best, best_score = None, 0.0
        for fname in uploads:
            score = SequenceMatcher(
                None,
                gold_title,
                clean_filename(fname)
            ).ratio()
            if score > best_score:
                best, best_score = fname, score

        writer.writerow([order, gold_title, best, f"{best_score:.2f}"])
        if best_score < 0.6:
            print(f"[!] LOW CONFIDENCE: {order} '{gold_title}' → '{best}' ({best_score:.2f})")

print(f"[✓] Order-based + fuzzy match done → {OUT_CSV}")

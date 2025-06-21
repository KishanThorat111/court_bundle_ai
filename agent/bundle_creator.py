# agent/bundle_creator.py

import fitz  # PyMuPDF
import csv
import os

MATCHED_CSV = "data/processed/matched_files.csv"
INDEX_PDF   = "data/processed/Index.pdf"
OUTPUT_PDF  = "data/processed/Final_Bundle.pdf"
UPLOAD_DIR  = "data/uploads"

# Step 1: Load matched files (excluding index)
files = []
with open(MATCHED_CSV, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        order = int(row["order"])
        if order == 1:
            continue  # skip index
        files.append((order, row["matched_filename"], row["gold_title"].title()))

# Step 2: Start new bundle and insert the index
bundle = fitz.open()
index_doc = fitz.open(INDEX_PDF)
bundle.insert_pdf(index_doc)
page_counter = index_doc.page_count

# Step 3: Insert documents and collect bookmarks & page references
toc = [[1, "INDEX", 1]]
index_map = []  # title → real start page

for order, filename, title in files:
    doc_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(doc_path):
        print(f"[!] File missing: {filename}")
        continue
    doc = fitz.open(doc_path)
    toc.append([1, title, page_counter + 1])
    index_map.append((title, page_counter + 1))
    bundle.insert_pdf(doc)
    page_counter += doc.page_count

# Step 4: Add bookmarks
bundle.set_toc(toc)

# Step 5: Update index page with real page numbers
index_page = bundle[0]
page_text = index_page.get_text("blocks")
lines = [block[4] for block in sorted(page_text, key=lambda b: -b[1])]  # top-down

# Replace placeholders by drawing real page numbers
for title, page_num in index_map:
    for i, line in enumerate(lines):
        if title.upper() in line.upper():
            y = sorted(page_text, key=lambda b: -b[1])[i][1]
            index_page.insert_text(
                (450, y),
                str(page_num),
                fontsize=10,
                fontname="helv",
                fill=(0, 0, 0)
            )
            break

# Step 6: Save final bundle
bundle.save(OUTPUT_PDF)
print(f"[✓] Final court bundle created → {OUTPUT_PDF}")

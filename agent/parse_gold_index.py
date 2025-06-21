# agent/parse_gold_index.py

import re
import csv
import pdfplumber

INPUT_PDF = "data/uploads/1-Index.pdf"
OUTPUT_CSV = "data/processed/gold_index.csv"

entries = []

with pdfplumber.open(INPUT_PDF) as pdf:
    text = pdf.pages[0].extract_text()

lines = text.split("\n")

for line in lines:
    # Match lines like: 1 Index 1  OR 2 Claim Form 2–8
    match = re.match(r"^\s*(\d{1,2})\s+(.+?)\s+(\d{1,3}(?:[-–]\d{1,3})?)\s*$", line)
    if match:
        s_no, title, page_range = match.groups()
        entries.append({
            "order": int(s_no),
            "title": title.strip(),
            "page_range": page_range.strip()
        })

# Write to CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["order", "title", "page_range"])
    writer.writeheader()
    writer.writerows(entries)

print(f"[✓] Extracted {len(entries)} index items → {OUTPUT_CSV}")

# agent/generate_index.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import csv

MATCHED_CSV = "data/processed/matched_files.csv"
OUTPUT_PDF  = "data/processed/Index.pdf"

# Read matched entries, skip order 1 (the index itself)
entries = []
with open(MATCHED_CSV, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if int(row["order"]) == 1:
            continue
        entries.append((int(row["order"]), row["gold_title"].title(), "##"))  # placeholder

# Create PDF
c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)
w, h = A4

c.setFont("Helvetica-Bold", 16)
c.drawCentredString(w/2, h-40, "INDEX")

c.setFont("Helvetica", 11)
y = h - 80
c.drawString(40, y, "S.No")
c.drawString(100, y, "Description")
c.drawString(450, y, "Page No")
y -= 20

for order, title, page in entries:
    if y < 50:
        c.showPage()
        c.setFont("Helvetica", 11)
        y = h - 50
    c.drawString(40, y, str(order))
    c.drawString(100, y, title)
    c.drawString(450, y, page)
    y -= 18

c.save()
print(f"[✓] Created index page → {OUTPUT_PDF}")

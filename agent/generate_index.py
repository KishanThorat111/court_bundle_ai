# agent/generate_index.py

import csv
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Paths
GOLD_CSV = "data/processed/gold_index.csv"
OUTPUT_PDF = "data/processed/Index.pdf"

# Load gold index data
entries = []
with open(GOLD_CSV, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        entries.append([
            row["order"],
            row["title"].replace("\u2019", "'").replace("\u2013", "-"),
            row["page_range"]
        ])

# Setup styles
styles = getSampleStyleSheet()
style_normal = ParagraphStyle(
    'Normal', parent=styles['Normal'],
    fontName='Helvetica', fontSize=9, leading=11
)
style_center = ParagraphStyle(
    'Center', parent=style_normal,
    alignment=1  # center
)
style_right = ParagraphStyle(
    'Right', parent=style_normal,
    alignment=2  # right
)
style_bold_center = ParagraphStyle(
    'Header', parent=style_center,
    fontName='Helvetica-Bold'
)

# Table data
table_data = [[
    Paragraph("S.No", style_bold_center),
    Paragraph("Description", style_bold_center),
    Paragraph("Page No", style_bold_center)
]]

for row in entries:
    table_data.append([
        Paragraph(row[0], style_center),
        Paragraph(row[1], style_normal),
        Paragraph(row[2], style_right)
    ])

# Table definition
table = Table(table_data, colWidths=[25*mm, 130*mm, 25*mm], repeatRows=1)

# Apply styling
table.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 1), (0, -1), 'CENTER'),   # S.No column
    ('ALIGN', (1, 1), (1, -1), 'LEFT'),     # Description
    ('ALIGN', (2, 1), (2, -1), 'RIGHT'),    # Page No
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
]))

# Document setup
doc = SimpleDocTemplate(
    OUTPUT_PDF,
    pagesize=A4,
    rightMargin=20*mm,
    leftMargin=20*mm,
    topMargin=25*mm,
    bottomMargin=20*mm
)

elements = [
    Paragraph("INDEX", ParagraphStyle(name='Title', fontSize=16, fontName='Helvetica-Bold', alignment=1)),
    Spacer(1, 10 * mm),
    table
]

# Save PDF
doc.build(elements)
print(f"[\u2713] Professional index created with aligned table \u2192 {OUTPUT_PDF}")

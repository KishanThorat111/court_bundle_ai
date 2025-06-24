# # agent/generate_index.py

# import csv
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.units import mm
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# # Paths
# GOLD_CSV = "data/processed/gold_index.csv"
# OUTPUT_PDF = "data/processed/Index.pdf"

# # Load gold index data
# entries = []
# with open(GOLD_CSV, encoding="utf-8") as f:
#     for row in csv.DictReader(f):
#         entries.append([
#             row["order"],
#             row["title"].replace("\u2019", "'").replace("\u2013", "-"),
#             row["page_range"]
#         ])

# # Setup styles
# styles = getSampleStyleSheet()
# style_normal = ParagraphStyle(
#     'Normal', parent=styles['Normal'],
#     fontName='Helvetica', fontSize=9, leading=11
# )
# style_center = ParagraphStyle(
#     'Center', parent=style_normal,
#     alignment=1  # center
# )
# style_right = ParagraphStyle(
#     'Right', parent=style_normal,
#     alignment=2  # right
# )
# style_bold_center = ParagraphStyle(
#     'Header', parent=style_center,
#     fontName='Helvetica-Bold'
# )

# # Table data
# table_data = [[
#     Paragraph("S.No", style_bold_center),
#     Paragraph("Description", style_bold_center),
#     Paragraph("Page No", style_bold_center)
# ]]

# for row in entries:
#     table_data.append([
#         Paragraph(row[0], style_center),
#         Paragraph(row[1], style_normal),
#         Paragraph(row[2], style_right)
#     ])

# # Table definition
# table = Table(table_data, colWidths=[25*mm, 130*mm, 25*mm], repeatRows=1)

# # Apply styling
# table.setStyle(TableStyle([
#     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
#     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#     ('FONTSIZE', (0, 0), (-1, -1), 9),
#     ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#     ('ALIGN', (0, 1), (0, -1), 'CENTER'),   # S.No column
#     ('ALIGN', (1, 1), (1, -1), 'LEFT'),     # Description
#     ('ALIGN', (2, 1), (2, -1), 'RIGHT'),    # Page No
#     ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
#     ('TOPPADDING', (0, 0), (-1, -1), 5),
# ]))

# # Document setup
# doc = SimpleDocTemplate(
#     OUTPUT_PDF,
#     pagesize=A4,
#     rightMargin=20*mm,
#     leftMargin=20*mm,
#     topMargin=25*mm,
#     bottomMargin=20*mm
# )

# elements = [
#     Paragraph("INDEX", ParagraphStyle(name='Title', fontSize=16, fontName='Helvetica-Bold', alignment=1)),
#     Spacer(1, 10 * mm),
#     table
# ]

# # Save PDF
# doc.build(elements)
# print(f"[\u2713] Professional index created with aligned table \u2192 {OUTPUT_PDF}")











# agent/generate_index.py

import csv
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Line

# Paths
GOLD_CSV = "data/processed/gold_index.csv"
OUTPUT_PDF = "data/processed/Index.pdf"

# # Client-provided inputs
# CLAIM_NO = "Claim No: M00CM402"
# COURT_NAME = "Chelmsford County Court"
# CLAIMANTS = ["Mr. Murali Narne (1)", "Mrs. Bharathi Narne (2)"]
# DEFENDANTS = ["Sandra Kim Durdin (1)", "Trevor Graham Dempsey (2)"]


# Load extracted metadata
with open("data/processed/extracted_metadata.json", encoding="utf-8") as f:
    meta = json.load(f)

CLAIM_NO = meta["CLAIM_NO"]
COURT_NAME = meta["COURT_NAME"]
CLAIMANTS = meta["CLAIMANTS"]
DEFENDANTS = meta["DEFENDANTS"]


# Load gold index entries
entries = []
with open(GOLD_CSV, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        entries.append([
            row["order"],
            row["title"].replace("\u2019", "'").replace("\u2013", "-"),
            row["page_range"]
        ])

# Define styles
styles = getSampleStyleSheet()
style_normal = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10, leading=13)
style_center = ParagraphStyle('Center', parent=style_normal, alignment=1)
style_right = ParagraphStyle('Right', parent=style_normal, alignment=2)
style_left = ParagraphStyle('Left', parent=style_normal, alignment=0)
style_bold = ParagraphStyle('Bold', parent=style_normal, fontName='Helvetica-Bold')
style_bold_center = ParagraphStyle('BoldCenter', parent=style_center, fontName='Helvetica-Bold')
style_bold_left = ParagraphStyle('BoldLeft', parent=style_left, fontName='Helvetica-Bold')
style_bold_right = ParagraphStyle('BoldRight', parent=style_right, fontName='Helvetica-Bold')
style_title = ParagraphStyle('Title', parent=style_bold_center, fontSize=14, spaceAfter=4*mm)
style_header = ParagraphStyle('Header', parent=style_bold_center, fontSize=12, spaceAfter=2*mm)
style_meta = ParagraphStyle('MetaRight', parent=style_bold_right, fontSize=10)

# Start building the index table
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

# Table setup
table = Table(table_data, colWidths=[25*mm, 130*mm, 25*mm], repeatRows=1)
table.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 1), (0, -1), 'CENTER'),   # S.No
    ('ALIGN', (1, 1), (1, -1), 'LEFT'),     # Description
    ('ALIGN', (2, 1), (2, -1), 'RIGHT'),    # Page No
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Grey background for header
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),       # Text color for header
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
]))

# Document setup
doc = SimpleDocTemplate(
    OUTPUT_PDF,
    pagesize=A4,
    rightMargin=20*mm,
    leftMargin=20*mm,
    topMargin=20*mm,
    bottomMargin=20*mm
)

# Compose the layout
elements = []

# Claim No (top right)
elements.append(Paragraph(CLAIM_NO, style_meta))
elements.append(Spacer(1, 3 * mm))

# Court Name (left aligned, bold)
elements.append(Paragraph("IN THE " + COURT_NAME, style_bold_left))
elements.append(Spacer(1, 3 * mm))

# BETWEEN line
elements.append(Paragraph("BETWEEN:", style_bold_left))
elements.append(Spacer(1, 2 * mm))

# Claimants (centered)
for claimant in CLAIMANTS:
    elements.append(Paragraph(claimant, style_bold_center))
elements.append(Spacer(1, 2 * mm))
elements.append(Paragraph("Claimants", style_right))
elements.append(Spacer(1, 2 * mm))

# Vs line
elements.append(Paragraph("-Vs-", style_center))
elements.append(Spacer(1, 2 * mm))

# Defendants (centered)
for defendant in DEFENDANTS:
    elements.append(Paragraph(defendant, style_bold_center))
elements.append(Spacer(1, 2 * mm))
elements.append(Paragraph("Defendant(s)", style_right))
elements.append(Spacer(1, 10 * mm))

# Line above INDEX
line_above = Drawing(0, 1)
line_above.add(Line(0, 0, A4[0] - 40*mm, 0, strokeColor=colors.black, strokeWidth=1.5))
elements.append(line_above)
elements.append(Spacer(1, 2 * mm))

# INDEX title and table
elements.append(Paragraph("INDEX", style_title))
elements.append(Spacer(1, 2 * mm))

# Line below INDEX
line_below = Drawing(0, 1)
line_below.add(Line(0, 0, A4[0] - 40*mm, 0, strokeColor=colors.black, strokeWidth=1.5))
elements.append(line_below)
elements.append(Spacer(1, 6 * mm))

elements.append(table)

# Build PDF
doc.build(elements)
print(f"[OK] Professionally styled index generated -> {OUTPUT_PDF}")







# # agent/generate_index.py

# import csv
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.units import mm
# from reportlab.platypus import (
#     SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
# )
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# # Paths
# GOLD_CSV = "data/processed/gold_index.csv"
# OUTPUT_PDF = "data/processed/Index.pdf"

# # Client-provided inputs
# CLAIM_NO = "Claim No: M00CM402"
# COURT_NAME = "Chelmsford County Court"
# CLAIMANTS = ["Mr. Murali Narne (1)", "Mrs. Bharathi Narne (2)"]
# DEFENDANTS = ["Sandra Kim Durdin (1)", "Trevor Graham Dempsey (2)"]

# # Load gold index entries
# entries = []
# with open(GOLD_CSV, encoding="utf-8") as f:
#     for row in csv.DictReader(f):
#         entries.append([
#             row["order"],
#             row["title"].replace("\u2019", "'").replace("\u2013", "-"),
#             row["page_range"]
#         ])

# # Define styles
# styles = getSampleStyleSheet()
# style_normal = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10, leading=13)
# style_center = ParagraphStyle('Center', parent=style_normal, alignment=1)
# style_right = ParagraphStyle('Right', parent=style_normal, alignment=2)
# style_left = ParagraphStyle('Left', parent=style_normal, alignment=0)
# style_bold = ParagraphStyle('Bold', parent=style_normal, fontName='Helvetica-Bold')
# style_bold_center = ParagraphStyle('BoldCenter', parent=style_center, fontName='Helvetica-Bold')
# style_bold_left = ParagraphStyle('BoldLeft', parent=style_left, fontName='Helvetica-Bold')
# style_bold_right = ParagraphStyle('BoldRight', parent=style_right, fontName='Helvetica-Bold')
# style_title = ParagraphStyle('Title', parent=style_bold_center, fontSize=14, spaceAfter=4*mm)
# style_header = ParagraphStyle('Header', parent=style_bold_center, fontSize=12, spaceAfter=2*mm)
# style_meta = ParagraphStyle('MetaRight', parent=style_bold_right, fontSize=10)

# # Start building the index table
# table_data = [[
#     Paragraph("S.No", style_bold_center),
#     Paragraph("Description", style_bold_center),
#     Paragraph("Page No", style_bold_center)
# ]]

# for row in entries:
#     table_data.append([
#         Paragraph(row[0], style_center),
#         Paragraph(row[1], style_normal),
#         Paragraph(row[2], style_right)
#     ])

# # Table setup
# table_widths = [25*mm, 130*mm, 25*mm]
# table = Table(table_data, colWidths=table_widths, repeatRows=1)
# table.setStyle(TableStyle([
#     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
#     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#     ('FONTSIZE', (0, 0), (-1, -1), 9),
#     ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#     ('ALIGN', (0, 1), (0, -1), 'CENTER'),   # S.No
#     ('ALIGN', (1, 1), (1, -1), 'LEFT'),     # Description
#     ('ALIGN', (2, 1), (2, -1), 'RIGHT'),    # Page No
#     ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Grey background for header
#     ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),       # Text color for header
#     ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
#     ('TOPPADDING', (0, 0), (-1, -1), 5),
# ]))

# # Document setup
# doc = SimpleDocTemplate(
#     OUTPUT_PDF,
#     pagesize=A4,
#     rightMargin=20*mm,
#     leftMargin=20*mm,
#     topMargin=20*mm,
#     bottomMargin=20*mm
# )

# # Compose the layout
# elements = []

# # Claim No (top right)
# elements.append(Paragraph(CLAIM_NO, style_meta))
# elements.append(Spacer(1, 3 * mm))

# # Court Name (left aligned, bold)
# elements.append(Paragraph("IN THE " + COURT_NAME, style_bold_left))
# elements.append(Spacer(1, 3 * mm))

# # BETWEEN line
# elements.append(Paragraph("BETWEEN:", style_bold_left))
# elements.append(Spacer(1, 2 * mm))

# # Claimants (centered)
# for claimant in CLAIMANTS:
#     elements.append(Paragraph(claimant, style_bold_center))
# elements.append(Spacer(1, 2 * mm))
# elements.append(Paragraph("Claimants", style_right))
# elements.append(Spacer(1, 2 * mm))

# # Vs line
# elements.append(Paragraph("-Vs-", style_center))
# elements.append(Spacer(1, 2 * mm))

# # Defendants (centered)
# for defendant in DEFENDANTS:
#     elements.append(Paragraph(defendant, style_bold_center))
# elements.append(Spacer(1, 2 * mm))
# elements.append(Paragraph("Defendant(s)", style_right))
# elements.append(Spacer(1, 10 * mm))

# # INDEX title and lines
# elements.append(HRFlowable(width=sum(table_widths), thickness=1.5, color=colors.black, spaceBefore=1*mm, spaceAfter=2*mm))
# elements.append(Paragraph("INDEX", style_title))
# elements.append(HRFlowable(width=sum(table_widths), thickness=1.5, color=colors.black, spaceBefore=2*mm, spaceAfter=6*mm))
# elements.append(table)

# # Build PDF
# doc.build(elements)
# print(f"[✓] Professionally styled index generated → {OUTPUT_PDF}")

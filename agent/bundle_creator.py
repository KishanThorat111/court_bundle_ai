# agent/bundle_creator.py

import fitz  # PyMuPDF
import csv
import os

MATCHED_CSV = "data/processed/matched_files.csv"
INDEX_PDF = "data/processed/Index.pdf"
OUTPUT_PDF = "data/processed/Final_Bundle.pdf"
UPLOAD_DIR = "data/uploads"

A4 = fitz.paper_size("a4")

# Step 1: Load matched files
files = []
with open(MATCHED_CSV, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        order = int(row["order"])
        title = row["gold_title"].replace("’", "'").replace("–", "-").replace("#", "").strip().title()
        if order == 1:
            index_entry = (order, row["matched_filename"], title)
        else:
            files.append((order, row["matched_filename"], title))

# Step 2: Start bundle and insert Index.pdf exactly as-is
bundle = fitz.open()
index_doc = fitz.open(INDEX_PDF)
bundle.insert_pdf(index_doc)  # Keep original layout

# Init TOC and map
toc = [[1, "INDEX", 1]]
index_map = [("Index", 1)]

# Step 3: Insert other documents with A4 scaling
for order, filename, title in sorted(files):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        print(f"[!] Missing: {filename}")
        continue

    src_doc = fitz.open(path)
    real_start_page = bundle.page_count + 1

    for page in src_doc:
        new_doc = fitz.open()
        new_page = new_doc.new_page(width=A4[0], height=A4[1])

        src_rect = page.rect
        scale = min(A4[0] / src_rect.width, A4[1] / src_rect.height)

        new_width = src_rect.width * scale
        new_height = src_rect.height * scale
        dx = (A4[0] - new_width) / 2
        dy = (A4[1] - new_height) / 2
        target_rect = fitz.Rect(dx, dy, dx + new_width, dy + new_height)

        new_page.show_pdf_page(target_rect, src_doc, page.number)
        bundle.insert_pdf(new_doc)

    toc.append([1, title, real_start_page])
    index_map.append((title, real_start_page))

# Step 4: Add bookmarks
bundle.set_toc(toc)

# Step 5: Insert bottom-right page numbers (remove old if any)
for i in range(bundle.page_count):
    page = bundle[i]
    number = str(i + 1)

    # Erase corner region (top-right and bottom-right area)
    page.draw_rect(fitz.Rect(A4[0] - 80, 0, A4[0], 50), color=(1, 1, 1), fill=(1, 1, 1))        # top-right
    page.draw_rect(fitz.Rect(A4[0] - 80, A4[1] - 40, A4[0], A4[1]), color=(1, 1, 1), fill=(1, 1, 1))  # bottom-right

    # Insert new number at bottom-right corner
    text_width = fitz.get_text_length(number, fontsize=9)
    x = A4[0] - text_width - 30  # 30pt from right
    y = A4[1] - 20               # 20pt from bottom
    page.insert_text((x, y), number, fontsize=9, color=(0, 0, 0))

# Step 6: Add hyperlinks to index entries (clickable)
index_page = bundle[0]
for title, page_num in index_map:
    if page_num == 1:
        continue  # Don't link to index itself

    for block in index_page.get_text("blocks"):
        block_text = block[4].replace("’", "'").replace("–", "-").replace("#", "").strip().lower()
        if title.lower() in block_text:
            x0, y0, x1, y1 = block[:4]
            index_page.insert_link({
                "kind": fitz.LINK_GOTO,
                "page": page_num - 1,  # 0-based index
                "from": fitz.Rect(x0, y0, x1, y1),
                "zoom": 0
            })
            break

# Step 7: Save final bundle
bundle.save(OUTPUT_PDF)
print(f"[✓] Final bundle created → {OUTPUT_PDF} (hyperlinked index, bookmarks, A4 scaled)")

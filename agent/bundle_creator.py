# # agent/bundle_creator.py

# import fitz  # PyMuPDF
# import csv
# import os

# MATCHED_CSV = "data/processed/matched_files.csv"
# INDEX_PDF = "data/processed/Index.pdf"
# OUTPUT_PDF = "data/processed/Final_Bundle.pdf"
# UPLOAD_DIR = "data/uploads"

# A4 = fitz.paper_size("a4")

# # Step 1: Load matched files
# files = []
# with open(MATCHED_CSV, encoding="utf-8") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         order = int(row["order"])
#         title = row["gold_title"].replace("’", "'").replace("–", "-").replace("#", "").strip().title()
#         if order == 1:
#             index_entry = (order, row["matched_filename"], title)
#         else:
#             files.append((order, row["matched_filename"], title))

# # Step 2: Start bundle and insert Index.pdf exactly as-is
# bundle = fitz.open()
# index_doc = fitz.open(INDEX_PDF)
# bundle.insert_pdf(index_doc)  # Keep original layout

# # Init TOC and map
# toc = [[1, "INDEX", 1]]
# index_map = [("Index", 1)]

# # Step 3: Insert other documents with A4 scaling
# for order, filename, title in sorted(files):
#     path = os.path.join(UPLOAD_DIR, filename)
#     if not os.path.exists(path):
#         print(f"[!] Missing: {filename}")
#         continue

#     src_doc = fitz.open(path)
#     real_start_page = bundle.page_count + 1

#     for page in src_doc:
#         new_doc = fitz.open()
#         new_page = new_doc.new_page(width=A4[0], height=A4[1])

#         src_rect = page.rect
#         scale = min(A4[0] / src_rect.width, A4[1] / src_rect.height)

#         new_width = src_rect.width * scale
#         new_height = src_rect.height * scale
#         dx = (A4[0] - new_width) / 2
#         dy = (A4[1] - new_height) / 2
#         target_rect = fitz.Rect(dx, dy, dx + new_width, dy + new_height)

#         new_page.show_pdf_page(target_rect, src_doc, page.number)
#         bundle.insert_pdf(new_doc)

#     toc.append([1, title, real_start_page])
#     index_map.append((title, real_start_page))

# # Step 4: Add bookmarks
# bundle.set_toc(toc)

# # Step 5: Insert bottom-right page numbers (remove old if any)
# for i in range(bundle.page_count):
#     page = bundle[i]
#     number = str(i + 1)

#     # Erase corner region (top-right and bottom-right area)
#     page.draw_rect(fitz.Rect(A4[0] - 80, 0, A4[0], 50), color=(1, 1, 1), fill=(1, 1, 1))        # top-right
#     page.draw_rect(fitz.Rect(A4[0] - 80, A4[1] - 40, A4[0], A4[1]), color=(1, 1, 1), fill=(1, 1, 1))  # bottom-right

#     # Insert new number at bottom-right corner
#     text_width = fitz.get_text_length(number, fontsize=9)
#     x = A4[0] - text_width - 30  # 30pt from right
#     y = A4[1] - 20               # 20pt from bottom
#     page.insert_text((x, y), number, fontsize=9, color=(0, 0, 0))

# # Step 6: Add hyperlinks to index entries (clickable)
# index_page = bundle[0]
# for title, page_num in index_map:
#     if page_num == 1:
#         continue  # Don't link to index itself

#     for block in index_page.get_text("blocks"):
#         block_text = block[4].replace("’", "'").replace("–", "-").replace("#", "").strip().lower()
#         if title.lower() in block_text:
#             x0, y0, x1, y1 = block[:4]
#             index_page.insert_link({
#                 "kind": fitz.LINK_GOTO,
#                 "page": page_num-2,  # 0-based index
#                 "from": fitz.Rect(x0, y0, x1, y1),
#                 "zoom": 0
#             })
#             break

# # Step 7: Save final bundle
# bundle.save(OUTPUT_PDF)
# print(f"[✓] Final bundle created → {OUTPUT_PDF} (hyperlinked index, bookmarks, A4 scaled)")
# agent/bundle_creator.py

# import fitz  # PyMuPDF
# import csv
# import os

# MATCHED_CSV = "data/processed/matched_files.csv"
# INDEX_PDF = "data/processed/Index.pdf"
# OUTPUT_PDF = "data/processed/Final_Bundle.pdf"
# UPLOAD_DIR = "data/uploads"

# a4_width, a4_height = fitz.paper_size("a4")

# # Step 1: Load matched files
# files = []
# with open(MATCHED_CSV, encoding="utf-8") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         order = int(row["order"])
#         title = row["gold_title"].replace("’", "'").replace("–", "-").replace("#", "").strip().title()
#         if order == 1:
#             index_entry = (order, row["matched_filename"], title)
#         else:
#             files.append((order, row["matched_filename"], title))

# # Step 2: Build file map and page map
# page_map = []  # (order, title, start_page, page_count)
# bundle = fitz.open()
# index_doc = fitz.open(INDEX_PDF)
# index_start_page = bundle.page_count + 1
# bundle.insert_pdf(index_doc)
# index_page_count = index_doc.page_count

# # Append all other documents and track real page numbers
# for order, filename, title in sorted(files):
#     path = os.path.join(UPLOAD_DIR, filename)
#     if not os.path.exists(path):
#         print(f"[!] Missing: {filename}")
#         continue

#     src_doc = fitz.open(path)
#     start_page = bundle.page_count + 1

#     for page in src_doc:
#         new_doc = fitz.open()
#         new_page = new_doc.new_page(width=a4_width, height=a4_height)

#         src_rect = page.rect
#         scale = min(a4_width / src_rect.width, a4_height / src_rect.height)
#         new_width = src_rect.width * scale
#         new_height = src_rect.height * scale
#         dx = (a4_width - new_width) / 2
#         dy = (a4_height - new_height) / 2
#         target_rect = fitz.Rect(dx, dy, dx + new_width, dy + new_height)

#         new_page.show_pdf_page(target_rect, src_doc, page.number)
#         bundle.insert_pdf(new_doc)

#     page_count = src_doc.page_count
#     page_map.append((order, title, start_page, page_count))

# # Step 3: Rewrite gold_index.csv with correct calculated page ranges
# with open("data/processed/gold_index.csv", "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(["order", "title", "page_range"])
#     writer.writerow(["1", "Index", f"{index_start_page}-{index_start_page + index_page_count - 1}"])
#     for order, title, start_page, count in page_map:
#         end_page = start_page + count - 1
#         page_range = f"{start_page}" if count == 1 else f"{start_page}-{end_page}"
#         writer.writerow([order, title, page_range])

# # Step 4: Add TOC
# toc = [[1, "Index", index_start_page]]
# for _, title, start_page, _ in page_map:
#     toc.append([1, title, start_page])
# bundle.set_toc(toc)

# # Step 5: Insert bottom-right page numbers
# for i in range(bundle.page_count):
#     page = bundle[i]
#     number = str(i + 1)
#     page.draw_rect(fitz.Rect(a4_width - 80, 0, a4_width, 50), color=(1, 1, 1), fill=(1, 1, 1))
#     page.draw_rect(fitz.Rect(a4_width - 80, a4_height - 40, a4_width, a4_height), color=(1, 1, 1), fill=(1, 1, 1))
#     text_width = fitz.get_text_length(number, fontsize=9)
#     x = a4_width - text_width - 30
#     y = a4_height - 20
#     page.insert_text((x, y), number, fontsize=9, color=(0, 0, 0))

# # Step 6: Add hyperlinks across all index pages
# for i in range(index_start_page - 1, index_start_page - 1 + index_page_count):
#     index_page = bundle[i]
#     for title, start_page, _ in [(t, s, c) for _, t, s, c in page_map]:
#         for block in index_page.get_text("blocks"):
#             block_text = block[4].replace("’", "'").replace("–", "-").replace("#", "").strip().lower()
#             if title.lower() in block_text:
#                 x0, y0, x1, y1 = block[:4]
#                 index_page.insert_link({
#                     "kind": fitz.LINK_GOTO,
#                     "page": start_page - 1,
#                     "from": fitz.Rect(x0, y0, x1, y1),
#                     "zoom": 0
#                 })
#                 break

# # Step 7: Save bundle
# bundle.save(OUTPUT_PDF)
# print(f"[✓] Final bundle created → {OUTPUT_PDF} (pages recalculated and index updated)")




# agent/bundle_creator.py

import fitz  # PyMuPDF
import csv
import os

MATCHED_CSV = "data/processed/matched_files.csv"
INDEX_PDF = "data/processed/Index.pdf"
OUTPUT_PDF = "data/processed/Final_Bundle.pdf"
UPLOAD_DIR = "data/uploads"

a4_width, a4_height = fitz.paper_size("a4")

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

# Step 2: Build file map and page map
page_map = []  # (order, title, start_page, page_count)
bundle = fitz.open()
index_doc = fitz.open(INDEX_PDF)
index_start_page = bundle.page_count + 1
bundle.insert_pdf(index_doc)
index_page_count = index_doc.page_count

# Append all other documents and track real page numbers
for order, filename, title in sorted(files):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        print(f"[!] Missing: {filename}")
        continue

    src_doc = fitz.open(path)
    start_page = bundle.page_count + 1

    for page in src_doc:
        new_doc = fitz.open()
        new_page = new_doc.new_page(width=a4_width, height=a4_height)

        src_rect = page.rect
        scale = min(a4_width / src_rect.width, a4_height / src_rect.height)
        new_width = src_rect.width * scale
        new_height = src_rect.height * scale
        dx = (a4_width - new_width) / 2
        dy = (a4_height - new_height) / 2
        target_rect = fitz.Rect(dx, dy, dx + new_width, dy + new_height)

        new_page.show_pdf_page(target_rect, src_doc, page.number)
        bundle.insert_pdf(new_doc)

    page_count = src_doc.page_count
    page_map.append((order, title, start_page, page_count))

# Step 3: Rewrite gold_index.csv with correct calculated page ranges
with open("data/processed/gold_index.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["order", "title", "page_range"])
    writer.writerow(["1", "Index", f"{index_start_page}-{index_start_page + index_page_count - 1}"])
    for order, title, start_page, count in page_map:
        end_page = start_page + count - 1
        page_range = f"{start_page}" if count == 1 else f"{start_page}-{end_page}"
        writer.writerow([order, title, page_range])

# Step 4: Add TOC
toc = [[1, "Index", index_start_page]]
for _, title, start_page, _ in page_map:
    toc.append([1, title, start_page])
bundle.set_toc(toc)

# Step 5: Insert bottom-right page numbers
for i in range(bundle.page_count):
    page = bundle[i]
    number = str(i + 1)
    page.draw_rect(fitz.Rect(a4_width - 80, 0, a4_width, 50), color=(1, 1, 1), fill=(1, 1, 1))
    page.draw_rect(fitz.Rect(a4_width - 80, a4_height - 40, a4_width, a4_height), color=(1, 1, 1), fill=(1, 1, 1))
    text_width = fitz.get_text_length(number, fontsize=9)
    x = a4_width - text_width - 30
    y = a4_height - 20
    page.insert_text((x, y), number, fontsize=9, color=(0, 0, 0))

# Step 6: Add hyperlinks across all index pages
for i in range(index_start_page - 1, index_start_page - 1 + index_page_count):
    index_page = bundle[i]
    for title, start_page, _ in [(t, s, c) for _, t, s, c in page_map]:
        for block in index_page.get_text("blocks"):
            block_text = block[4].replace("’", "'").replace("–", "-").replace("#", "").strip().lower()
            if title.lower() in block_text:
                x0, y0, x1, y1 = block[:4]
                index_page.insert_link({
                    "kind": fitz.LINK_GOTO,
                    "page": start_page - 1,
                    "from": fitz.Rect(x0, y0, x1, y1),
                    "zoom": 0
                })
                break

# Step 7: Save bundle
bundle.save(OUTPUT_PDF)
print(f"[✓] Final bundle created → {OUTPUT_PDF} (pages recalculated and index updated)")

# # agent/bundle_creator.py

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
#         # Corrected line: Removed .title() to preserve original capitalization
#         title = row["gold_title"].replace("’", "'").replace("–", "-").replace("#", "").strip()
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
#             # This .lower() is only for matching and does not affect the stored title
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
OUTPUT_PDF_TEMPLATE = "data/processed/Final_Bundle_{}.pdf"
UPLOAD_DIR = "data/uploads"

CLAIM_NO = "M00CM402"  # You can dynamically pass this if needed
OUTPUT_PDF = OUTPUT_PDF_TEMPLATE.format(CLAIM_NO.replace(" ", "_"))

a4_width, a4_height = fitz.paper_size("a4")

# Step 1: Load matched files
files = []
with open(MATCHED_CSV, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        order = int(row["order"])
        title = row["gold_title"].replace("’", "'").replace("–", "-").replace("#", "").strip()
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

        # Render original page onto new A4-sized blank page
        new_page.show_pdf_page(target_rect, src_doc, page.number)

        # # Remove old page numbers (top-right and bottom-right)
        # new_page.draw_rect(fitz.Rect(a4_width - 80, 0, a4_width, 50), color=(1, 1, 1), fill=(1, 1, 1))
        new_page.draw_rect(fitz.Rect(a4_width - 50, a4_height - 28, a4_width, a4_height), color=(1, 1, 1), fill=(1, 1, 1))

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

# Step 5: Insert bottom-right page numbers with transparent background, 16pt
for i in range(bundle.page_count):
    page = bundle[i]
    number = str(i + 1)
    text_width = fitz.get_text_length(number, fontsize=16)
    x = a4_width - text_width - 10
    y = a4_height - 10
    page.insert_text((x, y), number, fontsize=16, color=(0, 0, 0))



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


# import csv
# import os
# from difflib import SequenceMatcher

# GOLD_CSV = "data/processed/gold_index.csv"
# UPLOAD_DIR = "data/uploads"
# OUT_CSV = "data/processed/matched_files.csv"

# # Load gold entries, preserving the original title case
# gold_entries = []
# with open(GOLD_CSV, encoding="utf-8") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         # --- CHANGE 1: Store both the original title and a lowercase version for matching ---
#         original_title = row["title"].strip()
#         title_for_matching = original_title.lower()
#         gold_entries.append((int(row["order"]), original_title, title_for_matching))

# # List uploaded PDFs (excluding the index page)
# uploads = [
#     f for f in os.listdir(UPLOAD_DIR)
#     if f.lower().endswith(".pdf") and not f.lower().startswith("1-")
# ]

# def clean_filename(fname):
#     name = os.path.splitext(fname)[0]
#     name = name.replace("_", " ").replace("-", " ").lower()
#     # remove leading number token (e.g. "2 claim form" → "claim form")
#     parts = name.split()
#     return " ".join(parts[1:]) if parts and parts[0].isdigit() else name

# with open(OUT_CSV, "w", newline="", encoding="utf-8") as out:
#     writer = csv.writer(out)
#     writer.writerow(["order", "gold_title", "matched_filename", "score"])

#     # --- CHANGE 2: Unpack the tuple with three items ---
#     for order, original_title, title_for_matching in gold_entries:
#         # 1) Try a direct prefix match
#         prefix = f"{order}-"
#         direct = [f for f in uploads if f.lower().startswith(prefix)]
#         if direct:
#             # --- CHANGE 3: Write the original_title to the CSV ---
#             writer.writerow([order, original_title, direct[0], "1.00"])
#             continue

#         # 2) Fallback to fuzzy match
#         best, best_score = None, 0.0
#         for fname in uploads:
#             score = SequenceMatcher(
#                 None,
#                 # --- CHANGE 4: Use the lowercase version for matching ---
#                 title_for_matching,
#                 clean_filename(fname)
#             ).ratio()
#             if score > best_score:
#                 best, best_score = fname, score

#         # --- CHANGE 5: Write the original_title to the CSV here as well ---
#         writer.writerow([order, original_title, best, f"{best_score:.2f}"])
#         if best_score < 0.6:
#             # --- CHANGE 6: Use the original_title in the warning for clarity ---
#             print(f"[!] LOW CONFIDENCE: {order} '{original_title}' → '{best}' ({best_score:.2f})")

# print(f"[✓] Order-based + fuzzy match done → {OUT_CSV}")
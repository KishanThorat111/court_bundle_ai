# ocr_extract.py
import pytesseract
from pdf2image import convert_from_path
import sqlite3
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

DB = "courtbundles.db"
UPLOAD_DIR = "data\\uploads"

conn = sqlite3.connect(DB)

# Add `text` column if missing
existing_columns = [row[1] for row in conn.execute("PRAGMA table_info(documents)")]
if "text" not in existing_columns:
    conn.execute("ALTER TABLE documents ADD COLUMN text")

# Process PDFs
for doc_id, fname in conn.execute("SELECT id, filename FROM documents WHERE filename LIKE '%.pdf'"):
    pdf_path = os.path.join(UPLOAD_DIR, fname)
    pages = convert_from_path(
    pdf_path,
    dpi=300,
    poppler_path=r"C:\Program Files\poppler\Library\bin"
)

    full_text = ""
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        full_text += f"\n--- PAGE {i+1} ---\n{text}"
    conn.execute("UPDATE documents SET text = ? WHERE id = ?", (full_text, doc_id))
    print(f"OCR complete: {fname}")

conn.commit()
conn.close()

# convert_docx.py
from docx2pdf import convert
import os

UPLOAD_DIR = "data\\uploads"

for fname in os.listdir(UPLOAD_DIR):
    if fname.lower().endswith(".docx"):
        src = os.path.join(UPLOAD_DIR, fname)
        dst = os.path.join(UPLOAD_DIR, fname[:-5] + ".pdf")
        print(f"Converting {fname} → {os.path.basename(dst)}")
        convert(src, dst)

print("Done.")
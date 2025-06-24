# Court Bundle AI Generator

> An AI-powered Python tool to automatically generate UK civil court bundles from raw scanned or uploaded PDFs.

---

## 🚀 Overview

This project streamlines the creation of professional, hyperlinked, paginated court bundles. It replicates a gold-standard structure from a reference `1-Index.pdf`, matches supporting files using AI techniques, and outputs a clean, bookmarked PDF bundle suitable for legal submissions.

---

## 🗂 Project Structure

```
court_bundle_ai/
├── agent/
│   ├── bundle_creator.py        # Core logic to generate final bundle
│   ├── generate_index.py        # Builds and styles the final Index.pdf
│   ├── match_to_gold.py         # Fuzzy matching files to gold-standard index
│   ├── parse_gold_index.py      # Extracts structure from 1-Index.pdf
│   ├── extract_case_metadata.py # Extracts court, claimants, defendants info
│
├── tools/                       # Optional CLI tools
│   ├── convert_docx.py          # Converts DOCX to PDF
│   ├── ocr_extract.py           # Runs OCR on scanned files
│   └── intake.py                # Registers uploaded files to SQLite
│
├── data/
│   ├── processed/               # Auto-generated intermediate files
│   │   ├── gold_index.csv
│   │   ├── matched_files.csv
│   │   ├── extracted_metadata.json
│   │   ├── Index.pdf
│   ├── uploads/                 # Raw user files (e.g., 1-Index.pdf + other docs)
│       ├── 1-Index.pdf
│       ├── Claim Form.pdf, etc.
│
├── run.py                       # Single command runner
├── requirements.txt             # Python dependencies
├── .gitignore
├── README.md                    # You're reading this
```

---

## ✅ Features

* ✅ Parses `1-Index.pdf` for structure and page ranges
* ✅ Extracts metadata like Claim No, Court name, parties
* ✅ Fuzzy matches evidence/supporting PDFs to gold index
* ✅ Generates styled, table-formatted `Index.pdf`
* ✅ Inserts page numbers (16pt, bottom-right)
* ✅ Adds internal hyperlinks and bookmarks
* ✅ Output: `Final_Bundle_<ClaimNumber>.pdf`

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/KishanThorat111/court_bundle_ai
cd court_bundle_ai
```

### 2. Set Up Python Environment

```bash
python -m venv venv
venv\Scripts\activate     # on Windows
# or
source venv/bin/activate  # on macOS/Linux

pip install -r requirements.txt
```

### 3. Install System Dependencies

* ✅ [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (for OCR)
* ✅ [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/) (for `pdf2image`)

Ensure these are added to your system PATH.

---

## 📁 How to Use

### Step 1: Place Files

Put all court documents inside `data/uploads/`. Include `1-Index.pdf` as the gold reference structure.

### Step 2: Run the Agent

```bash
python run.py
```

This executes the full pipeline:

* Parses `1-Index.pdf`
* Extracts parties and claim info
* Matches and aligns other PDFs
* Generates styled index
* Creates final bundle: `data/processed/Final_Bundle_<ClaimNo>.pdf`

---

## 🧪 Optional Utilities (CLI)

* `python tools/convert_docx.py` → Converts DOCX to PDF
* `python tools/intake.py` → Registers files into SQLite
* `python tools/ocr_extract.py` → Runs OCR on unsearchable PDFs

---

## 💡 Notes for Deployment

* Keep `run.py` as your CLI entrypoint
* Use `.gitignore` to avoid committing `data/processed/`, `*.db`, and `venv/`
* Consider Dockerizing for future deployment

---

## 📬 Contact

Maintained by \[Kishan Thorat]. For inquiries, please raise an issue or email [kishanthorat111@outlook.com](mailto:kishanthorat111@outlook.com).

---

## 📄 License

MIT License. See `LICENSE` file.

import re
import pdfplumber
import json

INPUT_PDF = "data/uploads/1-Index.pdf"
OUTPUT_JSON = "data/processed/extracted_metadata.json"

metadata = {
    "CLAIM_NO": None,
    "COURT_NAME": None,
    "CLAIMANTS": [],
    "DEFENDANTS": []
}

with pdfplumber.open(INPUT_PDF) as pdf:
    text = pdf.pages[0].extract_text()

# Normalize newlines and remove blank lines
lines = [line.strip() for line in text.split("\n") if line.strip()]

# --- Extract Claim No ---
for line in lines:
    match = re.search(r"Claim\s+No[:\s]*([A-Z0-9]+)", line, re.IGNORECASE)
    if match:
        metadata["CLAIM_NO"] = f"Claim No: {match.group(1)}"
        break

# --- Extract Court Name ---
for line in lines:
    match = re.search(r"IN THE\s+(.+?Court)", line, re.IGNORECASE)
    if match:
        metadata["COURT_NAME"] = match.group(1).strip()
        break

# --- Extract Claimants and Defendants ---
claimant_lines = []
defendant_lines = []

# Locate BETWEEN and -Vs- section
between_index = next((i for i, line in enumerate(lines) if "BETWEEN" in line.upper()), None)
vs_index = next((i for i, line in enumerate(lines) if "-VS-" in line.upper() or "Vs" in line), None)

if between_index is not None and vs_index is not None:
    # Filter out unwanted labels like "Claimants"
    claimant_lines = [
        line for line in lines[between_index + 1 : vs_index]
        if not re.search(r"(claimant[s]?)", line, re.IGNORECASE)
    ]
    # Look ahead after -Vs- to get defendants
    for i in range(vs_index + 1, len(lines)):
        line = lines[i]
        if re.match(r"^\d+\s+", line):  # Stop at index table start
            break
        if not re.search(r"(defendant[s]?|index|description|page\s+no)", line, re.IGNORECASE):
            defendant_lines.append(line)

metadata["CLAIMANTS"] = claimant_lines
metadata["DEFENDANTS"] = defendant_lines

# ✅ Save cleaned JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print(f"[OK] Clean metadata extracted -> {OUTPUT_JSON}")

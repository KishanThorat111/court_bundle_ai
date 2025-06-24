# intake.py
import os, sqlite3, uuid, datetime

UPLOAD_DIR = "data\\uploads"
DB = "courtbundles.db"

# Connect or create database
conn = sqlite3.connect(DB)
conn.execute("""
CREATE TABLE IF NOT EXISTS documents (
  id TEXT PRIMARY KEY,
  filename TEXT,
  uploaded_at TEXT
)
""")
conn.commit()

# Insert each new file
for fname in os.listdir(UPLOAD_DIR):
    if fname.lower().endswith((".pdf", ".docx")):
        doc_id = str(uuid.uuid4())
        conn.execute("INSERT INTO documents(id, filename, uploaded_at) VALUES (?,?,?)",
                     (doc_id, fname, datetime.datetime.utcnow().isoformat()))
        print(f"Registered: {fname}")
conn.commit()
conn.close()

print("Done.")
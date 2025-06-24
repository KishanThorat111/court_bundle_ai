# run.py (corrected)

import subprocess
import sys

steps = [
    "agent/parse_gold_index.py",
    "agent/extract_case_metadata.py",
    "agent/match_to_gold.py",
    "agent/generate_index.py",     # ✅ Move this up before bundling
    "agent/bundle_creator.py"
]

for script in steps:
    print(f"\n[🚀] Running: {script}")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("[⚠️ STDERR]", result.stderr)
    if result.returncode != 0:
        print(f"[❌] Failed: {script}")
        break
else:
    print("\n✅ All steps completed successfully!")

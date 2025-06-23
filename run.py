# run.py

import os
import subprocess

def run_script(script_name):
    print(f"\n[🔧] Running: {script_name}")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("[⚠️ STDERR]")
        print(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"{script_name} failed with exit code {result.returncode}")

try:
    # Step 1: Build bundle & update gold_index.csv
    run_script("agent/bundle_creator.py")

    # Step 2: Regenerate index with updated page numbers
    run_script("agent/generate_index.py")

    # Step 3: Final bundle rebuild with new index page
    run_script("agent/bundle_creator.py")

    print("\n✅ Bundle generation complete: final version now has accurate page numbers and index links.")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
#!/usr/bin/env python3
"""
Apply the two small source fixes used by this demo.

Run from the root of the tobii-pytracker checkout.

1. Read YAML files explicitly as UTF-8.
2. Rename the built-in fallback response from "none" to "nie wiem"
   in all dataset classes.

The script is idempotent.
"""

from pathlib import Path
import sys

ROOT = Path.cwd()

config_file = ROOT / "src/tobii_pytracker/configs/custom_config.py"
dataset_file = ROOT / "src/tobii_pytracker/datasets/custom_dataset.py"

errors = []

if not config_file.exists():
    errors.append(f"Missing: {config_file}")
else:
    text = config_file.read_text(encoding="utf-8")
    old = 'with open(filename, "r") as f:'
    new = 'with open(filename, "r", encoding="utf-8") as f:'

    if new in text:
        print("[OK] YAML UTF-8 fix already present.")
    elif old in text:
        config_file.write_text(text.replace(old, new, 1), encoding="utf-8")
        print("[CHANGED] YAML files are now read explicitly as UTF-8.")
    else:
        print("[WARN] Expected YAML loading line was not found.")

if not dataset_file.exists():
    errors.append(f"Missing: {dataset_file}")
else:
    text = dataset_file.read_text(encoding="utf-8")
    old = 'self.classes.append("none")'
    new = 'self.classes.append("nie wiem")'

    count = text.count(old)

    if count:
        dataset_file.write_text(text.replace(old, new), encoding="utf-8")
        print(f'[CHANGED] Replaced {count} occurrence(s) of "none" with "nie wiem".')
    elif new in text:
        print('[OK] "nie wiem" fallback response already present.')
    else:
        print("[WARN] No fallback response line was found.")

if errors:
    for error in errors:
        print("[ERROR]", error)
    sys.exit(1)

print("\nReview changes with:")
print("  git diff")

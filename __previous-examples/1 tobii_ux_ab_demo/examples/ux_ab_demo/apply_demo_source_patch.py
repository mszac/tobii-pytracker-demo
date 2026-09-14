#!/usr/bin/env python3
"""
Apply two small source-level fixes to a checkout of tobii-pytracker/psychopy:

1. Read YAML configuration explicitly as UTF-8.
2. Rename the TextDataset fallback button from "none" to "nie wiem".

Run from the repository root:
    python examples/ux_ab_demo/apply_demo_source_patch.py

Afterwards inspect `git diff` and commit the changes to your fork.
"""

from pathlib import Path
import sys

ROOT = Path.cwd()

changes = [
    (
        ROOT / "src/tobii_pytracker/configs/custom_config.py",
        'with open(filename, "r") as f:',
        'with open(filename, "r", encoding="utf-8") as f:',
        "UTF-8 YAML loading",
    ),
    (
        ROOT / "src/tobii_pytracker/datasets/custom_dataset.py",
        'self.classes.append("none")',
        'self.classes.append("nie wiem")',
        'TextDataset button "none" -> "nie wiem"',
    ),
]

failed = False

for path, old, new, description in changes:
    if not path.exists():
        print(f"[ERROR] Missing: {path}")
        failed = True
        continue

    text = path.read_text(encoding="utf-8")

    if new in text:
        print(f"[OK] Already applied: {description}")
        continue

    if old not in text:
        print(f"[ERROR] Expected source fragment not found for: {description}")
        print(f"        File: {path}")
        failed = True
        continue

    # Only one replacement is intended here.
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    print(f"[CHANGED] {description}")

if failed:
    sys.exit(1)

print("\nDone. Review the changes with:")
print("  git diff")
print("\nThen reinstall the editable/local package if needed:")
print("  pip install -e .")

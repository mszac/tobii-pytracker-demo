#!/usr/bin/env python3
"""
Apply repository-level fixes used by the text demos.

Run from the root of the tobii-pytracker checkout BEFORE the first `pip install .`
(or once when maintaining your fork).

Changes:
1. Explicit UTF-8 when reading YAML config files.
2. TextDataset fallback class: "none" -> "nie wiem".
3. Explicit UTF-8 when reading text CSV datasets.

After applying, inspect `git diff` and commit these source changes to your fork.
"""

from pathlib import Path
import sys

root = Path.cwd()

changes = [
    (
        root / "src/tobii_pytracker/configs/custom_config.py",
        'with open(filename, "r") as f:',
        'with open(filename, "r", encoding="utf-8") as f:',
        "CustomConfig YAML UTF-8",
    ),
    (
        root / "src/tobii_pytracker/datasets/custom_dataset.py",
        'df = pd.read_csv(self.dataset_path, header=0)',
        'df = pd.read_csv(self.dataset_path, header=0, encoding="utf-8")',
        "TextDataset CSV UTF-8",
    ),
    (
        root / "src/tobii_pytracker/datasets/custom_dataset.py",
        'self.classes.append("none")',
        'self.classes.append("nie wiem")',
        'TextDataset "none" -> "nie wiem"',
    ),
]

failed = False

for path, old, new, label in changes:
    if not path.exists():
        print(f"[ERROR] Brak pliku: {path}")
        failed = True
        continue

    text = path.read_text(encoding="utf-8")

    if new in text:
        print(f"[OK] Już zastosowano: {label}")
        continue

    if old not in text:
        print(f"[ERROR] Nie znaleziono oczekiwanego fragmentu: {label}")
        print(f"        {path}")
        failed = True
        continue

    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"[CHANGED] {label}")

if failed:
    sys.exit(1)

print("\nGotowe. Sprawdź zmiany:")
print("  git diff")
print("\nJeżeli to pierwsza instalacja forka, dopiero teraz wykonaj:")
print("  pip install .")
print("\nPodczas developmentu możesz użyć:")
print("  pip install -e .")

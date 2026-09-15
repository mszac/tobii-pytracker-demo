from __future__ import annotations

import argparse
import ast
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

EXPECTED_TRIALS = 12
EXPECTED_CLASSES = {"biological": 4, "object": 4, "scene": 4}
REQUIRED_COLUMNS = {
    "input_data", "classification", "user_classification", "gaze_data", "objects_bboxes"
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validate one completed native 12-image semantic session.")
    p.add_argument("--output-root", default="output/tobii_image_semantic_demo")
    p.add_argument("--manifest", default="examples/tobii_image_semantic_demo/stimuli_manifest.csv")
    p.add_argument("--session")
    p.add_argument("--started-at", type=float)
    return p.parse_args()


def safe_parse(value: Any, expected_type: type, default: Any) -> Any:
    if isinstance(value, expected_type):
        return value
    text = "" if value is None else str(value).strip()
    if not text:
        return default
    for parser in (json.loads, ast.literal_eval):
        try:
            parsed = parser(text)
            if isinstance(parsed, expected_type):
                return parsed
        except Exception:
            pass
    return default


def newest_session(root: Path, started_at: float | None) -> Path:
    if not root.is_dir():
        raise RuntimeError(f"Output directory does not exist: {root}")
    sessions: list[Path] = []
    for p in root.iterdir():
        data_csv = p / "data.csv"
        if p.is_dir() and data_csv.is_file():
            if started_at is None or data_csv.stat().st_mtime >= started_at - 1.0:
                sessions.append(p)
    if not sessions:
        raise RuntimeError(f"No completed session with data.csv under {root}")
    return max(sessions, key=lambda p: (p / "data.csv").stat().st_mtime)


def main() -> int:
    args = parse_args()
    root = Path(args.output_root).resolve()
    manifest = pd.read_csv(Path(args.manifest).resolve())
    if len(manifest) != EXPECTED_TRIALS:
        raise RuntimeError(f"Manifest must contain {EXPECTED_TRIALS} images")
    if dict(Counter(manifest["class"].astype(str).str.lower())) != EXPECTED_CLASSES:
        raise RuntimeError("Manifest class balance must be 4/4/4")
    expected = {
        str(filename): str(cls).lower()
        for filename, cls in zip(manifest["filename"], manifest["class"])
    }

    session = Path(args.session).resolve() if args.session else newest_session(root, args.started_at)
    data_csv = session / "data.csv"
    csv.field_size_limit(16 * 1024 * 1024)
    with data_csv.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter=";"))
    if len(rows) != EXPECTED_TRIALS:
        raise RuntimeError(f"Expected {EXPECTED_TRIALS} trials, got {len(rows)}")
    missing = REQUIRED_COLUMNS - set(rows[0])
    if missing:
        raise RuntimeError(f"Missing data.csv columns: {sorted(missing)}")

    seen: set[str] = set()
    collected_classes: Counter[str] = Counter()
    responses: Counter[str] = Counter()
    missing_gaze_trials: list[int] = []
    for idx, row in enumerate(rows, start=1):
        filename = Path(str(row["input_data"])).name
        if filename not in expected:
            raise RuntimeError(f"Trial {idx}: unknown image {filename!r}")
        if filename in seen:
            raise RuntimeError(f"Trial {idx}: duplicate image {filename!r}")
        seen.add(filename)
        cls = str(row["classification"]).strip().lower()
        if cls != expected[filename]:
            raise RuntimeError(f"Trial {idx}: class mismatch for {filename}: {cls!r}")
        collected_classes[cls] += 1

        response = str(row["user_classification"]).strip().lower()
        if response not in {"biological", "object", "scene", "none"}:
            raise RuntimeError(f"Trial {idx}: unexpected or missing response {response!r}")
        responses[response] += 1

        gaze = safe_parse(row["gaze_data"], list, [])
        if not gaze:
            missing_gaze_trials.append(idx)

        objects = safe_parse(row["objects_bboxes"], dict, {})
        grid = objects.get("image_bboxes", []) if isinstance(objects, dict) else []
        if len(grid) != 9:
            raise RuntimeError(f"Trial {idx}: expected 9 grid bboxes, got {len(grid)}")
        for cell in grid:
            if not isinstance(cell, dict) or cell.get("class") != "grid":
                raise RuntimeError(f"Trial {idx}: malformed grid bbox")
            bbox = cell.get("bbox")
            if not isinstance(bbox, dict) or not {"cx", "cy", "w", "h"} <= set(bbox):
                raise RuntimeError(f"Trial {idx}: malformed bbox geometry")

    if len(seen) != EXPECTED_TRIALS:
        raise RuntimeError(f"Expected {EXPECTED_TRIALS} unique images, got {len(seen)}")
    if dict(collected_classes) != EXPECTED_CLASSES:
        raise RuntimeError(f"Unexpected collected class balance: {dict(collected_classes)}")

    print(f"session={session}")
    print(f"trials={len(rows)} classes={dict(collected_classes)} responses={dict(responses)}")
    if missing_gaze_trials:
        print(f"WARNING: no gaze samples in trials {missing_gaze_trials}; classification data are complete")
    print("NATIVE_IMAGE_SEMANTIC_COLLECTION_PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

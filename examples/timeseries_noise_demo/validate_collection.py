from __future__ import annotations

import argparse
import ast
import csv
import json
import sys
from pathlib import Path
from typing import Any

EXPECTED_TRIALS = 9
EXPECTED_CLASSES = {"low", "medium", "high"}
REQUIRED_COLUMNS = {
    "screenshot_file",
    "input_data",
    "classification",
    "user_classification",
    "gaze_data",
    "objects_bboxes",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validate one completed native time-series block.")
    p.add_argument("--domain", choices=("machine", "pv"), required=True)
    p.add_argument("--output-root", default="output/timeseries_noise_demo")
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


def newest_session(root: Path, started_at: float | None = None) -> Path:
    sessions = [p for p in root.iterdir() if p.is_dir() and (p / "data.csv").is_file()] if root.is_dir() else []
    if started_at is not None:
        sessions = [p for p in sessions if (p / "data.csv").stat().st_mtime >= started_at - 1.0]
    if not sessions:
        raise RuntimeError(f"No session with data.csv under {root}")
    return max(sessions, key=lambda p: p.stat().st_mtime)


def stimulus_id(value: str) -> str:
    name = Path(value.replace("\\", "/")).name
    return name[:-4] if name.lower().endswith(".png") else name


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root).resolve()
    session = Path(args.session).resolve() if args.session else newest_session(output_root / args.domain, args.started_at)
    data_csv = session / "data.csv"

    csv.field_size_limit(16 * 1024 * 1024)
    with data_csv.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter=";"))

    if len(rows) != EXPECTED_TRIALS:
        raise RuntimeError(f"{args.domain}: expected {EXPECTED_TRIALS} trials, got {len(rows)} in {data_csv}")
    missing = REQUIRED_COLUMNS - set(rows[0])
    if missing:
        raise RuntimeError(f"{args.domain}: missing data.csv columns: {sorted(missing)}")

    seen_ids: set[str] = set()
    missing_gaze_trials: list[int] = []
    class_counts = {name: 0 for name in sorted(EXPECTED_CLASSES)}
    for i, row in enumerate(rows, start=1):
        expected = str(row["classification"]).strip().lower()
        response = str(row["user_classification"]).strip().lower()
        if expected not in EXPECTED_CLASSES:
            raise RuntimeError(f"{args.domain}: trial {i} has unexpected class {expected!r}")
        if not response:
            raise RuntimeError(f"{args.domain}: trial {i} has no response")
        class_counts[expected] += 1

        sid = stimulus_id(str(row["screenshot_file"]))
        prefix = "machine_" if args.domain == "machine" else "pv_"
        if not sid.startswith(prefix):
            raise RuntimeError(f"{args.domain}: trial {i} screenshot/id mismatch: {sid}")
        if sid in seen_ids:
            raise RuntimeError(f"{args.domain}: duplicate stimulus id: {sid}")
        seen_ids.add(sid)

        gaze = safe_parse(row["gaze_data"], list, [])
        if not gaze:
            missing_gaze_trials.append(i)

        objects = safe_parse(row["objects_bboxes"], dict, {})
        boxes = objects.get("timeseries_bboxes", []) if isinstance(objects, dict) else []
        if len(boxes) != 128:
            raise RuntimeError(
                f"{args.domain}: trial {i} ({sid}) expected 128 native time-series bboxes, got {len(boxes)}"
            )
        indices = []
        for box in boxes:
            if not isinstance(box, dict) or not isinstance(box.get("bbox"), dict):
                raise RuntimeError(f"{args.domain}: trial {i} ({sid}) malformed time-series bbox")
            try:
                indices.append((int(box["start_idx"]), int(box["end_idx"])))
            except (KeyError, TypeError, ValueError) as exc:
                raise RuntimeError(f"{args.domain}: trial {i} ({sid}) malformed bbox indices") from exc
        if indices != [(j, j) for j in range(128)]:
            raise RuntimeError(f"{args.domain}: trial {i} ({sid}) unexpected bbox/sample index contract")

    if class_counts != {"high": 3, "low": 3, "medium": 3}:
        raise RuntimeError(f"{args.domain}: unexpected class balance: {class_counts}")

    print(f"session={session}")
    print(f"trials={len(rows)} class_counts={class_counts}")
    if missing_gaze_trials:
        print(f"WARNING: {args.domain}: no gaze samples in trials {missing_gaze_trials}; response/bbox data are complete")
    print(f"NATIVE_TIMESERIES_BLOCK_PASS domain={args.domain}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

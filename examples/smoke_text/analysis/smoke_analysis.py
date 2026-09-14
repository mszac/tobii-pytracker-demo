from __future__ import annotations

import argparse
import csv
from pathlib import Path

REQUIRED_COLUMNS = {
    "screenshot_file",
    "input_data",
    "classification",
    "user_classification",
    "gaze_data",
    "objects_bboxes",
    "voice_file",
    "voice_start_timestamp",
}


def resolve_session(output_root: Path, session: Path | None) -> Path:
    if session is not None:
        return session.resolve()
    candidates = sorted(
        (p for p in output_root.resolve().iterdir() if p.is_dir()),
        key=lambda p: p.name,
    )
    if not candidates:
        raise FileNotFoundError(f"No session directories found under {output_root}")
    return candidates[-1]


def load_rows(csv_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    return fieldnames, rows


def validate_session(session_dir: Path, expected_rows: int | None = 4) -> dict[str, int | str]:
    csv_path = session_dir / "data.csv"
    if not csv_path.is_file():
        raise FileNotFoundError(f"Missing session CSV: {csv_path}")

    fieldnames, rows = load_rows(csv_path)
    missing = REQUIRED_COLUMNS.difference(fieldnames)
    if missing:
        raise ValueError(f"Missing required output columns: {sorted(missing)}")
    if not rows:
        raise ValueError("data.csv contains no trial rows")
    if expected_rows is not None and len(rows) != expected_rows:
        raise ValueError(f"Expected {expected_rows} trial rows, found {len(rows)}")

    nonempty_inputs = sum(bool((row.get("input_data") or "").strip()) for row in rows)
    nonempty_responses = sum(bool((row.get("user_classification") or "").strip()) for row in rows)
    gaze_rows = sum(bool((row.get("gaze_data") or "").strip()) for row in rows)

    if nonempty_inputs == 0:
        raise ValueError("No non-empty input_data values found")

    return {
        "session": str(session_dir),
        "rows": len(rows),
        "nonempty_inputs": nonempty_inputs,
        "nonempty_responses": nonempty_responses,
        "rows_with_gaze": gaze_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Tobii Pytracker smoke-demo output session.")
    parser.add_argument("--output-root", default="output", type=Path)
    parser.add_argument("--session", type=Path)
    parser.add_argument("--expected-rows", type=int, default=4, help="Expected completed trial count; use a negative value to disable the exact-count check.")
    args = parser.parse_args()

    session_dir = resolve_session(args.output_root, args.session)
    expected_rows = None if args.expected_rows < 0 else args.expected_rows
    summary = validate_session(session_dir, expected_rows=expected_rows)
    for key, value in summary.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

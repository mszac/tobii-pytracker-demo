from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any

import pandas as pd

EXPECTED = {
    "astronaut.png": "human",
    "cat.png": "animal",
    "coffee.png": "object",
}
VALID_RESPONSES = {"human", "animal", "object", "none"}
REQUIRED_COLUMNS = {
    "input_data",
    "classification",
    "user_classification",
    "gaze_data",
}


def _parse_gaze(value: Any) -> list[Any]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return value
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return []
    for parser in (json.loads, ast.literal_eval):
        try:
            parsed = parser(text)
            return parsed if isinstance(parsed, list) else []
        except Exception:
            pass
    return []


def _stimulus_name(value: Any) -> str:
    return Path(str(value).replace("\\", "/")).name.lower()


def _candidate_sessions(output_root: Path, min_mtime: float | None) -> list[Path]:
    if not output_root.is_dir():
        return []
    sessions = [p for p in output_root.iterdir() if p.is_dir() and (p / "data.csv").is_file()]
    if min_mtime is not None:
        sessions = [p for p in sessions if (p / "data.csv").stat().st_mtime >= (min_mtime - 1.0)]
    return sorted(sessions, key=lambda p: (p / "data.csv").stat().st_mtime, reverse=True)


def _validate_session(session: Path) -> tuple[pd.DataFrame, list[int], list[int]]:
    raw = pd.read_csv(session / "data.csv", sep=";")
    missing = REQUIRED_COLUMNS - set(raw.columns)
    if missing:
        raise RuntimeError(f"missing columns: {sorted(missing)}")
    if len(raw) != 3:
        raise RuntimeError(f"expected exactly 3 trials, got {len(raw)}")

    names = [_stimulus_name(v) for v in raw["input_data"]]
    if set(names) != set(EXPECTED):
        raise RuntimeError(f"unexpected three-image stimulus set: {names}")
    if len(set(names)) != 3:
        raise RuntimeError(f"stimuli are not unique: {names}")

    gaze_counts: list[int] = []
    missing_gaze_trials: list[int] = []
    for idx, row in raw.reset_index(drop=True).iterrows():
        name = _stimulus_name(row["input_data"])
        actual = str(row["classification"]).strip().lower()
        response = str(row["user_classification"]).strip().lower()
        if actual != EXPECTED[name]:
            raise RuntimeError(
                f"trial {idx}: classification mismatch for {name}: {actual!r} != {EXPECTED[name]!r}"
            )
        if response not in VALID_RESPONSES:
            raise RuntimeError(f"trial {idx}: missing/invalid button response: {response!r}")
        gaze = _parse_gaze(row["gaze_data"])
        if not gaze:
            missing_gaze_trials.append(idx + 1)
        gaze_counts.append(len(gaze))

    return raw, gaze_counts, missing_gaze_trials


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the completed three-image native test demo.")
    parser.add_argument("--output-root", type=Path, default=Path("output/test_demo"))
    parser.add_argument("--min-mtime", type=float, default=None, help="Ignore sessions whose data.csv predates this epoch time.")
    args = parser.parse_args()

    failures: list[str] = []
    for session in _candidate_sessions(args.output_root.resolve(), args.min_mtime):
        try:
            raw, gaze_counts, missing_gaze_trials = _validate_session(session)
        except Exception as exc:
            failures.append(f"{session.name}: {exc}")
            continue

        print(f"session={session}")
        for idx, row in raw.reset_index(drop=True).iterrows():
            print(
                f"trial={idx + 1} stimulus={_stimulus_name(row['input_data'])} "
                f"expected={str(row['classification']).lower()} "
                f"response={str(row['user_classification']).lower()} "
                f"gaze_samples={gaze_counts[idx]}"
            )
        if missing_gaze_trials:
            print(f"WARNING: no gaze samples in trials {missing_gaze_trials}; responses were still collected correctly")
        print("NATIVE_TEST_DEMO_COLLECTION_PASS")
        return 0

    detail = "; ".join(failures[:5]) if failures else "no output/<session>/data.csv found"
    raise RuntimeError(f"No valid TEST DEMO session found under {args.output_root.resolve()}: {detail}")


if __name__ == "__main__":
    raise SystemExit(main())

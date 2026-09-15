from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

EXPECTED_TRIALS = 12
REQUIRED_COLUMNS = {"input_data", "classification", "user_classification", "gaze_data", "objects_bboxes"}


def safe_parse(value: Any, expected_type: type, default: Any) -> Any:
    if isinstance(value, expected_type):
        return value
    text = "" if value is None else str(value).strip()
    if not text or text.lower() == "nan":
        return default
    for parser in (json.loads, ast.literal_eval):
        try:
            parsed = parser(text)
            if isinstance(parsed, expected_type):
                return parsed
        except Exception:
            pass
    return default


def normalize_token(value: Any) -> str:
    return re.sub(r"[^0-9a-ząćęłńóśźż]+", "", str(value).casefold())


def target_phrase_found(objects: dict[str, Any], phrase: str) -> bool:
    words = objects.get("words", []) if isinstance(objects, dict) else []
    tokens = [normalize_token(w.get("word", "")) for w in words if isinstance(w, dict)]
    target = [normalize_token(x) for x in str(phrase).split()]
    target = [x for x in target if x]
    if not target:
        return False
    width = len(target)
    return any(tokens[i:i + width] == target for i in range(0, len(tokens) - width + 1))


def newest_session(root: Path, started_at: float | None) -> Path:
    sessions = []
    if root.is_dir():
        for p in root.iterdir():
            data_csv = p / "data.csv"
            if p.is_dir() and data_csv.is_file() and (started_at is None or data_csv.stat().st_mtime >= started_at - 1.0):
                sessions.append(p)
    if not sessions:
        raise RuntimeError(f"No current UX A/B session with data.csv under {root}")
    return max(sessions, key=lambda p: (p / "data.csv").stat().st_mtime)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", default="output/tobii_ux_ab_demo")
    ap.add_argument("--dataset", default="examples/tobii_ux_ab_demo/data/text_search.csv")
    ap.add_argument("--started-at", type=float)
    args = ap.parse_args()

    dataset = pd.read_csv(Path(args.dataset).resolve(), encoding="utf-8")
    if len(dataset) != EXPECTED_TRIALS:
        raise RuntimeError(f"Expected {EXPECTED_TRIALS} dataset rows, got {len(dataset)}")
    stimuli = set(dataset["text"].astype(str))
    lookup = dataset.set_index("text", drop=False)
    if len(stimuli) != EXPECTED_TRIALS:
        raise RuntimeError("UX A/B text values must be unique")

    session = newest_session(Path(args.output_root).resolve(), args.started_at)
    csv.field_size_limit(16 * 1024 * 1024)
    with (session / "data.csv").open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter=";"))
    if len(rows) != EXPECTED_TRIALS:
        raise RuntimeError(f"Expected {EXPECTED_TRIALS} trials, got {len(rows)}")
    missing = REQUIRED_COLUMNS - set(rows[0])
    if missing:
        raise RuntimeError(f"Missing data.csv columns: {sorted(missing)}")

    conditions = Counter()
    responses = Counter()
    missing_gaze: list[int] = []
    for idx, row in enumerate(rows, start=1):
        text = str(row["input_data"])
        if text not in stimuli:
            raise RuntimeError(f"Trial {idx}: stimulus does not belong to UX A/B dataset")
        meta = lookup.loc[text]
        if isinstance(meta, pd.DataFrame):
            raise RuntimeError("UX A/B dataset text must be unique")
        expected = str(meta["answer"]).strip().lower()
        if str(row["classification"]).strip().lower() != expected:
            raise RuntimeError(f"Trial {idx}: classification mismatch")
        response = str(row["user_classification"]).strip().lower()
        if response not in {"tak", "nie", "none"}:
            raise RuntimeError(f"Trial {idx}: missing/invalid response {response!r}")
        responses[response] += 1
        conditions[str(meta["condition"]).upper()] += 1
        if not safe_parse(row["gaze_data"], list, []):
            missing_gaze.append(idx)
        objects = safe_parse(row["objects_bboxes"], dict, {})
        if not target_phrase_found(objects, str(meta["target_phrase"])):
            raise RuntimeError(f"Trial {idx}: target phrase missing from native word bboxes")

    if dict(conditions) != {"EARLY": 6, "LATE": 6}:
        raise RuntimeError(f"Unexpected condition balance: {dict(conditions)}")
    print(f"session={session}")
    print(f"trials={len(rows)} responses={dict(responses)}")
    if missing_gaze:
        print(f"WARNING: no gaze samples in trials {missing_gaze}; response/text-bbox data are complete")
    print("NATIVE_UX_AB_COLLECTION_PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

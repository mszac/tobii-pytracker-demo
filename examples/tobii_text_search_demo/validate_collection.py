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
EXPECTED_CONDITIONS = {"EARLY": 6, "LATE": 6}
EXPECTED_CONDITION_ANSWERS = {
    ("EARLY", "tak"): 3,
    ("EARLY", "nie"): 3,
    ("LATE", "tak"): 3,
    ("LATE", "nie"): 3,
}
REQUIRED_COLUMNS = {
    "screenshot_file",
    "input_data",
    "classification",
    "user_classification",
    "gaze_data",
    "objects_bboxes",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validate one completed native text-search session.")
    p.add_argument("--output-root", default="output/tobii_text_search_demo")
    p.add_argument("--dataset", default="examples/tobii_text_search_demo/data/text_search.csv")
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


def normalize_token(value: Any) -> str:
    return re.sub(r"[^0-9a-ząćęłńóśźż]+", "", str(value).casefold())


def target_phrase_found(objects: dict[str, Any], phrase: str) -> bool:
    words = objects.get("words", []) if isinstance(objects, dict) else []
    tokens = [normalize_token(w.get("word", "")) for w in words if isinstance(w, dict)]
    target = [normalize_token(x) for x in str(phrase).split()]
    target = [x for x in target if x]
    if not target:
        return False

    # Restrict matching to the TEKST section if the marker exists.
    start = 0
    for idx, token in enumerate(tokens):
        if token == "tekst":
            start = idx + 1
            break
    tokens = tokens[start:]
    width = len(target)
    return any(tokens[i:i + width] == target for i in range(0, len(tokens) - width + 1))


def newest_session(root: Path, started_at: float | None) -> Path:
    if not root.is_dir():
        raise RuntimeError(f"Output directory does not exist: {root}")
    sessions = []
    for p in root.iterdir():
        data_csv = p / "data.csv"
        if p.is_dir() and data_csv.is_file():
            if started_at is None or data_csv.stat().st_mtime >= started_at - 1.0:
                sessions.append(p)
    if not sessions:
        suffix = f" created after {started_at}" if started_at is not None else ""
        raise RuntimeError(f"No session with data.csv under {root}{suffix}")
    return max(sessions, key=lambda p: (p / "data.csv").stat().st_mtime)


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root).resolve()
    dataset_path = Path(args.dataset).resolve()
    session = Path(args.session).resolve() if args.session else newest_session(output_root, args.started_at)
    data_csv = session / "data.csv"

    dataset = pd.read_csv(dataset_path, encoding="utf-8")
    required_dataset = {
        "item_id", "topic", "condition", "answer", "critical_phrase",
        "question", "text_body", "text_word_count", "selected_text",
    }
    missing_dataset = required_dataset - set(dataset.columns)
    if missing_dataset:
        raise RuntimeError(f"Dataset missing columns: {sorted(missing_dataset)}")
    if len(dataset) != EXPECTED_TRIALS or dataset["selected_text"].nunique() != EXPECTED_TRIALS:
        raise RuntimeError("Dataset must contain exactly 12 unique stimuli")

    condition_counts = Counter(dataset["condition"].astype(str).str.upper())
    if dict(condition_counts) != EXPECTED_CONDITIONS:
        raise RuntimeError(f"Unexpected EARLY/LATE balance: {dict(condition_counts)}")
    pair_counts = Counter(
        (str(r.condition).upper(), str(r.answer).lower())
        for r in dataset.itertuples(index=False)
    )
    if dict(pair_counts) != EXPECTED_CONDITION_ANSWERS:
        raise RuntimeError(f"Unexpected condition/answer balance: {dict(pair_counts)}")

    csv.field_size_limit(16 * 1024 * 1024)
    with data_csv.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter=";"))
    if len(rows) != EXPECTED_TRIALS:
        raise RuntimeError(f"Expected {EXPECTED_TRIALS} trials, got {len(rows)} in {data_csv}")
    if not rows:
        raise RuntimeError("data.csv is empty")
    missing = REQUIRED_COLUMNS - set(rows[0])
    if missing:
        raise RuntimeError(f"Missing data.csv columns: {sorted(missing)}")

    lookup = dataset.set_index("selected_text", drop=False)
    seen: set[str] = set()
    output_condition_counts: Counter[str] = Counter()
    response_counts: Counter[str] = Counter()
    missing_gaze_trials: list[int] = []

    for idx, row in enumerate(rows, start=1):
        stimulus = str(row["input_data"])
        if stimulus not in lookup.index:
            raise RuntimeError(f"Trial {idx} stimulus not found in committed dataset")
        if stimulus in seen:
            raise RuntimeError(f"Trial {idx} duplicates a stimulus")
        seen.add(stimulus)
        meta = lookup.loc[stimulus]
        if isinstance(meta, pd.DataFrame):
            raise RuntimeError("Dataset selected_text values must be unique")

        expected = str(meta["answer"]).strip().lower()
        output_expected = str(row["classification"]).strip().lower()
        if output_expected != expected:
            raise RuntimeError(
                f"Trial {idx} classification mismatch: output={output_expected!r}, dataset={expected!r}"
            )
        response = str(row["user_classification"]).strip().lower()
        if response not in {"tak", "nie", "none"}:
            raise RuntimeError(f"Trial {idx} unexpected or missing response: {response!r}")
        response_counts[response] += 1
        output_condition_counts[str(meta["condition"]).upper()] += 1

        gaze = safe_parse(row["gaze_data"], list, [])
        if not gaze:
            missing_gaze_trials.append(idx + 1)

        objects = safe_parse(row["objects_bboxes"], dict, {})
        words = objects.get("words", []) if isinstance(objects, dict) else []
        if not words:
            raise RuntimeError(f"Trial {idx} item={meta['item_id']} has no native word bboxes")
        if not target_phrase_found(objects, str(meta["critical_phrase"])):
            raise RuntimeError(
                f"Trial {idx} item={meta['item_id']} critical phrase not found in native word bboxes"
            )

    if len(seen) != EXPECTED_TRIALS:
        raise RuntimeError(f"Expected 12 unique stimuli, got {len(seen)}")
    if dict(output_condition_counts) != EXPECTED_CONDITIONS:
        raise RuntimeError(f"Unexpected collected condition balance: {dict(output_condition_counts)}")

    print(f"session={session}")
    print(f"trials={len(rows)} responses={dict(response_counts)}")
    if missing_gaze_trials:
        print(f"WARNING: no gaze samples in trials {missing_gaze_trials}; response/text-bbox data are complete")
    print("NATIVE_TEXT_SEARCH_COLLECTION_PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

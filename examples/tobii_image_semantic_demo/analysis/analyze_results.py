from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any

import pandas as pd
from tobii_pytracker.analyze import HeatmapAnalyzer, FixationAnalyzer, SaccadeAnalyzer, EntropyAnalyzer

EXPECTED_TRIALS = 12
EXPECTED_CLASSES = {"biological": 4, "object": 4, "scene": 4}


def parse_value(value: Any, expected: type, default: Any) -> Any:
    if isinstance(value, expected):
        return value
    text = "" if value is None else str(value).strip()
    if not text or text.lower() == "nan":
        return default
    for parser in (json.loads, ast.literal_eval):
        try:
            parsed = parser(text)
            if isinstance(parsed, expected):
                return parsed
        except Exception:
            pass
    return default


def newest_session(root: Path) -> Path:
    sessions = [p for p in root.iterdir() if p.is_dir() and (p / "data.csv").is_file()]
    if not sessions:
        raise RuntimeError(f"No session with data.csv under {root}")
    return max(sessions, key=lambda p: (p / "data.csv").stat().st_mtime)


def first_value(d: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in d and d[name] is not None:
            return d[name]
    return None


def flatten(session: Path, raw: pd.DataFrame) -> pd.DataFrame:
    out: list[dict[str, Any]] = []
    for slide_index, row in raw.reset_index(drop=True).iterrows():
        gaze = parse_value(row.get("gaze_data"), list, [])
        for sample in gaze:
            if not isinstance(sample, dict):
                continue
            x = first_value(sample, "avg_gaze_x", "gaze_x", "x")
            y = first_value(sample, "avg_gaze_y", "gaze_y", "y")
            t = first_value(sample, "system_time", "time", "timestamp")
            if x is None or y is None:
                continue
            out.append({
                "set_name": session.name,
                "slide_index": int(slide_index),
                "input_data": row.get("input_data"),
                "classification": str(row.get("classification", "")).lower(),
                "avg_gaze_x": float(x),
                "avg_gaze_y": float(y),
                "system_time": float(t) if t is not None else float(len(out)),
            })
    return pd.DataFrame.from_records(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyze the 12-image semantic native demo.")
    ap.add_argument("--output-root", default="output/tobii_image_semantic_demo")
    ap.add_argument("--session")
    args = ap.parse_args()

    root = Path(args.output_root).resolve()
    session = Path(args.session).resolve() if args.session else newest_session(root)
    raw = pd.read_csv(session / "data.csv", sep=";")
    required = {"input_data", "classification", "user_classification", "gaze_data"}
    missing = required - set(raw.columns)
    if missing:
        raise RuntimeError(f"Missing data.csv columns: {sorted(missing)}")
    if len(raw) != EXPECTED_TRIALS:
        raise RuntimeError(f"Expected {EXPECTED_TRIALS} trials, got {len(raw)}")

    raw["classification"] = raw["classification"].astype(str).str.lower()
    raw["user_classification"] = raw["user_classification"].astype(str).str.lower()
    if raw["classification"].value_counts().to_dict() != EXPECTED_CLASSES:
        raise RuntimeError(f"Unexpected class balance: {raw['classification'].value_counts().to_dict()}")

    gaze_counts = [len(parse_value(v, list, [])) for v in raw["gaze_data"]]
    if any(n == 0 for n in gaze_counts):
        raise RuntimeError(f"Every image must contain gaze samples; counts={gaze_counts}")

    flat = flatten(session, raw)
    if flat.empty:
        raise RuntimeError("No usable gaze samples after flattening")

    analysis_dir = session / "analysis_image_semantic_demo"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    flat.to_csv(analysis_dir / "flattened_gaze.csv", index=False)

    heatmap = HeatmapAnalyzer(analysis_dir).analyze(flat, per="slide")
    fixations = FixationAnalyzer(analysis_dir, method="dispersion").analyze(flat)
    saccades = SaccadeAnalyzer(analysis_dir, method="ivt").analyze(flat)
    entropy = EntropyAnalyzer(analysis_dir).analyze(flat, per="slide")

    heatmap.to_csv(analysis_dir / "heatmap_stats.csv", index=False)
    fixations.to_csv(analysis_dir / "fixations.csv", index=False)
    saccades.to_csv(analysis_dir / "saccades.csv", index=False)
    entropy.to_csv(analysis_dir / "entropy.csv", index=False)

    trial = pd.DataFrame({
        "slide_index": range(EXPECTED_TRIALS),
        "image_file": [Path(str(v)).name for v in raw["input_data"]],
        "category": raw["classification"],
        "response": raw["user_classification"],
        "correct": (raw["classification"] == raw["user_classification"]).astype(int),
        "gaze_samples": gaze_counts,
    })
    if not fixations.empty and "slide_index" in fixations.columns:
        trial = trial.merge(fixations.groupby("slide_index").size().rename("fixations"), on="slide_index", how="left")
    else:
        trial["fixations"] = 0
    if not saccades.empty and "slide_index" in saccades.columns:
        trial = trial.merge(saccades.groupby("slide_index").size().rename("saccades"), on="slide_index", how="left")
    else:
        trial["saccades"] = 0
    trial["fixations"] = trial["fixations"].fillna(0).astype(int)
    trial["saccades"] = trial["saccades"].fillna(0).astype(int)
    trial.to_csv(analysis_dir / "trial_metrics.csv", index=False)

    category = (
        trial.groupby("category", as_index=False)
        .agg(
            trials=("slide_index", "size"),
            accuracy=("correct", "mean"),
            mean_gaze_samples=("gaze_samples", "mean"),
            mean_fixations=("fixations", "mean"),
            mean_saccades=("saccades", "mean"),
        )
    )
    category.to_csv(analysis_dir / "category_summary.csv", index=False)

    report = [
        "Native 12-image semantic gaze demo",
        f"session={session}",
        f"trials={len(raw)}",
        f"overall_accuracy={trial['correct'].mean():.3f}",
        f"gaze_samples={sum(gaze_counts)}",
        f"fixations={len(fixations)}",
        f"saccades={len(saccades)}",
        f"entropy_rows={len(entropy)}",
        "",
        "Category summary:",
        category.to_string(index=False),
        "",
        "Interpretation: descriptive smoke/demo output only; this is not an inferential study.",
    ]
    (analysis_dir / "report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")

    print(category.to_string(index=False))
    print(f"analysis_dir={analysis_dir}")
    print("NATIVE_IMAGE_SEMANTIC_ANALYSIS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

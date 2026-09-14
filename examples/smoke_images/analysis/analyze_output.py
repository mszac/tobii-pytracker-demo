\
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any

import pandas as pd
from tobii_pytracker.analyze import HeatmapAnalyzer, FixationAnalyzer, SaccadeAnalyzer, EntropyAnalyzer

EXPECTED_TRIALS = 3
REQUIRED_COLUMNS = {"input_data", "gaze_data"}


def newest_session(output_root: Path) -> Path:
    sessions = sorted((p for p in output_root.iterdir() if p.is_dir() and (p / "data.csv").is_file()), key=lambda p: p.stat().st_mtime)
    if not sessions:
        raise FileNotFoundError(f"No output session with data.csv under {output_root}")
    return sessions[-1]


def parse_gaze_cell(value: Any) -> list[dict[str, Any]]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return [x for x in value if isinstance(x, dict)]
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return []
    for parser in (json.loads, ast.literal_eval):
        try:
            parsed = parser(text)
            if isinstance(parsed, list):
                return [x for x in parsed if isinstance(x, dict)]
        except Exception:
            pass
    raise ValueError("Cannot parse gaze_data cell")


def first_value(d: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in d and d[name] is not None:
            return d[name]
    return None


def flatten(session: Path, raw: pd.DataFrame) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    for slide_index, row in raw.reset_index(drop=True).iterrows():
        gaze = parse_gaze_cell(row.get("gaze_data"))
        for sample in gaze:
            x = first_value(sample, "avg_gaze_x", "gaze_x", "x")
            y = first_value(sample, "avg_gaze_y", "gaze_y", "y")
            t = first_value(sample, "system_time", "time", "timestamp")
            if x is None or y is None:
                continue
            records.append({
                "set_name": session.name,
                "slide_index": int(slide_index),
                "input_data": row.get("input_data"),
                "avg_gaze_x": float(x),
                "avg_gaze_y": float(y),
                "system_time": float(t) if t is not None else float(len(records)),
            })
    return pd.DataFrame.from_records(records)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", default="output")
    ap.add_argument("--session")
    args = ap.parse_args()

    output_root = Path(args.output_root).resolve()
    session = Path(args.session).resolve() if args.session else newest_session(output_root)
    raw = pd.read_csv(session / "data.csv", sep=";")
    missing = REQUIRED_COLUMNS - set(raw.columns)
    if missing:
        raise RuntimeError(f"Missing required data.csv columns: {sorted(missing)}")
    if len(raw) != EXPECTED_TRIALS:
        raise RuntimeError(f"Expected exactly {EXPECTED_TRIALS} trials, got {len(raw)}")

    gaze_counts = [len(parse_gaze_cell(v)) for v in raw["gaze_data"]]
    if any(c == 0 for c in gaze_counts):
        raise RuntimeError(f"Every image must contain gaze samples; per-trial counts={gaze_counts}")

    flat = flatten(session, raw)
    if flat.empty:
        raise RuntimeError("No usable gaze samples after flattening")

    analysis_dir = session / "analysis_image_demo"
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

    summary = raw[["input_data"]].copy()
    summary["slide_index"] = range(len(summary))
    summary["gaze_samples"] = gaze_counts
    if not fixations.empty:
        fc = fixations.groupby("slide_index").size().rename("fixations")
        summary = summary.merge(fc, on="slide_index", how="left")
    else:
        summary["fixations"] = 0
    if not saccades.empty:
        sc = saccades.groupby("slide_index").size().rename("saccades")
        summary = summary.merge(sc, on="slide_index", how="left")
    else:
        summary["saccades"] = 0
    summary["fixations"] = summary["fixations"].fillna(0).astype(int)
    summary["saccades"] = summary["saccades"].fillna(0).astype(int)
    summary.to_csv(analysis_dir / "summary.csv", index=False)

    report = [
        "Native image smoke analysis",
        f"session={session}",
        f"trials={len(raw)}",
        f"gaze_samples={sum(gaze_counts)}",
        f"fixations={len(fixations)}",
        f"saccades={len(saccades)}",
        f"entropy_rows={len(entropy)}",
        "",
        "Interpretation: this is a pipeline smoke test, not an inferential study.",
    ]
    (analysis_dir / "report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")

    print(summary.to_string(index=False))
    print(f"analysis_dir={analysis_dir}")
    print("NATIVE_IMAGE_ANALYSIS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

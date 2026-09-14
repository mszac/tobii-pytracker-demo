from __future__ import annotations

import argparse
import ast
import json
import math
import re
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tobii_pytracker.analyze import FixationAnalyzer

EXPECTED_TRIALS_PER_BLOCK = 9
TEMPORAL_WINDOWS = 8
REQUIRED_COLUMNS = {
    "screenshot_file",
    "classification",
    "user_classification",
    "gaze_data",
    "objects_bboxes",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--demo-root", default="tobii-pytracker-demo")
    p.add_argument("--machine-session")
    p.add_argument("--pv-session")
    return p.parse_args()


def newest_session(root: Path) -> Path:
    sessions = [p for p in root.iterdir() if p.is_dir() and (p / "data.csv").is_file()] if root.is_dir() else []
    if not sessions:
        raise FileNotFoundError(f"No session with data.csv under {root}")
    return max(sessions, key=lambda p: p.stat().st_mtime)


def safe_parse(value: Any, expected_type: type, default: Any) -> Any:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return default
    if isinstance(value, expected_type):
        return value
    text = str(value).strip()
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


def first_value(d: dict[str, Any], *names: str) -> Any:
    for name in names:
        value = d.get(name)
        if value is not None:
            return value
    return None


def stimulus_id_from_screenshot(value: Any) -> str:
    name = Path(str(value).replace("\\", "/")).name
    if name.lower().endswith(".png"):
        name = name[:-4]
    if not re.fullmatch(r"(?:machine|pv)_(?:low|medium|high)_\d{2}", name.lower()):
        raise ValueError(f"Unrecognised time-series stimulus screenshot: {value}")
    return name.lower()


def parse_timeseries_bboxes(value: Any) -> list[dict[str, Any]]:
    objects = safe_parse(value, dict, {})
    items = objects.get("timeseries_bboxes", []) if isinstance(objects, dict) else []
    result: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("bbox"), dict):
            continue
        try:
            box = item["bbox"]
            result.append({
                "start_idx": int(item["start_idx"]),
                "end_idx": int(item["end_idx"]),
                "cx": float(box["cx"]),
                "w": float(box["w"]),
            })
        except (KeyError, TypeError, ValueError):
            continue
    return sorted(result, key=lambda x: (x["start_idx"], x["cx"]))


def flatten_session(domain: str, session: Path, raw: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    set_name = f"{domain}:{session.name}"
    for slide_index, trial in raw.reset_index(drop=True).iterrows():
        gaze = safe_parse(trial.get("gaze_data"), list, [])
        for sample in gaze:
            if not isinstance(sample, dict):
                continue
            x = first_value(sample, "avg_gaze_x", "gaze_x", "x")
            y = first_value(sample, "avg_gaze_y", "gaze_y", "y")
            t = first_value(sample, "system_time", "time", "timestamp", "logged_time")
            if x is None or y is None or t is None:
                continue
            try:
                rows.append({
                    "set_name": set_name,
                    "slide_index": int(slide_index),
                    "avg_gaze_x": float(x),
                    "avg_gaze_y": float(y),
                    "system_time": float(t),
                })
            except (TypeError, ValueError):
                continue
    return pd.DataFrame(rows)


def sample_index_for_x(x: float, boxes: list[dict[str, Any]]) -> int | None:
    if not boxes:
        return None
    for box in boxes:
        left = box["cx"] - box["w"] / 2.0
        right = box["cx"] + box["w"] / 2.0
        if left <= x <= right:
            return int(box["start_idx"])
    nearest = min(boxes, key=lambda b: abs(float(b["cx"]) - x))
    return int(nearest["start_idx"])


def entropy(values: list[float]) -> float:
    arr = np.asarray(values, dtype=float)
    arr = arr[arr > 0]
    if len(arr) == 0:
        return math.nan
    if len(arr) == 1:
        return 0.0
    p = arr / arr.sum()
    return float(-(p * np.log(p)).sum() / np.log(len(p)))


def load_block(domain: str, session: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(session / "data.csv", sep=";", encoding="utf-8")
    missing = REQUIRED_COLUMNS - set(raw.columns)
    if missing:
        raise RuntimeError(f"{domain}: missing data.csv columns: {sorted(missing)}")
    if len(raw) != EXPECTED_TRIALS_PER_BLOCK:
        raise RuntimeError(f"{domain}: expected {EXPECTED_TRIALS_PER_BLOCK} trials, got {len(raw)}")
    flat = flatten_session(domain, session, raw)
    return raw, flat


def main() -> int:
    args = parse_args()
    demo_root = Path(args.demo_root).resolve()
    output_root = demo_root / "output" / "tobii_timeseries_noise_demo"
    machine_session = Path(args.machine_session).resolve() if args.machine_session else newest_session(output_root / "machine")
    pv_session = Path(args.pv_session).resolve() if args.pv_session else newest_session(output_root / "pv")

    raw_by_domain: dict[str, pd.DataFrame] = {}
    flat_parts: list[pd.DataFrame] = []
    sessions = {"machine": machine_session, "pv": pv_session}
    for domain, session in sessions.items():
        raw, flat = load_block(domain, session)
        raw_by_domain[domain] = raw
        flat_parts.append(flat)

    flat = pd.concat(flat_parts, ignore_index=True) if flat_parts else pd.DataFrame()
    if flat.empty:
        raise RuntimeError("No usable gaze samples in either block")

    analysis_dir = output_root / "analysis_latest"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    flat.to_csv(analysis_dir / "flattened_gaze.csv", index=False)

    fixations = FixationAnalyzer(analysis_dir, method="dispersion").analyze(flat)
    fixations.to_csv(analysis_dir / "fixations.csv", index=False)

    rows: list[dict[str, Any]] = []
    for domain, raw in raw_by_domain.items():
        set_name = f"{domain}:{sessions[domain].name}"
        for slide_index, trial in raw.reset_index(drop=True).iterrows():
            stim_id = stimulus_id_from_screenshot(trial.get("screenshot_file", ""))
            meta = re.fullmatch(r"(machine|pv)_(low|medium|high)_(\d{2})", stim_id)
            assert meta is not None
            _, noise_class, repetition = meta.groups()
            gaze = flat[(flat["set_name"] == set_name) & (flat["slide_index"] == slide_index)].copy()
            fx = fixations[(fixations["set_name"] == set_name) & (fixations["slide_index"] == slide_index)].copy() if not fixations.empty else pd.DataFrame()
            boxes = parse_timeseries_bboxes(trial.get("objects_bboxes"))
            if len(boxes) < 100:
                raise RuntimeError(f"{stim_id}: expected per-sample time-series bboxes, got {len(boxes)}")
            max_idx = max(int(b["end_idx"]) for b in boxes)
            n_samples = max_idx + 1
            dwell = [0.0] * TEMPORAL_WINDOWS
            visited: set[int] = set()
            sample_indices: list[int] = []
            if not fx.empty:
                for _, f in fx.iterrows():
                    idx = sample_index_for_x(float(f["x_mean"]), boxes)
                    if idx is None:
                        continue
                    sample_indices.append(idx)
                    bucket = min(TEMPORAL_WINDOWS - 1, int(idx * TEMPORAL_WINDOWS / max(n_samples, 1)))
                    visited.add(bucket)
                    dwell[bucket] += float(f["duration"])
            expected = str(trial.get("classification", "")).strip().casefold()
            response = str(trial.get("user_classification", "")).strip().casefold()
            gaze_span = math.nan
            if not gaze.empty:
                gaze_span = float(gaze["system_time"].max() - gaze["system_time"].min())
            horizontal_span = math.nan
            if len(fx) >= 2:
                horizontal_span = float(fx["x_mean"].max() - fx["x_mean"].min())
            elif len(fx) == 1:
                horizontal_span = 0.0
            rows.append({
                "session": sessions[domain].name,
                "domain": domain,
                "trial_no": int(slide_index + 1),
                "stimulus_id": stim_id,
                "noise_class": noise_class,
                "repetition": int(repetition),
                "expected_answer": expected,
                "user_answer": response,
                "correct": expected == response,
                "gaze_sample_count": int(len(gaze)),
                "gaze_span_s": gaze_span,
                "fixation_count": int(len(fx)),
                "fixation_dwell_s": float(fx["duration"].sum()) if not fx.empty else 0.0,
                "horizontal_fixation_span_px": horizontal_span,
                "unique_temporal_windows": len(visited),
                "time_axis_coverage": len(visited) / TEMPORAL_WINDOWS,
                "horizontal_dwell_entropy": entropy(dwell),
                "timeseries_bbox_count": len(boxes),
                "n_samples": n_samples,
            })

    metrics = pd.DataFrame(rows)
    if len(metrics) != 18:
        raise RuntimeError(f"Expected 18 analysed trials, got {len(metrics)}")
    if (metrics["gaze_sample_count"] == 0).any():
        bad = metrics.loc[metrics["gaze_sample_count"] == 0, "stimulus_id"].tolist()
        raise RuntimeError(f"Every trial must contain gaze samples; missing={bad}")

    metrics.to_csv(analysis_dir / "trial_metrics.csv", index=False, encoding="utf-8-sig")
    class_summary = metrics.groupby("noise_class").agg(
        n_trials=("stimulus_id", "size"),
        accuracy=("correct", "mean"),
        mean_fixation_count=("fixation_count", "mean"),
        mean_fixation_dwell_s=("fixation_dwell_s", "mean"),
        mean_gaze_span_s=("gaze_span_s", "mean"),
        mean_time_axis_coverage=("time_axis_coverage", "mean"),
        mean_horizontal_span_px=("horizontal_fixation_span_px", "mean"),
        mean_horizontal_dwell_entropy=("horizontal_dwell_entropy", "mean"),
    ).reset_index()
    domain_summary = metrics.groupby(["domain", "noise_class"]).agg(
        n_trials=("stimulus_id", "size"),
        accuracy=("correct", "mean"),
        mean_fixation_count=("fixation_count", "mean"),
        mean_fixation_dwell_s=("fixation_dwell_s", "mean"),
        mean_time_axis_coverage=("time_axis_coverage", "mean"),
        mean_horizontal_dwell_entropy=("horizontal_dwell_entropy", "mean"),
    ).reset_index()
    class_summary.to_csv(analysis_dir / "class_summary.csv", index=False, encoding="utf-8-sig")
    domain_summary.to_csv(analysis_dir / "domain_class_summary.csv", index=False, encoding="utf-8-sig")

    order = ["low", "medium", "high"]
    plot_df = class_summary.set_index("noise_class").reindex(order)
    for filename, col, ylabel in [
        ("01_fixation_count.png", "mean_fixation_count", "Mean fixation count"),
        ("02_fixation_dwell.png", "mean_fixation_dwell_s", "Mean fixation dwell time [s]"),
        ("03_time_axis_coverage.png", "mean_time_axis_coverage", "Mean time-axis coverage"),
        ("04_accuracy.png", "accuracy", "Accuracy"),
    ]:
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(order, plot_df[col])
        ax.set_xlabel("Variability class")
        ax.set_ylabel(ylabel)
        if col in {"mean_time_axis_coverage", "accuracy"}:
            ax.set_ylim(0, 1)
        fig.tight_layout()
        fig.savefig(analysis_dir / filename, dpi=160)
        plt.close(fig)

    report = """NATIVE TIME-SERIES VARIABILITY DEMO\n===================================\n\nH1: Higher variability -> more fixations.\nH2: MEDIUM -> longest visual decision process.\nH3: HIGH -> broader horizontal exploration.\nH4: Machine and PV -> different attention distributions.\nH5: MEDIUM -> lowest classification accuracy.\n\nCLASS SUMMARY\n-------------\n{class_summary}\n\nDOMAIN x CLASS SUMMARY\n----------------------\n{domain_summary}\n\nThese summaries are descriptive; this demo is not an inferential study.\n""".format(
        class_summary=class_summary.to_string(index=False),
        domain_summary=domain_summary.to_string(index=False),
    )
    (analysis_dir / "hypothesis_summary.txt").write_text(report, encoding="utf-8")

    print(class_summary.to_string(index=False))
    print(domain_summary.to_string(index=False))
    print(f"analysis_dir={analysis_dir}")
    print("NATIVE_TIMESERIES_ANALYSIS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

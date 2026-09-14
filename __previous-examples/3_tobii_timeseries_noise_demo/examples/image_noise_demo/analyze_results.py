#!/usr/bin/env python3
"""
Descriptive analysis for the image-based time-series variability demo.

Expected experiment output:
    output/image_noise_demo/<timestamp>/data.csv

Expected stimulus filenames:
    machine_low_01.png
    machine_medium_02.png
    machine_high_03.png
    pv_low_01.png
    pv_medium_02.png
    pv_high_03.png

The script uses the 3 x 3 grid AOIs produced by bbox_model=grid and reports
horizontal exploration because the plot x-axis represents time.
"""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


AOI_WIDTH = 1600.0


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--dispersion-threshold", type=float, default=50.0)
    parser.add_argument("--min-fixation-duration", type=float, default=0.10)
    return parser.parse_args()


def safe_literal(value, default):
    if value is None:
        return default
    if isinstance(value, float) and np.isnan(value):
        return default
    if isinstance(value, (dict, list)):
        return value
    try:
        return ast.literal_eval(str(value))
    except Exception:
        return default


def as_float(value):
    try:
        value = float(value)
        return value if np.isfinite(value) else np.nan
    except Exception:
        return np.nan


def gaze_frame(gaze_data):
    rows = []

    for sample in gaze_data:
        if not isinstance(sample, dict):
            continue

        x = as_float(sample.get("avg_gaze_x"))
        y = as_float(sample.get("avg_gaze_y"))

        if not np.isfinite(x):
            xs = [
                as_float(sample.get("gaze_x_left")),
                as_float(sample.get("gaze_x_right")),
            ]
            xs = [v for v in xs if np.isfinite(v)]
            x = float(np.mean(xs)) if xs else np.nan

        if not np.isfinite(y):
            ys = [
                as_float(sample.get("gaze_y_left")),
                as_float(sample.get("gaze_y_right")),
            ]
            ys = [v for v in ys if np.isfinite(v)]
            y = float(np.mean(ys)) if ys else np.nan

        t = as_float(sample.get("system_time"))
        if not np.isfinite(t):
            t = as_float(sample.get("logged_time"))

        if np.isfinite(x) and np.isfinite(y) and np.isfinite(t):
            rows.append({"x": x, "y": y, "t_abs": t})

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df = df.sort_values("t_abs").reset_index(drop=True)
    df["t"] = df["t_abs"] - df["t_abs"].iloc[0]
    return df


def dispersion(window):
    return (
        window["x"].max() - window["x"].min()
        + window["y"].max() - window["y"].min()
    )


def detect_fixations(gaze, threshold=50.0, min_duration=0.10):
    columns = ["start", "end", "duration", "x", "y"]
    if len(gaze) < 2:
        return pd.DataFrame(columns=columns)

    result = []
    t = gaze["t"].to_numpy()
    i = 0
    n = len(gaze)

    while i < n - 1:
        j = i
        while j < n - 1 and t[j] - t[i] < min_duration:
            j += 1

        if t[j] - t[i] < min_duration:
            break

        if dispersion(gaze.iloc[i:j + 1]) <= threshold:
            k = j
            while (
                k + 1 < n
                and dispersion(gaze.iloc[i:k + 2]) <= threshold
            ):
                k += 1

            window = gaze.iloc[i:k + 1]
            result.append({
                "start": float(window["t"].iloc[0]),
                "end": float(window["t"].iloc[-1]),
                "duration": float(window["t"].iloc[-1] - window["t"].iloc[0]),
                "x": float(window["x"].mean()),
                "y": float(window["y"].mean()),
            })
            i = k + 1
        else:
            i += 1

    return pd.DataFrame(result, columns=columns)


def stimulus_metadata(path_value):
    # Normalise both Windows and POSIX separators.
    filename = str(path_value).replace("\\", "/").split("/")[-1].lower()
    match = re.match(
        r"^(machine|pv)_(low|medium|high)_(\d+)\.(png|jpg|jpeg|bmp|gif)$",
        filename,
    )
    if not match:
        return None

    domain, noise_class, repetition, _ = match.groups()
    return {
        "filename": filename,
        "domain": domain,
        "noise_class": noise_class,
        "repetition": int(repetition),
    }


def parse_grid_boxes(objects):
    if not isinstance(objects, dict):
        return []

    boxes = []
    for item in objects.get("image_bboxes", []):
        try:
            bbox = item["bbox"]
            boxes.append({
                "cx": float(bbox["cx"]),
                "cy": float(bbox["cy"]),
                "w": float(bbox["w"]),
                "h": float(bbox["h"]),
            })
        except (KeyError, TypeError, ValueError):
            pass

    if not boxes:
        return []

    xs = sorted({round(b["cx"], 6) for b in boxes})
    ys = sorted({round(b["cy"], 6) for b in boxes}, reverse=True)

    for box in boxes:
        box["col"] = xs.index(round(box["cx"], 6))
        box["row"] = ys.index(round(box["cy"], 6))

    return boxes


def assign_cell(x, y, boxes):
    for box in boxes:
        if (
            box["cx"] - box["w"] / 2 <= x <= box["cx"] + box["w"] / 2
            and box["cy"] - box["h"] / 2 <= y <= box["cy"] + box["h"] / 2
        ):
            return box["row"], box["col"]
    return None


def entropy(values):
    values = np.asarray(values, dtype=float)
    values = values[values > 0]

    if len(values) == 0:
        return np.nan
    if len(values) == 1:
        return 0.0

    p = values / values.sum()
    return float(-np.sum(p * np.log(p)) / np.log(len(p)))


def main():
    args = parse_args()
    repo = Path(args.repo_root).resolve()

    output_root = repo / "output" / "image_noise_demo"
    results_dir = repo / "examples" / "image_noise_demo" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    data_files = sorted(output_root.glob("*/data.csv"))
    if not data_files:
        raise SystemExit(
            "No session data found in output/image_noise_demo/<timestamp>/data.csv"
        )

    rows = []

    for data_file in data_files:
        df = pd.read_csv(data_file, sep=";", encoding="utf-8")
        session = data_file.parent.name

        for trial_no, trial in df.iterrows():
            meta = stimulus_metadata(trial.get("input_data", ""))
            if meta is None:
                print("[WARN] Unrecognised stimulus:", trial.get("input_data"))
                continue

            gaze = gaze_frame(safe_literal(trial.get("gaze_data"), []))
            fixations = detect_fixations(
                gaze,
                threshold=args.dispersion_threshold,
                min_duration=args.min_fixation_duration,
            )

            boxes = parse_grid_boxes(
                safe_literal(trial.get("objects_bboxes"), {})
            )

            cells = [
                assign_cell(fix["x"], fix["y"], boxes)
                for _, fix in fixations.iterrows()
            ]

            valid_cells = [cell for cell in cells if cell is not None]
            unique_cells = set(valid_cells)
            unique_cols = {cell[1] for cell in valid_cells}

            column_dwell = [0.0, 0.0, 0.0]
            for (_, fix), cell in zip(fixations.iterrows(), cells):
                if cell is not None and 0 <= cell[1] < 3:
                    column_dwell[cell[1]] += float(fix["duration"])

            if len(fixations) >= 2:
                horizontal_span = float(
                    fixations["x"].max() - fixations["x"].min()
                )
            elif len(fixations) == 1:
                horizontal_span = 0.0
            else:
                horizontal_span = np.nan

            expected = str(trial.get("classification", "")).strip().casefold()
            response = str(trial.get("user_classification", "")).strip().casefold()

            rows.append({
                "session": session,
                "trial_no": trial_no + 1,
                **meta,
                "expected_answer": expected,
                "user_answer": response,
                "correct": expected == response,
                "gaze_sample_count": len(gaze),
                "gaze_span_s": float(gaze["t"].max()) if len(gaze) else np.nan,
                "fixation_count": len(fixations),
                "fixation_dwell_s": (
                    float(fixations["duration"].sum())
                    if len(fixations)
                    else 0.0
                ),
                "horizontal_fixation_span_px": horizontal_span,
                "horizontal_span_fraction": (
                    horizontal_span / AOI_WIDTH
                    if np.isfinite(horizontal_span)
                    else np.nan
                ),
                "unique_grid_cells": len(unique_cells),
                "unique_grid_columns": len(unique_cols),
                "time_axis_coverage": len(unique_cols) / 3.0,
                "left_column_dwell_s": column_dwell[0],
                "middle_column_dwell_s": column_dwell[1],
                "right_column_dwell_s": column_dwell[2],
                "horizontal_dwell_entropy": entropy(column_dwell),
                "grid_bbox_count": len(boxes),
            })

    metrics = pd.DataFrame(rows)
    if metrics.empty:
        raise SystemExit("No trials could be analysed.")

    metrics.to_csv(
        results_dir / "trial_metrics.csv",
        index=False,
        encoding="utf-8-sig",
    )

    class_summary = (
        metrics.groupby("noise_class")
        .agg(
            n_trials=("trial_no", "size"),
            accuracy=("correct", "mean"),
            mean_fixation_count=("fixation_count", "mean"),
            mean_fixation_dwell_s=("fixation_dwell_s", "mean"),
            mean_gaze_span_s=("gaze_span_s", "mean"),
            mean_time_axis_coverage=("time_axis_coverage", "mean"),
            mean_horizontal_span_fraction=("horizontal_span_fraction", "mean"),
            mean_horizontal_dwell_entropy=("horizontal_dwell_entropy", "mean"),
        )
        .reset_index()
    )

    domain_summary = (
        metrics.groupby(["domain", "noise_class"])
        .agg(
            n_trials=("trial_no", "size"),
            accuracy=("correct", "mean"),
            mean_fixation_count=("fixation_count", "mean"),
            mean_fixation_dwell_s=("fixation_dwell_s", "mean"),
            mean_time_axis_coverage=("time_axis_coverage", "mean"),
            mean_horizontal_dwell_entropy=("horizontal_dwell_entropy", "mean"),
        )
        .reset_index()
    )

    class_summary.to_csv(
        results_dir / "class_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )
    domain_summary.to_csv(
        results_dir / "domain_class_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    order = ["low", "medium", "high"]
    plot_df = class_summary.set_index("noise_class").reindex(order)

    chart_specs = [
        ("01_fixation_count.png", "mean_fixation_count", "Mean fixation count"),
        ("02_fixation_dwell.png", "mean_fixation_dwell_s", "Mean fixation dwell time [s]"),
        ("03_time_axis_coverage.png", "mean_time_axis_coverage", "Mean time-axis coverage"),
        ("04_accuracy.png", "accuracy", "Accuracy"),
    ]

    for filename, column, ylabel in chart_specs:
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(order, plot_df[column])
        ax.set_xlabel("Variability class")
        ax.set_ylabel(ylabel)
        if column in {"mean_time_axis_coverage", "accuracy"}:
            ax.set_ylim(0, 1)
        fig.tight_layout()
        fig.savefig(results_dir / filename, dpi=160)
        plt.close(fig)

    hypothesis_text = f"""IMAGE-BASED TIME-SERIES VARIABILITY DEMO
========================================

H1: Higher variability -> more fixations.
H2: MEDIUM -> longest visual decision process.
H3: HIGH -> broader horizontal exploration.
H4: Machine and PV -> different attention distributions.
H5: MEDIUM -> lowest classification accuracy.

CLASS SUMMARY
-------------
{class_summary.to_string(index=False)}

These summaries are descriptive. A formal study should use participant- and
stimulus-level statistical modelling.
"""
    (results_dir / "hypothesis_summary.txt").write_text(
        hypothesis_text,
        encoding="utf-8",
    )

    print("Saved analysis to:", results_dir)


if __name__ == "__main__":
    main()

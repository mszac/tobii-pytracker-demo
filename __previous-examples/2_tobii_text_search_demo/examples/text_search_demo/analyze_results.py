#!/usr/bin/env python3
"""
Analiza demo "wyszukiwanie konkretnej informacji w krótkim tekście"
dla tobii-pytracker, branch psychopy.

Czyta:
  output/text_search_demo/<timestamp>/data.csv
  datasets/text_search_demo.csv

Tworzy:
  examples/text_search_demo/results/trial_metrics.csv
  examples/text_search_demo/results/condition_summary.csv
  examples/text_search_demo/results/01_ttff_target.png
  examples/text_search_demo/results/02_fixations_before_target.png
  examples/text_search_demo/results/03_target_dwell.png
  examples/text_search_demo/results/04_accuracy_by_target_seen.png
  examples/text_search_demo/results/hypothesis_summary.txt
"""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", default=".",
                   help="Katalog główny checkoutu tobii-pytracker.")
    p.add_argument("--dispersion-threshold", type=float, default=50.0,
                   help="Próg dyspersji I-DT w pikselach.")
    p.add_argument("--min-fixation-duration", type=float, default=0.10,
                   help="Minimalny czas fiksacji w sekundach.")
    return p.parse_args()


def safe_literal(value, default):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return default
    if isinstance(value, (dict, list)):
        return value
    try:
        return ast.literal_eval(str(value))
    except Exception:
        return default


def numeric(value):
    try:
        x = float(value)
        return x if np.isfinite(x) else np.nan
    except Exception:
        return np.nan


def gaze_frame(gaze):
    """Convert filtered gaze_data saved by current psychopy branch to DataFrame."""
    records = []
    for sample in gaze:
        if not isinstance(sample, dict):
            continue

        x = numeric(sample.get("avg_gaze_x"))
        y = numeric(sample.get("avg_gaze_y"))

        # Fallback for alternative/raw-like dictionaries.
        if not np.isfinite(x):
            xs = [numeric(sample.get("gaze_x_left")), numeric(sample.get("gaze_x_right"))]
            xs = [v for v in xs if np.isfinite(v)]
            x = float(np.mean(xs)) if xs else np.nan
        if not np.isfinite(y):
            ys = [numeric(sample.get("gaze_y_left")), numeric(sample.get("gaze_y_right"))]
            ys = [v for v in ys if np.isfinite(v)]
            y = float(np.mean(ys)) if ys else np.nan

        t = numeric(sample.get("system_time"))
        if not np.isfinite(t):
            t = numeric(sample.get("logged_time"))

        if np.isfinite(x) and np.isfinite(y) and np.isfinite(t):
            records.append({"x": x, "y": y, "t_abs": t})

    df = pd.DataFrame(records)
    if df.empty:
        return df

    df = df.sort_values("t_abs").drop_duplicates().reset_index(drop=True)
    df["t"] = df["t_abs"] - df["t_abs"].iloc[0]
    return df


def dispersion(window):
    return ((window["x"].max() - window["x"].min())
            + (window["y"].max() - window["y"].min()))


def detect_fixations(gaze, threshold=50.0, min_duration=0.10):
    """Simple I-DT fixation detector for a compact, dependency-free demo."""
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
            while k + 1 < n and dispersion(gaze.iloc[i:k + 2]) <= threshold:
                k += 1

            w = gaze.iloc[i:k + 1]
            result.append({
                "start": float(w["t"].iloc[0]),
                "end": float(w["t"].iloc[-1]),
                "duration": float(w["t"].iloc[-1] - w["t"].iloc[0]),
                "x": float(w["x"].mean()),
                "y": float(w["y"].mean()),
            })
            i = k + 1
        else:
            i += 1

    return pd.DataFrame(result, columns=columns)


def norm_token(value):
    return re.sub(
        r"[^\wąćęłńóśźż-]+", "", str(value).casefold(),
        flags=re.UNICODE
    )


def get_word_boxes(objects):
    if not isinstance(objects, dict):
        return []

    result = []
    for idx, item in enumerate(objects.get("words", [])):
        try:
            box = item["bbox"]
            result.append({
                "index": idx,
                "word": str(item.get("word", "")),
                "token": norm_token(item.get("word", "")),
                "cx": float(box["cx"]),
                "cy": float(box["cy"]),
                "w": float(box["w"]),
                "h": float(box["h"]),
            })
        except (KeyError, TypeError, ValueError):
            continue
    return result


def inside(x, y, box):
    return (
        box["cx"] - box["w"] / 2 <= x <= box["cx"] + box["w"] / 2
        and box["cy"] - box["h"] / 2 <= y <= box["cy"] + box["h"] / 2
    )


def text_start_index(boxes):
    """Return first word index after marker TEKST:."""
    for b in boxes:
        if b["token"] == "tekst":
            return b["index"] + 1
    return 0


def target_boxes(boxes, critical_phrase):
    """Find phrase only in TEKST section, not in the question."""
    start = text_start_index(boxes)
    subset = boxes[start:]
    target = [norm_token(x) for x in str(critical_phrase).split()]
    target = [x for x in target if x]
    tokens = [b["token"] for b in subset]
    L = len(target)

    for i in range(0, len(tokens) - L + 1):
        if tokens[i:i + L] == target:
            return subset[i:i + L]
    return []


def target_hit(fix, boxes):
    return any(inside(fix["x"], fix["y"], b) for b in boxes)


def main():
    args = parse_args()
    repo = Path(args.repo_root).resolve()

    dataset_path = repo / "datasets" / "text_search_demo.csv"
    output_root = repo / "output" / "text_search_demo"
    result_dir = repo / "examples" / "text_search_demo" / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    dataset = pd.read_csv(dataset_path, encoding="utf-8")
    data_files = sorted(output_root.glob("*/data.csv"))

    if not data_files:
        raise SystemExit(
            "Brak output/text_search_demo/<timestamp>/data.csv. "
            "Najpierw przeprowadź eksperyment."
        )

    result = []

    for data_file in data_files:
        session = data_file.parent.name
        trials = pd.read_csv(data_file, sep=";", encoding="utf-8")

        required = {
            "screenshot_file", "input_data", "classification",
            "user_classification", "gaze_data", "objects_bboxes",
            "voice_file", "voice_start_timestamp"
        }
        missing = required - set(trials.columns)
        if missing:
            raise SystemExit(
                f"{data_file}: brak wymaganych kolumn: {sorted(missing)}"
            )

        for trial_idx, trial in trials.iterrows():
            matches = dataset[
                dataset["selected_text"].astype(str) == str(trial["input_data"])
            ]
            if matches.empty:
                print(
                    f"[WARN] Nie znaleziono bodźca w datasecie: "
                    f"{session}, wiersz {trial_idx + 1}"
                )
                continue

            meta = matches.iloc[0]
            gaze = gaze_frame(safe_literal(trial["gaze_data"], []))
            fix = detect_fixations(
                gaze,
                threshold=args.dispersion_threshold,
                min_duration=args.min_fixation_duration,
            )

            boxes = get_word_boxes(
                safe_literal(trial["objects_bboxes"], {})
            )
            target = target_boxes(boxes, meta["critical_phrase"])

            if len(fix) and target:
                mask = fix.apply(
                    lambda r: target_hit(r, target), axis=1
                )
                target_fix = fix[mask].copy()
            else:
                target_fix = fix.iloc[0:0].copy()

            target_seen = len(target_fix) > 0

            if target_seen:
                first_target_start = float(target_fix["start"].min())
                ttff = first_target_start
                before_target = int(
                    (fix["start"] < first_target_start).sum()
                )
                target_dwell = float(target_fix["duration"].sum())
                target_count = int(len(target_fix))
            else:
                ttff = np.nan
                before_target = np.nan
                target_dwell = 0.0
                target_count = 0

            total_dwell = (
                float(fix["duration"].sum()) if len(fix) else 0.0
            )
            target_share = (
                target_dwell / total_dwell if total_dwell > 0 else np.nan
            )

            expected = str(trial["classification"]).strip().casefold()
            response = str(trial["user_classification"]).strip().casefold()

            result.append({
                "session": session,
                "trial_no": trial_idx + 1,
                "item_id": int(meta["item_id"]),
                "topic": meta["topic"],
                "condition": meta["condition"],
                "expected_answer": expected,
                "user_answer": response,
                "correct": response == expected,
                "critical_phrase": meta["critical_phrase"],
                "text_word_count": int(meta["text_word_count"]),
                "gaze_sample_count": int(len(gaze)),
                "fixation_count_total": int(len(fix)),
                "target_bbox_found": bool(target),
                "target_seen": target_seen,
                "ttff_target_s": ttff,
                "fixations_before_target": before_target,
                "target_fixation_count": target_count,
                "target_dwell_s": target_dwell,
                "target_dwell_share": target_share,
            })

    metrics = pd.DataFrame(result)
    if metrics.empty:
        raise SystemExit("Nie znaleziono prób możliwych do analizy.")

    metrics.to_csv(
        result_dir / "trial_metrics.csv",
        index=False,
        encoding="utf-8-sig"
    )

    summary = (
        metrics.groupby("condition")
        .agg(
            n_trials=("trial_no", "size"),
            accuracy=("correct", "mean"),
            target_seen_rate=("target_seen", "mean"),
            mean_ttff_target_s=("ttff_target_s", "mean"),
            mean_fixations_before_target=("fixations_before_target", "mean"),
            mean_target_fixation_count=("target_fixation_count", "mean"),
            mean_target_dwell_s=("target_dwell_s", "mean"),
            mean_target_dwell_share=("target_dwell_share", "mean"),
        )
        .reset_index()
    )
    summary.to_csv(
        result_dir / "condition_summary.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # H2: TTFF
    plot = summary.dropna(subset=["mean_ttff_target_s"])
    if not plot.empty:
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(plot["condition"], plot["mean_ttff_target_s"])
        ax.set_ylabel("Średni TTFF do informacji kluczowej [s]")
        ax.set_xlabel("Pozycja informacji")
        ax.set_title("EARLY vs LATE — czas odnalezienia informacji")
        fig.tight_layout()
        fig.savefig(result_dir / "01_ttff_target.png", dpi=160)
        plt.close(fig)

    # H2 auxiliary: fixations before target
    plot = summary.dropna(subset=["mean_fixations_before_target"])
    if not plot.empty:
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(plot["condition"], plot["mean_fixations_before_target"])
        ax.set_ylabel("Średnia liczba fiksacji przed targetem")
        ax.set_xlabel("Pozycja informacji")
        ax.set_title("Praca wzrokowa przed odnalezieniem informacji")
        fig.tight_layout()
        fig.savefig(
            result_dir / "02_fixations_before_target.png", dpi=160
        )
        plt.close(fig)

    # H1: target dwell
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(summary["condition"], summary["mean_target_dwell_s"])
    ax.set_ylabel("Średni dwell time na target [s]")
    ax.set_xlabel("Pozycja informacji")
    ax.set_title("Uwaga poświęcona informacji kluczowej")
    fig.tight_layout()
    fig.savefig(result_dir / "03_target_dwell.png", dpi=160)
    plt.close(fig)

    # H3: accuracy by target seen
    accuracy_seen = (
        metrics.groupby("target_seen")
        .agg(n=("correct", "size"), accuracy=("correct", "mean"))
        .reset_index()
    )
    if not accuracy_seen.empty:
        labels = [
            "Target niewidziany" if not bool(x) else "Target widziany"
            for x in accuracy_seen["target_seen"]
        ]
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(labels, accuracy_seen["accuracy"])
        ax.set_ylim(0, 1)
        ax.set_ylabel("Odsetek poprawnych odpowiedzi")
        ax.set_title("Poprawność odpowiedzi a fiksacja na target")
        fig.tight_layout()
        fig.savefig(
            result_dir / "04_accuracy_by_target_seen.png", dpi=160
        )
        plt.close(fig)

    early = summary[summary["condition"] == "EARLY"]
    late = summary[summary["condition"] == "LATE"]

    lines = [
        "DEMO: WYSZUKIWANIE KONKRETNEJ INFORMACJI W TEKŚCIE",
        "==================================================",
        "",
        "H1: uczestnicy powinni kierować uwagę na informację kluczową.",
        f"Ogólny target_seen_rate: {metrics['target_seen'].mean():.3f}",
        f"Średni target dwell: {metrics['target_dwell_s'].mean():.3f} s",
        "",
        "H2: EARLY powinno mieć krótszy TTFF i mniej fiksacji przed targetem.",
    ]

    if len(early) and len(late):
        lines.extend([
            f"EARLY TTFF: {early['mean_ttff_target_s'].iloc[0]:.3f} s",
            f"LATE  TTFF: {late['mean_ttff_target_s'].iloc[0]:.3f} s",
            (
                "EARLY fiksacje przed targetem: "
                f"{early['mean_fixations_before_target'].iloc[0]:.3f}"
            ),
            (
                "LATE  fiksacje przed targetem: "
                f"{late['mean_fixations_before_target'].iloc[0]:.3f}"
            ),
        ])

    lines.extend([
        "",
        "H3: target_seen=True powinno wiązać się z większą poprawnością.",
    ])
    for _, r in accuracy_seen.iterrows():
        lines.append(
            f"target_seen={bool(r['target_seen'])}: "
            f"accuracy={r['accuracy']:.3f}, n={int(r['n'])}"
        )

    lines.extend([
        "",
        "To jest podsumowanie opisowe. Demo nie zastępuje pełnej analizy",
        "statystycznej i nie powinno być traktowane jako gotowy protokół",
        "badania inferencyjnego.",
    ])

    (result_dir / "hypothesis_summary.txt").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    print("\nZapisano:")
    for p in sorted(result_dir.iterdir()):
        print(" -", p.relative_to(repo))


if __name__ == "__main__":
    main()

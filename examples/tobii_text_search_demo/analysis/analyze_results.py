from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

from tobii_pytracker.analyze import DataLoader, FixationAnalyzer
from tobii_pytracker.configs.custom_config import CustomConfig

EXPECTED_TRIALS = 12


def normalize_token(value: Any) -> str:
    return re.sub(r"[^0-9a-ząćęłńóśźż]+", "", str(value).casefold())


def parse_struct(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return {}
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return {}
    for parser in (json.loads, ast.literal_eval):
        try:
            return parser(text)
        except Exception:
            pass
    raise ValueError("Cannot parse structured output field")


def find_target_boxes(objects_bboxes: Any, target_phrase: str) -> list[dict[str, float]]:
    parsed = parse_struct(objects_bboxes)
    words = parsed.get("words", []) if isinstance(parsed, dict) else []
    tokens = [normalize_token(w.get("word", "")) for w in words]

    start = 0
    for idx, token in enumerate(tokens):
        if token == "tekst":
            start = idx + 1
            break

    target = [normalize_token(x) for x in str(target_phrase).split()]
    target = [x for x in target if x]
    if not target:
        raise ValueError(f"Empty target phrase: {target_phrase!r}")

    subset_words = words[start:]
    subset_tokens = tokens[start:]
    width = len(target)
    for i in range(0, len(subset_tokens) - width + 1):
        if subset_tokens[i:i + width] == target:
            boxes: list[dict[str, float]] = []
            for item in subset_words[i:i + width]:
                bbox = item.get("bbox", {})
                if not {"cx", "cy", "w", "h"}.issubset(bbox):
                    raise ValueError(f"Incomplete target bbox for {target_phrase!r}: {bbox}")
                boxes.append({k: float(bbox[k]) for k in ("cx", "cy", "w", "h")})
            return boxes
    raise ValueError(f"Target phrase {target_phrase!r} not found in TEKST word bboxes")


def point_in_boxes(x: float, y: float, boxes: list[dict[str, float]], padding: float = 8.0) -> bool:
    for box in boxes:
        half_w = box["w"] / 2.0 + padding
        half_h = box["h"] / 2.0 + padding
        if (box["cx"] - half_w) <= x <= (box["cx"] + half_w) and (box["cy"] - half_h) <= y <= (box["cy"] + half_h):
            return True
    return False


def discover_sessions(loader: DataLoader, stimuli: set[str]) -> list[str]:
    matches: list[str] = []
    for session in loader.get_subjects():
        raw = loader.get_subject_data(session, flatten=False)
        if "input_data" not in raw.columns:
            continue
        overlap = raw["input_data"].astype(str).isin(stimuli)
        if not overlap.any():
            continue
        if len(raw) != EXPECTED_TRIALS or int(overlap.sum()) != EXPECTED_TRIALS:
            raise RuntimeError(
                f"Text-search session {session!r} is incomplete or mixed: "
                f"rows={len(raw)}, matched_trials={int(overlap.sum())}, expected={EXPECTED_TRIALS}"
            )
        matches.append(session)
    if not matches:
        raise FileNotFoundError("No complete text-search session found under output/tobii_text_search_demo/")
    return sorted(matches)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze completed native text-search sessions.")
    parser.add_argument("--session", action="append", help="Analyze only this output session; may be repeated.")
    args = parser.parse_args()

    script = Path(__file__).resolve()
    example_root = script.parents[1]
    repo_root = script.parents[3]
    config_path = example_root / "config.native.yaml"
    dataset_path = example_root / "data" / "text_search.csv"
    results_root = example_root / "results"
    results_root.mkdir(parents=True, exist_ok=True)

    stimuli_df = pd.read_csv(dataset_path, encoding="utf-8")
    required_dataset = {
        "item_id", "topic", "condition", "answer", "critical_phrase",
        "question", "text_body", "text_word_count", "selected_text",
    }
    missing_dataset = required_dataset - set(stimuli_df.columns)
    if missing_dataset:
        raise RuntimeError(f"Dataset missing columns: {sorted(missing_dataset)}")
    if len(stimuli_df) != EXPECTED_TRIALS or stimuli_df["selected_text"].nunique() != EXPECTED_TRIALS:
        raise RuntimeError("Expected exactly 12 unique committed text stimuli")

    config = CustomConfig(str(config_path))
    loader = DataLoader(config, root=repo_root)
    stimulus_lookup = stimuli_df.set_index("selected_text", drop=False)
    stimulus_set = set(stimuli_df["selected_text"].astype(str))
    sessions = args.session or discover_sessions(loader, stimulus_set)

    trial_rows: list[dict[str, Any]] = []
    example_plot: tuple[str, int] | None = None
    fixation_dir = results_root / "_fixation_runtime"

    for session in sessions:
        raw = loader.get_subject_data(session, flatten=False).reset_index(drop=True)
        if len(raw) != EXPECTED_TRIALS:
            raise RuntimeError(f"Session {session!r}: expected 12 rows, got {len(raw)}")
        if not raw["input_data"].astype(str).isin(stimulus_set).all():
            raise RuntimeError(f"Session {session!r} contains non-text-search trials")

        flat = loader.get_subject_data(session, flatten=True)
        if flat.empty:
            raise RuntimeError(f"Session {session!r} contains no usable gaze samples")
        flat = flat[flat["input_data"].astype(str).isin(stimulus_set)].copy()
        fixations = FixationAnalyzer(fixation_dir, method="dispersion").analyze(flat)

        for slide_index, row in raw.iterrows():
            input_text = str(row["input_data"])
            meta = stimulus_lookup.loc[input_text]
            if isinstance(meta, pd.DataFrame):
                raise RuntimeError("Dataset selected_text values must be unique")

            slide_flat = flat[pd.to_numeric(flat["slide_index"], errors="coerce") == slide_index].copy()
            gaze_samples = len(slide_flat)
            if gaze_samples == 0:
                raise RuntimeError(f"Session {session!r} trial {slide_index} has no gaze samples")

            slide_data = loader.get_slide_data(session, slide_index, flatten=False)
            target_boxes = find_target_boxes(slide_data.get("objects_bboxes", {}), str(meta["critical_phrase"]))

            if fixations.empty:
                slide_fix = fixations.copy()
            else:
                slide_fix = fixations[pd.to_numeric(fixations.get("slide_index"), errors="coerce") == slide_index].copy()
                slide_fix = slide_fix.sort_values("fix_start").reset_index(drop=True)

            if not slide_fix.empty:
                hit_mask = slide_fix.apply(
                    lambda f: point_in_boxes(float(f["x_mean"]), float(f["y_mean"]), target_boxes), axis=1
                )
                target_fix = slide_fix[hit_mask]
            else:
                target_fix = slide_fix.copy()

            trial_start = pd.to_numeric(slide_flat["system_time"], errors="coerce").dropna().min()
            total_dwell = float(pd.to_numeric(slide_fix.get("duration"), errors="coerce").fillna(0).sum()) if not slide_fix.empty else 0.0
            target_seen = not target_fix.empty

            if target_seen:
                first_fix = target_fix.iloc[0]
                first_target_time = float(first_fix["fix_start"])
                ttff = float(first_target_time - trial_start) if pd.notna(trial_start) else float("nan")
                target_dwell = float(pd.to_numeric(target_fix["duration"], errors="coerce").fillna(0).sum())
                target_count = int(len(target_fix))
                before_target = int((pd.to_numeric(slide_fix["fix_start"], errors="coerce") < first_target_time).sum())
                if example_plot is None:
                    example_plot = (session, slide_index)
            else:
                ttff = float("nan")
                target_dwell = 0.0
                target_count = 0
                before_target = int(len(slide_fix))

            target_share = target_dwell / total_dwell if total_dwell > 0 else float("nan")
            expected = str(meta["answer"]).strip().lower()
            observed = str(row.get("user_classification", "")).strip().lower()

            trial_rows.append({
                "session": session,
                "slide_index": slide_index,
                "item_id": int(meta["item_id"]),
                "topic": meta["topic"],
                "condition": str(meta["condition"]).upper(),
                "expected_answer": expected,
                "user_answer": observed,
                "user_answer_display": "nie wiem" if observed == "none" else observed,
                "correct": observed == expected,
                "critical_phrase": meta["critical_phrase"],
                "text_word_count": int(meta["text_word_count"]),
                "gaze_sample_count": gaze_samples,
                "fixation_count_total": int(len(slide_fix)),
                "target_bbox_found": True,
                "target_seen": target_seen,
                "ttff_target_s": ttff,
                "fixations_before_target": before_target,
                "target_fixation_count": target_count,
                "target_dwell_s": target_dwell,
                "target_dwell_share": target_share,
            })

    metrics = pd.DataFrame(trial_rows)
    metrics.to_csv(results_root / "trial_metrics.csv", index=False, encoding="utf-8")

    summary = (
        metrics.groupby("condition", dropna=False)
        .agg(
            n_trials=("item_id", "size"),
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
    summary.to_csv(results_root / "condition_summary.csv", index=False, encoding="utf-8")

    plot = summary.dropna(subset=["mean_ttff_target_s"])
    fig, ax = plt.subplots(figsize=(7, 5))
    if plot.empty:
        ax.text(0.5, 0.5, "No target fixations detected", ha="center", va="center", transform=ax.transAxes)
        ax.set_xticks([])
    else:
        ax.bar(plot["condition"], plot["mean_ttff_target_s"])
    ax.set_ylabel("Mean TTFF to target [s]")
    ax.set_title("EARLY vs LATE — target acquisition")
    fig.tight_layout()
    fig.savefig(results_root / "01_ttff_target.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(summary["condition"], summary["mean_fixations_before_target"])
    ax.set_ylabel("Mean fixations before target")
    ax.set_title("Visual search before finding the answer")
    fig.tight_layout()
    fig.savefig(results_root / "02_fixations_before_target.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(summary["condition"], summary["mean_target_dwell_s"])
    ax.set_ylabel("Mean target dwell [s]")
    ax.set_title("Attention on answer-relevant phrase")
    fig.tight_layout()
    fig.savefig(results_root / "03_target_dwell.png", dpi=160)
    plt.close(fig)

    accuracy_seen = metrics.groupby("target_seen")["correct"].mean().reindex([False, True])
    fig, ax = plt.subplots(figsize=(7, 5))
    if accuracy_seen.dropna().empty:
        ax.text(0.5, 0.5, "No classified trials", ha="center", va="center", transform=ax.transAxes)
        ax.set_xticks([])
    else:
        accuracy_seen.plot(kind="bar", ax=ax)
        ax.set_xticklabels(["target not fixated", "target fixated"], rotation=0)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Accuracy")
    ax.set_title("Accuracy by target fixation")
    fig.tight_layout()
    fig.savefig(results_root / "04_accuracy_by_target_seen.png", dpi=160)
    plt.close(fig)

    if example_plot is None:
        first = metrics.iloc[0]
        example_plot = (str(first["session"]), int(first["slide_index"]))
    loader.plot_gaze(
        example_plot[0],
        example_plot[1],
        save_path=results_root / "05_example_trial_gaze.png",
        show=False,
        gradient=True,
    )

    early = summary[summary["condition"] == "EARLY"]
    late = summary[summary["condition"] == "LATE"]
    lines = [
        "TEXT SEARCH DEMO — DESCRIPTIVE ANALYSIS",
        f"sessions={len(sessions)}",
        f"trials={len(metrics)}",
        f"overall_accuracy={metrics['correct'].mean():.3f}",
        f"target_seen_rate={metrics['target_seen'].mean():.3f}",
        f"mean_target_dwell_s={metrics['target_dwell_s'].mean():.3f}",
        "",
        "H1: answer-relevant information should attract fixation/dwell.",
        "H2: EARLY should show shorter TTFF and fewer fixations before target than LATE.",
        "H3: trials with target_seen=True may show higher accuracy.",
    ]
    if not early.empty and not late.empty:
        lines.extend([
            "",
            f"EARLY_mean_TTFF_s={early.iloc[0]['mean_ttff_target_s']}",
            f"LATE_mean_TTFF_s={late.iloc[0]['mean_ttff_target_s']}",
            f"EARLY_mean_fixations_before_target={early.iloc[0]['mean_fixations_before_target']}",
            f"LATE_mean_fixations_before_target={late.iloc[0]['mean_fixations_before_target']}",
        ])
    seen_summary = metrics.groupby("target_seen").agg(n=("correct", "size"), accuracy=("correct", "mean")).reset_index()
    for _, r in seen_summary.iterrows():
        lines.append(f"target_seen={bool(r['target_seen'])}: accuracy={r['accuracy']:.3f}, n={int(r['n'])}")
    lines.extend([
        "",
        "Descriptive demo only; no inferential claim is made.",
        "The upstream NONE response is interpreted as NIE WIEM and is never a correct target class.",
    ])
    (results_root / "hypothesis_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(summary.to_string(index=False))
    print(f"results_dir={results_root}")
    print("NATIVE_TEXT_SEARCH_ANALYSIS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

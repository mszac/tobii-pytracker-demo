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
    return re.sub(r"[^0-9a-ząćęłńóśźż]+", "", str(value).lower())


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
    target = [normalize_token(x) for x in target_phrase.split()]
    target = [x for x in target if x]
    if not target:
        raise ValueError(f"Empty target phrase: {target_phrase!r}")

    for start in range(0, len(tokens) - len(target) + 1):
        if tokens[start:start + len(target)] == target:
            boxes = []
            for item in words[start:start + len(target)]:
                bbox = item.get("bbox", {})
                if not {"cx", "cy", "w", "h"}.issubset(bbox):
                    raise ValueError(f"Incomplete target bbox for {target_phrase!r}: {bbox}")
                boxes.append({k: float(bbox[k]) for k in ("cx", "cy", "w", "h")})
            return boxes
    raise ValueError(f"Target phrase {target_phrase!r} not found in text word bboxes")


def point_in_boxes(x: float, y: float, boxes: list[dict[str, float]], padding: float = 8.0) -> bool:
    for box in boxes:
        half_w = box["w"] / 2.0 + padding
        half_h = box["h"] / 2.0 + padding
        if (box["cx"] - half_w) <= x <= (box["cx"] + half_w) and (box["cy"] - half_h) <= y <= (box["cy"] + half_h):
            return True
    return False


def discover_ux_sessions(loader: DataLoader, stimuli: set[str]) -> list[str]:
    matches: list[str] = []
    for session in loader.get_subjects():
        raw = loader.get_subject_data(session, flatten=False)
        if "input_data" not in raw.columns:
            continue
        overlap = raw["input_data"].astype(str).isin(stimuli)
        if overlap.any():
            if len(raw) != EXPECTED_TRIALS or int(overlap.sum()) != EXPECTED_TRIALS:
                raise RuntimeError(
                    f"UX A/B session {session!r} is incomplete or mixed: "
                    f"rows={len(raw)}, matched_trials={int(overlap.sum())}, expected={EXPECTED_TRIALS}"
                )
            matches.append(session)
    if not matches:
        raise FileNotFoundError("No complete UX A/B session found under output/")
    return sorted(matches)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze completed UX A/B text-search sessions.")
    parser.add_argument("--session", action="append", help="Analyze only this output session; may be repeated.")
    args = parser.parse_args()

    script = Path(__file__).resolve()
    example_root = script.parents[1]
    repo_root = script.parents[3]
    config_path = example_root / "config.native.yaml"
    dataset_path = example_root / "data" / "text_search.csv"
    results_root = example_root / "results"
    results_root.mkdir(parents=True, exist_ok=True)

    stimuli_df = pd.read_csv(dataset_path)
    required_dataset = {"id", "condition", "answer", "target_phrase", "text"}
    missing_dataset = required_dataset - set(stimuli_df.columns)
    if missing_dataset:
        raise RuntimeError(f"Dataset missing columns: {sorted(missing_dataset)}")
    if len(stimuli_df) != EXPECTED_TRIALS:
        raise RuntimeError(f"Expected {EXPECTED_TRIALS} dataset rows, got {len(stimuli_df)}")

    config = CustomConfig(str(config_path))
    loader = DataLoader(config, root=repo_root)
    stimulus_lookup = stimuli_df.set_index("text", drop=False)
    stimulus_set = set(stimuli_df["text"].astype(str))

    sessions = args.session or discover_ux_sessions(loader, stimulus_set)
    trial_rows: list[dict[str, Any]] = []
    example_plot: tuple[str, int] | None = None

    for session in sessions:
        raw = loader.get_subject_data(session, flatten=False).reset_index(drop=True)
        if len(raw) != EXPECTED_TRIALS:
            raise RuntimeError(f"Session {session!r}: expected {EXPECTED_TRIALS} rows, got {len(raw)}")
        if not raw["input_data"].astype(str).isin(stimulus_set).all():
            raise RuntimeError(f"Session {session!r} contains non-UX-A/B trials")

        flat = loader.get_subject_data(session, flatten=True)
        if flat.empty:
            raise RuntimeError(f"Session {session!r} contains no usable gaze samples")
        flat = flat[flat["input_data"].astype(str).isin(stimulus_set)].copy()
        fixation_dir = results_root / "_fixation_runtime"
        fixations = FixationAnalyzer(fixation_dir, method="dispersion").analyze(flat)

        for slide_index, row in raw.iterrows():
            input_text = str(row["input_data"])
            meta = stimulus_lookup.loc[input_text]
            if isinstance(meta, pd.DataFrame):
                raise RuntimeError("Dataset text values must be unique for analysis joining")

            slide_flat = flat[pd.to_numeric(flat["slide_index"], errors="coerce") == slide_index].copy()
            gaze_samples = len(slide_flat)
            if gaze_samples == 0:
                raise RuntimeError(f"Session {session!r} trial {slide_index} has no gaze samples")

            slide_data = loader.get_slide_data(session, slide_index, flatten=False)
            target_boxes = find_target_boxes(slide_data.get("objects_bboxes", {}), str(meta["target_phrase"]))
            slide_fix = fixations[pd.to_numeric(fixations.get("slide_index"), errors="coerce") == slide_index].copy() if not fixations.empty else fixations.copy()
            if not slide_fix.empty:
                slide_fix = slide_fix.sort_values("fix_start").reset_index(drop=True)
                hit_mask = slide_fix.apply(
                    lambda f: point_in_boxes(float(f["x_mean"]), float(f["y_mean"]), target_boxes), axis=1
                )
                target_fix = slide_fix[hit_mask]
            else:
                hit_mask = pd.Series(dtype=bool)
                target_fix = slide_fix

            trial_start = pd.to_numeric(slide_flat["system_time"], errors="coerce").dropna().min()
            target_seen = not target_fix.empty
            if target_seen:
                first_fix = target_fix.iloc[0]
                ttff = float(first_fix["fix_start"] - trial_start) if pd.notna(trial_start) else float("nan")
                dwell = float(pd.to_numeric(target_fix["duration"], errors="coerce").fillna(0).sum())
                fixation_count = int(len(target_fix))
                first_target_time = float(first_fix["fix_start"])
                before_target = int((pd.to_numeric(slide_fix["fix_start"], errors="coerce") < first_target_time).sum())
                if example_plot is None:
                    example_plot = (session, slide_index)
            else:
                ttff = float("nan")
                dwell = 0.0
                fixation_count = 0
                before_target = int(len(slide_fix))

            expected = str(meta["answer"]).lower()
            observed = str(row.get("user_classification", "")).lower()
            trial_rows.append({
                "session": session,
                "slide_index": slide_index,
                "item_id": meta["id"],
                "condition": meta["condition"],
                "expected_answer": expected,
                "user_answer": observed,
                "correct": observed == expected,
                "target_phrase": meta["target_phrase"],
                "target_seen": target_seen,
                "ttff_target_s": ttff,
                "target_dwell_s": dwell,
                "target_fixation_count": fixation_count,
                "fixations_before_target": before_target,
                "gaze_samples": gaze_samples,
            })

    trial_metrics = pd.DataFrame(trial_rows)
    trial_metrics.to_csv(results_root / "trial_metrics.csv", index=False)

    condition_summary = (
        trial_metrics.groupby("condition", dropna=False)
        .agg(
            trials=("item_id", "size"),
            accuracy=("correct", "mean"),
            target_seen_rate=("target_seen", "mean"),
            mean_ttff_target_s=("ttff_target_s", "mean"),
            mean_target_dwell_s=("target_dwell_s", "mean"),
            mean_target_fixation_count=("target_fixation_count", "mean"),
        )
        .reset_index()
    )
    condition_summary.to_csv(results_root / "condition_summary.csv", index=False)

    ttff_plot = trial_metrics.dropna(subset=["ttff_target_s"]).groupby("condition")["ttff_target_s"].mean()
    fig, ax = plt.subplots(figsize=(7, 4))
    if ttff_plot.empty:
        ax.text(0.5, 0.5, "No target fixations detected", ha="center", va="center", transform=ax.transAxes)
        ax.set_xticks([])
    else:
        ttff_plot.plot(kind="bar", ax=ax)
    ax.set_ylabel("Mean TTFF to target [s]")
    ax.set_title("Target acquisition: EARLY vs LATE")
    fig.tight_layout()
    fig.savefig(results_root / "ttff_by_condition.png", dpi=160)
    plt.close(fig)

    accuracy_plot = trial_metrics.groupby("target_seen")["correct"].mean().reindex([False, True])
    fig, ax = plt.subplots(figsize=(7, 4))
    if accuracy_plot.dropna().empty:
        ax.text(0.5, 0.5, "No classified trials", ha="center", va="center", transform=ax.transAxes)
        ax.set_xticks([])
    else:
        accuracy_plot.plot(kind="bar", ax=ax)
        ax.set_xticklabels(["target not fixated", "target fixated"], rotation=0)
    ax.set_ylabel("Accuracy")
    ax.set_ylim(0, 1)
    ax.set_title("Accuracy by target fixation")
    fig.tight_layout()
    fig.savefig(results_root / "accuracy_by_target_seen.png", dpi=160)
    plt.close(fig)

    if example_plot is None:
        first = trial_metrics.iloc[0]
        example_plot = (str(first["session"]), int(first["slide_index"]))
    loader.plot_gaze(
        example_plot[0],
        example_plot[1],
        save_path=results_root / "example_trial_gaze.png",
        show=False,
        gradient=True,
    )

    early = condition_summary[condition_summary["condition"].astype(str).str.upper() == "EARLY"]
    late = condition_summary[condition_summary["condition"].astype(str).str.upper() == "LATE"]
    summary_lines = [
        "UX A/B text-search demo — descriptive analysis",
        f"sessions={len(sessions)}",
        f"trials={len(trial_metrics)}",
        f"overall_accuracy={trial_metrics['correct'].mean():.3f}",
        f"target_seen_rate={trial_metrics['target_seen'].mean():.3f}",
    ]
    if not early.empty and not late.empty:
        summary_lines.extend([
            f"EARLY_mean_TTFF_s={early.iloc[0]['mean_ttff_target_s']}",
            f"LATE_mean_TTFF_s={late.iloc[0]['mean_ttff_target_s']}",
        ])
    summary_lines.extend([
        "",
        "Interpretation: descriptive demo only; no inferential claim is made.",
        "H2 demo expectation: EARLY TTFF < LATE TTFF.",
        "H3 demo expectation: accuracy may be higher when the target is fixated.",
    ])
    (results_root / "hypothesis_summary.txt").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    # Analyzer-generated scratch files are not part of the user-facing result set.
    if fixation_dir.exists() and not any(fixation_dir.iterdir()):
        fixation_dir.rmdir()

    print(condition_summary.to_string(index=False))
    print(f"results_dir={results_root}")
    print("NATIVE_UX_AB_ANALYSIS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Tobii native text-search demo

This example migrates the supplied legacy `2_tobii_text_search_demo` to the current native workflow without modifying the original `sbobek/tobii-pytracker` checkout.

## What changed from the legacy bundle

Removed from the runtime path:

- `apply_repo_fixes.py`;
- local/duplicate eyetracker configuration;
- source patches for YAML/CSV encoding;
- source patch that renamed upstream `NONE` to `NIE WIEM`;
- `.bat` wrappers tied to the old repository layout.

The current upstream is the only package/runtime authority. `NONE` remains the upstream button label and means **NIE WIEM** in this demo.

The source dataset logic is preserved: 12 trials, 6 EARLY / 6 LATE and 3 TAK / 3 NIE within each condition. The rendered text is normalized to a single line so native PsychoPy word bboxes stay aligned with the displayed stimulus.

## Run

From the parent `tobii-pytracker` directory:

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/tobii_text_search_demo/run_native.sh
```

MouseGaze controls:

- hold RIGHT mouse button while moving to generate gaze;
- release RIGHT before LEFT CLICK;
- click `TAK`, `NIE`, or `NONE` (`NONE` = `NIE WIEM`).

A valid 12-trial collection ends with:

```text
NATIVE_TEXT_SEARCH_COLLECTION_PASS
NATIVE_TEXT_SEARCH_COLLECTION_COMPLETE
```

## Analyze

From the parent `tobii-pytracker` directory:

```bash
conda run --no-capture-output -n pytracker-env \
  python tobii-pytracker-demo/examples/tobii_text_search_demo/analysis/analyze_results.py
```

Expected final marker:

```text
NATIVE_TEXT_SEARCH_ANALYSIS_PASS
```

User-facing outputs are written to `examples/tobii_text_search_demo/results/` and include trial metrics, condition summary, four hypothesis-oriented charts, one gaze overlay and a descriptive hypothesis summary.

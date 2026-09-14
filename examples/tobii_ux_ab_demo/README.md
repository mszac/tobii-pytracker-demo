# Tobii UX A/B text-search demo

Migrated native example for `https://github.com/mszac/tobii-pytracker-demo`.

The legacy source contract in `__previous-examples/1 tobii_ux_ab_demo/README.md` described a 12-trial text-search task with EARLY/LATE information placement and later analysis of accuracy, target fixation, TTFF and dwell time. This version aligns that workflow with the already working native `smoke_images` architecture: the demo repository is cloned inside a clean upstream `tobii-pytracker` clone, relative paths resolve from the demo-repository root, and MouseGaze uses the original upstream tracker config.

## Run

From the `tobii-pytracker-demo` repository root, after the common native preflight:

```bash
conda run --no-capture-output -n pytracker-env bash examples/tobii_ux_ab_demo/run_native.sh
```

Controls are the original upstream MouseGaze controls:

- hold RIGHT mouse button while moving to generate gaze samples;
- release RIGHT before LEFT CLICK;
- click TAK or NIE to answer;
- do not select the upstream-added NONE button;
- SPACE starts the procedure;
- ESC exits after the outro.

The run is forced to exactly 12 trials and writes to the shared repository-root `output/<session>/data.csv`.

## Analyze

After one or more completed UX A/B sessions:

```bash
conda run --no-capture-output -n pytracker-env python examples/tobii_ux_ab_demo/analysis/analyze_results.py
```

The analyzer ignores unrelated output sessions (for example the three-image smoke session), requires complete 12-trial UX A/B sessions, uses `DataLoader` and `FixationAnalyzer` from the installed upstream package, and writes generated files under:

```text
examples/tobii_ux_ab_demo/results/
```

Expected files include `trial_metrics.csv`, `condition_summary.csv`, `hypothesis_summary.txt`, `ttff_by_condition.png`, `accuracy_by_target_seen.png`, and `example_trial_gaze.png`.

Successful completion prints `NATIVE_UX_AB_ANALYSIS_PASS`.

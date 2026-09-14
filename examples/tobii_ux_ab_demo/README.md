# Tobii UX A/B text-search demo

Migrated native example for `https://github.com/mszac/tobii-pytracker-demo`.

The legacy source contract in `__previous-examples/1 tobii_ux_ab_demo/README.md` described a 12-trial text-search task with EARLY/LATE information placement and later analysis of accuracy, target fixation, TTFF and dwell time. This version aligns that workflow with the already working native `smoke_images` architecture. The demo repository is cloned inside a clean upstream `tobii-pytracker` clone, and the user's terminal remains at the **parent upstream root**. The launcher internally switches to the demo root so its relative config/data/output paths preserve the validated behavior.

Before running, verify from `tobii-pytracker` that the launcher exists:

```bash
test -f tobii-pytracker-demo/examples/tobii_ux_ab_demo/run_native.sh && echo "RUNNER_OK"
```

## Run

From the original `tobii-pytracker` root, after the common native preflight:

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/tobii_ux_ab_demo/run_native.sh
```

Controls are the original upstream MouseGaze controls:

- hold RIGHT mouse button while moving to generate gaze samples;
- release RIGHT before LEFT CLICK;
- click TAK or NIE to answer;
- do not select the upstream-added NONE button;
- SPACE starts the procedure;
- ESC exits after the outro.

The run is forced to exactly 12 trials and writes to `tobii-pytracker-demo/output/<session>/data.csv`.

## Analyze

After one or more completed UX A/B sessions, still from `tobii-pytracker`:

```bash
conda run --no-capture-output -n pytracker-env python tobii-pytracker-demo/examples/tobii_ux_ab_demo/analysis/analyze_results.py
```

The analyzer ignores unrelated output sessions (for example the three-image smoke session), requires complete 12-trial UX A/B sessions, uses `DataLoader` and `FixationAnalyzer` from the installed upstream package, and writes generated files under:

```text
tobii-pytracker-demo/examples/tobii_ux_ab_demo/results/
```

Expected files include `trial_metrics.csv`, `condition_summary.csv`, `hypothesis_summary.txt`, `ttff_by_condition.png`, `accuracy_by_target_seen.png`, and `example_trial_gaze.png`.

Successful completion prints `NATIVE_UX_AB_ANALYSIS_PASS`.

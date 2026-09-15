# Tobii UX A/B text-search demo

12-trial EARLY/LATE information-placement experiment using the unmodified upstream runtime.

## Run

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/tobii_ux_ab_demo/run_native.sh
```

Hold RIGHT while moving for MouseGaze, release RIGHT, then LEFT-click TAK or NIE. The stimulus remains visible until a response. Collection is isolated under `tobii-pytracker-demo/output/tobii_ux_ab_demo/`. Missing gaze is a warning rather than a reason to discard a completed response trial.

Expected collection markers: `NATIVE_UX_AB_COLLECTION_PASS`, `NATIVE_UX_AB_COLLECTION_COMPLETE`.

## Analyze in Jupyter

```bash
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/tobii_ux_ab_demo/analysis/ux_ab_analysis.ipynb
```

The notebook reads real experiment output, uses upstream `FixationAnalyzer` when gaze is available, and keeps behavioral accuracy analysis for trials without gaze.

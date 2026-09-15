# Three-image TEST DEMO

Purpose: end-to-end test of image presentation, interactive response buttons, MouseGaze collection, output creation and notebook analysis.

## Interaction

Each image remains visible without a response timeout until the participant LEFT-clicks HUMAN, ANIMAL, OBJECT or NONE. For MouseGaze hold RIGHT while moving, then release RIGHT before the LEFT-click response. Missing gaze does not invalidate an otherwise complete behavioral trial; it is reported as a data-quality warning.

## Run

From the parent `tobii-pytracker` root:

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/test_demo/run.sh
```

The collection validator confirms the completed three-trial session. Output is isolated under `tobii-pytracker-demo/output/test_demo/<session>/data.csv`.

## Analyze in Jupyter

```bash
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/test_demo/analysis/test_demo_analysis.ipynb
```

The notebook reads only real collected `data.csv`, reports response accuracy for all trials and gaze/fixation/saccade/entropy metrics where gaze exists.

# Native image gaze smoke demo

Purpose: a minimal end-to-end validation of image presentation, upstream MouseGaze collection, output creation and post-hoc analysis using public `tobii-pytracker` analyzers.

The three stimuli represent three deliberately broad semantic categories: **human**, **animal** and **object**. The scientific interpretation is intentionally modest: the demo can illustrate differences in spatial exploration across semantically different images, but three stimuli from one participant are only a pipeline smoke test, not an inferential study.

Before running, verify from `tobii-pytracker` that the launcher exists:

```bash
test -f tobii-pytracker-demo/examples/smoke_images/run_native.sh && echo "RUNNER_OK"
```

## Collection

Keep the terminal in the original parent `tobii-pytracker` root and invoke the nested demo launcher:

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/smoke_images/run_native.sh
```

The launcher internally establishes the `tobii-pytracker-demo` working directory because the config uses demo-root-relative paths.

MouseGaze uses the **original upstream controls**:

- hold RIGHT mouse button and move the pointer to generate gaze samples;
- release RIGHT before LEFT CLICK;
- LEFT CLICK selects the category;
- SPACE starts the procedure;
- ESC exits after the outro.

The run is forced to exactly three trials. Generate at least some gaze on every image.

## Analysis

After the experiment exits, still from `tobii-pytracker`:

```bash
conda run --no-capture-output -n pytracker-env python tobii-pytracker-demo/examples/smoke_images/analysis/analyze_output.py --output-root tobii-pytracker-demo/output
```

The analysis requires exactly three trials and gaze data on all three. It uses the public pytracker analyzers for heatmap statistics, fixation detection, saccade detection and spatial entropy. Lack of detected fixations or saccades is allowed; lack of gaze on any trial is a smoke-test failure.

# Native image gaze smoke demo

Purpose: a minimal end-to-end validation of image presentation, upstream MouseGaze collection, output creation and post-hoc analysis using public `tobii-pytracker` analyzers.

The three stimuli represent three deliberately broad semantic categories: **human**, **animal** and **object**. The scientific interpretation is intentionally modest: the demo can illustrate differences in spatial exploration across semantically different images, but three stimuli from one participant are only a pipeline smoke test, not an inferential study.

## Collection

Run from the root of `tobii-pytracker-examples`, which is cloned inside the original `tobii-pytracker` directory:

```bash
bash examples/smoke_images/run_native.sh
```

MouseGaze uses the **original upstream controls**:

- hold RIGHT mouse button and move the pointer to generate gaze samples;
- release RIGHT before LEFT CLICK;
- LEFT CLICK selects the category;
- SPACE starts the procedure;
- ESC exits after the outro.

The run is forced to exactly three trials. Generate at least some gaze on every image.

## Analysis

After the experiment exits:

```bash
python examples/smoke_images/analysis/analyze_output.py --output-root output
```

The analysis requires exactly three trials and gaze data on all three. It uses the public pytracker analyzers for heatmap statistics, fixation detection, saccade detection and spatial entropy. Lack of detected fixations or saccades is allowed; lack of gaze on any trial is a smoke-test failure.

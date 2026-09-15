# Time-Series Noise Demo

## Modality

**Time-series data** — 18 fixed CSV stimuli across two signal domains.

## Research question

How do people visually inspect and classify different levels of short-term variability in time-series signals, and does the inspection strategy change when the same LOW/MEDIUM/HIGH judgment is applied to different signal domains?

The demo uses built-in `dataset.time_series` support rather than pre-rendered plot images. This preserves the sample structure in the experiment data and exposes per-sample spatial regions through `timeseries_bboxes`.

## Experimental design

There are two domain blocks and 18 total stimuli:

| Domain | LOW | MEDIUM | HIGH | Total |
|---|---:|---:|---:|---:|
| Machine vibration | 3 | 3 | 3 | 9 |
| PV power | 3 | 3 | 3 | 9 |
| **Total** | **6** | **6** | **6** | **18** |

Each CSV row is one signal. It contains:

- a stimulus identifier;
- one domain-specific numeric value;
- 128 ordered time-series samples;
- the target class `low`, `medium`, or `high`.

The two CSV fixtures are committed directly to the repository. There is no data generator in the final demo and no PNG plot dataset.

## Participant task

In the machine-vibration block the participant judges the magnitude of irregular vibration fluctuations. In the PV-power block the participant judges the magnitude of short-term production fluctuations. The available target responses are **LOW**, **MEDIUM**, and **HIGH**.

The trial remains visible until a response is selected.

## Scientific rationale

Time-series interpretation requires observers to integrate information distributed over the horizontal axis rather than inspect a single localized object. Eye tracking can therefore be used to study **where along the temporal sequence participants sample evidence before committing to a category**.

The example is useful for several research questions:

1. **Variability and inspection effort**
   Signals with greater or more ambiguous variability may elicit more fixations or longer viewing before classification.

2. **Ambiguity of the middle class**
   `MEDIUM` signals lie between the LOW and HIGH category prototypes. They may therefore require more comparison across peaks, troughs, or extended intervals.

3. **Horizontal coverage**
   Because samples are spatially ordered, gaze coverage can be expressed in terms of how much of the time axis was inspected and which temporal regions received the most attention.

4. **Domain dependence**
   The same variability judgment is performed on machine-vibration and PV-power signals. Differences in gaze strategy between domains can reveal whether participants rely on the same visual cues when the signal context changes.

5. **Decision confidence**
   Longer inspection, repeated revisits, or broader horizontal exploration may accompany uncertain classifications, although such measures should not be equated directly with confidence without an explicit confidence measure.

## Example hypotheses

- **H1 — Variability and effort:** fixation count tends to increase from LOW to HIGH.
- **H2 — Middle-category ambiguity:** MEDIUM produces the longest or most distributed visual decision process.
- **H3 — Exploration:** HIGH variability produces broader horizontal exploration of the time axis.
- **H4 — Domain effect:** machine-vibration and PV-power signals produce different gaze distributions for the same nominal variability class.
- **H5 — Behavioral difficulty:** MEDIUM has lower classification accuracy than the two more extreme classes.

These hypotheses are descriptive starting points rather than validated effects.

## Measures that are scientifically meaningful here

- classification accuracy;
- total trial duration;
- fixation count and fixation duration;
- horizontal gaze span or sample-index coverage;
- first-viewed and most-viewed temporal regions;
- revisits to previously inspected regions;
- gaze distribution across equal-width time segments;
- comparisons by variability class and signal domain.

The per-sample bounding boxes make it possible to express gaze relative to the underlying time-series index rather than only as raw screen coordinates.

## Why this is a useful basic example

The demo shows that `tobii-pytracker` is not limited to conventional text or image stimuli. It demonstrates how structured numeric sequences can remain structured numeric data throughout presentation and gaze collection, enabling analyses that refer back to individual samples or temporal regions.

## Limitations

- The signals are fixed demonstration fixtures rather than a validated perceptual stimulus set.
- Domain is blocked rather than fully randomized, so domain comparisons can be influenced by order and practice effects.
- LOW/MEDIUM/HIGH labels describe the constructed examples and should not be interpreted as universal thresholds.
- A full experiment should counterbalance or randomize block order across participants if domain differences are a primary research question.

## Run the demo

See the root [setup and execution guide](../../README_TESTING.md).

Demo directory: `examples/timeseries_noise_demo/`.

## Jupyter analysis

The analysis workflow is documented inside the notebook itself. It combines gaze/fixation summaries with sample-index attention derived from the stored time-series bounding boxes, including temporal coverage, segment-level attention, revisits, entropy, domain/class comparisons, and representative signal overlays. Short notes identify which stages use `tobii-pytracker` analyzers and which are specific to the sample-index interpretation.

Notebook: `examples/timeseries_noise_demo/analysis/timeseries_analysis.ipynb`.

## Further reading

- Duchowski, A. T. (2017). *Eye Tracking Methodology: Theory and Practice* (3rd ed.). Springer. DOI: 10.1007/978-3-319-57883-5.

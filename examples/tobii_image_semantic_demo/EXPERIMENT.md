# Experiment contract — 12-image semantic gaze demo

## Purpose

Demonstrate a longer native image experiment while retaining a simple interpretable task. The participant sees 12 images and assigns each image to one of three broad categories: `BIOLOGICAL`, `OBJECT`, or `SCENE`.

## Design

- 12 committed local image stimuli.
- 3 semantic classes.
- 4 images per class.
- Trial order is randomized by the upstream `ImageDataset` loader.
- Each image is rendered inside the same 900x700 AOI.
- `bbox_model: grid` produces the upstream 3x3 image AOI grid.
- MouseGaze uses the untouched upstream configuration.

## Descriptive questions

H1 / pipeline sanity: classification accuracy should be measurable for all 12 trials.

H2 / exploration: gaze-sample, fixation and saccade counts can be compared descriptively between semantic classes.

H3 / spatial exploration: the upstream heatmap and entropy analyzers provide per-image exploration summaries suitable for demonstrating downstream analysis.

These are demonstration questions only. No inferential claim should be made from this stimulus set.

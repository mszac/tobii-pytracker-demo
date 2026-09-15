# Image Semantic Demo

## Modality

**Image data** — 12 mixed semantic-classification trials.

## Research question

Do gaze patterns differ while observers categorize images from broad semantic classes, and what spatial evidence is sampled before a category decision?

The example is intentionally simple: it uses three broad classes — **BIOLOGICAL**, **OBJECT**, and **SCENE** — to demonstrate how image classification, spatial AOIs, gaze data, and behavioral responses can be collected in a single experiment.

## Experimental design

The stimulus set contains 12 distinct images:

- 4 `BIOLOGICAL`;
- 4 `OBJECT`;
- 4 `SCENE`.

At the start of each session, the demo shuffles images within each class and constructs a constrained mixed sequence. Every consecutive group of three trials contains one image from each category and adjacent trials cannot share a category. There are no visible category blocks.

Only three response buttons are shown: **BIOLOGICAL**, **OBJECT**, and **SCENE**. The generic upstream `NONE` response is deliberately removed for this demo so the task is a forced-choice three-class categorization.

## Participant task

The participant views the image and selects the semantic category that best describes it. The image remains visible until the participant responds.

## Scientific rationale

Image categorization involves both rapid global processing and selective inspection of local visual evidence. Eye tracking provides a way to observe how the participant distributes attention before choosing a category.

This basic example supports several kinds of exploratory question:

1. **Category-dependent exploration**
   Biological stimuli, single objects, and broader scenes may produce different spatial distributions of fixations because the information needed for categorization is organized differently across the image.

2. **Local versus global evidence**
   A compact object can be identified from a relatively localized region, while a scene may require broader spatial sampling. A coarse AOI grid provides a simple way to quantify this difference without requiring semantic object annotations.

3. **Decision efficiency**
   Correct classifications reached after fewer fixations or shorter viewing may indicate that category evidence was visually accessible, whereas longer scanpaths can identify stimuli that require more exploration.

4. **Spatial concentration**
   Heatmaps, fixation dispersion, and entropy-like measures can describe whether gaze is concentrated in a small number of regions or distributed broadly across the image.

5. **Stimulus-level diagnostics**
   Because the demo contains several exemplars per category, an experimenter can identify individual images that produce unusually high error rates or atypical gaze patterns.

## Example hypotheses

- **H1 — Category effect:** gaze distribution differs across BIOLOGICAL, OBJECT, and SCENE stimuli.
- **H2 — Spatial breadth:** SCENE trials tend to produce broader spatial exploration than compact OBJECT trials.
- **H3 — Decision efficiency:** correctly classified stimuli tend to require fewer or shorter fixations than difficult/misclassified stimuli.
- **H4 — Stimulus heterogeneity:** within-category exemplars can still show substantial differences, emphasizing the importance of stimulus-level inspection rather than category averages alone.

These are illustrative hypotheses. The 12-image set is not designed as a normed semantic-perception battery.

## Measures that are scientifically meaningful here

- category response and accuracy;
- trial duration;
- fixation count and duration;
- saccade count and amplitude;
- gaze distribution across the 3×3 image grid;
- spatial dispersion or entropy;
- heatmaps by stimulus or category;
- stimulus-level and category-level error patterns.

## Why constrained mixing matters

Presenting all images from one category as a block would make the previous trial highly predictive of the next response and could create adaptation, expectation, and simple response-repetition effects. The constrained mixed order keeps category frequency balanced locally while reducing obvious run-length structure.

## Why this is a useful basic example

The demo demonstrates the standard image-dataset workflow while still having a meaningful behavioral task. It shows how folder-based class labels, image presentation, response buttons, coarse spatial bounding boxes, and gaze data can be combined without requiring a separate object-detection model.

## Limitations

- The three categories are intentionally broad and visually heterogeneous.
- The stimulus set is small and not matched for luminance, complexity, salience, or semantic familiarity.
- The 3×3 grid is a coarse spatial representation, not a semantic AOI model.
- Any confirmatory category comparison would need more stimuli, more participants, and tighter stimulus control.

## Run the demo

See the root [setup and execution guide](../../README_TESTING.md).

Demo directory: `examples/image_semantic_demo/`.

## Jupyter analysis

The analysis workflow is documented inside the notebook itself. It demonstrates fixation, saccade, scanpath, entropy, heatmap/focus-map, clustering, and 3×3 grid attention analyses, with both category-level and stimulus-level diagnostics. Short notes indicate where the public `tobii-pytracker` analyzers provide the analytical operation.

Notebook: `examples/image_semantic_demo/analysis/image_semantic_analysis.ipynb`.

## Further reading

- Duchowski, A. T. (2017). *Eye Tracking Methodology: Theory and Practice* (3rd ed.). Springer. DOI: 10.1007/978-3-319-57883-5.
- Goldberg, J. H., & Kotval, X. P. (1999). *Computer interface evaluation using eye movements: methods and constructs*. International Journal of Industrial Ergonomics, 24(6), 631–645. DOI: 10.1016/S0169-8141(98)00068-7.

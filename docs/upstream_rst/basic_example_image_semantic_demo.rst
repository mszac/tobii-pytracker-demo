.. _basic-example-image-semantic-demo:

===================
Image Semantic Demo
===================

Modality
--------

**Image data** -- 12 mixed semantic-classification trials.

Research question
-----------------

Do gaze patterns differ while observers categorize images from broad semantic
classes, and what spatial evidence is sampled before a category decision?

The example uses three intentionally broad classes -- ``BIOLOGICAL``,
``OBJECT``, and ``SCENE`` -- to demonstrate how image classification, spatial
AOIs, gaze data, and behavioral responses can be collected in one experiment.

Experimental design
-------------------

The stimulus set contains 12 distinct images:

* 4 ``BIOLOGICAL``;
* 4 ``OBJECT``;
* 4 ``SCENE``.

At the beginning of each session, images are shuffled within class and a
constrained mixed sequence is constructed.  Every consecutive group of three
trials contains one image from each category, and adjacent trials cannot share
a category.  The participant therefore does not encounter visible category
blocks.

Only three response buttons are shown: ``BIOLOGICAL``, ``OBJECT``, and
``SCENE``.  The generic upstream ``NONE`` response is deliberately removed for
this example so that the task is a forced-choice three-class categorization.

Participant task
----------------

The participant views an image and selects the semantic category that best
describes it.  The image remains visible until a response is selected.

Scientific rationale
--------------------

Image categorization can combine rapid global processing with selective
inspection of local visual evidence.  Eye tracking provides a way to observe
how attention is distributed before the participant chooses a category.

The example supports several exploratory questions:

1. **Category-dependent exploration.**
   Biological stimuli, single objects, and scenes can differ in the spatial
   distribution of information needed for categorization.
2. **Local versus global evidence.**
   A compact object may be identified from a localized region, while a scene
   can require broader spatial sampling.  A coarse AOI grid provides a simple
   way to quantify this difference without semantic object annotations.
3. **Decision efficiency.**
   Correct classifications reached after fewer fixations or shorter viewing
   can identify stimuli whose category evidence is visually accessible, while
   longer scanpaths can flag trials that require more exploration.
4. **Spatial concentration.**
   Heatmaps, fixation dispersion, and entropy-like measures describe whether
   gaze is concentrated or broadly distributed.
5. **Stimulus-level diagnostics.**
   Multiple exemplars per class make it possible to detect individual images
   that produce unusually high error rates or atypical gaze patterns.

Example hypotheses
------------------

* **H1 -- Category effect:** gaze distribution differs across BIOLOGICAL,
  OBJECT, and SCENE stimuli.
* **H2 -- Spatial breadth:** SCENE trials tend to produce broader spatial
  exploration than compact OBJECT trials.
* **H3 -- Decision efficiency:** correctly classified stimuli tend to require
  fewer or shorter fixations than difficult or misclassified stimuli.
* **H4 -- Stimulus heterogeneity:** within-category exemplars can show
  substantial differences, so stimulus-level inspection remains important.

These are illustrative hypotheses.  The 12-image set is not a normed
semantic-perception battery.

Scientifically useful measures
------------------------------

* category response and accuracy;
* trial duration;
* fixation count and duration;
* saccade count and amplitude;
* gaze distribution across the 3x3 image grid;
* spatial dispersion or entropy;
* heatmaps by stimulus or category;
* stimulus-level and category-level error patterns.

Why constrained mixing matters
------------------------------

Presenting one category as a block would make the preceding trial predictive of
the next response and could introduce adaptation, expectation, or simple
response-repetition effects.  Constrained mixing keeps category frequency
balanced locally while reducing obvious run-length structure.

Tobii-Pytracker analysis support
--------------------------------

This example can use the largest part of the built-in analysis API directly.
The companion notebook uses ``DataLoader``, ``FixationAnalyzer``,
``SaccadeAnalyzer``, ``ScanpathsAnalyzer``, ``EntropyAnalyzer``,
``HeatmapAnalyzer``, ``FocusMapAnalyzer``, ``ClusterAnalyzer``, and
``BBoxAttentionAnalyzer``.  The 3x3 grid is represented by the image bounding
boxes saved with each trial.  See :doc:`data_analyzers` for an overview of the
available analyzer classes.

Why this is a useful basic example
----------------------------------

The example demonstrates the standard image-dataset workflow while retaining a
meaningful behavioral task.  It combines folder-based class labels, image
presentation, interactive responses, coarse spatial bounding boxes, and gaze
recording without requiring an external object-detection model.

Limitations
-----------

* The three categories are deliberately broad and visually heterogeneous.
* The stimulus set is small and not matched for luminance, complexity, salience,
  or semantic familiarity.
* The 3x3 grid is a coarse spatial representation, not a semantic AOI model.
* Confirmatory category comparisons require more stimuli, more participants,
  and tighter stimulus control.

Implementation and analysis notebook
------------------------------------

* `Image Semantic Demo directory <https://github.com/mszac/tobii-pytracker-demo/tree/main/examples/image_semantic_demo>`_
* `Jupyter analysis notebook <https://github.com/mszac/tobii-pytracker-demo/blob/main/examples/image_semantic_demo/analysis/image_semantic_analysis.ipynb>`_
* `Demo setup and execution guide <https://github.com/mszac/tobii-pytracker-demo/blob/main/README_TESTING.md>`_

The notebook demonstrates fixation, saccade, scanpath, entropy,
heatmap/focus-map, clustering, and 3x3-grid attention analyses with category-
and stimulus-level diagnostics.  It also marks which operations are supplied by
the Tobii-Pytracker analysis API.

Further reading
---------------

* Duchowski, A. T. (2017). *Eye Tracking Methodology: Theory and Practice*
  (3rd ed.). Springer. DOI: 10.1007/978-3-319-57883-5.
* Goldberg, J. H., & Kotval, X. P. (1999). *Computer interface evaluation using
  eye movements: methods and constructs*. International Journal of Industrial
  Ergonomics, 24(6), 631--645. DOI: 10.1016/S0169-8141(98)00068-7.

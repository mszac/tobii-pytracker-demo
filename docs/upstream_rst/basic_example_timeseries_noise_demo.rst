.. _basic-example-timeseries-noise-demo:

======================
Time-Series Noise Demo
======================

Modality
--------

**Time-series data** -- 18 fixed CSV stimuli across two signal domains.

Research question
-----------------

How do people visually inspect and classify different levels of short-term
variability in time-series signals, and does the inspection strategy change
when the same ``LOW``/``MEDIUM``/``HIGH`` judgment is applied to different
signal domains?

The example uses the built-in ``dataset.time_series`` workflow rather than
pre-rendered plot images.  The numeric sample structure is therefore retained in
the experiment data and per-sample spatial regions are available through
``timeseries_bboxes``.

Experimental design
-------------------

There are two domain blocks and 18 total stimuli:

.. list-table:: Stimulus balance
   :header-rows: 1
   :widths: 35 15 15 15 15

   * - Domain
     - LOW
     - MEDIUM
     - HIGH
     - Total
   * - Machine vibration
     - 3
     - 3
     - 3
     - 9
   * - PV power
     - 3
     - 3
     - 3
     - 9
   * - **Total**
     - **6**
     - **6**
     - **6**
     - **18**

Each CSV row represents one signal and contains a stimulus identifier, ordered
numeric samples, and the target class ``low``, ``medium``, or ``high``.  The two
fixed CSV fixtures are committed directly to the companion repository; the
final demo does not generate the series or convert them to PNG stimuli.

Participant task
----------------

In the machine-vibration block, the participant judges the magnitude of
irregular vibration fluctuations.  In the PV-power block, the participant
judges the magnitude of short-term production fluctuations.  Available target
responses are ``LOW``, ``MEDIUM``, and ``HIGH``.

Each trial remains visible until the participant selects a response.

Scientific rationale
--------------------

Time-series interpretation requires evidence to be integrated across the
horizontal axis rather than within one localized object.  Eye tracking can
therefore be used to examine **where along the sequence participants sample
visual evidence before committing to a category**.

The example supports several descriptive questions:

1. **Variability and inspection effort.**
   Signals with greater or more ambiguous variability may elicit more fixations
   or longer viewing before classification.
2. **Ambiguity of the middle class.**
   ``MEDIUM`` signals lie between LOW and HIGH category prototypes and may
   require more comparison across peaks, troughs, or intervals.
3. **Horizontal coverage.**
   Gaze coverage can be expressed as how much of the sample index was visually
   inspected and which temporal regions received the most attention.
4. **Domain dependence.**
   Machine-vibration and PV-power signals allow the same nominal variability
   judgment to be compared across two signal contexts.
5. **Decision difficulty.**
   Longer inspection, repeated revisits, or broader exploration can accompany a
   difficult decision, although these measures should not be interpreted as a
   direct confidence measure without collecting confidence explicitly.

Example hypotheses
------------------

* **H1 -- Variability and effort:** fixation count tends to increase from LOW to
  HIGH.
* **H2 -- Middle-category ambiguity:** MEDIUM produces the longest or most
  distributed visual decision process.
* **H3 -- Exploration:** HIGH variability produces broader horizontal
  exploration of the time axis.
* **H4 -- Domain effect:** machine-vibration and PV-power signals produce
  different gaze distributions for the same nominal class.
* **H5 -- Behavioral difficulty:** MEDIUM has lower classification accuracy than
  the two more extreme classes.

These are descriptive starting points rather than validated effects.

Scientifically useful measures
------------------------------

* classification accuracy;
* total trial duration;
* fixation count and fixation duration;
* horizontal gaze span and sample-index coverage;
* first-viewed and most-viewed temporal regions;
* revisits to previously inspected regions;
* gaze distribution across equal-width time segments;
* comparisons by variability class and signal domain.

The per-sample bounding boxes allow attention to be expressed relative to the
underlying sample index rather than only as screen coordinates.

Tobii-Pytracker analysis support
--------------------------------

The companion notebook uses ``DataLoader`` to load recorded sessions,
``FixationAnalyzer`` for fixation extraction, ``ScanpathsAnalyzer`` for
fixation-transition summaries, and ``EntropyAnalyzer`` for screen-space gaze
dispersion.  Mapping fixations to sample indices and computing one-dimensional
temporal coverage/entropy are experiment-specific operations based on stored
``timeseries_bboxes``.  See :doc:`data_analyzers` for the available analyzers.

Why this is a useful basic example
----------------------------------

The example demonstrates that Tobii-Pytracker is not limited to conventional
text or image stimuli.  Structured numeric sequences remain structured data
throughout presentation and recording, enabling analysis relative to individual
samples or temporal regions.

Limitations
-----------

* The signals are fixed demonstration fixtures rather than a validated
  perceptual stimulus set.
* Domain is blocked rather than fully randomized, so domain comparisons can be
  influenced by order and practice effects.
* LOW/MEDIUM/HIGH describe the constructed examples and are not universal
  signal thresholds.
* A full experiment should counterbalance or randomize block order across
  participants when domain differences are a primary research question.

Implementation and analysis notebook
------------------------------------

* `Time-Series Noise Demo directory <https://github.com/mszac/tobii-pytracker-demo/tree/main/examples/timeseries_noise_demo>`_
* `Jupyter analysis notebook <https://github.com/mszac/tobii-pytracker-demo/blob/main/examples/timeseries_noise_demo/analysis/timeseries_analysis.ipynb>`_
* `Demo setup and execution guide <https://github.com/mszac/tobii-pytracker-demo/blob/main/README_TESTING.md>`_

The notebook combines gaze/fixation summaries with sample-index attention,
including temporal coverage, segment-level attention, revisits, entropy,
domain/class comparisons, and representative signal overlays.  Notes in the
notebook distinguish built-in Tobii-Pytracker analysis from sample-index logic
specific to this experiment.

Further reading
---------------

* Duchowski, A. T. (2017). *Eye Tracking Methodology: Theory and Practice*
  (3rd ed.). Springer. DOI: 10.1007/978-3-319-57883-5.

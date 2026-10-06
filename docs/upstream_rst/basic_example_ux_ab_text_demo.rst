.. _basic-example-ux-ab-text-demo:

==================
UX A/B Text Demo
==================

Modality
--------

**Text data** -- 12 response-gated trials.

Research question
-----------------

How does the position of answer-relevant information within a short
interface-style text affect visual search and decision behavior?

The example implements a controlled **EARLY versus LATE** information-placement
manipulation.  The same type of practical question is paired with
answer-relevant information located either near the beginning or near the end
of the text.  The design therefore models a common UX problem: whether
information architecture places decision-critical content where users can find
it efficiently.

Experimental design
-------------------

The English dataset contains 12 trials:

* 6 ``EARLY`` trials, where the answer-relevant phrase occurs in the first
  sentence;
* 6 ``LATE`` trials, where the corresponding phrase occurs in the final
  sentence;
* within each condition, 3 correct answers are ``YES`` and 3 are ``NO``;
* ``I DON'T KNOW`` is available as an uncertainty response but is never a
  correct target class.

The materials form matched EARLY/LATE pairs around practical questions such as
refund timing, support response time, and return periods.  The response-relevant
value changes with the target answer while the surrounding interface-style
content remains deliberately similar.

Each stimulus is formatted as:

.. code-block:: text

   QUESTION: ...

   TEXT: ...

The blank line is preserved by the demo's text adapter when word bounding boxes
are generated, so gaze coordinates can be interpreted against the displayed
paragraph structure.

Participant task
----------------

The participant reads the question and text, then selects ``YES``, ``NO``, or
``I DON'T KNOW``.  The stimulus remains on screen until a response is selected,
so viewing time is participant-controlled rather than timer-controlled.

A preserved Polish version uses the same structure and is available in the
companion repository through files carrying the ``_pl`` suffix.

Scientific rationale
--------------------

The manipulation targets **information access cost**.  Decision-relevant
content placed later in a text normally requires the reader to traverse more
material before reaching it.  Eye tracking makes that traversal observable
instead of inferring it only from response time.

The design separates several questions that ordinary usability testing can
conflate:

1. **Was the relevant information looked at?**
   The critical phrase can be represented as an area of interest (AOI), making
   target acquisition distinguishable from trials where the participant answers
   without visibly reaching that region.
2. **How long did target acquisition take?**
   Time to first fixation (TTFF) on the critical phrase provides a descriptive
   measure of visual search efficiency.
3. **How much visual work preceded target acquisition?**
   The number of fixations before the first target fixation describes search
   effort independently of the final response.
4. **What happened after target acquisition?**
   Dwell time and repeated returns to the target can show whether finding the
   information was immediately sufficient or whether further verification
   occurred.
5. **Does visual access relate to behavioral correctness?**
   Accuracy can be compared between trials with and without target acquisition,
   while treating this as descriptive evidence rather than a causal estimate.

Example hypotheses
------------------

* **H1 -- Target acquisition:** the answer-relevant phrase is fixated on most
  trials with usable gaze.
* **H2 -- Placement effect:** target TTFF is lower in ``EARLY`` than ``LATE``
  trials.
* **H3 -- Search effort:** fewer fixations occur before first target acquisition
  in ``EARLY`` trials.
* **H4 -- Behavior and gaze:** trials with successful target acquisition may
  have higher response accuracy than trials without target acquisition.

These are example research hypotheses, not guaranteed outcomes.

Scientifically useful measures
------------------------------

Useful dependent variables include:

* response and response accuracy;
* target-acquisition rate;
* target TTFF;
* fixation count before the target;
* fixation count on the target;
* target dwell time and dwell-time share;
* total trial duration;
* optional scanpath comparisons between EARLY and LATE conditions.

A single eye-movement metric should not be treated as a direct measure of a
latent construct such as cognitive load.  Measures are most interpretable when
combined with the task structure and behavioral response.

Tobii-Pytracker analysis support
--------------------------------

The companion notebook uses Tobii-Pytracker's ``DataLoader`` for session/trial
data, ``FixationAnalyzer`` for fixation extraction, and ``ScanpathsAnalyzer``
for fixation-transition summaries.  Mapping the known critical phrase onto
word-level AOIs is experiment-specific logic built from the bounding boxes
stored with the trial.  See :doc:`data_analyzers` for the built-in analyzers.

Why this is a useful basic example
----------------------------------

The example connects a text CSV dataset, word-level spatial regions,
behavioral classification, and gaze-derived AOI measures in one compact
manipulation.  It therefore provides a bridge between simple text presentation
and controlled UX/HCI experimentation.

Limitations
-----------

* Twelve trials are suitable for demonstration but not a well-powered
  confirmatory study.
* Text length and sentence structure are controlled only approximately.
* The material is interface-style text rather than a validated psycholinguistic
  corpus.
* Frequent ``I DON'T KNOW`` responses require an explicit analysis strategy.
* Missing gaze samples must be treated as data quality rather than silently
  converted into negative target-acquisition evidence.

Implementation and analysis notebook
------------------------------------

The executable example and fixed datasets are maintained in the companion
repository:

* `UX A/B Text Demo directory <https://github.com/mszac/tobii-pytracker-demo/tree/main/examples/ux_ab_demo>`_
* `Jupyter analysis notebook <https://github.com/mszac/tobii-pytracker-demo/blob/main/examples/ux_ab_demo/analysis/ux_ab_analysis.ipynb>`_
* `Demo setup and execution guide <https://github.com/mszac/tobii-pytracker-demo/blob/main/README_TESTING.md>`_

The notebook covers data-quality checks, fixation and scanpath extraction,
critical-phrase AOI analysis, target acquisition, TTFF, pre-target search effort,
target dwell/revisits, and condition-level summaries.  Short notes identify
which stages are delegated to Tobii-Pytracker analyzers and which are
experiment-specific AOI logic.

Further reading
---------------

* Rayner, K. (1998). *Eye movements in reading and information processing:
  20 years of research*. Psychological Bulletin, 124(3), 372--422.
  DOI: 10.1037/0033-2909.124.3.372.
* Goldberg, J. H., & Kotval, X. P. (1999). *Computer interface evaluation using
  eye movements: methods and constructs*. International Journal of Industrial
  Ergonomics, 24(6), 631--645. DOI: 10.1016/S0169-8141(98)00068-7.
* Duchowski, A. T. (2017). *Eye Tracking Methodology: Theory and Practice*
  (3rd ed.). Springer. DOI: 10.1007/978-3-319-57883-5.

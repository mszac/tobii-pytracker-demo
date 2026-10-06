.. _basic-example-text-search-demo:

================
Text Search Demo
================

Modality
--------

**Text data** -- 12 response-gated practical-information trials.

Research question
-----------------

How does the location of a critical phrase influence visual search when users
answer practical questions from short, heterogeneous texts?

Unlike the more tightly paired :doc:`UX A/B Text Demo <basic_example_ux_ab_text_demo>`,
this example uses different topics, including
returns, delivery, complaints, account settings, refunds, booking,
subscriptions, warranties, passwords, invoices, pickup, and personal data.  It
therefore represents a more ecologically varied information-retrieval task.

Experimental design
-------------------

The English dataset contains 12 unique trials:

* 6 ``EARLY`` trials, where the critical phrase appears in the first sentence of
  the text body;
* 6 ``LATE`` trials, where the critical phrase appears in the final sentence;
* ``YES`` and ``NO`` responses are represented across the material;
* ``I DON'T KNOW`` is available as an uncertainty response but is not a target
  label.

Every trial contains an explicit question, a blank separator line, and the text
body:

.. code-block:: text

   QUESTION: ...

   TEXT: ...

The local text adapter preserves the same separation in generated word-bbox
geometry.  A Polish version is preserved through files carrying the ``_pl``
suffix.

Participant task
----------------

The participant searches the text for information required to answer the
question and selects ``YES``, ``NO``, or ``I DON'T KNOW``.  There is no response
timer; the current trial remains visible until an answer is selected.

Scientific rationale
--------------------

This is a compact **goal-directed reading and visual-search** paradigm.  The
critical phrase is known from the dataset in advance, allowing gaze behavior to
be compared with the location that contains the answer-relevant information.

The experiment separates five stages of the search process:

1. **Initial orientation** -- where gaze first lands after stimulus onset.
2. **Search progression** -- how much visual activity occurs before the
   critical phrase is reached.
3. **Target acquisition** -- whether and when the critical phrase receives a
   fixation.
4. **Verification** -- whether the participant remains on or returns to the
   target before answering.
5. **Decision outcome** -- whether the selected answer matches the dataset
   label.

Because topics vary across trials, the example is less controlled than a strict
psycholinguistic experiment.  Its purpose is to demonstrate how an applied
information-search study can be represented with Tobii-Pytracker.

Example hypotheses
------------------

* **H1 -- Critical-phrase attention:** the critical phrase receives at least one
  fixation on a substantial proportion of trials with usable gaze.
* **H2 -- Position effect:** TTFF is lower for ``EARLY`` than ``LATE`` trials.
* **H3 -- Pre-target search:** fewer fixations occur before target acquisition in
  ``EARLY`` trials.
* **H4 -- Verification behavior:** difficult or uncertain trials may contain
  more target refixations or longer target dwell.
* **H5 -- Behavioral association:** successful critical-phrase acquisition may
  be associated with greater answer accuracy.

Scientifically useful measures
------------------------------

* response and response accuracy;
* critical-phrase acquisition rate;
* TTFF to the critical phrase;
* fixation count before target;
* fixation count and dwell time on target;
* returns to the target after first acquisition;
* post-target viewing duration;
* total trial duration;
* uncertainty-response frequency.

Eye movements are closely related to the moment-to-moment allocation of visual
attention during reading, but a fixation is not a direct measurement of
comprehension.  The example is best interpreted as a study of search behavior
and access to answer-relevant information, with response accuracy as a separate
behavioral outcome.

Tobii-Pytracker analysis support
--------------------------------

The notebook uses ``DataLoader`` for recorded sessions, ``FixationAnalyzer`` for
fixation extraction, and ``ScanpathsAnalyzer`` for transition summaries.
Critical-phrase hit testing and post-target verification metrics are specific to
this experiment and use the word bounding boxes stored in each trial.  See
:doc:`data_analyzers` for the built-in analysis components.

Why this is a useful basic example
----------------------------------

The example demonstrates:

* loading labeled text stimuli from CSV;
* preserving structured question/text presentation;
* using word-level spatial information for AOIs;
* combining gaze behavior with a discrete response;
* comparing target placement across multiple content topics.

Limitations
-----------

* Topic and placement are not fully orthogonalized across only 12 texts.
* The task is not a validated reading-comprehension instrument.
* Missing gaze must be reported separately from a genuine failure to fixate the
  target.
* Confirmatory use requires predefined trial exclusions, participant
  exclusions, AOI rules, and statistical models.

Implementation and analysis notebook
------------------------------------

* `Text Search Demo directory <https://github.com/mszac/tobii-pytracker-demo/tree/main/examples/text_search_demo>`_
* `Jupyter analysis notebook <https://github.com/mszac/tobii-pytracker-demo/blob/main/examples/text_search_demo/analysis/text_search_analysis.ipynb>`_
* `Demo setup and execution guide <https://github.com/mszac/tobii-pytracker-demo/blob/main/README_TESTING.md>`_

The notebook follows the sequence orientation, search, target acquisition,
post-target verification, behavioral outcome, and condition/topic diagnostics.
It marks the operations supplied by Tobii-Pytracker separately from the
critical-phrase logic implemented for this example.

Further reading
---------------

* Rayner, K. (1998). *Eye movements in reading and information processing:
  20 years of research*. Psychological Bulletin, 124(3), 372--422.
  DOI: 10.1037/0033-2909.124.3.372.
* Duchowski, A. T. (2017). *Eye Tracking Methodology: Theory and Practice*
  (3rd ed.). Springer. DOI: 10.1007/978-3-319-57883-5.

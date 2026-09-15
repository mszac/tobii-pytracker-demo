# UX A/B Text Demo

## Modality

**Text data** — 12 response-gated trials.

## Research question

How does the position of answer-relevant information within a short interface-style text affect visual search and decision behavior?

The demo implements a controlled **EARLY versus LATE** information-placement manipulation. The same practical question can be paired with a target phrase that appears near the beginning or near the end of the text. This makes the example useful for studying a common UX problem: whether information architecture places decision-critical content where users are likely to find it efficiently.

## Experimental design

The English dataset contains 12 trials:

- 6 `EARLY` trials, where the answer-relevant phrase occurs in the first sentence;
- 6 `LATE` trials, where the corresponding phrase occurs in the final sentence;
- within each condition, 3 correct answers are `YES` and 3 are `NO`;
- `I DON'T KNOW` is available as an uncertainty response but is never a correct target class.

The materials form matched EARLY/LATE pairs around practical questions such as refund timing, support response time, and return periods. The response-relevant value changes with the target answer while the surrounding interface-style content remains deliberately similar.

Each stimulus is formatted as:

```text
QUESTION: ...

TEXT: ...
```

The blank line is preserved in the local word-bbox geometry so that gaze coordinates can be interpreted against the displayed paragraph structure.

## Participant task

The participant reads the question and text, then selects **YES**, **NO**, or **I DON'T KNOW**. The stimulus remains on screen until a response is selected, so viewing time is participant-controlled rather than timer-controlled.

The preserved Polish version uses the same structure and is provided through `_pl` files.

## Scientific rationale

The manipulation targets **information access cost**. In an interface, decision-relevant content placed later in a text usually requires the reader to traverse more material before it can be found. Eye tracking makes that traversal observable rather than inferring it only from response time.

The design separates several questions that are often conflated in ordinary usability testing:

1. **Was the relevant information looked at at all?**
   A target phrase can be represented as an area of interest (AOI). Target acquisition can then be distinguished from trials where the participant answers without visibly reaching that region.

2. **How long did it take to reach the target?**
   Time to first fixation (TTFF) on the critical phrase is a direct descriptive measure of search efficiency. EARLY placement should, by construction, reduce the amount of preceding text that must be visually traversed.

3. **How much visual work occurred before the target?**
   The number of fixations before first target acquisition can describe search effort independently of the final YES/NO response.

4. **What happens after target acquisition?**
   Dwell time and repeated returns to the target can indicate whether finding the phrase was sufficient for the decision or whether additional verification occurred.

5. **Does visual access relate to behavioral correctness?**
   Response accuracy can be compared between trials where the target was fixated and those where it was not. This is descriptive evidence only; the demo is not powered to establish a causal relationship.

## Example hypotheses

- **H1 — Target acquisition:** the answer-relevant phrase is fixated on most trials with usable gaze.
- **H2 — Placement effect:** target TTFF is lower in `EARLY` than in `LATE` trials.
- **H3 — Search effort:** fewer fixations occur before first target acquisition in `EARLY` trials.
- **H4 — Behavior and gaze:** trials with successful target acquisition may have higher response accuracy than trials without target acquisition.

These are example research hypotheses, not guaranteed outcomes.

## Measures that are scientifically meaningful here

Useful dependent variables include:

- response and response accuracy;
- target acquisition rate;
- target TTFF;
- fixation count before the target;
- fixation count on the target;
- target dwell time and dwell-time share;
- total trial duration;
- optional scanpath comparisons between EARLY and LATE conditions.

A single metric should not be treated as a direct measure of a latent construct such as cognitive load. Eye-movement measures are best interpreted jointly with the task structure and behavioral response.

## Why this is a useful basic example

This demo shows how `tobii-pytracker` can connect a text dataset, word-level bounding boxes, behavioral classification, and gaze-derived AOI measures in one compact experimental manipulation. It is therefore a suitable bridge between simple text presentation and controlled UX/HCI experimentation.

## Limitations

- Twelve trials are sufficient for demonstration but not for a well-powered confirmatory study.
- Text length and sentence structure are controlled only approximately.
- The example uses practical interface-style texts rather than a validated psycholinguistic corpus.
- `I DON'T KNOW` introduces a useful uncertainty option but requires an analysis plan if it is frequent.
- Missing gaze samples should be treated as data quality, not silently converted into negative target-acquisition evidence.

## Run the demo

See the root [setup and execution guide](../../README_TESTING.md).

Demo directory: `examples/ux_ab_demo/`.

## Jupyter analysis

The analysis workflow is documented inside the notebook itself. It covers data-quality checks, fixation and scanpath extraction, critical-phrase AOI analysis, target acquisition, TTFF, pre-target search effort, target dwell/revisits, and condition-level summaries. Short notes identify the steps delegated to `tobii-pytracker` analyzers versus experiment-specific AOI logic.

Notebook: `examples/ux_ab_demo/analysis/ux_ab_analysis.ipynb`.

## Further reading

- Rayner, K. (1998). *Eye movements in reading and information processing: 20 years of research*. Psychological Bulletin, 124(3), 372–422. DOI: 10.1037/0033-2909.124.3.372.
- Goldberg, J. H., & Kotval, X. P. (1999). *Computer interface evaluation using eye movements: methods and constructs*. International Journal of Industrial Ergonomics, 24(6), 631–645. DOI: 10.1016/S0169-8141(98)00068-7.
- Duchowski, A. T. (2017). *Eye Tracking Methodology: Theory and Practice* (3rd ed.). Springer. DOI: 10.1007/978-3-319-57883-5.

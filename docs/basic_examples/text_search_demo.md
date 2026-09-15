# Text Search Demo

## Modality

**Text data** — 12 response-gated practical-information trials.

## Research question

How does the location of a critical phrase influence visual search when users answer practical questions from short, heterogeneous texts?

Unlike the more tightly paired UX A/B Text Demo, this example uses different topics — returns, delivery, complaints, account settings, refunds, booking, subscriptions, warranties, passwords, invoices, pickup, and personal data. It therefore illustrates a more ecologically varied information-retrieval task.

## Experimental design

The English dataset contains 12 unique trials:

- 6 `EARLY` trials, where the critical phrase appears in the first sentence of the text body;
- 6 `LATE` trials, where the critical phrase appears in the final sentence;
- `YES` and `NO` responses are represented across the material;
- `I DON'T KNOW` is available as an uncertainty response but is not a target label.

Every trial contains an explicit question, a blank separator line, and the text body:

```text
QUESTION: ...

TEXT: ...
```

The local text adapter preserves the same separation in the generated word-bbox geometry. A preserved Polish version is available through `_pl` files.

## Participant task

The participant searches the text for information needed to answer the question and then selects **YES**, **NO**, or **I DON'T KNOW**. No response timer forces the transition to the next trial.

## Scientific rationale

This is a compact **goal-directed reading and visual-search** paradigm. The critical phrase is known in advance from the dataset, which allows the experimenter to compare the participant's gaze against the location that actually contains the answer-relevant information.

The scientific value comes from distinguishing the stages of the search process:

1. **Initial orientation** — where gaze first lands after stimulus onset.
2. **Search progression** — how many fixations and saccades occur before the critical phrase is reached.
3. **Target acquisition** — whether and when the critical phrase receives a fixation.
4. **Verification** — whether the participant remains on or returns to the critical phrase before answering.
5. **Decision outcome** — whether the selected answer matches the dataset label.

Because topics vary across trials, the example is less controlled than a strict psycholinguistic experiment but demonstrates how an applied information-search study can be represented with `tobii-pytracker`.

## Example hypotheses

- **H1 — Critical-phrase attention:** the critical phrase attracts at least one fixation on a substantial proportion of trials with usable gaze.
- **H2 — Position effect:** TTFF to the critical phrase is lower for `EARLY` than `LATE` trials.
- **H3 — Pre-target search:** fewer fixations occur before the critical phrase in `EARLY` trials.
- **H4 — Verification behavior:** difficult or uncertain trials may contain more refixations or longer dwell on the critical phrase.
- **H5 — Behavioral association:** successful critical-phrase acquisition may be associated with greater answer accuracy.

## Measures that are scientifically meaningful here

- response and response accuracy;
- critical-phrase acquisition rate;
- TTFF to the critical phrase;
- fixation count before target;
- fixation count and dwell time on target;
- regressions/returns to previously viewed text regions;
- total gaze coverage and trial duration;
- uncertainty-response frequency.

## Relationship to reading research

Eye movements are tightly linked to the moment-to-moment allocation of visual attention during reading, but a fixation is not a direct readout of comprehension. The example is therefore best used to study **search behavior and access to answer-relevant information**, with response accuracy providing a separate behavioral outcome.

## Why this is a useful basic example

The demo illustrates:

- loading labeled text stimuli from CSV;
- preserving structured question/text presentation;
- using word-level spatial information for AOIs;
- combining gaze behavior with a discrete response;
- comparing target placement across multiple content topics.

## Limitations

- The 12 texts vary in topic and wording, so topic and placement are not fully orthogonalized.
- The task is a demonstration and should not be treated as a validated reading-comprehension test.
- Missing gaze must be reported separately from a genuine failure to fixate the target.
- Any confirmatory study should predefine trial exclusions, participant exclusions, AOI rules, and statistical models.

## Run the demo

See the root [setup and execution guide](../../README_TESTING.md).

Demo directory: `examples/text_search_demo/`.

## Jupyter analysis

The analysis workflow is documented inside the notebook itself. It follows orientation, search, critical-phrase acquisition, post-target verification, behavioral accuracy, and condition/topic diagnostics. Short notes identify the steps delegated to `tobii-pytracker` analyzers versus experiment-specific critical-phrase logic.

Notebook: `examples/text_search_demo/analysis/text_search_analysis.ipynb`.

## Further reading

- Rayner, K. (1998). *Eye movements in reading and information processing: 20 years of research*. Psychological Bulletin, 124(3), 372–422. DOI: 10.1037/0033-2909.124.3.372.
- Duchowski, A. T. (2017). *Eye Tracking Methodology: Theory and Practice* (3rd ed.). Springer. DOI: 10.1007/978-3-319-57883-5.

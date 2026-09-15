# UX A/B Text Demo — information placement

## Goal

This demonstrator tests whether answer-relevant information is easier to find when it appears **EARLY** versus **LATE** in a short interface-style text.

Each of the 12 trials contains a question, a blank separator line, and a short text. The participant answers **YES** or **NO**; **I DON'T KNOW** is available as an uncertainty response and is never a target class. YES/NO is balanced within both EARLY and LATE conditions. Target phrases such as `7 days` or `48 hours` occur in every trial so gaze-to-target metrics can be computed for both answer classes.

## Descriptive hypotheses

- H1: participants should fixate the answer-relevant target on most trials with usable gaze.
- H2: time to first target fixation (TTFF) should be lower in EARLY than LATE trials.
- H3: trials in which the target is fixated may show higher response accuracy than trials in which it is not.

## Language variants

- `data/text_search.csv`: active English stimulus set; the default experiment configuration uses this dataset.
- `data/text_search_pl.csv`: preserved Polish version.

The active runner uses a local adapter that displays the upstream `none` response as **I DON'T KNOW** and keeps explicit paragraph breaks aligned with word-bbox geometry. The upstream runtime repository is not modified.

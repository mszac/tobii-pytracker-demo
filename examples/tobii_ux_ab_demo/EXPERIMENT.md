# UX information-placement A/B demo

## Goal

This is a demonstration workflow, not an inferential study. It tests whether the same answer-relevant information is easier to find when it appears **EARLY** versus **LATE** in a short interface-style text.

Each of the 12 trials contains a question and a short text. The participant answers **TAK** or **NIE**. The dataset balances TAK/NIE within both EARLY and LATE conditions. A target phrase such as `7 dni` or `48 godzin` is present in every trial so gaze-to-target metrics are defined for both response classes.

## Descriptive hypotheses

- H1: participants should fixate the answer-relevant target on most completed trials.
- H2: time to first target fixation (TTFF) should be lower in EARLY than LATE trials.
- H3: trials in which the target is fixated may show higher response accuracy than trials in which it is not.

These are demonstration hypotheses only. A real study needs more items, participants, randomized/counterbalanced order and a pre-specified statistical model.

## Runtime contract

The example is owned by `tobii-pytracker-demo`, but runtime code and MouseGaze configuration come from the unmodified parent `sbobek/tobii-pytracker` clone. The example does not vendor or patch upstream runtime files.

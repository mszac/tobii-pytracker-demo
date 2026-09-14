# Native text-search demo

## Goal

The participant receives a question and a short practical-information text (FAQ, policy or service message). The task is to find the answer-relevant phrase and respond **TAK / NIE / NIE WIEM**.

In the current unmodified upstream `TextDataset`, the third button is named `NONE`. In this native demo, `NONE` is the operational equivalent of **NIE WIEM** and is never a correct target class.

## Experimental manipulation

The committed dataset contains 12 unique trials:

- 6 x `EARLY`: the critical phrase is in the first sentence of the text body;
- 6 x `LATE`: the critical phrase is in the last sentence of the text body.

Within each condition:

- 3 target answers are `tak`;
- 3 target answers are `nie`.

The 12-item content, topics, target phrases and EARLY/LATE assignment are preserved from the supplied legacy demo.

## Hypotheses

### H1 — critical information attracts attention

Expected descriptive metrics:

- `target_seen`;
- `target_fixation_count`;
- `target_dwell_s`;
- `target_dwell_share`.

### H2 — critical-phrase position changes search time

Expected demo direction:

```text
TTFF: EARLY < LATE
fixations before target: EARLY < LATE
```

### H3 — reaching the target is associated with response accuracy

Trials with `target_seen=True` are expected to have higher descriptive accuracy than trials without a detected target fixation.

## Native AOI contract

The config uses `dataset.text` with `bbox_model: word`. The unmodified upstream saves native word bounding boxes in `objects_bboxes`. Analysis finds the `critical_phrase` only after the `TEKST:` marker so a similar phrase in the question cannot be mistaken for the target.

The rendered `selected_text` is intentionally stored as one line in the CSV. This avoids the mismatch between explicit line breaks in PsychoPy text rendering and the current upstream word-bbox reflow implementation.

## Scope

This is a demonstrator, not a complete inferential protocol. A research deployment should add participants/items, counterbalance the same information across EARLY/LATE conditions and predefine inferential models.

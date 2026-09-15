# Native text-search demo

## Goal

The participant receives a question and a short practical-information text. The task is to locate the answer-relevant phrase and respond **YES / NO / I DON'T KNOW**.

## Experimental manipulation

The active English dataset contains 12 unique trials:

- 6 x `EARLY`: the critical phrase is in the first sentence of the text body;
- 6 x `LATE`: the critical phrase is in the last sentence of the text body;
- within each condition, 3 targets are `yes` and 3 are `no`.

Each rendered item uses an explicit section boundary:

```text
QUESTION: ...

TEXT: ...
```

The local text adapter preserves this blank line in native word-bbox geometry, so AOIs match the displayed paragraph layout.

## Language variants

- `data/text_search.csv` / `config.native.yaml`: active English version.
- `data/text_search_pl.csv` / `config.native_pl.yaml`: preserved Polish version using `PYTANIE` and `TEKST` with the same blank-line separation.

In the English runner the upstream `none` class is displayed as **I DON'T KNOW**. It is an uncertainty response, not a target label.

## Hypotheses

- H1: the critical phrase attracts visual attention.
- H2: `TTFF(EARLY) < TTFF(LATE)` and fewer fixations are expected before the target in EARLY trials.
- H3: reaching the target may be associated with higher descriptive response accuracy.

This remains a demonstrator rather than a complete inferential protocol.

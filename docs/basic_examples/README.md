# Basic Examples — demo documentation source

These Markdown pages are prepared as source material for future inclusion in the upstream `tobii-pytracker` **Basic Examples** documentation. The current upstream documentation groups examples by modality: Image Data, Text Data, and Time Series Data.

The technical `test_demo` is intentionally excluded from this documentation set because it exists to verify installation and interaction mechanics rather than to illustrate an experimental research design.

## Image Data Examples

- [Image Semantic Demo](image_semantic_demo.md) — semantic categorization of mixed biological, object, and scene images.

## Text Data Examples

- [UX A/B Text Demo](ux_ab_text_demo.md) — controlled manipulation of where answer-relevant information appears in short texts.
- [Text Search Demo](text_search_demo.md) — visual search and information retrieval across varied practical-information texts.

## Time Series Data Examples

- [Time-Series Noise Demo](timeseries_noise_demo.md) — perception and classification of signal variability in machine-vibration and PV-power series.

## Running the examples

Use the root [setup and execution guide](../../README_TESTING.md) for both local and Docker execution.

## Analysis documentation status

Each page links to a Jupyter notebook that analyzes collected experiment data. The notebooks now contain the step-by-step analytical workflow, scientific interpretation notes, and short annotations indicating where `tobii-pytracker` analysis helpers are used. The Markdown pages focus on the experimental rationale and do not duplicate the notebook code walkthroughs.

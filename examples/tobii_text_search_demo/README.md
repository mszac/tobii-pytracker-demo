# Tobii native text-search demo

12-trial EARLY/LATE text-search experiment running against the clean upstream runtime. `NONE` means NIE WIEM.

## Run

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/tobii_text_search_demo/run_native.sh
```

Expected collection markers: `NATIVE_TEXT_SEARCH_COLLECTION_PASS`, `NATIVE_TEXT_SEARCH_COLLECTION_COMPLETE`. Missing gaze is reported as a quality warning; responses and native word-bboxes remain valid collected data.

## Analyze in Jupyter

```bash
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/tobii_text_search_demo/analysis/text_search_analysis.ipynb
```

The notebook reads the real session, uses upstream `FixationAnalyzer` when gaze exists and computes behavioral/target metrics without synthetic fallback.

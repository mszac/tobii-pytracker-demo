# Text Search Demo

12-trial EARLY/LATE text-search experiment running against the clean upstream runtime.

The active English dataset is `data/text_search.csv`. The preserved Polish dataset is `data/text_search_pl.csv`; `config.native_pl.yaml` points to that version.

Run the English demo from the parent `tobii-pytracker` root:

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/text_search_demo/run_native.sh
```

Responses are **YES**, **NO**, and **I DON'T KNOW**. The third option is the semantic replacement for upstream `NONE`; it is never a correct target class. The stimulus remains visible until one response is clicked.

Every text stimulus is formatted as:

```text
QUESTION: ...

TEXT: ...
```

The blank separator line is preserved both visually and in the word-bbox geometry by a local demo adapter. The upstream `tobii-pytracker` source remains unmodified.

Open the notebook analysis after collecting data:

```bash
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/text_search_demo/analysis/text_search_analysis.ipynb
```

## Preserved Polish variant

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/text_search_demo/run_native_pl.sh
```

The `_pl` runner uses the preserved Polish dataset/config and displays the uncertainty response as **NIE WIEM**.

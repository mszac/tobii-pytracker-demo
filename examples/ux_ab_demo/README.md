# UX A/B Text Demo

12-trial text experiment comparing EARLY versus LATE placement of answer-relevant information.

The active English dataset is `data/text_search.csv`. The preserved Polish version is `data/text_search_pl.csv`.

Run the English demo from the parent `tobii-pytracker` root:

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/ux_ab_demo/run.sh
```

The visible response buttons are **YES**, **NO**, and **I DON'T KNOW**. The stimulus remains visible until one response is clicked. MouseGaze still uses RIGHT-hold + pointer motion for gaze; release RIGHT before LEFT-clicking a response.

The rendered stimulus always has two sections separated by one blank line:

```text
QUESTION: ...

TEXT: ...
```

The local demo adapter preserves that explicit paragraph break in the word-bbox geometry while leaving the parent `tobii-pytracker` source unchanged.

Analysis is notebook-only and consumes the newest real collected session:

```bash
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/ux_ab_demo/analysis/ux_ab_analysis.ipynb
```

## Preserved Polish variant

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/ux_ab_demo/run_pl.sh
```

The `_pl` runner uses the preserved Polish dataset/config and displays the uncertainty response as **NIE WIEM**.

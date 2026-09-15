# Time-Series Variability Classification Demo

## Design

The demo preserves the scientific logic of the earlier image-based example but uses the built-in `time_series` modality of `tobii-pytracker` instead of rendered PNG plots.

There are two blocks and 18 total stimuli:

| Domain | LOW | MEDIUM | HIGH | Total |
|---|---:|---:|---:|---:|
| Machine vibration | 3 | 3 | 3 | 9 |
| PV power | 3 | 3 | 3 | 9 |
| **Total** | **6** | **6** | **6** | **18** |

Machine question: **How large are the irregular vibration fluctuations in the signal?**

PV question: **How large are the short-term fluctuations in PV power production?**

Responses are LOW / MEDIUM / HIGH. The upstream loader also exposes `NONE`, which is treated as an uncertain response rather than a target class.

## Hypotheses

- **H1:** higher variability tends to increase fixation count: LOW < MEDIUM < HIGH.
- **H2:** MEDIUM tends to produce the longest visual decision process because it is the ambiguous middle class.
- **H3:** HIGH tends to produce broader exploration of the horizontal time axis.
- **H4:** gaze distribution differs between machine vibration and PV power for the same variability class.
- **H5:** MEDIUM tends to have the lowest classification accuracy.

## Time-series implementation

Each CSV row is one stimulus. The first column is the stimulus ID, the final column is the class, and the 128 numeric values in between are the time-series samples. The runtime uses `dataset.time_series` with `bbox_model: sample`, so `objects_bboxes` contains per-sample time-series regions with sample indices.

The experiment uses two fixed CSV fixtures committed directly to the demo repository. There is no data generator and no PNG stimulus dataset in this demo.

# Native Time-Series Noise Demo

This example is the CSV/time-series implementation of the earlier variability-classification experiment. It uses the unmodified upstream `TimeSeriesDataset` and upstream MouseGaze.

## Fixed stimuli

- `data/machine_vibration.csv` — 9 machine-vibration series.
- `data/pv_power.csv` — 9 PV-power series.

The numeric stimulus values come from the supplied pre-generated fixtures. The final demo contains no generator. Rows are stored in a fixed interleaved class order so the upstream loader does not present three LOW, then three MEDIUM, then three HIGH trials. The first numeric column header is renamed per block so the upstream single-channel y-axis label is meaningful; numeric values, IDs and class labels are unchanged.

## Run from the parent `tobii-pytracker` directory

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/tobii_timeseries_noise_demo/run_native.sh
```

The runner launches two 9-trial blocks: machine first, then PV. At the end of the machine outro, press ESC to continue to the PV block. After each block it validates the newest `data.csv`: exactly 9 trials, 3/3/3 LOW/MEDIUM/HIGH, non-empty gaze on every trial, and 128 native per-sample `timeseries_bboxes`. The PV block starts only after the machine block passes this gate.

MouseGaze: hold RIGHT while moving to generate gaze, release RIGHT, then LEFT CLICK the response.

## Analysis

```bash
conda run --no-capture-output -n pytracker-env \
  python tobii-pytracker-demo/examples/tobii_timeseries_noise_demo/analysis/analyze_results.py
```

The analysis uses upstream `FixationAnalyzer` and the `timeseries_bboxes` saved by the native time-series dataset to summarize fixation count, dwell, time-axis coverage, horizontal exploration and classification accuracy.

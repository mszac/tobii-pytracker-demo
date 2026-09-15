# Time-Series Noise Demo

Two fixed CSV blocks: 9 machine-vibration series followed by 9 PV-power series. No generator and no PNG stimuli are used.

## Run

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/timeseries_noise_demo/run.sh
```

Each block validates 9 responses, 3/3/3 LOW/MEDIUM/HIGH balance and 128 `timeseries_bboxes` per trial. The validator raises the Python CSV field-size limit so the large serialized bbox field is accepted. Missing gaze is reported but does not prevent the second block from running.

The collection validator confirms each completed domain block and the complete experiment.

## Analyze in Jupyter

```bash
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/timeseries_noise_demo/analysis/timeseries_analysis.ipynb
```

The notebook analyzes the newest real machine and/or PV block available.

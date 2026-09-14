# Time-Series Noise Demo for `tobii-pytracker`

## Overview

This demo uses the **Time Series** stimulus modality to investigate how people
visually assess short-term variability in two realistic signal domains:

1. **machine vibration**, and
2. **photovoltaic (PV) power production**.

The experiment contains **18 stimuli**:

```text
Machine vibration:  3 LOW + 3 MEDIUM + 3 HIGH = 9
PV production:      3 LOW + 3 MEDIUM + 3 HIGH = 9
---------------------------------------------------
Total:                                         18
```

The detailed hypotheses and experimental workflow are documented in
[`EXPERIMENT.md`](EXPERIMENT.md).

---

## Why two blocks are recommended

The current `TimeSeriesDataset` renders the numeric series and creates time-series
bounding boxes, but the dataset format does not provide a native per-row text field
for displaying a different question for each stimulus.

For that reason, the most natural workflow is:

### Block 1 — Machine vibration

Participant question:

> **How large are the irregular vibration fluctuations in the signal?**

Responses:

```text
LOW | MEDIUM | HIGH
```

Dataset:

```text
datasets/machine_vibration.csv
```

### Block 2 — PV power

Participant question:

> **How large are the short-term fluctuations in PV power production?**

Responses:

```text
LOW | MEDIUM | HIGH
```

Dataset:

```text
datasets/pv_power.csv
```

The order of the two blocks should ideally be counterbalanced across participants
in a full study.

---

## Dataset format

`tobii-pytracker` expects a time-series CSV with:

- the first column used as the stimulus identifier,
- numeric time-series values in the remaining data columns,
- a label column specified by `label_column_name`.

This demo uses 128 samples per stimulus:

```csv
id,s000,s001,s002,...,s127,class
```

The generator creates:

```text
datasets/
├── machine_vibration.csv       # 9 stimuli
├── pv_power.csv                # 9 stimuli
└── time_series_noise_demo.csv  # optional combined 18-stimulus file
```

The combined file is useful for generic testing or later analysis. The recommended
experiment itself uses the two domain-specific files as separate blocks.

---

# Python data generator

Save the following code as:

```text
generate_data.py
```

and run it from the repository root:

```bash
python generate_data.py
```

The script uses `numpy`, `pandas`, and `matplotlib`.

It generates **both CSV datasets and high-resolution PNG plots**.
All generated files are saved into one directory:

```text
generated_dataset/
```


```python
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# Demo data generator for tobii-pytracker time-series examples
# ============================================================
#
# This script generates:
#   1. CSV datasets
#   2. high-resolution PNG plots for each stimulus
#   3. an index CSV linking stimulus IDs to plot files
#
# All generated outputs are saved into a single directory:
#
#   generated_dataset/
#
# Output structure:
#
# generated_dataset/
# ├── machine_vibration.csv
# ├── pv_power.csv
# ├── time_series_noise_demo.csv
# ├── plots_index.csv
# └── plots/
#     ├── machine_low_01.png
#     ├── machine_medium_01.png
#     ├── pv_low_01.png
#     └── ...
#
# ============================================================

SEED = 20260910
N_SAMPLES = 128
N_PER_LEVEL = 3
LEVELS = ("low", "medium", "high")

OUT_DIR = Path("generated_dataset")
PLOTS_DIR = OUT_DIR / "plots"

# Plot styling
FIGSIZE = (12, 6)
DPI = 220
LINE_WIDTH = 1.8
GRID_COLOR = "#d3d3d3"
GRID_WIDTH = 0.8
LINE_COLOR = "#1f77b4"
AXIS_LABEL_SIZE = 16
TICK_LABEL_SIZE = 13

# Fixed Y-axis limits per domain
Y_LIMITS = {
    "machine": (-1.7, 1.7),
    "pv": (0.35, 1.02),
}


def ar1_noise(rng, n, sigma, rho=0.55):
    """Generate temporally correlated noise."""
    eps = rng.normal(0.0, sigma, n)
    x = np.zeros(n, dtype=float)
    for i in range(1, n):
        x[i] = rho * x[i - 1] + eps[i]
    return x


def gaussian_burst(t, center, width, amplitude):
    """Short vibration burst with a smooth envelope."""
    envelope = np.exp(-0.5 * ((t - center) / width) ** 2)
    carrier = np.sin(2 * np.pi * 13.0 * t)
    return amplitude * envelope * carrier


def generate_machine_signal(rng, level, n=N_SAMPLES):
    """
    Simulated accelerometer signal from a rotating machine.

    Natural interpretation:
    - low: regular operation, small broadband vibration;
    - medium: stronger irregular vibration under load;
    - high: stronger broadband vibration plus several short bursts.
    """
    t = np.linspace(0.0, 2.0, n, endpoint=False)

    base = (
        0.85 * np.sin(2 * np.pi * 4.0 * t)
        + 0.22 * np.sin(2 * np.pi * 8.0 * t + 0.35)
    )

    params = {
        "low": {
            "noise_sigma": 0.035,
            "burst_count": 0,
            "burst_amp": 0.00,
        },
        "medium": {
            "noise_sigma": 0.105,
            "burst_count": 2,
            "burst_amp": 0.18,
        },
        "high": {
            "noise_sigma": 0.220,
            "burst_count": 4,
            "burst_amp": 0.38,
        },
    }[level]

    irregular = ar1_noise(rng, n, sigma=params["noise_sigma"], rho=0.45)
    signal = base + irregular

    if params["burst_count"] > 0:
        centers = rng.uniform(0.20, 1.80, params["burst_count"])
        widths = rng.uniform(0.025, 0.060, params["burst_count"])
        for center, width in zip(centers, widths):
            amp = params["burst_amp"] * rng.uniform(0.75, 1.15)
            signal += gaussian_burst(t, center, width, amp)

    return signal


def smooth_cloud_dip(x, center, width, depth):
    """Smooth multiplicative loss caused by a passing cloud."""
    return depth * np.exp(-0.5 * ((x - center) / width) ** 2)


def generate_pv_signal(rng, level, n=N_SAMPLES):
    """
    Simulated PV power over a short daytime interval.

    Natural interpretation:
    - low: mostly clear sky;
    - medium: several moderate cloud passages;
    - high: frequent and deeper cloud passages.
    """
    x = np.linspace(0.0, 1.0, n)

    clear_sky = 0.68 + 0.30 * np.sin(np.pi * (0.18 + 0.64 * x))

    params = {
        "low": {
            "n_clouds": 1,
            "depth": (0.025, 0.060),
            "width": (0.050, 0.085),
            "measurement_sigma": 0.004,
        },
        "medium": {
            "n_clouds": 3,
            "depth": (0.080, 0.170),
            "width": (0.035, 0.075),
            "measurement_sigma": 0.006,
        },
        "high": {
            "n_clouds": 6,
            "depth": (0.160, 0.340),
            "width": (0.020, 0.060),
            "measurement_sigma": 0.009,
        },
    }[level]

    attenuation = np.zeros(n, dtype=float)
    centers = rng.uniform(0.08, 0.92, params["n_clouds"])

    for center in centers:
        width = rng.uniform(*params["width"])
        depth = rng.uniform(*params["depth"])
        attenuation += smooth_cloud_dip(x, center, width, depth)

    transmittance = np.clip(1.0 - attenuation, 0.42, 1.0)

    measurement_noise = ar1_noise(
        rng, n, sigma=params["measurement_sigma"], rho=0.65
    )

    power = clear_sky * transmittance + measurement_noise
    return np.clip(power, 0.0, None)


def make_rows(generator, prefix, rng):
    rows = []
    sample_columns = [f"s{i:03d}" for i in range(N_SAMPLES)]

    for level in LEVELS:
        for repetition in range(1, N_PER_LEVEL + 1):
            values = generator(rng, level)

            row = {"id": f"{prefix}_{level}_{repetition:02d}"}
            row.update({
                column: float(value)
                for column, value in zip(sample_columns, values)
            })
            row["class"] = level
            rows.append(row)

    return pd.DataFrame(rows)


def save_csv_datasets(machine, pv):
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    machine_path = OUT_DIR / "machine_vibration.csv"
    pv_path = OUT_DIR / "pv_power.csv"
    combined_path = OUT_DIR / "time_series_noise_demo.csv"

    machine.to_csv(machine_path, index=False, encoding="utf-8")
    pv.to_csv(pv_path, index=False, encoding="utf-8")
    pd.concat([machine, pv], ignore_index=True).to_csv(
        combined_path, index=False, encoding="utf-8"
    )

    return machine_path, pv_path, combined_path


def render_plots(df, domain, xlabel, ylabel):
    """
    Render all plots for one domain into generated_dataset/plots/.

    All PNG files are saved directly in the same plots directory.
    """
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    sample_columns = [c for c in df.columns if c.startswith("s")]
    metadata = []
    y_min, y_max = Y_LIMITS[domain]

    for _, row in df.iterrows():
        stimulus_id = row["id"]
        label = str(row["class"]).upper()

        x = np.arange(len(sample_columns))
        y = row[sample_columns].astype(float).to_numpy()

        fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
        ax.plot(x, y, linewidth=LINE_WIDTH, color=LINE_COLOR)
        ax.set_xlabel(xlabel, fontsize=AXIS_LABEL_SIZE)
        ax.set_ylabel(ylabel, fontsize=AXIS_LABEL_SIZE)
        ax.tick_params(axis="both", labelsize=TICK_LABEL_SIZE)
        ax.grid(True, color=GRID_COLOR, linewidth=GRID_WIDTH)
        ax.set_xlim(0, len(sample_columns) - 1)
        ax.set_ylim(y_min, y_max)

        # No title — intended for clean experimental stimuli or documentation use.
        out_path = PLOTS_DIR / f"{stimulus_id}.png"
        fig.tight_layout()
        fig.savefig(out_path, facecolor="white")
        plt.close(fig)

        metadata.append({
            "stimulus_id": stimulus_id,
            "domain": domain,
            "class": label,
            "image_path": str(out_path),
            "y_min": y_min,
            "y_max": y_max,
        })

    return pd.DataFrame(metadata)


def generate_plots(machine, pv):
    machine_index = render_plots(
        machine,
        domain="machine",
        xlabel="Sample index",
        ylabel="Vibration amplitude",
    )

    pv_index = render_plots(
        pv,
        domain="pv",
        xlabel="Sample index",
        ylabel="Power output",
    )

    index = pd.concat([machine_index, pv_index], ignore_index=True)
    index_path = OUT_DIR / "plots_index.csv"
    index.to_csv(index_path, index=False, encoding="utf-8")

    return index_path


def main():
    rng = np.random.default_rng(SEED)

    machine = make_rows(
        generate_machine_signal,
        prefix="machine",
        rng=rng,
    )

    pv = make_rows(
        generate_pv_signal,
        prefix="pv",
        rng=rng,
    )

    machine_path, pv_path, combined_path = save_csv_datasets(machine, pv)
    index_path = generate_plots(machine, pv)

    print("Generated datasets:")
    print(f"  {machine_path}")
    print(f"  {pv_path}")
    print(f"  {combined_path}")
    print("Generated plots index:")
    print(f"  {index_path}")
    print("All outputs were saved in:")
    print(f"  {OUT_DIR.resolve()}")
    print("")
    print("Fixed Y-axis limits:")
    print(f"  machine: {Y_LIMITS['machine']}")
    print(f"  pv:      {Y_LIMITS['pv']}")


if __name__ == "__main__":
    main()
```

---

# How the synthetic data reflect natural processes

## Machine vibration

The machine signal is built from a stable rotating-machine component plus
temporally correlated irregular vibration:

```text
fundamental rotation
+ harmonic component
+ correlated vibration noise
+ optional transient bursts
```

The classes are generated as follows:

| Class | Simulation interpretation |
|---|---|
| LOW | regular operation with small irregular vibration |
| MEDIUM | stronger irregular vibration and a small number of transient disturbances |
| HIGH | pronounced broadband vibration with several transient disturbances |

The task is deliberately limited to **vibration magnitude**. It does not ask the
participant to diagnose a specific fault.

---

## PV power

The PV signal uses a shared smooth clear-sky curve and multiplies it by simulated
cloud transmittance.

Cloud passages are represented by smooth Gaussian-shaped reductions in irradiance,
which produce temporally correlated power drops.

| Class | Simulation interpretation |
|---|---|
| LOW | mostly clear sky; one very shallow cloud event |
| MEDIUM | several moderate cloud passages |
| HIGH | frequent and deeper cloud passages |

A small correlated measurement component is added after the cloud model.

This is preferable to simply adding white noise because short-term PV fluctuations
are naturally caused by moving cloud fields and therefore have temporal structure.

---

# Example `tobii-pytracker` configuration

## Machine block

```yaml
dataset:
  time_series:
    label_column_name: class
    bbox_model: sample
    path: datasets/machine_vibration.csv
```

Suggested instruction:

```yaml
instructions:
  intro:
    - "Machine vibration"
    - ""
    - "You will see short accelerometer time series recorded from a rotating machine."
    - "For each plot, answer the following question:"
    - "How large are the irregular vibration fluctuations in the signal?"
    - ""
    - "Select LOW, MEDIUM, or HIGH."
    - ""
    - "Click the window and press SPACE to begin."
```

## PV block

```yaml
dataset:
  time_series:
    label_column_name: class
    bbox_model: sample
    path: datasets/pv_power.csv
```

Suggested instruction:

```yaml
instructions:
  intro:
    - "PV power production"
    - ""
    - "You will see short time series of photovoltaic power production."
    - "For each plot, answer the following question:"
    - "How large are the short-term fluctuations in PV power production?"
    - ""
    - "Select LOW, MEDIUM, or HIGH."
    - ""
    - "Click the window and press SPACE to begin."
```

Only one dataset modality should be active in a given main configuration.

---

# Bounding boxes and eye-tracking analysis

For time-series data, the built-in configuration supports:

```yaml
bbox_model: sample
```

or:

```yaml
bbox_model: window
```

For this demo, `sample` is the safer starting point.

The generated bounding-box records contain the time-series indices associated with
the region, including values such as:

```text
start_idx
end_idx
bbox
```

This allows gaze to be related back to specific temporal portions of the series.

For analysis, neighbouring sample-level regions can be grouped into larger windows,
for example:

```text
samples 000-015
samples 016-031
samples 032-047
...
```

This makes measures such as time-axis coverage or local dwell time easier to
interpret.

---

# Hypotheses

The experiment tests five main hypotheses.

### H1 — Fixation count increases with variability

Higher signal variability should require more visual sampling:

```text
LOW < MEDIUM < HIGH
```

### H2 — MEDIUM requires the longest decision process

MEDIUM is expected to be the most ambiguous category and may therefore produce the
longest total fixation dwell time or viewing duration.

### H3 — HIGH produces broader exploration

HIGH-variability signals should lead to gaze covering a larger proportion of the
horizontal time axis.

### H4 — Attention differs by physical domain

Machine vibration should encourage relatively distributed inspection of the trace,
whereas PV attention should cluster more strongly around local cloud-induced drops
and recoveries.

### H5 — MEDIUM produces the lowest accuracy

The middle category should be more difficult to classify than the perceptually more
distinct LOW and HIGH categories.

See `EXPERIMENT.md` for operational definitions and rationale.

---

# Recommended workflow

```text
1. Generate CSV files
        |
        v
2. Run machine-vibration block (9 trials)
        |
        v
3. Record LOW / MEDIUM / HIGH responses + gaze
        |
        v
4. Run PV-power block (9 trials)
        |
        v
5. Record LOW / MEDIUM / HIGH responses + gaze
        |
        v
6. Map fixations to time-series bounding boxes
        |
        v
7. Aggregate sample AOIs into temporal windows
        |
        v
8. Compare:
   - LOW / MEDIUM / HIGH
   - MACHINE / PV
   - noise level x domain
```

---

# Suggested outcome variables

At minimum, report:

| Variable | Interpretation |
|---|---|
| Accuracy | whether the participant selected the correct class |
| Fixation count | amount of visual sampling |
| Total fixation dwell | total visual processing time |
| Horizontal gaze dispersion | how broadly the series was explored |
| Unique AOIs visited | number of temporal regions inspected |
| Time-axis coverage | proportion of the series visually visited |
| Scanpath transitions | movement between temporal regions |

For H4, it is particularly useful to compare the distribution of dwell time over
the time axis.

---

# Important note about the current renderer

The current time-series renderer scales the displayed signal using the minimum and
maximum values of the current series.

For this reason, the demo generator does **not** define LOW / MEDIUM / HIGH only by
multiplying white-noise amplitude. Doing so could be visually misleading after
per-stimulus scaling.

Instead, class differences are encoded in temporal structure:

- machine: broadband irregularity plus different numbers and magnitudes of transient
  vibration bursts;
- PV: different numbers, widths, and depths of smooth cloud-induced power reductions.

This makes the demonstration more robust and more physically interpretable.

---

# Requirements for the generator

```bash
pip install numpy pandas
```

The generated CSVs can then be used directly by the `time_series` dataset loader.

---

# Notes for a scientific study

This package is designed as a **demo workflow**. For a formal study:

- counterbalance the order of MACHINE and PV blocks;
- use more than three exemplars per class;
- pre-test the perceptual separability of LOW / MEDIUM / HIGH;
- keep the number of samples and display geometry constant;
- define the fixation algorithm before data collection;
- analyse participant and stimulus variability with mixed-effects models;
- avoid interpreting HIGH machine vibration as evidence of a specific mechanical
  fault unless independently validated diagnostic labels are available.

---

## Generated output structure

After running `generate_data.py`, all dataset-related files are written to:

```text
generated_dataset/
├── machine_vibration.csv
├── pv_power.csv
├── time_series_noise_demo.csv
├── plots_index.csv
└── plots/
    ├── machine_low_01.png
    ├── machine_medium_01.png
    ├── machine_high_01.png
    ├── pv_low_01.png
    ├── pv_medium_01.png
    ├── pv_high_01.png
    └── ...
```

The generated plots:

- have **no titles**,
- use a **light gray grid**,
- have **labeled axes**,
- use a **clear line color on white background**,
- use **larger axis-label and tick fonts**,
- use **fixed Y-axis limits within each domain**,
- are saved as **high-resolution PNG files**.

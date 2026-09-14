# Image-Based Time-Series Variability Demo

## Overview

This demo uses the **Image Data** modality of `tobii-pytracker`.

It presents 18 previously prepared plot images:

```text
Machine vibration:
3 LOW + 3 MEDIUM + 3 HIGH = 9

PV power:
3 LOW + 3 MEDIUM + 3 HIGH = 9

Total = 18 stimuli
```

This demo contains **no data-generation script** and does not use any intermediate
generated-data directory.

The plot images are copied manually into `datasets/image_noise_demo/`.

---

# 1. Required dataset structure

The current `ImageDataset` obtains the response classes from subdirectory names.
For this reason, the 18 images must be arranged as:

```text
datasets/
└── image_noise_demo/
    ├── low/
    │   ├── machine_low_01.png
    │   ├── machine_low_02.png
    │   ├── machine_low_03.png
    │   ├── pv_low_01.png
    │   ├── pv_low_02.png
    │   └── pv_low_03.png
    │
    ├── medium/
    │   ├── machine_medium_01.png
    │   ├── machine_medium_02.png
    │   ├── machine_medium_03.png
    │   ├── pv_medium_01.png
    │   ├── pv_medium_02.png
    │   └── pv_medium_03.png
    │
    └── high/
        ├── machine_high_01.png
        ├── machine_high_02.png
        ├── machine_high_03.png
        ├── pv_high_01.png
        ├── pv_high_02.png
        └── pv_high_03.png
```

Copy the PNG files into these directories manually before running the experiment.

The folder names:

```text
low
medium
high
```

become the ground-truth classes and the response buttons displayed by
`tobii-pytracker`.

---

# 2. Repository structure

The relevant project structure is:

```text
tobii-pytracker/
├── configs/
│   ├── config_image_noise_demo.yaml
│   └── eyetracker_config.yaml
│
├── datasets/
│   └── image_noise_demo/
│       ├── low/
│       ├── medium/
│       └── high/
│
├── examples/
│   └── image_noise_demo/
│       ├── README.md
│       ├── EXPERIMENT.md
│       ├── apply_repo_fixes.py
│       ├── analyze_results.py
│       ├── run_tobii.bat
│       ├── run_tobii.sh
│       ├── analyze.bat
│       └── analyze.sh
│
└── output/
    └── image_noise_demo/
```

Use the existing official:

```text
configs/eyetracker_config.yaml
```

from the repository.

---

# 3. Main experiment config

The experiment uses:

```text
configs/config_image_noise_demo.yaml
```

The image dataset is configured as:

```yaml
dataset:
  image:
    bbox_model: grid
    path: datasets/image_noise_demo
```

No other dataset location is used by this demo.

---

# 4. Participant task

The images represent two physical domains.

## Machine vibration

Question:

> **How large are the irregular vibration fluctuations in the signal?**

## PV power

Question:

> **How large are the short-term fluctuations in PV power production?**

The y-axis label identifies the domain.

Responses:

```text
LOW | MEDIUM | HIGH | NIE WIEM
```

Detailed hypotheses are documented in:

```text
examples/image_noise_demo/EXPERIMENT.md
```

---

# 5. Display geometry

The prepared plots use an approximately 2:1 aspect ratio.

The experiment therefore uses:

```yaml
aoe:
  - 1600
  - 800
```

`ImageDataset` displays each image using this AOI size.

Update the monitor parameters if your physical setup differs:

```yaml
display:
  monitor:
    resolution:
      - 2560
      - 1440
    width: 35
    distance: 60
    display_number: 0
```

---

# 6. Optional repository fixes

The stock dataset classes currently append an additional response named:

```text
none
```

If this change has not already been committed to your fork, run:

```bash
python examples/image_noise_demo/apply_repo_fixes.py
```

The patch changes the fallback response from:

```python
self.classes.append("none")
```

to:

```python
self.classes.append("nie wiem")
```

It also makes main YAML loading explicitly UTF-8.

For a first installation:

```bash
python examples/image_noise_demo/apply_repo_fixes.py
git diff
pip install .
```

If you use an editable development installation:

```bash
pip install -e .
```

source changes are reflected directly.

---

# 7. Quick GUI test

Before connecting the Tobii tracker, test two stimuli:

```bash
tobii-pytracker \
  --config_file configs/config_image_noise_demo.yaml \
  --loop_count 2
```

You should see:

- one of the prepared plot images,
- LOW,
- MEDIUM,
- HIGH,
- NIE WIEM.

If the images are not found, verify the structure under:

```text
datasets/image_noise_demo/
```

---

# 8. Run the complete experiment

With Tobii connected:

```bash
tobii-pytracker \
  --config_file configs/config_image_noise_demo.yaml \
  --eyetracker_config_file configs/eyetracker_config.yaml \
  --enable_eyetracker \
  --loop_count 18
```

Windows:

```text
examples/image_noise_demo/run_tobii.bat
```

Linux/macOS:

```bash
bash examples/image_noise_demo/run_tobii.sh
```

---

# 9. Trial workflow

```text
fixation point
      |
      v
prepared plot image
      |
      v
participant inspects variability
      |
      v
LOW / MEDIUM / HIGH / NIE WIEM
      |
      v
gaze + response saved
      |
      v
next image
```

The current `ImageDataset` shuffles the loaded samples before presentation.

---

# 10. Output

The demo saves sessions under:

```text
output/image_noise_demo/
```

A session contains the standard PsychoPy experiment output, including:

```text
screenshot_file
input_data
classification
user_classification
gaze_data
objects_bboxes
voice_file
voice_start_timestamp
```

For this image experiment:

- `input_data` contains the image path,
- `classification` contains the class-folder name: `low`, `medium`, or `high`.

---

# 11. Grid AOIs

The config uses:

```yaml
bbox_model: grid
```

The current fallback detector divides the AOI into a 3 x 3 grid.

Conceptually:

```text
+---------+---------+---------+
|         |         |         |
|  LEFT   | MIDDLE  |  RIGHT  |
|         |         |         |
+---------+---------+---------+
|         |         |         |
|  LEFT   | MIDDLE  |  RIGHT  |
|         |         |         |
+---------+---------+---------+
|         |         |         |
|  LEFT   | MIDDLE  |  RIGHT  |
|         |         |         |
+---------+---------+---------+
```

Since the plot x-axis represents time, the three columns provide a simple
horizontal exploration measure.

---

# 12. Analysis

After collecting at least one session, run:

```bash
python examples/image_noise_demo/analyze_results.py
```

or on Windows:

```text
examples/image_noise_demo/analyze.bat
```

Results are written to:

```text
examples/image_noise_demo/results/
```

The analysis produces:

```text
trial_metrics.csv
class_summary.csv
domain_class_summary.csv
hypothesis_summary.txt
01_fixation_count.png
02_fixation_dwell.png
03_time_axis_coverage.png
04_accuracy.png
05_domain_attention.png
```

---

# 13. Main metrics

The analysis reports:

- classification accuracy,
- fixation count,
- fixation dwell time,
- horizontal fixation span,
- number of unique grid cells visited,
- number of horizontal grid columns visited,
- time-axis coverage,
- horizontal dwell entropy.

These measures correspond to the five hypotheses described in
`EXPERIMENT.md`.

---

# 14. Complete workflow

```text
1. Copy the 18 PNG images manually to:
   datasets/image_noise_demo/low/
   datasets/image_noise_demo/medium/
   datasets/image_noise_demo/high/

2. If required, apply the source-level NONE -> NIE WIEM patch.

3. Install the fork.

4. Run a two-trial GUI test.

5. Run the 18-trial experiment with Tobii.

6. Analyse the saved results.
```

There is no automatic image-generation or dataset-preparation step in this demo.

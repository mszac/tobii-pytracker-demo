# Image-Based Time-Series Variability Demo

## What is included

This overlay contains everything needed for the demo **except the 18 dataset
images**.

It includes:

- the default `configs/config.yaml`,
- the explicit `configs/config_image_noise_demo.yaml`,
- `configs/eyetracker_config.yaml`,
- run scripts,
- a non-destructive dataset validator,
- the source-fix helper for `NIE WIEM`,
- the result-analysis script,
- experiment documentation.

No image-generation or dataset-preparation script is included.

---

## Required dataset

Copy the 18 prepared plot images manually into:

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

`ImageDataset` obtains the class labels from these subdirectory names.

---

## Recommended repository structure

```text
tobii-pytracker/
├── configs/
│   ├── config.yaml
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
│       ├── check_dataset.py
│       ├── apply_repo_fixes.py
│       ├── analyze_results.py
│       ├── run_gui_test.bat
│       ├── run_tobii.bat
│       ├── analyze.bat
│       ├── run_gui_test.sh
│       ├── run_tobii.sh
│       └── analyze.sh
│
└── output/
```

---

## Why `configs/config.yaml` is included

The current CLI defaults to:

```text
configs/config.yaml
```

when `--config_file` is not supplied.

Therefore this overlay deliberately includes a copy of the experiment config
under that filename.

This means:

```bash
tobii-pytracker
```

can start the GUI demo without failing because `configs/config.yaml` is missing.

However, the CLI default is currently only **10 trials**, so use the supplied run
script or `--loop_count 18` for the complete experiment.

---

## 1. Validate the manually copied images

From the repository root:

```bash
python examples/image_noise_demo/check_dataset.py
```

The script does not modify any file. A correct dataset should report:

```text
low   : 6 image(s)
medium: 6 image(s)
high  : 6 image(s)
total : 18 image(s)
[OK] Dataset structure is ready for the experiment.
```

---

## 2. Apply the `NIE WIEM` source fix if required

The current dataset classes append a fallback response named `none`.

For this demo it should be displayed as:

```text
NIE WIEM
```

Run:

```bash
python examples/image_noise_demo/apply_repo_fixes.py
```

Then inspect:

```bash
git diff
```

If you have not installed the package yet:

```bash
pip install .
```

If the source was changed after a normal `pip install .`, reinstall it.

For development, this is convenient:

```bash
pip install -e .
```

---

## 3. GUI-only test

Use:

```bash
tobii-pytracker --config_file configs/config_image_noise_demo.yaml --loop_count 2
```

or on Windows:

```text
examples\image_noise_demo\run_gui_test.bat
```

No physical eye tracker is enabled in this command.

You should see:

```text
LOW | MEDIUM | HIGH | NIE WIEM
```

and one prepared plot image.

---

## 4. Full 18-trial experiment with Tobii

Run:

```bash
tobii-pytracker --config_file configs/config_image_noise_demo.yaml --eyetracker_config_file configs/eyetracker_config.yaml --enable_eyetracker --loop_count 18
```

Windows shortcut:

```text
examples\image_noise_demo\run_tobii.bat
```

Linux/macOS:

```bash
bash examples/image_noise_demo/run_tobii.sh
```

---

## 5. Bare `tobii-pytracker`

Because this package includes `configs/config.yaml`, this now works:

```bash
tobii-pytracker
```

It starts the experiment using the image dataset, but because the current CLI
default is 10 trials, it is only a quick run.

For all 18 stimuli, use `run_tobii.bat/.sh` or specify:

```bash
--loop_count 18
```

---

## 6. Main experiment configuration

```yaml
dataset:
  image:
    bbox_model: grid
    path: datasets/image_noise_demo
```

The display AOI is:

```yaml
aoe:
  - 1600
  - 800
```

This matches the approximate 2:1 plot aspect ratio.

---

## 7. Output

Sessions are saved under:

```text
output/image_noise_demo/<timestamp>/
```

The standard PsychoPy `data.csv` contains, among other fields:

```text
input_data
classification
user_classification
gaze_data
objects_bboxes
```

For this demo:

- `input_data` is the image path,
- `classification` is `low`, `medium`, or `high`,
- `objects_bboxes` contains the image grid AOIs.

---

## 8. Analysis

After collecting data:

```bash
python examples/image_noise_demo/analyze_results.py
```

or:

```text
examples\image_noise_demo\analyze.bat
```

Results are written into:

```text
examples/image_noise_demo/results/
```

including:

```text
trial_metrics.csv
class_summary.csv
domain_class_summary.csv
hypothesis_summary.txt
01_fixation_count.png
02_fixation_dwell.png
03_time_axis_coverage.png
04_accuracy.png
```

See `EXPERIMENT.md` for the hypotheses and rationale.

---

## Troubleshooting

### `Configuration file 'configs/config.yaml' not found`

This means the overlay was not copied into the repository root, or
`configs/config.yaml` is missing.

This package includes that file. Make sure you run the command from the
`tobii-pytracker` repository root.

### `pytables package not found`

The warning about the ioHub HDF5 datastore is not the same as a fatal Python
traceback. Diagnose the actual exception printed after the warning.

### Images are not loaded

Run:

```bash
python examples/image_noise_demo/check_dataset.py
```

and verify that the three class directories are directly inside:

```text
datasets/image_noise_demo/
```

### Button still says `NONE`

Apply:

```bash
python examples/image_noise_demo/apply_repo_fixes.py
```

If the project was installed non-editably before the source change, reinstall it.

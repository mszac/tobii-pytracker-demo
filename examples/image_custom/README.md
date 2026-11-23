# Image Custom Demo

Run the image experiment of `image_semantic_demo` on **your own images**. The
stimuli are not part of the demo, you put them in one folder and the demo shows
all of them, one per trial.

## 1. Put your images in the stimulus folder

```
examples/image_custom/data/pix/
```

One flat folder, **no subfolders**. Supported file types are PNG, JPG, JPEG,
BMP, GIF, TIFF.

## 2. Order of presentation

Images are shown in alphabetical order of the file name, so the order is the one
you see in the file manager. Prefixing the names with numbers fixes the order:

```
1_intro.png
2_task.png
3_result.png
```

Plain alphabetical order puts `10_` before `2_`, so use `01_`, `02_`, ... when a
session has more than nine images.

## 3. Write your instructions

The intro and outro screens of `config.native.yaml` carry the placeholder
`Put your text here`. Replace those lines with your own text. The number of
screens, the response buttons, the fixation dot and the calibration are the ones
of `image_semantic_demo` and need no change.

The lines about the response timer, MouseGaze and the SPACE key were kept,
because they describe how the demo is operated rather than what the task is.

## 4. Run

```bash
examples/image_custom/run.sh
```

The script checks the upstream checkout, counts the images, prints the list in
presentation order and starts the experiment. Every image of the folder becomes
one trial. To show only the first N images, call the runner directly:

```bash
python examples/image_custom/run_experiment.py --loop-count 5
```

## 5. Where the data lands

```
output/image_custom/<session>/data.csv
```

One row per trial, the columns of the upstream runtime: `screenshot_file`,
`input_data`, `classification`, `user_classification`, `gaze_data`,
`objects_bboxes`, `voice_file`, `voice_start_timestamp`.

A flat folder carries no category, so `classification` holds the file name of
the stimulus without its extension, and `user_classification` holds the button
the participant clicked.

## 6. Analysis

The file is the usual tobii-pytracker `data.csv` and works with
`workflow-pytracker-heatmap.ipynb` without any change. Copy two things into the
analysis project:

- the recording to `data/logs/<experiment>/`,
- your stimulus images to `data/pix/<experiment>/`,

then set `DATA_DIR`, `DATA_FILE` and `IMAGE_DIR` in section 2 of the notebook.
The notebook matches a trial to its image by file name, which is why the images
have to be next to the recording. Use `workflow-pytracker-raw.ipynb` when you
want to look at the recording without the images.

## 7. Files of this demo

| File | Purpose |
|---|---|
| `config.native.yaml` | Display, buttons, output folder, instruction screens. |
| `image_custom_dataset.py` | Reads the flat folder in alphabetical order. |
| `run_experiment.py` | Counts the images and starts the upstream runtime. |
| `run.sh`, `run_native.sh` | Checks and launch. |
| `data/pix/` | Your stimulus images. |

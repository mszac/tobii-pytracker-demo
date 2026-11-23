# Image Custom Demo, experiment protocol

## Design

One block, one stimulus per trial, as many trials as there are images in
`examples/image_custom/data/pix`. There are no conditions and no blocks, the
images are presented in alphabetical order of the file name, which keeps the
order under the control of whoever names the files.

This is the simplification against `image_semantic_demo`, where 12 fixed images
of three categories are interleaved so that two images of one category rarely
follow each other. Here nothing is shuffled and nothing is balanced.

## Trial

1. The stimulus is drawn in the area of interest, 900 x 700 px by default.
2. Gaze is recorded for the whole time the stimulus is visible.
3. The participant answers by clicking one of the response buttons.
4. There is no response timer, the stimulus stays visible until a button is
   clicked, and the answer ends the trial.

The response buttons are the ones of `image_semantic_demo`: BIOLOGICAL, OBJECT
and SCENE. Change `RESPONSE_BUTTONS` in `image_custom_dataset.py` to use other
labels, the number of buttons is free.

## Screens

Intro and outro, the two screens of the original demo, with their text replaced
by the placeholder `Put your text here` in `config.native.yaml`. Calibration,
fixation dot and the SPACE key to start behave as in the original.

## Recorded data

`output/image_custom/<session>/data.csv`, one row per trial, with the columns of
the upstream runtime. Two of them deserve a note:

- `classification`: the file name of the stimulus without its extension. A flat
  folder has no categories, so this column identifies the stimulus instead of
  naming a ground truth.
- `user_classification`: the label of the button the participant clicked.

Gaze samples sit in `gaze_data`, in screen pixels with the origin at the centre
of the screen and y growing upward, the format the analysis notebooks expect.

## Known limits

- No ground truth, so accuracy cannot be computed from the file alone. Encode
  the expected answer in the file name when you need it, for example
  `03_object_lamp.png`, and split that name during the analysis.
- The order is fixed for every participant. Shuffling would need a change in
  `image_custom_dataset.py`, where the sorted list is built.
- Plain alphabetical order puts `10_` before `2_`, so number the files `01_`,
  `02_` when a session has more than nine images.

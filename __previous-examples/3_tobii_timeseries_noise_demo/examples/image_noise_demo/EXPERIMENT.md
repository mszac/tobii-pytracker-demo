# Image-Based Time-Series Variability Demo

## Experiment design

The experiment contains exactly **18 image stimuli**:

| Domain | LOW | MEDIUM | HIGH | Total |
|---|---:|---:|---:|---:|
| Machine vibration | 3 | 3 | 3 | 9 |
| PV power | 3 | 3 | 3 | 9 |
| **Total** | **6** | **6** | **6** | **18** |

The images are stored manually under:

```text
datasets/image_noise_demo/
├── low/
├── medium/
└── high/
```

The class-directory name is the ground-truth classification used by
`tobii-pytracker`.

## Participant task

For a machine-vibration image:

> **How large are the irregular vibration fluctuations in the signal?**

For a PV image:

> **How large are the short-term fluctuations in PV power production?**

The plot's y-axis label tells the participant which signal domain is shown.

Responses:

```text
LOW | MEDIUM | HIGH | NIE WIEM
```

## Hypotheses

### H1 — Variability increases visual sampling

Higher variability should require more fixations:

```text
LOW < MEDIUM < HIGH
```

Primary metric: fixation count.

### H2 — MEDIUM requires the longest decision process

MEDIUM lies between two perceptual extremes and should be the most ambiguous.

Primary metrics:

- total fixation dwell time,
- gaze-recording duration before the response.

### H3 — HIGH produces broader horizontal exploration

HIGH-variability plots contain more local changes across the time axis.

Primary metrics:

- unique horizontal grid columns visited,
- time-axis coverage,
- horizontal fixation span.

### H4 — Viewing strategy differs between machine and PV plots

Machine vibration contains distributed oscillatory irregularity, whereas PV
variation is dominated by local cloud-related drops and recoveries.

Primary metrics:

- dwell distribution across horizontal regions,
- time-axis coverage,
- horizontal dwell entropy.

### H5 — MEDIUM produces the lowest accuracy

Expected:

```text
accuracy(MEDIUM) < accuracy(LOW)
accuracy(MEDIUM) < accuracy(HIGH)
```

## Workflow

```text
manually prepared image dataset
        |
        v
ImageDataset loads LOW / MEDIUM / HIGH folders
        |
        v
stimuli are shuffled
        |
        v
fixation point
        |
        v
plot image
        |
        v
LOW / MEDIUM / HIGH / NIE WIEM response
        |
        v
gaze + response + grid AOIs saved
        |
        v
analysis of fixation count, dwell, coverage and accuracy
```

## AOI strategy

The config uses:

```yaml
bbox_model: grid
```

The current image fallback detector creates a **3 x 3 grid**. Because the x-axis
of each stimulus is time, the three grid columns form simple LEFT / MIDDLE / RIGHT
temporal regions.

This supports a clear demo of horizontal exploration without requiring an
external object-detection model.

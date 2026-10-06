# Tobii Pytracker Demo — setup and execution

This repository contains the experiment examples, fixed stimuli, collection validators, Jupyter notebooks, and Docker bridge used with `tobii-pytracker`.

There is one experiment workflow and one set of demos. You can execute the same experiments either directly from a Python 3.10 environment or inside the upstream `psychopy` Docker image. Both methods write compatible session data to the demo repository's `output/` directory, and the same Jupyter notebooks are used afterward.

## Demo catalog

- **Test Demo** — technical three-image installation and interaction check.
- **UX A/B Text Demo** — controlled EARLY/LATE placement of answer-relevant information in short texts.
- **Time-Series Noise Demo** — LOW/MEDIUM/HIGH variability classification for machine-vibration and PV-power signals.
- **Text Search Demo** — visual search for answer-relevant phrases in practical-information texts.
- **Image Semantic Demo** — mixed semantic image categorization across BIOLOGICAL, OBJECT, and SCENE stimuli.

All experiment trials are response-gated: the current stimulus remains visible until the participant selects an answer.

---

# Local execution

## 1. Clone the repositories

Windows 11 + Git Bash reference layout:

```bash
rm -rf tobii-pytracker

git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
```

Keep the shell in the parent `tobii-pytracker` directory for the commands below.

```text
tobii-pytracker/
├── src/
├── configs/
└── tobii-pytracker-demo/
    ├── examples/
    ├── docs/
    ├── docker/
    └── output/
```

## 2. Create the Python environment

```bash
conda env remove -n pytracker-env -y || true
conda create -n pytracker-env python=3.10 -y

conda run -n pytracker-env python -m pip install --upgrade pip
conda run -n pytracker-env python -m pip install .
conda run -n pytracker-env python -m pip install \
  'pyzmq>=22.2.1' ujson 'tables==3.9.1' \
  'jupyterlab>=4,<5' 'ipykernel>=6,<7'
conda run -n pytracker-env python -m pip install \
  'psychopy==2024.1.4' --no-deps
```

## 3. Run the demos locally

### Test Demo

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/test_demo/run.sh
```

### UX A/B Text Demo

English:

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/ux_ab_demo/run.sh
```

Polish variant:

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/ux_ab_demo/run_pl.sh
```

### Time-Series Noise Demo

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/timeseries_noise_demo/run.sh
```

### Text Search Demo

English:

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/text_search_demo/run.sh
```

Polish variant:

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/text_search_demo/run_pl.sh
```

### Image Semantic Demo

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/image_semantic_demo/run.sh
```

## 4. MouseGaze interaction

With the upstream MouseGaze configuration:

- hold the **RIGHT mouse button** while moving the pointer to generate gaze samples;
- release RIGHT before selecting an answer with **LEFT click**;
- the current stimulus has no response timeout and remains visible until an answer is selected;
- `ESC` exits the experiment.

A missing MouseGaze segment is reported as a data-quality issue; it does not invalidate an otherwise recorded behavioral response.

## 5. Analyze collected sessions in Jupyter

The notebooks read real `data.csv` files written by completed experiments. They do not generate replacement experiment data.

```bash
conda run --no-capture-output -n pytracker-env \
  jupyter lab tobii-pytracker-demo/examples/ux_ab_demo/analysis/ux_ab_analysis.ipynb

conda run --no-capture-output -n pytracker-env \
  jupyter lab tobii-pytracker-demo/examples/timeseries_noise_demo/analysis/timeseries_analysis.ipynb

conda run --no-capture-output -n pytracker-env \
  jupyter lab tobii-pytracker-demo/examples/text_search_demo/analysis/text_search_analysis.ipynb

conda run --no-capture-output -n pytracker-env \
  jupyter lab tobii-pytracker-demo/examples/image_semantic_demo/analysis/image_semantic_analysis.ipynb
```

The technical Test Demo notebook is `examples/test_demo/analysis/test_demo_analysis.ipynb`.

## 6. Verify the upstream checkout

```bash
git status --porcelain
```

The command should produce no output in the parent `tobii-pytracker` repository.

---

# Docker execution

Docker runs the same demo files inside the image defined by the upstream `sbobek/tobii-pytracker` `psychopy` branch. The demo repository supplies only the Compose bridge and dispatcher; it does not fork the upstream runtime.

## 1. Requirements

- Docker Desktop or Docker Engine with Docker Compose v2;
- a VNC client;
- network access during the first image build.

A local clone of upstream `tobii-pytracker` is not required when experiments are executed through Docker.

## 2. Clone the demo repository

```bash
cd /d/pytracker
rm -rf tobii-pytracker-demo
git clone https://github.com/mszac/tobii-pytracker-demo.git
cd tobii-pytracker-demo
```

The Compose bridge builds from:

```text
https://github.com/sbobek/tobii-pytracker.git#psychopy
```

## 3. Run a demo

### Test Demo

```bash
DEMO=test_demo docker compose -f docker/compose.yaml up --build
```

### UX A/B Text Demo

English:

```bash
DEMO=ux_ab_demo docker compose -f docker/compose.yaml up --build
```

Polish variant:

```bash
DEMO=ux_ab_demo DEMO_LANG=pl docker compose -f docker/compose.yaml up --build
```

### Time-Series Noise Demo

```bash
DEMO=timeseries_noise_demo docker compose -f docker/compose.yaml up --build
```

### Text Search Demo

English:

```bash
DEMO=text_search_demo docker compose -f docker/compose.yaml up --build
```

Polish variant:

```bash
DEMO=text_search_demo DEMO_LANG=pl docker compose -f docker/compose.yaml up --build
```

### Image Semantic Demo

```bash
DEMO=image_semantic_demo docker compose -f docker/compose.yaml up --build
```

## 4. Connect through VNC

Connect the VNC client to:

```text
localhost:5900
```

The PsychoPy intro screen waits for participant input, so the experiment does not advance while the VNC client is being opened.

To select another host port:

```bash
VNC_PORT=5901 DEMO=image_semantic_demo \
  docker compose -f docker/compose.yaml up --build
```

Then connect to `localhost:5901`.

## 5. Output and Jupyter analysis

The demo repository is bind-mounted into the container. Collected sessions are written directly to the host repository's `output/` directory.

Jupyter analysis is performed on those host-side sessions with the notebooks listed in the **Analyze collected sessions in Jupyter** section above. The upstream experiment image is intentionally not extended with a second notebook environment.

## 6. Stop Docker

```bash
docker compose -f docker/compose.yaml down
```

---

# Command reference — Bash vs Windows CMD

This section is an **alternative command reference only**. 

> **Important:** run the commands from the same directories described in the main instructions above.  


---

## ═══════════════════════════════════════
## WINDOWS CMD
## ═══════════════════════════════════════

These commands are alternatives for **Windows Command Prompt (`cmd.exe`)**. 

### Clone the repositories

```bat
if exist tobii-pytracker rmdir /s /q tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
```

### Create the Python environment

```bat
conda env remove -n pytracker-env -y
conda create -n pytracker-env python=3.10 -y
conda run -n pytracker-env python -m pip install --upgrade pip
conda run -n pytracker-env python -m pip install .
conda run -n pytracker-env python -m pip install "pyzmq>=22.2.1" ujson "tables==3.9.1" "jupyterlab>=4,<5" "ipykernel>=6,<7"
conda run -n pytracker-env python -m pip install "psychopy==2024.1.4" --no-deps
```

### Run demos locally

The local demo launchers are Bash scripts, so the Windows CMD variants below assume **Git for Windows / Git Bash** is installed and `bash.exe` is available on `PATH`.

**Test Demo**

```bat
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/test_demo/run.sh
```

**UX A/B Text Demo — English**

```bat
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/ux_ab_demo/run.sh
```

**UX A/B Text Demo — Polish**

```bat
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/ux_ab_demo/run_pl.sh
```

**Time-Series Noise Demo**

```bat
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/timeseries_noise_demo/run.sh
```

**Text Search Demo — English**

```bat
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/text_search_demo/run.sh
```

**Text Search Demo — Polish**

```bat
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/text_search_demo/run_pl.sh
```

**Image Semantic Demo**

```bat
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/image_semantic_demo/run.sh
```

### Jupyter analysis

```bat
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/ux_ab_demo/analysis/ux_ab_analysis.ipynb
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/timeseries_noise_demo/analysis/timeseries_analysis.ipynb
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/text_search_demo/analysis/text_search_analysis.ipynb
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/image_semantic_demo/analysis/image_semantic_analysis.ipynb
```

### Verify upstream checkout

```bat
git status --porcelain
```

### Docker — clone demo repository

Example for `D:\pytracker`:

```bat
cd /d D:\pytracker
if exist tobii-pytracker-demo rmdir /s /q tobii-pytracker-demo
git clone https://github.com/mszac/tobii-pytracker-demo.git
cd tobii-pytracker-demo
```

### Docker — run demos

**Test Demo**

```bat
set "DEMO=test_demo" && docker compose -f docker/compose.yaml up --build
```

**UX A/B Text Demo — English**

```bat
set "DEMO=ux_ab_demo" && docker compose -f docker/compose.yaml up --build
```

**UX A/B Text Demo — Polish**

```bat
set "DEMO=ux_ab_demo" && set "DEMO_LANG=pl" && docker compose -f docker/compose.yaml up --build
```

**Time-Series Noise Demo**

```bat
set "DEMO=timeseries_noise_demo" && docker compose -f docker/compose.yaml up --build
```

**Text Search Demo — English**

```bat
set "DEMO=text_search_demo" && docker compose -f docker/compose.yaml up --build
```

**Text Search Demo — Polish**

```bat
set "DEMO=text_search_demo" && set "DEMO_LANG=pl" && docker compose -f docker/compose.yaml up --build
```

**Image Semantic Demo**

```bat
set "DEMO=image_semantic_demo" && docker compose -f docker/compose.yaml up --build
```

### Docker — alternate VNC port

```bat
set "VNC_PORT=5901" && set "DEMO=image_semantic_demo" && docker compose -f docker/compose.yaml up --build
```

### Docker — stop

```bat
docker compose -f docker/compose.yaml down
```

---

## Notes about Windows shells
- **PowerShell:** the Bash commands are not PowerShell syntax. If you launch Docker directly from PowerShell, set environment variables with `$env:NAME="value"` before the `docker compose` command. The Windows CMD examples above are specifically for `cmd.exe`.


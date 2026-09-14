# Linux installation

This section describes the installation of `tobii-pytracker` on Linux using Ubuntu 24.04 as an example. Conda or Miniconda is assumed to be already installed.

## 1. Install Linux system dependencies

Install the required Linux system packages:

```bash
sudo apt update

sudo apt install -y \
    git \
    build-essential \
    pkg-config \
    avahi-daemon \
    libportaudio2 \
    portaudio19-dev \
    libasound2-dev \
    libsndfile1 \
    libgl1 \
    libglu1-mesa \
    libx11-6 \
    libxrandr2 \
    libxi6 \
    libxcursor1 \
    libxinerama1
```

Enable the Avahi service:

```bash
sudo systemctl enable --now avahi-daemon
systemctl is-active avahi-daemon
```

Expected output:

```text
active
```

## 2. Create the Python 3.10 environment

`tobii-pytracker` requires Python 3.10.

Create and activate a dedicated Conda environment:

```bash
conda create -y -n pytracker-env python=3.10 pip
conda activate pytracker-env
```

Verify the Python version:

```bash
python --version
```

The expected version is Python 3.10.x.

## 3. Clone the repository

```bash
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
```

## 4. Install repository dependencies

First upgrade `pip` and `wheel`:

```bash
python -m pip install --upgrade pip wheel
```

Install the dependencies defined in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

The repository requirements include, among others:

```text
numpy==1.26.4
PyYAML==6.0.1
pyserial==3.5
scipy==1.13.1
json_tricks==3.17.3
Pillow==10.3.0
pandas==2.2.2
psutil==5.9.8
psychopy-eyetracker-tobii==0.0.3
tobii-research==2.0.0
```

## 5. Install PsychoPy

PsychoPy is intentionally not installed through `requirements.txt`. Install the supported version without automatically pulling its complete desktop dependency stack:

```bash
python -m pip install "psychopy==2024.2.5" --no-deps
```

## 6. Install Linux-specific PsychoPy/ioHub dependencies

Install the additional modules required by PsychoPy/ioHub on Linux:

```bash
python -m pip install \
    "pyzmq>=22.2.1" \
    ujson \
    python-xlib \
    distro
```

## 7. Install audio dependencies on Linux

The current `requirements.txt` installs `sounddevice` and `soundfile` only on Windows:

```text
sounddevice==0.5.3; platform_system == "Windows"
soundfile==0.13.1; platform_system == "Windows"
```

However, `tobii_pytracker.utils.voice` imports both modules independently of the operating system.

On Linux, install them manually:

```bash
python -m pip install \
    "sounddevice==0.5.3" \
    "soundfile==0.13.1"
```

On Windows, these packages are installed automatically through `requirements.txt`.

## 8. Resolve Linux dependency conflicts

### pyglet

`requirements.txt` installs:

```text
pyglet==1.4.11
```

but PsychoPy 2024.2.5 requires `pyglet==1.5.27` on Linux.

Install the PsychoPy-compatible version:

```bash
python -m pip install --force-reinstall --no-deps \
    "pyglet==1.5.27"
```

### setuptools

PsychoPy 2024.2.5 expects:

```text
setuptools==70.3.0
```

Set the compatible version:

```bash
python -m pip install --force-reinstall \
    "setuptools==70.3.0"
```

### ultralytics

The repository contains different `ultralytics` constraints in `requirements.txt` and `pyproject.toml`. Use the stricter project constraint:

```bash
python -m pip install --force-reinstall --no-deps \
    "ultralytics<8.4"
```

Do not run `pip install -r requirements.txt` again after these overrides, because it may restore versions that are incompatible with the Linux PsychoPy configuration.

## 9. Install tobii-pytracker

For a cloned repository, an editable installation is recommended:

```bash
python -m pip install -e . --no-deps
hash -r
```

Verify the command-line interface:

```bash
which tobii-pytracker
tobii-pytracker --help
```

## 10. Verify Python imports

```bash
python - <<'PY'
import sys
import yaml
import serial
import psutil
import json_tricks
import numpy
import pyglet
import psychopy
import tobii_research
import sounddevice
import soundfile
import tobii_pytracker

from PIL import Image
from psychopy import core, event, visual, monitors
from psychopy.iohub import launchHubServer

print("Python:", sys.version)
print("NumPy:", numpy.__version__)
print("PsychoPy:", psychopy.__version__)
print("pyglet:", pyglet.version)
print("tobii_research: OK")
print("PsychoPy/ioHub: OK")
print("sounddevice/soundfile: OK")
print("tobii_pytracker: OK")
print("ALL REQUIRED IMPORTS OK")
PY
```

A warning such as:

```text
WARNING: pytables package not found.
ioHub hdf5 datastore functionality will be disabled.
```

is not fatal unless PsychoPy's HDF5/ioHub datastore functionality is required.

PyTables can optionally be installed with:

```bash
python -m pip install tables
```

## 11. Verify Tobii device discovery

With the Tobii eye tracker connected:

```bash
python - <<'PY'
import tobii_research as tr

trackers = tr.find_all_eyetrackers()

print("Detected eye trackers:", len(trackers))

for tracker in trackers:
    print("Model:", tracker.model)
    print("Name:", tracker.device_name)
    print("Serial:", tracker.serial_number)
    print("Address:", tracker.address)
    print()
PY
```

The eye tracker should be detected by the Tobii SDK before testing it through PsychoPy or `tobii-pytracker`.

## 12. Run tobii-pytracker

Activate the environment and enter the repository directory:

```bash
conda activate pytracker-env
cd /path/to/tobii-pytracker
```

Basic execution:

```bash
tobii-pytracker \
    --config_file configs/config.local.yaml \
    --loop_count 1 \
    --log_level debug
```

Execution with a physical Tobii eye tracker:

```bash
tobii-pytracker \
    --config_file configs/config.local.yaml \
    --eyetracker_config_file configs/eyetracker_config.yaml \
    --enable_eyetracker \
    --loop_count 1 \
    --log_level debug
```

## Linux vs. Windows dependency differences

| Dependency | Windows | Linux |
|---|---|---|
| Python | Python 3.10 required | Python 3.10 required |
| `pywin32` | Installed by `requirements.txt` | Not required |
| `pyWinhook` | Installed by `requirements.txt` | Not required |
| `sounddevice` | Installed by `requirements.txt` | Must currently be installed manually |
| `soundfile` | Installed by `requirements.txt` | Must currently be installed manually |
| `pyglet` | Repository version can be used | Override with `1.5.27` for PsychoPy 2024.2.5 |
| `python-xlib` | Not required | Required for the Linux/X11 PsychoPy stack |
| PortAudio/ALSA | Usually provided through Windows runtime packages | Install `libportaudio2`, `portaudio19-dev`, `libasound2-dev` |
| Avahi | Not used | Required/recommended for Tobii device discovery |

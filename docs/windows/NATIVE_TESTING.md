# Windows native testing — v1.7.0

Primary target: Windows 11 + Git Bash. Keep the shell in the parent `tobii-pytracker` root after cloning `tobii-pytracker-demo` inside it.

## Fresh clone

```bash
cd /d/pytracker
rm -rf tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
```

## Environment

```bash
conda env remove -n pytracker-env -y || true
conda create -n pytracker-env python=3.10 -y
conda run -n pytracker-env python -m pip install --upgrade pip
conda run -n pytracker-env python -m pip install .
conda run -n pytracker-env python -m pip install 'pyzmq>=22.2.1' ujson 'tables==3.9.1' 'jupyterlab>=4,<5' 'ipykernel>=6,<7'
conda run -n pytracker-env python -m pip install 'psychopy==2024.1.4' --no-deps
conda run --no-capture-output -n pytracker-env python tobii-pytracker-demo/tools/native_preflight.py --require-iohub
```

`tables==3.9.1` is included because the physical test of v1.4 showed PsychoPy warning that PyTables was absent and ioHub functionality was disabled. JupyterLab/IPython kernel are explicit analysis dependencies.

## Demos

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/test_demo/run_native.sh
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/ux_ab_demo/run_native.sh
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/timeseries_noise_demo/run_native.sh
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/text_search_demo/run_native.sh
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/image_semantic_demo/run_native.sh
```

All stimuli remain response-gated. Missing gaze is a data-quality warning, not a collection failure, provided the response and structural trial data were recorded.

## Notebook analyses

Open one notebook at a time:

```bash
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/test_demo/analysis/test_demo_analysis.ipynb
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/ux_ab_demo/analysis/ux_ab_analysis.ipynb
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/timeseries_noise_demo/analysis/timeseries_analysis.ipynb
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/text_search_demo/analysis/text_search_analysis.ipynb
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/image_semantic_demo/analysis/image_semantic_analysis.ipynb
```

Every notebook automatically locates the demo repository and reads the newest real session from that demo's dedicated output folder.

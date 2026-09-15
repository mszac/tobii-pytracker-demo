# Run Instructions

## Setup

```bash
cd /d/pytracker

rm -rf tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git

conda env remove -n pytracker-env -y || true
conda create -n pytracker-env python=3.10 -y

conda run -n pytracker-env python -m pip install --upgrade pip
conda run -n pytracker-env python -m pip install .
conda run -n pytracker-env python -m pip install \
  'pyzmq>=22.2.1' ujson 'tables==3.9.1' \
  'jupyterlab>=4,<5' 'ipykernel>=6,<7'
conda run -n pytracker-env python -m pip install \
  'psychopy==2024.1.4' --no-deps

conda run --no-capture-output -n pytracker-env \
  python tobii-pytracker-demo/tools/native_preflight.py --require-iohub
```

## 1. Test Demo

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/test_demo/run_native.sh
```

```bash
conda run --no-capture-output -n pytracker-env \
  jupyter lab tobii-pytracker-demo/examples/test_demo/analysis/test_demo_analysis.ipynb
```

## 2. UX A/B Demo

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/ux_ab_demo/run_native.sh
```

```bash
conda run --no-capture-output -n pytracker-env \
  jupyter lab tobii-pytracker-demo/examples/ux_ab_demo/analysis/ux_ab_analysis.ipynb
```

### Polish version

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/ux_ab_demo/run_native_pl.sh
```

## 3. Time Series Noise Demo

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/timeseries_noise_demo/run_native.sh
```

```bash
conda run --no-capture-output -n pytracker-env \
  jupyter lab tobii-pytracker-demo/examples/timeseries_noise_demo/analysis/timeseries_analysis.ipynb
```

## 4. Text Search Demo

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/text_search_demo/run_native.sh
```

```bash
conda run --no-capture-output -n pytracker-env \
  jupyter lab tobii-pytracker-demo/examples/text_search_demo/analysis/text_search_analysis.ipynb
```

### Polish version

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/text_search_demo/run_native_pl.sh
```

## 5. Image Semantic Demo

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/image_semantic_demo/run_native.sh
```

```bash
conda run --no-capture-output -n pytracker-env \
  jupyter lab tobii-pytracker-demo/examples/image_semantic_demo/analysis/image_semantic_analysis.ipynb
```

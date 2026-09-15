# Native demo testing — v1.6.0

All operator commands after cloning are run from the parent `tobii-pytracker` root.

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

## Run demos

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/test_demo/run_native.sh
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/tobii_ux_ab_demo/run_native.sh
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/tobii_timeseries_noise_demo/run_native.sh
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/tobii_text_search_demo/run_native.sh
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/tobii_image_semantic_demo/run_native.sh
```

## Open analyses

```bash
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/test_demo/analysis/test_demo_analysis.ipynb
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/tobii_ux_ab_demo/analysis/ux_ab_analysis.ipynb
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/tobii_timeseries_noise_demo/analysis/timeseries_analysis.ipynb
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/tobii_text_search_demo/analysis/text_search_analysis.ipynb
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/tobii_image_semantic_demo/analysis/image_semantic_analysis.ipynb
```

Notebook analyses consume real collected `data.csv` only. They never create synthetic replacement data. Missing MouseGaze samples are reported per trial and do not erase valid behavioral responses.

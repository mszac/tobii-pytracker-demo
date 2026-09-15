# Native test iteration protocol — v1.6.0

1. Start from a fresh parent `tobii-pytracker` clone and nested `tobii-pytracker-demo` clone.
2. Create fresh Python 3.10 env and install upstream package, `pyzmq`, `ujson`, `tables==3.9.1`, JupyterLab/ipykernel, then `PsychoPy==2024.1.4 --no-deps`.
3. Run `native_preflight.py --require-iohub`.
4. Run a demo launcher. Collection gates require complete trial/response structure; missing gaze is recorded as a warning.
5. Open the demo's `.ipynb` notebook and analyze the actual `data.csv`. Do not use generated/synthetic fallback data for physical validation.
6. Keep upstream `git status --porcelain` clean.

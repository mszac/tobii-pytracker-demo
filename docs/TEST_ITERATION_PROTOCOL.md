# Test iteration protocol

1. Start from a fresh upstream `tobii-pytracker` checkout and the current `tobii-pytracker-demo` checkout when testing locally, or from a fresh demo checkout when testing with Docker.
2. For local execution, create a fresh Python 3.10 environment and install the upstream package, `pyzmq`, `ujson`, `tables==3.9.1`, JupyterLab/ipykernel, then `PsychoPy==2024.1.4 --no-deps`.
3. Run the compatibility/import preflight before the first local experiment.
4. Run a demo. Collection gates require complete trial/response structure; missing gaze is recorded as a data-quality warning.
5. Open the demo's `.ipynb` notebook and analyze the actual collected `data.csv`. Do not use generated or synthetic fallback data for physical validation.
6. For local execution, keep the upstream checkout clean before and after the run.
7. For Docker execution, record the Docker/Compose version, image build result, VNC interaction, collected output location, and any host-specific display/input issues.

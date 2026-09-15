# Linux native testing — Bash

From the parent `tobii-pytracker` root use the same native launchers as Windows. Install the analysis extras in `pytracker-env`: `pyzmq`, `ujson`, `tables==3.9.1`, `jupyterlab>=4,<5`, `ipykernel>=6,<7`, then the selected upstream-supported PsychoPy version.

Run demos with `bash tobii-pytracker-demo/examples/<demo>/run_native.sh`. Open analyses with `jupyter lab tobii-pytracker-demo/examples/<demo>/analysis/<notebook>.ipynb`. Notebook analyses consume only real collected output.

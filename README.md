# Tobii Pytracker Demo

Version: see [`VERSION`](VERSION).

This repository contains five runnable Tobii Pytracker demos, fixed datasets, collection validators, Jupyter analysis notebooks, and the Docker bridge used with [`sbobek/tobii-pytracker`](https://github.com/sbobek/tobii-pytracker).

## Start here

For the complete local and Docker setup, MouseGaze controls, output locations, and Jupyter workflow, read [`README_TESTING.md`](README_TESTING.md).

For local execution, clone this repository **inside** the original upstream checkout and create the documented Python 3.10 environment. Once that environment is installed, verify the repository payload and upstream/package integration:

```bash
python tobii-pytracker-demo/tools/audit_repository.py

conda run --no-capture-output -n pytracker-env \
  python tobii-pytracker-demo/tools/preflight.py --require-iohub
```

The repository audit uses PyYAML from the installed pytracker environment. Then run a demo with the unified dispatcher:

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/tools/run-demo.sh test_demo
```

Available selections:

```text
test_demo
ux_ab_demo
ux_ab_demo pl
timeseries_noise_demo
text_search_demo
text_search_demo pl
image_semantic_demo
```

The dispatcher only calls the existing public `examples/*/run.sh` or `run_pl.sh` entrypoints; it does not implement a second experiment path.

## Output

Completed sessions are written under `output/`. Generated session data are intentionally ignored by Git; `output/.gitkeep` preserves the directory.

## Repository boundaries

- The upstream `tobii-pytracker` checkout remains authoritative and should stay clean.
- Demo-specific adapters live in this repository; upstream source is not patched at runtime.
- All trials are response-gated: a stimulus remains visible until the participant selects an answer.
- With upstream MouseGaze, hold **RIGHT** while moving the pointer to generate gaze samples, release RIGHT, then use **LEFT click** to answer.
- Missing MouseGaze on an otherwise completed trial is a data-quality warning rather than a behavioral-response failure.

Research documentation is under [`docs/basic_examples/`](docs/basic_examples/). RST sources prepared for upstream ReadTheDocs integration are under [`docs/upstream_rst/`](docs/upstream_rst/).

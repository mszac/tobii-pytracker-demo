# Docker runtime

This layer runs the existing native demo files unchanged. The original
`sbobek/tobii-pytracker` source clone is not edited. Docker applies its mouse
adapter only to the installed `site-packages` copy of `tobii_pytracker`.

## Start

From the `tobii-pytracker-demo` repository root:

```bash
docker compose -f docker/compose.yaml up --build -d
```

Open the PsychoPy desktop through noVNC:

```text
http://localhost:6080/vnc.html?autoconnect=true&resize=scale
```

JupyterLab:

```text
http://localhost:8888/lab
```

## Run demos

```bash
bash docker/run-demo.sh test_demo
bash docker/run-demo.sh ux_ab_demo
bash docker/run-demo.sh ux_ab_demo_pl
bash docker/run-demo.sh timeseries_noise_demo
bash docker/run-demo.sh text_search_demo
bash docker/run-demo.sh text_search_demo_pl
bash docker/run-demo.sh image_semantic_demo
```

The wrapper calls the existing `examples/.../run_native.sh` files. It does not
maintain Docker-specific copies of the experiments.

## MouseGaze controls

The Docker mouse backend preserves the same procedure as native MouseGaze:

- hold RIGHT mouse button while moving the pointer to record gaze;
- release RIGHT;
- LEFT-click a response button.

The experiment changes stimulus only after a response button is clicked.

## Output

The demo repository is bind-mounted into the container. Files written under
`output/` therefore appear directly in the host repository and are available
to the existing Jupyter notebooks.

## Stop

```bash
docker compose -f docker/compose.yaml down
```

## Optional upstream pin

By default Docker builds the current upstream `main`. To reproduce a specific
upstream revision, set `PYTRACKER_UPSTREAM_REF` before building:

```bash
export PYTRACKER_UPSTREAM_REF=<branch-tag-or-commit>
docker compose -f docker/compose.yaml build --no-cache
```

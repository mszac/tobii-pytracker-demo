# Docker runner (upstream `psychopy` branch)

Full setup and experiment instructions are maintained in the repository root [README_TESTING.md](../README_TESTING.md#docker-execution).

This directory contains infrastructure only. Existing demo configs, datasets, runtime adapters, validators, and launchers are reused rather than duplicated for Docker.

The Compose service builds directly from:

`https://github.com/sbobek/tobii-pytracker.git#psychopy`

The local demo repository is bind-mounted at `/app/tobii-pytracker-demo`. A logical `/workspace/tobii-pytracker -> /app` link recreates the repository layout expected by the existing launcher scripts, so Docker executes the same experiment files used by local execution.

## Requirements

- Docker Desktop / Docker Engine with Compose v2
- a VNC client
- network access when the upstream image is built for the first time

No local clone of the upstream `psychopy` branch is required for Docker execution.

## Run

Run commands from the root of `tobii-pytracker-demo`.

```bash
DEMO=test_demo docker compose -f docker/compose.yaml up --build
DEMO=ux_ab_demo docker compose -f docker/compose.yaml up --build
DEMO=timeseries_noise_demo docker compose -f docker/compose.yaml up --build
DEMO=text_search_demo docker compose -f docker/compose.yaml up --build
DEMO=image_semantic_demo docker compose -f docker/compose.yaml up --build
```

Polish text variants:

```bash
DEMO=ux_ab_demo DEMO_LANG=pl docker compose -f docker/compose.yaml up --build
DEMO=text_search_demo DEMO_LANG=pl docker compose -f docker/compose.yaml up --build
```

After the container starts, connect the VNC client to `localhost:5900`.

MouseGaze uses the same interaction contract in every execution environment: hold RIGHT while moving the pointer to generate gaze samples, release RIGHT, then LEFT-click a response button.

Collected sessions are written directly to the repository's `output/` directory on the host.

## Different host VNC port

```bash
VNC_PORT=5901 DEMO=test_demo docker compose -f docker/compose.yaml up --build
```

Then connect the VNC client to `localhost:5901`.

## Stop

```bash
docker compose -f docker/compose.yaml down
```

## Scope

The Docker image and dependency set remain owned by the upstream `psychopy` branch. This repository supplies only the Compose bridge and display/runner bootstrap required to execute the same demo files in that image.

Jupyter notebook analysis remains a post-experiment workflow over the collected host-side session data.

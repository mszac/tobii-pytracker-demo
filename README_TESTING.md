# Pytracker examples test overlay

This package is intended to be committed to the examples repository for iterative validation.

Application/test assets live at repository root (`examples/`, `tools/`, `docs/`). Internal project-development records are isolated under `_project_logs/` and are **not part of the pytracker application/runtime**. Keep `_project_logs/` through development; remove it only during final cleanup after an explicit decision to do so.

Primary current target: native Windows using the unmodified original `sbobek/tobii-pytracker` runtime.

- Windows procedure: `docs/windows/NATIVE_TESTING.md`
- Linux procedure: `docs/linux/NATIVE_TESTING.md` (planned, not yet physically certified)
- Controlled examples: `examples/smoke_text/` and `examples/smoke_images/`
- Upstream refresh helpers: `tools/refresh_original_pytracker.sh` and `.ps1`
- Provenance/import gate: `tools/native_preflight.py`

## Native image smoke demo

`examples/smoke_images/` is the current three-photograph native MouseGaze validation bundle. It presents one HUMAN, one ANIMAL and one OBJECT stimulus, records upstream MouseGaze data, and then exercises pytracker analysis APIs (`DataLoader`, heatmap, fixation, saccade and entropy analysis).

Use the fresh-clone procedure in `docs/windows/NATIVE_TESTING.md`; do not install runtime code from this examples repository.

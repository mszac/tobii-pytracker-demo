# Tobii Pytracker demo — native validation

Repository: `https://github.com/mszac/tobii-pytracker-demo`.

This repository contains example-owned configs, datasets, launchers and analysis code. The original `sbobek/tobii-pytracker` clone is the only runtime/package authority and must remain unmodified during native validation.

Development logs, validation reports and historical patches are distributed in a separate project-logs ZIP and are not committed to this demo repository.

## Required directory layout

The demo repository is cloned **inside** the original upstream clone:

```text
<workspace>/
└── tobii-pytracker/                  # operator working directory after cloning
    └── tobii-pytracker-demo/         # this repository
```

The fresh reset must be started from `<workspace>`, never from inside an existing `tobii-pytracker` clone. After cloning, all test commands are issued from the parent `tobii-pytracker` root. The launchers internally switch their own process to `tobii-pytracker-demo` because config/data/output paths are demo-root-relative.

Current Windows environment candidate: Python 3.10 + `PsychoPy==2024.1.4` + upstream package installed from `tobii-pytracker`. This exact PsychoPy pin is pending physical reconfirmation; the previously tested experiment ran with 2024.2.5 despite pip metadata warnings.

- Windows procedure: `tobii-pytracker-demo/docs/windows/NATIVE_TESTING.md`
- Linux procedure: `tobii-pytracker-demo/docs/linux/NATIVE_TESTING.md` (planned; not physically certified)
- Provenance/import gate: `tobii-pytracker-demo/tools/native_preflight.py`
- Working reference smoke: `tobii-pytracker-demo/examples/smoke_images/`
- Migrated legacy demo: `tobii-pytracker-demo/examples/tobii_ux_ab_demo/`

## Active examples

### Three-image smoke

`examples/smoke_images/` presents three photographs (human / animal / object), records the original upstream MouseGaze stream and provides post-hoc analysis using public `tobii-pytracker` analyzers.

### UX information-placement A/B demo

`examples/tobii_ux_ab_demo/` is a 12-trial text-search workflow reconstructed from the legacy `__previous-examples/1 tobii_ux_ab_demo/README.md` contract and aligned to the working native smoke architecture. It compares answer-relevant information appearing EARLY versus LATE in short interface-style text.

### Native text-search demo

`examples/tobii_text_search_demo/` migrates the supplied legacy `2_tobii_text_search_demo` without patching upstream. It preserves the 12-trial EARLY/LATE information-search task, uses native word AOIs, maps upstream `NONE` to the conceptual `NIE WIEM` response, and validates each completed collection before analysis.

## Refresh helper note

The historical `tools/refresh_original_pytracker.*` helpers are deliberately disabled in the canonical nested layout. Recreating a parent repository from a script stored in its child is unsafe. Use the explicit workspace-level reset in `docs/windows/NATIVE_TESTING.md`.

## Native time-series variability demo

Run from the parent `tobii-pytracker` directory:

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/tobii_timeseries_noise_demo/run_native.sh
```

A successful collection prints `NATIVE_TIMESERIES_BLOCK_PASS` for `machine` and `pv`, followed by `NATIVE_TIMESERIES_COLLECTION_COMPLETE`.


Analyze the newest machine + PV sessions (the analysis will fail if either newest session is incomplete):

```bash
conda run --no-capture-output -n pytracker-env \
  python tobii-pytracker-demo/examples/tobii_timeseries_noise_demo/analysis/analyze_results.py
```
## Native text-search demo

Run from the parent `tobii-pytracker` directory:

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/tobii_text_search_demo/run_native.sh
```

Analyze:

```bash
conda run --no-capture-output -n pytracker-env \
  python tobii-pytracker-demo/examples/tobii_text_search_demo/analysis/analyze_results.py
```

Collection markers: `NATIVE_TEXT_SEARCH_COLLECTION_PASS` and `NATIVE_TEXT_SEARCH_COLLECTION_COMPLETE`. Analysis marker: `NATIVE_TEXT_SEARCH_ANALYSIS_PASS`.

# Tobii Pytracker demo — native validation

Repository: `https://github.com/mszac/tobii-pytracker-demo`.

This repository contains example-owned configs, datasets, launchers and analysis code. The original `sbobek/tobii-pytracker` clone remains the only runtime/package authority and must stay unmodified during the native reference workflow.

Development logs, validation reports and historical patches are distributed in a **separate project-logs ZIP** and are not committed to this demo repository.

Primary current target: native Windows 11. Docker/WSL are not used for this path.

- Windows procedure: `docs/windows/NATIVE_TESTING.md`
- Linux procedure: `docs/linux/NATIVE_TESTING.md` (planned; not physically certified yet)
- Provenance/import gate: `tools/native_preflight.py`
- Working reference smoke: `examples/smoke_images/`
- Migrated legacy demo: `examples/tobii_ux_ab_demo/`

## Current native examples

### Three-image smoke

`examples/smoke_images/` presents three photographs (human / animal / object), records the original upstream MouseGaze stream and provides post-hoc analysis using public `tobii-pytracker` analyzers.

### UX information-placement A/B demo

`examples/tobii_ux_ab_demo/` is a 12-trial text-search workflow reconstructed from the legacy `__previous-examples/1 tobii_ux_ab_demo/README.md` contract and aligned to the working native smoke architecture. It compares answer-relevant information appearing EARLY versus LATE in short interface-style text. The bundled analysis produces trial metrics, condition summaries and example gaze visualizations.

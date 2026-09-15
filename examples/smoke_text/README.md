# Text smoke demo

This older controlled text fixture remains available for regression work. The current three-image reference example is `test_demo`.

The demo repository must be nested inside a clean original upstream clone:

```text
<workspace>/
└── tobii-pytracker/                  # operator cwd
    └── tobii-pytracker-demo/
```

Install `tobii-pytracker` only from the original clone. Keep the operator shell in `tobii-pytracker`; if this fixture is used manually, the CLI process must run with the demo root as its working directory because config/output paths are demo-root-relative. See the root `README_TESTING.md` for the authoritative current workflow.

MouseGaze uses the original upstream control contract: hold the **RIGHT mouse button** while moving to produce gaze samples; release RIGHT before LEFT CLICK because upstream MouseGaze also maps simultaneous LEFT+RIGHT to blink.

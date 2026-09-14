# Linux native testing

Linux/WSL physical validation is deferred. Bash-only reference layout. Start the reset from the workspace directory and, after cloning, keep the shell in the original `tobii-pytracker` root:

```bash
mkdir -p ~/pytracker-test
cd ~/pytracker-test
rm -rf tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
pwd
test -f tobii-pytracker-demo/examples/smoke_images/run_native.sh && echo "SMOKE_RUNNER_OK"
test -f tobii-pytracker-demo/examples/tobii_ux_ab_demo/run_native.sh && echo "UX_AB_RUNNER_OK"
```

Reference invariants: Python 3.10; install the package only from the current original clone (`pip install .`); never install the demo repo; invoke demo scripts through `tobii-pytracker-demo/...`; launchers may internally switch to the demo root because config/data/output paths are demo-root-relative. Linux/WSL dependency closure remains pending physical validation.

### Time-series variability demo

From the parent `tobii-pytracker` root:

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/tobii_timeseries_noise_demo/run_native.sh
```

A successful collection prints `NATIVE_TIMESERIES_BLOCK_PASS` for `machine` and `pv`, followed by `NATIVE_TIMESERIES_COLLECTION_COMPLETE`.


Analyze the newest machine + PV sessions:

```bash
conda run --no-capture-output -n pytracker-env \
  python tobii-pytracker-demo/examples/tobii_timeseries_noise_demo/analysis/analyze_results.py
```

### Native text-search demo

From the parent `tobii-pytracker` root:

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/tobii_text_search_demo/run_native.sh

conda run --no-capture-output -n pytracker-env \
  python tobii-pytracker-demo/examples/tobii_text_search_demo/analysis/analyze_results.py
```

Linux/WSL physical execution remains uncertified.

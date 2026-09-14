# Test iteration protocol

Every native iteration starts from fresh repositories. The reset is always executed from the **workspace directory**, not from inside an old `tobii-pytracker` clone.

Canonical layout:

```text
<workspace>/
└── tobii-pytracker/                  # original sbobek upstream; operator cwd
    └── tobii-pytracker-demo/         # mszac demo repository (main)
```

Canonical Git Bash reset (replace `/d/pytracker` if your workspace differs):

```bash
cd /d/pytracker
rm -rf tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
```

Immediately verify the layout while still in `tobii-pytracker`:

```bash
pwd
test -f tobii-pytracker-demo/examples/smoke_images/run_native.sh && echo "SMOKE_RUNNER_OK"
test -f tobii-pytracker-demo/examples/tobii_ux_ab_demo/run_native.sh && echo "UX_AB_RUNNER_OK"
```

Expected `pwd` ends in `/tobii-pytracker`. Both `*_RUNNER_OK` markers must appear before environment setup.

From this point keep the user's shell in `tobii-pytracker`. Create the Python 3.10 environment, install the original package with `pip install .`, run `tobii-pytracker-demo/tools/native_preflight.py`, invoke launchers via `tobii-pytracker-demo/examples/...`, validate output/analysis, and finish with `git status --porcelain` on the upstream clone.

Launchers may change their own process working directory to the nested demo root because current configs intentionally use demo-root-relative dataset/output paths. This does not change the operator-cwd rule.

Git Bash note: moving one directory up is `cd ..` (with a space). `cd..` is not a Bash command.

### Time-series variability demo

From the parent `tobii-pytracker` root:

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/tobii_timeseries_noise_demo/run_native.sh

conda run --no-capture-output -n pytracker-env \
  python tobii-pytracker-demo/examples/tobii_timeseries_noise_demo/analysis/analyze_results.py
```


## Text-search regression gate

When validating the migrated text-search example, run it only after N1R passes and require the collection markers before post-hoc analysis. The upstream tree must remain clean.

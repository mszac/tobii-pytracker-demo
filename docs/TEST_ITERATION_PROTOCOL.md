# Test iteration protocol

Every native iteration starts from fresh repositories. Canonical layout:

```text
<workspace>/
└── tobii-pytracker/                  # original sbobek upstream; operator cwd
    └── tobii-pytracker-demo/         # mszac demo repository (main)
```

Canonical Git Bash reset:

```bash
cd /c/work/pytracker-test
rm -rf tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
```

From this point, keep the user's shell in `tobii-pytracker`. Create the Python 3.10 environment, install the original package with `pip install .`, run `tobii-pytracker-demo/tools/native_preflight.py`, invoke selected launchers via `tobii-pytracker-demo/examples/...`, validate output/analysis, and finish with `git status --porcelain` on the upstream clone.

Launchers are allowed to change their own process working directory to the nested demo root because the current example configs intentionally use demo-root-relative dataset/output paths. This internal behavior does not change the operator-cwd rule.

The demo repository is an asset/experiment repository only; it is never installed as the `tobii-pytracker` runtime.

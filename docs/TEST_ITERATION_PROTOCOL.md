# Test iteration protocol

Every native iteration starts from fresh repositories. Canonical layout:

```text
<workspace>/
└── tobii-pytracker/                  # original sbobek upstream
    └── tobii-pytracker-demo/              # mszac demo repository (main)
```

Canonical Git Bash reset:

```bash
cd /c/work/pytracker-test
rm -rf tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
cd tobii-pytracker-demo
```

Then create a fresh Python 3.10 environment, install the original package from `..`, run `tools/native_preflight.py`, execute the selected example, validate its output and analysis, and confirm `git -C .. status --porcelain` remains empty.

The demo repository is an asset/experiment repository only; it is never installed as the `tobii-pytracker` runtime.

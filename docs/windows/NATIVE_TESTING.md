# Windows native testing

Primary target: Windows 11, original upstream runtime, demo repository cloned **inside** the upstream clone. Docker/WSL are not used here. After the fresh clone, every operator command is issued from the root of `tobii-pytracker`. Git Bash commands are authoritative for the current physical tests; PowerShell equivalents are included for the final documentation path.

The demo launchers internally switch their own process to `tobii-pytracker-demo` because example config/data/output paths are demo-root-relative. The user's shell stays at the upstream root.

## 1. Fresh clones — important directory rule

Do **not** run the cleanup block while already inside an existing `tobii-pytracker`. First go to the workspace directory. For the current test machine this is `/d/pytracker`.

### Git Bash

```bash
cd /d/pytracker
rm -rf tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
```

Now stay in `tobii-pytracker` and validate the layout:

```bash
pwd
test -f tobii-pytracker-demo/examples/smoke_images/run_native.sh && echo "SMOKE_RUNNER_OK"
test -f tobii-pytracker-demo/examples/tobii_ux_ab_demo/run_native.sh && echo "UX_AB_RUNNER_OK"
```

Expected:

```text
.../tobii-pytracker
SMOKE_RUNNER_OK
UX_AB_RUNNER_OK
```

If `pwd` ends with `tobii-pytracker/tobii-pytracker`, the upstream repo was cloned inside itself. Return to the workspace with `cd /d/pytracker` and repeat the reset. In Git Bash the relative command is `cd ..`, not `cd..`.

### PowerShell

```powershell
Set-Location D:\pytracker
if (Test-Path .\tobii-pytracker) { Remove-Item .\tobii-pytracker -Recurse -Force }
git clone https://github.com/sbobek/tobii-pytracker.git
Set-Location .\tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
```

Record provenance while still in `tobii-pytracker`:

### Git Bash
```bash
git remote get-url origin
git rev-parse HEAD
git -C tobii-pytracker-demo remote get-url origin
git -C tobii-pytracker-demo rev-parse HEAD
```

### PowerShell
```powershell
git remote get-url origin
git rev-parse HEAD
git -C tobii-pytracker-demo remote get-url origin
git -C tobii-pytracker-demo rev-parse HEAD
```

## 2. Fresh Python 3.10 environment

Reference candidate for the next physical test: `PsychoPy==2024.1.4`. It is the minimum version documented by upstream and avoids the concrete `setuptools==70.3.0` metadata conflict reported by PsychoPy 2024.2.5 against current upstream `setuptools<=66.1.1`. The exact 2024.1.4 combination is not yet marked runtime PASS.

Install `pyzmq` and `ujson` before the `--no-deps` PsychoPy install. Keep these commands on one line each in Git Bash.

### Git Bash
```bash
conda env remove -n pytracker-env -y || true
conda create -n pytracker-env python=3.10 -y
conda run -n pytracker-env python -m pip install --upgrade pip
conda run -n pytracker-env python -m pip install .
conda run -n pytracker-env python -m pip install 'pyzmq>=22.2.1' ujson
conda run -n pytracker-env python -m pip install 'psychopy==2024.1.4' --no-deps
```

### PowerShell
```powershell
conda env remove -n pytracker-env -y
conda create -n pytracker-env python=3.10 -y
conda run -n pytracker-env python -m pip install --upgrade pip
conda run -n pytracker-env python -m pip install .
conda run -n pytracker-env python -m pip install "pyzmq>=22.2.1" ujson
conda run -n pytracker-env python -m pip install "psychopy==2024.1.4" --no-deps
```

Do not install `tobii-pytracker-demo` as a Python package.

Optional version check:

```bash
conda run -n pytracker-env python -c "import psychopy, setuptools, pyglet; print('PsychoPy:', psychopy.__version__); print('setuptools:', setuptools.__version__); print('pyglet:', pyglet.version)"
```

## 3. Provenance preflight

### Git Bash
```bash
conda run --no-capture-output -n pytracker-env python tobii-pytracker-demo/tools/native_preflight.py --require-iohub
```

### PowerShell
```powershell
conda run --no-capture-output -n pytracker-env python tobii-pytracker-demo\tools\native_preflight.py --require-iohub
```

Required result: `N1R_PACKAGE_PROVENANCE_PASS`.

## 4. Three-image MouseGaze demo

### Git Bash
```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/smoke_images/run_native.sh
```

If `conda run ... bash` is unavailable:

```bash
conda activate pytracker-env
bash tobii-pytracker-demo/examples/smoke_images/run_native.sh
```

### PowerShell
```powershell
Push-Location .\tobii-pytracker-demo; conda run --no-capture-output -n pytracker-env tobii-pytracker --config_file examples\smoke_images\config.native.yaml --eyetracker_config_file ..\configs\mouse_eyetracker_config.yaml --enable_eyetracker --loop_count 3; Pop-Location
```

During each image: hold RIGHT mouse button while moving to generate gaze; release RIGHT before LEFT CLICK; click HUMAN/ANIMAL/OBJECT. After the third trial the outro appears; press ESC to close.

## 5. Analyze newest image output

### Git Bash
```bash
conda run --no-capture-output -n pytracker-env python tobii-pytracker-demo/examples/smoke_images/analysis/analyze_output.py --output-root tobii-pytracker-demo/output
```

### PowerShell
```powershell
conda run --no-capture-output -n pytracker-env python tobii-pytracker-demo\examples\smoke_images\analysis\analyze_output.py --output-root tobii-pytracker-demo\output
```

Expected marker: `NATIVE_IMAGE_ANALYSIS_PASS`. Results are written to `tobii-pytracker-demo/output/<session>/analysis_image_demo/`.

## 6. UX A/B text-search demo

Run only after the image smoke proves the environment.

### Git Bash
```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/tobii_ux_ab_demo/run_native.sh
```

### PowerShell
```powershell
Push-Location .\tobii-pytracker-demo; conda run --no-capture-output -n pytracker-env tobii-pytracker --config_file examples\tobii_ux_ab_demo\config.native.yaml --eyetracker_config_file ..\configs\mouse_eyetracker_config.yaml --enable_eyetracker --loop_count 12; Pop-Location
```

Hold RIGHT while moving to generate gaze, release RIGHT, then LEFT CLICK TAK or NIE. Do not select the upstream-added NONE button.

Analyze completed UX sessions:

### Git Bash
```bash
conda run --no-capture-output -n pytracker-env python tobii-pytracker-demo/examples/tobii_ux_ab_demo/analysis/analyze_results.py
```

### PowerShell
```powershell
conda run --no-capture-output -n pytracker-env python tobii-pytracker-demo\examples\tobii_ux_ab_demo\analysis\analyze_results.py
```

Expected marker: `NATIVE_UX_AB_ANALYSIS_PASS`.

## 7. Native text-search demo

### Git Bash
```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/tobii_text_search_demo/run_native.sh
```

Use RIGHT+move for MouseGaze, release RIGHT, then LEFT CLICK `TAK`, `NIE`, or `NONE` (`NONE` = `NIE WIEM`).

Analyze:

```bash
conda run --no-capture-output -n pytracker-env python tobii-pytracker-demo/examples/tobii_text_search_demo/analysis/analyze_results.py
```

Expected markers: `NATIVE_TEXT_SEARCH_COLLECTION_PASS`, `NATIVE_TEXT_SEARCH_COLLECTION_COMPLETE`, `NATIVE_TEXT_SEARCH_ANALYSIS_PASS`.

## 8. Final upstream-clean check

Still from `tobii-pytracker`:

```bash
git status --porcelain
```

It must remain empty.

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

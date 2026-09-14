# Windows native testing

Primary target: Windows 11, original upstream runtime, demo repository cloned **inside** the upstream clone. Docker/WSL are not used here. All operator commands after cloning are issued from the root of `tobii-pytracker`. Git Bash commands are shown first; equivalent PowerShell commands are also provided.

The demo launchers may internally switch to `tobii-pytracker-demo` because example config/data/output paths are demo-root-relative. The user's shell remains at the upstream root.

## 1. Fresh clones

### Git Bash

```bash
cd /c/work/pytracker-test
rm -rf tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
```

### PowerShell

```powershell
Set-Location C:\work\pytracker-test
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

Reference native pin for the next physical test: `PsychoPy==2024.1.4`. It is the minimum version documented by upstream. Install `pyzmq`/`ujson` before the `--no-deps` PsychoPy install so the successful package installs are not obscured by the known incomplete PsychoPy dependency set.

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
Run from `tobii-pytracker`; the one-liner temporarily enters the demo directory only for the upstream CLI process:

```powershell
Push-Location .\tobii-pytracker-demo; conda run --no-capture-output -n pytracker-env tobii-pytracker --config_file examples\smoke_images\config.native.yaml --eyetracker_config_file ..\configs\mouse_eyetracker_config.yaml --enable_eyetracker --loop_count 3; Pop-Location
```

During each image: hold RIGHT mouse button while moving to generate gaze; release RIGHT before LEFT CLICK; click the correct HUMAN/ANIMAL/OBJECT category. After the third trial the outro appears; press ESC to close.

## 5. Analyze newest image output

### Git Bash
```bash
conda run --no-capture-output -n pytracker-env python tobii-pytracker-demo/examples/smoke_images/analysis/analyze_output.py --output-root tobii-pytracker-demo/output
```

### PowerShell
```powershell
conda run --no-capture-output -n pytracker-env python tobii-pytracker-demo\examples\smoke_images\analysis\analyze_output.py --output-root tobii-pytracker-demo\output
```

Expected terminal marker: `NATIVE_IMAGE_ANALYSIS_PASS`. Results are written to `tobii-pytracker-demo/output/<session>/analysis_image_demo/`.

## 6. UX A/B text-search demo

After the image smoke has proven the environment:

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

Expected marker: `NATIVE_UX_AB_ANALYSIS_PASS`. Generated reports are under `tobii-pytracker-demo/examples/tobii_ux_ab_demo/results/`.

## 7. Final upstream-clean check

Still from `tobii-pytracker`:

```bash
git status --porcelain
```

It must remain empty.

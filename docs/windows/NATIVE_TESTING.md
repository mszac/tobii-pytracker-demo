# Windows native testing

Primary target: Windows 11, original upstream runtime, demo repository cloned **inside** the upstream clone. Docker/WSL are not used here. Git Bash commands are shown first; equivalent PowerShell commands are also provided.

## 1. Fresh clones

### Git Bash

```bash
cd /c/work/pytracker-test
rm -rf tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
cd tobii-pytracker-demo
```

### PowerShell

```powershell
Set-Location C:\work\pytracker-test
if (Test-Path .\tobii-pytracker) { Remove-Item .\tobii-pytracker -Recurse -Force }
git clone https://github.com/sbobek/tobii-pytracker.git
Set-Location .\tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
Set-Location .\tobii-pytracker-demo
```

Record provenance:

### Git Bash
```bash
git -C .. remote get-url origin
git -C .. rev-parse HEAD
git remote get-url origin
git rev-parse HEAD
```

### PowerShell
```powershell
git -C .. remote get-url origin
git -C .. rev-parse HEAD
git remote get-url origin
git rev-parse HEAD
```

## 2. Fresh Python 3.10 environment

### Git Bash
```bash
conda env remove -n pytracker-env -y || true
conda create -n pytracker-env python=3.10 -y
conda run -n pytracker-env python -m pip install --upgrade pip
conda run -n pytracker-env python -m pip install ..
conda run -n pytracker-env python -m pip install 'psychopy>=2024.1.4,<2025.1.0' --no-deps
conda run -n pytracker-env python -m pip install 'pyzmq>=22.2.1' ujson
```

### PowerShell
```powershell
conda env remove -n pytracker-env -y
conda create -n pytracker-env python=3.10 -y
conda run -n pytracker-env python -m pip install --upgrade pip
conda run -n pytracker-env python -m pip install ..
conda run -n pytracker-env python -m pip install "psychopy>=2024.1.4,<2025.1.0" --no-deps
conda run -n pytracker-env python -m pip install "pyzmq>=22.2.1" ujson
```

Do not run `pip install .` from `tobii-pytracker-demo`; install only the parent original upstream clone.

## 3. Provenance preflight

### Git Bash
```bash
conda run --no-capture-output -n pytracker-env python tools/native_preflight.py --require-iohub
```

### PowerShell
```powershell
conda run --no-capture-output -n pytracker-env python tools\native_preflight.py --require-iohub
```

Required result: `N1R_PACKAGE_PROVENANCE_PASS`.

## 4. Three-image MouseGaze demo

### Git Bash
```bash
conda run --no-capture-output -n pytracker-env bash examples/smoke_images/run_native.sh
```

If `conda run ... bash` is unavailable, activate the environment first and run:

```bash
conda activate pytracker-env
bash examples/smoke_images/run_native.sh
```

### PowerShell
```powershell
conda run --no-capture-output -n pytracker-env tobii-pytracker `
  --config_file examples/smoke_images/config.native.yaml `
  --eyetracker_config_file ..\configs\mouse_eyetracker_config.yaml `
  --enable_eyetracker `
  --loop_count 3
```

During each image: hold RIGHT mouse button while moving to generate gaze; release RIGHT before LEFT CLICK; click the correct HUMAN/ANIMAL/OBJECT category. After the third trial the outro appears; press ESC to close.

## 5. Analyze newest output

### Git Bash
```bash
conda run --no-capture-output -n pytracker-env python examples/smoke_images/analysis/analyze_output.py --output-root output
```

### PowerShell
```powershell
conda run --no-capture-output -n pytracker-env python examples\smoke_images\analysis\analyze_output.py --output-root output
```

Expected terminal marker: `NATIVE_IMAGE_ANALYSIS_PASS`. Results are written to `output/<session>/analysis_image_demo/`.

Optional notebook:

```bash
conda run -n pytracker-env python -m pip install jupyterlab
conda run --no-capture-output -n pytracker-env jupyter lab
```

Open `examples/smoke_images/analysis/image_analysis_demo.ipynb`.

## 6. Final upstream-clean check

```bash
git -C .. status --porcelain
```

It must remain empty.


## 7. UX A/B text-search demo

After the image smoke has proven the environment, run the migrated 12-trial legacy demo:

### Git Bash
```bash
conda run --no-capture-output -n pytracker-env bash examples/tobii_ux_ab_demo/run_native.sh
```

### PowerShell
```powershell
conda run --no-capture-output -n pytracker-env tobii-pytracker `
  --config_file examples\tobii_ux_ab_demo\config.native.yaml `
  --eyetracker_config_file ..\configs\mouse_eyetracker_config.yaml `
  --enable_eyetracker `
  --loop_count 12
```

Hold RIGHT while moving to generate gaze, release RIGHT, then LEFT CLICK TAK or NIE. Do not select the upstream-added NONE button.

Analyze completed UX sessions:

### Git Bash
```bash
conda run --no-capture-output -n pytracker-env python examples/tobii_ux_ab_demo/analysis/analyze_results.py
```

### PowerShell
```powershell
conda run --no-capture-output -n pytracker-env python examples\tobii_ux_ab_demo\analysis\analyze_results.py
```

Expected marker: `NATIVE_UX_AB_ANALYSIS_PASS`. Generated reports are under `examples/tobii_ux_ab_demo/results/`.

#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path("/workspace/tobii-pytracker")
DEMO = ROOT / "tobii-pytracker-demo"
EXPECTED = [
    "test_demo",
    "ux_ab_demo",
    "timeseries_noise_demo",
    "text_search_demo",
    "image_semantic_demo",
]
MARKER = "PYTRACKER_DOCKER_DIRECT_MOUSE_BACKEND_V1"


def fail(message: str) -> None:
    raise SystemExit(f"DOCKER_RUNTIME_ERROR: {message}")


def main() -> int:
    if ROOT.name != "tobii-pytracker" or not (ROOT / ".git").is_dir():
        fail(f"missing original upstream clone at {ROOT}")
    if not DEMO.is_dir():
        fail(f"demo repository is not mounted at {DEMO}")
    for name in EXPECTED:
        launcher = DEMO / "examples" / name / "run_native.sh"
        if not launcher.is_file():
            fail(f"missing unchanged demo launcher: {launcher}")

    status = subprocess.check_output(
        ["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=no"],
        text=True,
    ).strip()
    if status:
        fail("upstream source clone is modified")

    spec = importlib.util.find_spec("tobii_pytracker.utils.eyetracker")
    if spec is None or not spec.origin:
        fail("installed tobii_pytracker package not found")
    installed = Path(spec.origin).resolve()
    if str(installed).startswith(str(ROOT / "src")):
        fail("Python resolves tobii_pytracker from source clone instead of site-packages")
    text = installed.read_text(encoding="utf-8")
    if MARKER not in text:
        fail("Docker direct-mouse overlay missing from installed package")

    if os.environ.get("PYTRACKER_DOCKER_DIRECT_MOUSE") != "1":
        fail("PYTRACKER_DOCKER_DIRECT_MOUSE must be 1")

    print(f"DOCKER_RUNTIME_PASS upstream={ROOT} demo={DEMO} installed={installed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

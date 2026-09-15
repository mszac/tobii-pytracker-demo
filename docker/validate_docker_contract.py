#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
COMPOSE = ROOT / "docker" / "compose.yaml"
RUNNER = ROOT / "docker" / "run-demo.sh"
EXPECTED = {
    "test_demo": ["run.sh"],
    "ux_ab_demo": ["run.sh", "run_pl.sh"],
    "timeseries_noise_demo": ["run.sh"],
    "text_search_demo": ["run.sh", "run_pl.sh"],
    "image_semantic_demo": ["run.sh"],
}


def fail(message: str) -> None:
    raise RuntimeError(message)


def main() -> int:
    data = yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))
    service = data["services"]["demo"]
    build = service["build"]
    if build["context"] != "https://github.com/sbobek/tobii-pytracker.git#psychopy":
        fail("Compose must build directly from upstream psychopy branch")
    if build.get("dockerfile") != "Dockerfile":
        fail("Compose must use upstream Dockerfile")
    if service.get("working_dir") != "/app/tobii-pytracker-demo":
        fail("Unexpected container demo working directory")

    volumes = service.get("volumes", [])
    if volumes != ["..:/app/tobii-pytracker-demo:rw"]:
        fail("Expected one writable demo-repository bind mount")

    command = service.get("command", [])
    if "/app/tobii-pytracker-demo/docker/run-demo.sh" not in command:
        fail("Docker bootstrap is not configured")

    text = RUNNER.read_text(encoding="utf-8")
    for demo, runners in EXPECTED.items():
        for filename in runners:
            path = ROOT / "examples" / demo / filename
            if not path.is_file():
                fail(f"Missing existing demo runner: {path.relative_to(ROOT)}")
        if demo not in text:
            fail(f"Docker dispatcher does not reference {demo}")

    if "bash \"tobii-pytracker-demo/$RUNNER\"" not in text:
        fail("Docker bootstrap must dispatch the documented public runner")
    if "ln -s \"$UPSTREAM_ROOT\" \"$LOGICAL_UPSTREAM\"" not in text:
        fail("Repository-compatible logical upstream path is missing")

    print("DOCKER_DEMO_CONTRACT_PASS")
    print("upstream=https://github.com/sbobek/tobii-pytracker.git#psychopy")
    print("active_demos=5")
    print("public_runners=reused")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"DOCKER_DEMO_CONTRACT_FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)

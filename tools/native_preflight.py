from __future__ import annotations

import argparse
import importlib.metadata as metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.parse import unquote

EXPECTED_UPSTREAM_URL_FRAGMENT = "sbobek/tobii-pytracker"
EXPECTED_DEMO_URL_FRAGMENT = "mszac/tobii-pytracker-demo"


def run_git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout.strip()


def normalize_url(value: str) -> str:
    return value.replace("\\", "/").lower()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate native pytracker provenance and imports.")
    parser.add_argument("--require-iohub", action="store_true", help="Fail when PsychoPy ioHub cannot be imported (use before N4-A).")
    args = parser.parse_args()

    demo_root = Path(__file__).resolve().parents[1]
    # Supported test layout: demo repo cloned inside the original upstream repo.
    # Legacy sibling layout is still accepted for convenience.
    parent = demo_root.parent
    if parent.name == "tobii-pytracker" and (parent / "pyproject.toml").is_file():
        upstream_root = parent
        workspace_root = parent.parent
    else:
        workspace_root = parent
        upstream_root = workspace_root / "tobii-pytracker"
    smoke_config = demo_root / "examples" / "smoke_text" / "config.native.yaml"
    smoke_data = demo_root / "examples" / "smoke_text" / "data" / "demo_text.csv"

    failures: list[str] = []
    notes: list[str] = []

    if sys.version_info[:2] != (3, 10):
        failures.append(f"Python must be 3.10.x, got {sys.version.split()[0]}")

    if not upstream_root.is_dir():
        failures.append(f"Missing sibling original upstream clone: {upstream_root}")
    if not smoke_config.is_file():
        failures.append(f"Missing smoke config: {smoke_config}")
    if not smoke_data.is_file():
        failures.append(f"Missing smoke dataset: {smoke_data}")

    try:
        demo_origin = run_git(demo_root, "remote", "get-url", "origin")
        demo_sha = run_git(demo_root, "rev-parse", "HEAD")
        if EXPECTED_DEMO_URL_FRAGMENT not in normalize_url(demo_origin):
            notes.append(f"Demo origin differs from expected public repo: {demo_origin}")
    except Exception as exc:
        failures.append(f"Cannot read demo Git provenance: {exc}")
        demo_origin = "<unavailable>"
        demo_sha = "<unavailable>"

    if upstream_root.is_dir():
        try:
            upstream_origin = run_git(upstream_root, "remote", "get-url", "origin")
            upstream_sha = run_git(upstream_root, "rev-parse", "HEAD")
            upstream_dirty = run_git(upstream_root, "status", "--porcelain")
            if EXPECTED_UPSTREAM_URL_FRAGMENT not in normalize_url(upstream_origin):
                failures.append(f"Unexpected upstream origin: {upstream_origin}")
            if upstream_dirty:
                failures.append("Original upstream working tree is not clean")
        except Exception as exc:
            failures.append(f"Cannot read upstream Git provenance: {exc}")
            upstream_origin = "<unavailable>"
            upstream_sha = "<unavailable>"
    else:
        upstream_origin = "<missing>"
        upstream_sha = "<missing>"

    try:
        dist = metadata.distribution("tobii-pytracker")
        dist_version = dist.version
        direct_url_text = dist.read_text("direct_url.json")
        direct_url = json.loads(direct_url_text) if direct_url_text else None
        if direct_url:
            source_url = str(direct_url.get("url", ""))
            normalized_source = normalize_url(unquote(source_url))
            if normalize_url(str(demo_root)) in normalized_source:
                failures.append("Installed tobii-pytracker points to the demo repository")
            if normalize_url(str(upstream_root)) not in normalized_source:
                notes.append(f"Installed package direct_url does not point to sibling upstream clone: {source_url}")
        else:
            notes.append("Installed distribution has no direct_url.json; source provenance cannot be proven from wheel metadata")
    except metadata.PackageNotFoundError:
        failures.append("tobii-pytracker distribution is not installed in this environment")
        dist_version = "<not installed>"
        direct_url = None

    try:
        import tobii_pytracker  # type: ignore

        module_path = Path(tobii_pytracker.__file__).resolve()
        if demo_root in module_path.parents:
            failures.append(f"tobii_pytracker imported from demo repository: {module_path}")
    except Exception as exc:
        failures.append(f"Cannot import tobii_pytracker: {exc}")
        module_path = Path("<unavailable>")

    psychopy_gui_status = "OK"
    try:
        import psychopy  # noqa: F401
        from psychopy import event, visual  # noqa: F401
    except Exception as exc:
        psychopy_gui_status = f"FAIL: {exc}"
        failures.append(f"PsychoPy GUI import preflight failed: {exc}")

    psychopy_iohub_status = "OK"
    try:
        import psychopy.iohub  # noqa: F401
    except Exception as exc:
        psychopy_iohub_status = f"FAIL: {exc}"
        if args.require_iohub:
            failures.append(f"PsychoPy ioHub import preflight failed: {exc}")
        else:
            notes.append(f"ioHub is not ready yet (allowed before N3-A): {exc}")

    cli_path = shutil.which("tobii-pytracker")
    if not cli_path:
        failures.append("tobii-pytracker CLI is not on PATH")

    print("NATIVE_PREFLIGHT")
    print(f"python={sys.version.split()[0]}")
    print(f"demo_root={demo_root}")
    print(f"demo_origin={demo_origin}")
    print(f"demo_commit={demo_sha}")
    print(f"upstream_root={upstream_root}")
    print(f"upstream_origin={upstream_origin}")
    print(f"upstream_commit={upstream_sha}")
    print(f"distribution_version={dist_version}")
    print(f"module_path={module_path}")
    print(f"cli_path={cli_path or '<missing>'}")
    print(f"psychopy_gui={psychopy_gui_status}")
    print(f"psychopy_iohub={psychopy_iohub_status}")
    for note in notes:
        print(f"NOTE: {note}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("N1R_PACKAGE_PROVENANCE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

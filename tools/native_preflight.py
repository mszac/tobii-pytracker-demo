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
    image_runner = demo_root / "examples" / "smoke_images" / "run_native.sh"
    ux_runner = demo_root / "examples" / "tobii_ux_ab_demo" / "run_native.sh"
    timeseries_runner = demo_root / "examples" / "tobii_timeseries_noise_demo" / "run_native.sh"
    timeseries_validator = demo_root / "examples" / "tobii_timeseries_noise_demo" / "validate_collection.py"
    timeseries_machine = demo_root / "examples" / "tobii_timeseries_noise_demo" / "data" / "machine_vibration.csv"
    timeseries_pv = demo_root / "examples" / "tobii_timeseries_noise_demo" / "data" / "pv_power.csv"
    text_search_runner = demo_root / "examples" / "tobii_text_search_demo" / "run_native.sh"
    text_search_validator = demo_root / "examples" / "tobii_text_search_demo" / "validate_collection.py"
    text_search_dataset = demo_root / "examples" / "tobii_text_search_demo" / "data" / "text_search.csv"
    response_gate_validator = demo_root / "tools" / "validate_response_gated_native.py"
    image_semantic_runner = demo_root / "examples" / "tobii_image_semantic_demo" / "run_native.sh"

    failures: list[str] = []
    notes: list[str] = []

    if sys.version_info[:2] != (3, 10):
        failures.append(f"Python must be 3.10.x, got {sys.version.split()[0]}")

    if not upstream_root.is_dir():
        failures.append(f"Missing parent original upstream clone: {upstream_root}")
    elif upstream_root.parent.name == "tobii-pytracker" and (upstream_root.parent / ".git").exists():
        failures.append(
            "Nested duplicate upstream clone detected: expected <workspace>/tobii-pytracker/"
            "tobii-pytracker-demo, not .../tobii-pytracker/tobii-pytracker/..."
        )
    if not image_runner.is_file():
        failures.append(f"Missing image smoke runner: {image_runner}")
    if not ux_runner.is_file():
        failures.append(f"Missing UX A/B runner: {ux_runner}")
    if not timeseries_runner.is_file():
        failures.append(f"Missing time-series runner: {timeseries_runner}")
    if not timeseries_validator.is_file():
        failures.append(f"Missing time-series collection validator: {timeseries_validator}")
    if not timeseries_machine.is_file():
        failures.append(f"Missing machine time-series dataset: {timeseries_machine}")
    if not timeseries_pv.is_file():
        failures.append(f"Missing PV time-series dataset: {timeseries_pv}")
    if not text_search_runner.is_file():
        failures.append(f"Missing text-search runner: {text_search_runner}")
    if not text_search_validator.is_file():
        failures.append(f"Missing text-search collection validator: {text_search_validator}")
    if not text_search_dataset.is_file():
        failures.append(f"Missing text-search dataset: {text_search_dataset}")
    if not image_semantic_runner.is_file():
        failures.append(f"Missing image-semantic runner: {image_semantic_runner}")
    if not response_gate_validator.is_file():
        failures.append(f"Missing native response-gate validator: {response_gate_validator}")
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

    if response_gate_validator.is_file() and upstream_root.is_dir():
        response_gate_proc = subprocess.run(
            [sys.executable, str(response_gate_validator), "--upstream-root", str(upstream_root)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        response_gate_output = response_gate_proc.stdout.strip()
        if response_gate_proc.returncode != 0:
            failures.append(f"Native response-gated trial contract failed: {response_gate_output}")
    else:
        response_gate_output = "<not checked>"

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
                notes.append(f"Installed package direct_url does not point to parent upstream clone: {source_url}")
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

    try:
        psychopy_version = metadata.version("psychopy")
    except metadata.PackageNotFoundError:
        psychopy_version = "<not installed>"
    try:
        setuptools_version = metadata.version("setuptools")
    except metadata.PackageNotFoundError:
        setuptools_version = "<not installed>"

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
    print(f"psychopy_version={psychopy_version}")
    print(f"setuptools_version={setuptools_version}")
    print(f"module_path={module_path}")
    print(f"cli_path={cli_path or '<missing>'}")
    print(f"psychopy_gui={psychopy_gui_status}")
    print(f"psychopy_iohub={psychopy_iohub_status}")
    print(f"response_gate={response_gate_output}")
    if psychopy_version != "2024.1.4":
        print(f"NOTE: current native candidate is PsychoPy 2024.1.4; installed={psychopy_version}")
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

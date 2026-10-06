from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

try:
    import yaml
except Exception as exc:  # pragma: no cover - setup diagnostic
    print(f"REPOSITORY_AUDIT_FAIL missing PyYAML: {exc}")
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "1.17.0-release-readiness"

DEMO_VARIANTS = {
    "test_demo": ["run.sh"],
    "ux_ab_demo": ["run.sh", "run_pl.sh"],
    "timeseries_noise_demo": ["run.sh"],
    "text_search_demo": ["run.sh", "run_pl.sh"],
    "image_semantic_demo": ["run.sh"],
}

RESEARCH_NOTEBOOKS = [
    "examples/ux_ab_demo/analysis/ux_ab_analysis.ipynb",
    "examples/timeseries_noise_demo/analysis/timeseries_analysis.ipynb",
    "examples/text_search_demo/analysis/text_search_analysis.ipynb",
    "examples/image_semantic_demo/analysis/image_semantic_analysis.ipynb",
]

ALL_NOTEBOOKS = RESEARCH_NOTEBOOKS + [
    "examples/test_demo/analysis/test_demo_analysis.ipynb",
    "examples/smoke_text/analysis/smoke_analysis.ipynb",
]

REQUIRED = [
    "README.md",
    "README_TESTING.md",
    "VERSION",
    ".gitattributes",
    ".gitignore",
    "docker/compose.yaml",
    "docker/run-demo.sh",
    "docker/validate_docker_contract.py",
    "tools/preflight.py",
    "tools/native_preflight.py",
    "tools/validate_response_gated_native.py",
    "tools/demo_runtime_adapters.py",
    "tools/run-demo.sh",
    "output/.gitkeep",
]

TRANSIENT_NAMES = {"__pycache__", ".ipynb_checkpoints", ".pytest_cache", ".mypy_cache"}
TRANSIENT_SUFFIXES = {".pyc", ".pyo"}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_required(errors: list[str]) -> None:
    for item in REQUIRED:
        if not (ROOT / item).exists():
            fail(errors, f"missing required path: {item}")
    for demo, runners in DEMO_VARIANTS.items():
        base = ROOT / "examples" / demo
        for name in runners:
            if not (base / name).is_file():
                fail(errors, f"missing public runner: examples/{demo}/{name}")
        if not (base / "README.md").is_file():
            fail(errors, f"missing demo README: examples/{demo}/README.md")
        if not (base / "validate_collection.py").is_file():
            fail(errors, f"missing collection validator: examples/{demo}/validate_collection.py")


def check_version(errors: list[str]) -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != EXPECTED_VERSION:
        fail(errors, f"VERSION mismatch: expected {EXPECTED_VERSION!r}, got {version!r}")


def check_python(errors: list[str], counts: dict[str, int]) -> None:
    for path in sorted(ROOT.rglob("*.py")):
        if any(part in TRANSIENT_NAMES for part in path.parts):
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            counts["python"] += 1
        except Exception as exc:
            fail(errors, f"Python syntax: {rel(path)}: {exc}")


def check_yaml(errors: list[str], counts: dict[str, int]) -> None:
    for pattern in ("*.yaml", "*.yml"):
        for path in sorted(ROOT.rglob(pattern)):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                if data is None:
                    fail(errors, f"empty YAML: {rel(path)}")
                counts["yaml"] += 1
            except Exception as exc:
                fail(errors, f"YAML parse: {rel(path)}: {exc}")

    for path in sorted((ROOT / "examples").glob("*/config*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            dataset = data.get("dataset", {})
            if not isinstance(dataset, dict) or len(dataset) != 1:
                fail(errors, f"config dataset contract: {rel(path)}")
                continue
            section = next(iter(dataset.values()))
            dataset_path = section.get("path") if isinstance(section, dict) else None
            if not dataset_path:
                fail(errors, f"config dataset path missing: {rel(path)}")
            elif not (ROOT / dataset_path).exists():
                fail(errors, f"config dataset path does not exist: {rel(path)} -> {dataset_path}")
            output = data.get("output", {})
            folder = output.get("folder") if isinstance(output, dict) else None
            if not isinstance(folder, str) or not folder.startswith("output"):
                fail(errors, f"config output must be under output/: {rel(path)} -> {folder!r}")
        except Exception as exc:
            fail(errors, f"config contract: {rel(path)}: {exc}")


def check_notebooks(errors: list[str], counts: dict[str, int]) -> None:
    for item in ALL_NOTEBOOKS:
        path = ROOT / item
        if not path.is_file():
            fail(errors, f"missing notebook: {item}")
            continue
        try:
            nb = json.loads(path.read_text(encoding="utf-8"))
            if nb.get("nbformat") != 4:
                fail(errors, f"unsupported notebook format: {item}")
            for index, cell in enumerate(nb.get("cells", [])):
                if cell.get("cell_type") != "code":
                    continue
                source = cell.get("source", "")
                if isinstance(source, list):
                    source = "".join(source)
                try:
                    ast.parse(source or "", filename=f"{item}:cell{index}")
                except SyntaxError as exc:
                    fail(errors, f"notebook code syntax: {item} cell {index}: {exc}")
            counts["notebooks"] += 1
        except Exception as exc:
            fail(errors, f"notebook JSON: {item}: {exc}")


def check_shell(errors: list[str], counts: dict[str, int]) -> None:
    bash = shutil.which("bash")
    scripts = sorted(ROOT.rglob("*.sh"))
    if not bash:
        fail(errors, "bash not found; cannot syntax-check shell entrypoints")
        return
    for path in scripts:
        proc = subprocess.run([bash, "-n", str(path)], text=True, capture_output=True)
        if proc.returncode:
            fail(errors, f"bash -n: {rel(path)}: {proc.stderr.strip()}")
        else:
            counts["shell"] += 1


def check_markdown_links(errors: list[str], counts: dict[str, int]) -> None:
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for raw in link_re.findall(text):
            target = raw.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(errors, f"Markdown link escapes repository: {rel(path)} -> {target}")
                continue
            if not resolved.exists():
                fail(errors, f"broken Markdown link: {rel(path)} -> {target}")
        counts["markdown"] += 1


def check_rst_contract(errors: list[str], counts: dict[str, int]) -> None:
    rst_root = ROOT / "docs" / "upstream_rst"
    expected = {
        "basic_examples.rst",
        "basic_example_ux_ab_text_demo.rst",
        "basic_example_timeseries_noise_demo.rst",
        "basic_example_text_search_demo.rst",
        "basic_example_image_semantic_demo.rst",
        "INTEGRATION_NOTES.rst",
    }
    actual = {p.name for p in rst_root.glob("*.rst")}
    if actual != expected:
        fail(errors, f"RST payload mismatch: expected {sorted(expected)}, got {sorted(actual)}")
    basic = rst_root / "basic_examples.rst"
    if basic.is_file():
        text = basic.read_text(encoding="utf-8")
        for stem in (
            "basic_example_ux_ab_text_demo",
            "basic_example_timeseries_noise_demo",
            "basic_example_text_search_demo",
            "basic_example_image_semantic_demo",
        ):
            if stem not in text:
                fail(errors, f"RST toctree missing {stem}")
    counts["rst"] = len(actual)


def check_transients(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if path.name in TRANSIENT_NAMES or path.suffix in TRANSIENT_SUFFIXES:
            fail(errors, f"transient artifact present: {rel(path)}")


def check_docker_contract(errors: list[str]) -> None:
    validator = ROOT / "docker" / "validate_docker_contract.py"
    proc = subprocess.run([sys.executable, str(validator)], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode:
        fail(errors, f"Docker contract validator failed: {proc.stdout.strip()} {proc.stderr.strip()}".strip())


def payload_hash() -> str:
    h = hashlib.sha256()
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file()):
        relative = rel(path)
        if any(part in TRANSIENT_NAMES for part in path.parts):
            continue
        h.update(relative.encode("utf-8"))
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def main() -> int:
    errors: list[str] = []
    counts = {"python": 0, "yaml": 0, "notebooks": 0, "shell": 0, "markdown": 0, "rst": 0}

    check_required(errors)
    check_version(errors)
    check_python(errors, counts)
    check_yaml(errors, counts)
    check_notebooks(errors, counts)
    check_shell(errors, counts)
    check_markdown_links(errors, counts)
    check_rst_contract(errors, counts)
    check_transients(errors)
    check_docker_contract(errors)

    print("REPOSITORY_AUDIT")
    print(f"version={(ROOT / 'VERSION').read_text(encoding='utf-8').strip()}")
    print("counts=" + ",".join(f"{k}:{v}" for k, v in counts.items()))
    print(f"payload_tree_sha256={payload_hash()}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"REPOSITORY_AUDIT_FAIL errors={len(errors)}")
        return 1
    print("REPOSITORY_AUDIT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

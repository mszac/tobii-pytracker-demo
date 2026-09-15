#!/usr/bin/env python3
"""Patch only the installed package with the Docker direct-mouse backend.

The source clone at /workspace/tobii-pytracker is never modified. The patch is
applied to site-packages after installation and is active only when
PYTRACKER_DOCKER_DIRECT_MOUSE=1.
"""
from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

MARKER = "PYTRACKER_DOCKER_DIRECT_MOUSE_BACKEND_V1"
IOHUB_IMPORT = "from psychopy.iohub import launchHubServer\n"
IOHUB_CALL = "    io = launchHubServer(**iohub_config, window=window)\n"


def locate_installed_eyetracker() -> Path:
    spec = importlib.util.find_spec("tobii_pytracker.utils.eyetracker")
    if spec is None or not spec.origin:
        raise RuntimeError("Cannot locate installed tobii_pytracker.utils.eyetracker")
    path = Path(spec.origin).resolve()
    if "/workspace/tobii-pytracker/src/" in path.as_posix():
        raise RuntimeError(f"Refusing to patch upstream source clone: {path}")
    return path


def apply_patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    if IOHUB_IMPORT not in text:
        raise RuntimeError("Upstream ioHub import contract changed; refusing blind patch")
    if IOHUB_CALL not in text:
        raise RuntimeError("Upstream launchHubServer call contract changed; refusing blind patch")

    # Keep ioHub completely lazy in Docker. The direct mouse path therefore
    # does not initialize Linux global ioHub input hooks at module import time.
    text = text.replace(
        IOHUB_IMPORT,
        f"# {MARKER}: ioHub import is intentionally lazy in Docker.\n",
        1,
    )

    tree = ast.parse(text)
    target = next(
        (node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "launch_hub_server"),
        None,
    )
    if target is None or not target.body:
        raise RuntimeError("launch_hub_server() not found in installed upstream package")
    first = target.body[0]
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
        and first.end_lineno is not None
    ):
        raise RuntimeError("launch_hub_server() docstring contract changed; refusing blind patch")

    insert_after = first.end_lineno
    lines = text.splitlines(keepends=True)
    snippet = f'''\n    # {MARKER}\n    import os as _docker_os\n    if _docker_os.environ.get("PYTRACKER_DOCKER_DIRECT_MOUSE") == "1":\n        from psychopy import core as _docker_core, event as _docker_event\n\n        iohub_config = CustomConfig.read_config(eyetracker_config_file)\n        tracker_class = get_tracker_class(iohub_config)\n        tracker_conf = iohub_config[tracker_class]\n        configured_hz = float(tracker_conf.get("runtime_settings", {{}}).get("sampling_rate", 50.0))\n        sampling_hz = float(_docker_os.environ.get("PYTRACKER_DOCKER_MOUSE_HZ", configured_hz))\n\n        class MonocularEyeSampleEvent:\n            def __init__(self, event_id, logged_time, gaze_x, gaze_y, pupil_measure=5.0):\n                self.event_id = event_id\n                self.logged_time = logged_time\n                self.time = logged_time\n                self.gaze_x = gaze_x\n                self.gaze_y = gaze_y\n                self.pupil_measure1 = pupil_measure\n                self.pupil_measure2 = None\n\n        class _DockerDirectMouseTracker:\n            def __init__(self, win, hz):\n                if win is None:\n                    raise RuntimeError("Docker direct MouseGaze requires a PsychoPy window")\n                if hz <= 0:\n                    raise RuntimeError("Docker MouseGaze sampling rate must be positive")\n                self._mouse = _docker_event.Mouse(win=win)\n                self._interval = 1.0 / hz\n                self._last_sample = None\n                self._event_id = 0\n                self._recording = False\n\n            def runSetupProcedure(self):\n                return {{"RESULT": "DIRECT_MOUSE_DOCKER_READY"}}\n\n            def setRecordingState(self, state):\n                self._recording = bool(state)\n                if self._recording:\n                    self._last_sample = None\n                return self._recording\n\n            def isRecordingEnabled(self):\n                return self._recording\n\n            def getEvents(self):\n                if not self._recording:\n                    return []\n                now = _docker_core.getTime()\n                if self._last_sample is not None and (now - self._last_sample) < self._interval:\n                    return []\n                self._last_sample = now\n                x, y = self._mouse.getPos()\n                self._event_id += 1\n                return [MonocularEyeSampleEvent(self._event_id, now, float(x), float(y))]\n\n            def clearEvents(self):\n                self._last_sample = _docker_core.getTime()\n\n        class _DockerDirectMouseIo:\n            def __init__(self, tracker):\n                self.devices = type("_Devices", (), {{"tracker": tracker}})()\n\n            def quit(self):\n                return None\n\n        tracker = _DockerDirectMouseTracker(window, sampling_hz)\n        io = _DockerDirectMouseIo(tracker)\n        result = tracker.runSetupProcedure()\n        LOGGER.debug(result)\n        tracker.setRecordingState(True)\n        LOGGER.info("Using Docker direct PsychoPy MouseGaze backend (ioHub/X RECORD bypassed).")\n        return io, tracker\n'''
    lines.insert(insert_after, snippet)
    patched = "".join(lines)
    patched = patched.replace(
        IOHUB_CALL,
        "    from psychopy.iohub import launchHubServer\n" + IOHUB_CALL,
        1,
    )
    ast.parse(patched)
    path.write_text(patched, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    path = locate_installed_eyetracker()
    changed = apply_patch(path)
    print(f"DOCKER_MOUSE_PATCH_{'APPLIED' if changed else 'ALREADY_PRESENT'} path={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

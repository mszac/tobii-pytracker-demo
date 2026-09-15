#!/usr/bin/env bash
set -euo pipefail

UPSTREAM_ROOT="/app"
DEMO_ROOT="/app/tobii-pytracker-demo"
LOGICAL_WORKSPACE="/workspace"
LOGICAL_UPSTREAM="$LOGICAL_WORKSPACE/tobii-pytracker"
DISPLAY="${DISPLAY:-:99}"
DEMO="${DEMO:-test_demo}"
DEMO_LANG="${DEMO_LANG:-en}"

export DISPLAY
export PYTHONDONTWRITEBYTECODE=1

fail() {
  echo "DOCKER_DEMO_FAIL: $*" >&2
  exit 2
}

[[ -f "$UPSTREAM_ROOT/src/tobii_pytracker/main.py" ]] || fail "upstream psychopy source is missing under $UPSTREAM_ROOT"
[[ -f "$UPSTREAM_ROOT/configs/mouse_eyetracker_config.yaml" ]] || fail "upstream MouseGaze config is missing"
[[ -d "$DEMO_ROOT/examples" ]] || fail "demo repository is not mounted at $DEMO_ROOT"

case "$DEMO_LANG" in
  en|pl) ;;
  *) fail "DEMO_LANG must be 'en' or 'pl'" ;;
esac

case "$DEMO" in
  test_demo)
    [[ "$DEMO_LANG" == "en" ]] || fail "test_demo has no _pl variant"
    RUNNER="examples/test_demo/run.sh"
    ;;
  ux_ab_demo)
    if [[ "$DEMO_LANG" == "pl" ]]; then
      RUNNER="examples/ux_ab_demo/run_pl.sh"
    else
      RUNNER="examples/ux_ab_demo/run.sh"
    fi
    ;;
  timeseries_noise_demo)
    [[ "$DEMO_LANG" == "en" ]] || fail "timeseries_noise_demo has no _pl variant"
    RUNNER="examples/timeseries_noise_demo/run.sh"
    ;;
  text_search_demo)
    if [[ "$DEMO_LANG" == "pl" ]]; then
      RUNNER="examples/text_search_demo/run_pl.sh"
    else
      RUNNER="examples/text_search_demo/run.sh"
    fi
    ;;
  image_semantic_demo)
    [[ "$DEMO_LANG" == "en" ]] || fail "image_semantic_demo has no _pl variant"
    RUNNER="examples/image_semantic_demo/run.sh"
    ;;
  *)
    fail "unknown DEMO '$DEMO'; expected test_demo, ux_ab_demo, timeseries_noise_demo, text_search_demo, or image_semantic_demo"
    ;;
esac

[[ -f "$DEMO_ROOT/$RUNNER" ]] || fail "runner not found: $RUNNER"

mkdir -p "$LOGICAL_WORKSPACE" /tmp/.cache /tmp/.matplotlib
rm -f "$LOGICAL_UPSTREAM"
ln -s "$UPSTREAM_ROOT" "$LOGICAL_UPSTREAM"

XVFB_PID=""
VNC_PID=""
cleanup() {
  if [[ -n "$VNC_PID" ]]; then kill "$VNC_PID" 2>/dev/null || true; fi
  if [[ -n "$XVFB_PID" ]]; then kill "$XVFB_PID" 2>/dev/null || true; fi
}
trap cleanup EXIT INT TERM

echo "[docker] Starting Xvfb on $DISPLAY (1920x1080x24)..."
Xvfb "$DISPLAY" -screen 0 1920x1080x24 -ac &
XVFB_PID=$!
sleep 2
kill -0 "$XVFB_PID" 2>/dev/null || fail "Xvfb failed to start"

echo "[docker] Starting x11vnc on container port 5900..."
x11vnc -display "$DISPLAY" -forever -nopw -xkb -shared -rfbport 5900 >/tmp/x11vnc.log 2>&1 &
VNC_PID=$!
sleep 1
kill -0 "$VNC_PID" 2>/dev/null || {
  cat /tmp/x11vnc.log >&2 || true
  fail "x11vnc failed to start"
}

echo "[docker] VNC is ready. Connect a VNC client to localhost:${VNC_PORT:-5900}."
echo "[docker] Running DEMO=$DEMO DEMO_LANG=$DEMO_LANG using the documented public runner."

cd "$LOGICAL_UPSTREAM"
bash "tobii-pytracker-demo/$RUNNER"

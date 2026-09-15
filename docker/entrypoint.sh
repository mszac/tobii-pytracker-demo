#!/usr/bin/env bash
set -euo pipefail

export DISPLAY="${DISPLAY:-:99}"
export PYTRACKER_DOCKER_DIRECT_MOUSE="${PYTRACKER_DOCKER_DIRECT_MOUSE:-1}"
export PYTRACKER_DOCKER_MOUSE_HZ="${PYTRACKER_DOCKER_MOUSE_HZ:-50}"
export LIBGL_ALWAYS_SOFTWARE="${LIBGL_ALWAYS_SOFTWARE:-1}"
export QT_X11_NO_MITSHM="${QT_X11_NO_MITSHM:-1}"

mkdir -p /tmp/pytracker-docker
rm -f /tmp/.X99-lock /tmp/.X11-unix/X99 || true

cleanup() {
  set +e
  for pid in "${JUPYTER_PID:-}" "${NOVNC_PID:-}" "${VNC_PID:-}" "${WM_PID:-}" "${XVFB_PID:-}"; do
    [[ -n "$pid" ]] && kill "$pid" 2>/dev/null || true
  done
}
trap cleanup EXIT INT TERM

Xvfb "$DISPLAY" -screen 0 "${PYTRACKER_SCREEN:-1920x1080x24}" -nolisten tcp -ac \
  >/tmp/pytracker-docker/xvfb.log 2>&1 &
XVFB_PID=$!

for _ in $(seq 1 100); do
  if xdpyinfo -display "$DISPLAY" >/dev/null 2>&1; then break; fi
  sleep 0.1
done
xdpyinfo -display "$DISPLAY" >/dev/null 2>&1 || {
  cat /tmp/pytracker-docker/xvfb.log >&2 || true
  echo "ERROR: Xvfb did not become ready" >&2
  exit 1
}

openbox >/tmp/pytracker-docker/openbox.log 2>&1 &
WM_PID=$!

x11vnc -display "$DISPLAY" -forever -shared -nopw -rfbport 5900 -noxdamage -repeat \
  >/tmp/pytracker-docker/x11vnc.log 2>&1 &
VNC_PID=$!

for _ in $(seq 1 100); do
  if nc -z 127.0.0.1 5900 >/dev/null 2>&1; then break; fi
  sleep 0.1
done
nc -z 127.0.0.1 5900 >/dev/null 2>&1 || {
  cat /tmp/pytracker-docker/x11vnc.log >&2 || true
  echo "ERROR: x11vnc did not become ready" >&2
  exit 1
}

websockify --web=/usr/share/novnc 6080 localhost:5900 \
  >/tmp/pytracker-docker/novnc.log 2>&1 &
NOVNC_PID=$!

jupyter lab \
  --ip=0.0.0.0 \
  --port=8888 \
  --no-browser \
  --allow-root \
  --ServerApp.token='' \
  --ServerApp.password='' \
  --ServerApp.root_dir=/workspace/tobii-pytracker/tobii-pytracker-demo \
  >/tmp/pytracker-docker/jupyter.log 2>&1 &
JUPYTER_PID=$!

echo "[docker] Running PsychoPy/X11 direct-mouse preflight..."
python - <<'PY'
from psychopy import visual, event, core, monitors
print("DOCKER_PSYCHOPY_X11_IMPORT_PASS")
PY

python /opt/pytracker-docker/validate_runtime.py

cat <<'EOF'
DOCKER_DESKTOP_READY
noVNC:   http://localhost:6080/vnc.html?autoconnect=true&resize=scale
Jupyter: http://localhost:8888/lab
EOF

wait -n "$XVFB_PID" "$WM_PID" "$VNC_PID" "$NOVNC_PID" "$JUPYTER_PID"
echo "ERROR: a Docker desktop service exited unexpectedly" >&2
exit 1

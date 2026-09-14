#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DEMO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
UPSTREAM_ROOT="$(cd -- "$DEMO_ROOT/.." && pwd)"

if [[ "$(basename -- "$UPSTREAM_ROOT")" != "tobii-pytracker" ]]; then
  echo "ERROR: expected tobii-pytracker-demo inside original tobii-pytracker clone." >&2
  echo "demo:     $DEMO_ROOT" >&2
  echo "upstream: $UPSTREAM_ROOT" >&2
  exit 2
fi
if [[ ! -f "$UPSTREAM_ROOT/configs/mouse_eyetracker_config.yaml" ]]; then
  echo "ERROR: missing upstream MouseGaze config: $UPSTREAM_ROOT/configs/mouse_eyetracker_config.yaml" >&2
  exit 2
fi

cd "$DEMO_ROOT"

run_block() {
  local domain="$1"
  local config="$2"
  local title="$3"

  echo "[timeseries-demo] Starting $title block (9 trials)..."
  tobii-pytracker \
    --config_file "$config" \
    --eyetracker_config_file ../configs/mouse_eyetracker_config.yaml \
    --enable_eyetracker \
    --loop_count 9

  python examples/tobii_timeseries_noise_demo/validate_collection.py \
    --domain "$domain" \
    --output-root output/tobii_timeseries_noise_demo
}

run_block machine examples/tobii_timeseries_noise_demo/config.machine.native.yaml "MACHINE VIBRATION"
run_block pv examples/tobii_timeseries_noise_demo/config.pv.native.yaml "PV POWER"

echo "NATIVE_TIMESERIES_COLLECTION_COMPLETE"

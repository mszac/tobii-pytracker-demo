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

python "$DEMO_ROOT/tools/validate_response_gated_native.py" \
  --upstream-root "$UPSTREAM_ROOT"

cd "$DEMO_ROOT"
STARTED_AT="$(python -c 'import time; print(time.time())')"

tobii-pytracker \
  --config_file examples/tobii_ux_ab_demo/config.native.yaml \
  --eyetracker_config_file ../configs/mouse_eyetracker_config.yaml \
  --enable_eyetracker \
  --loop_count 12

python examples/tobii_ux_ab_demo/validate_collection.py \
  --output-root output/tobii_ux_ab_demo \
  --started-at "$STARTED_AT"

echo "NATIVE_UX_AB_COLLECTION_COMPLETE"

#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
UPSTREAM_ROOT="$(cd -- "$EXAMPLES_ROOT/.." && pwd)"

if [[ "$(basename -- "$UPSTREAM_ROOT")" != "tobii-pytracker" ]]; then
  echo "ERROR: expected demo repository inside original tobii-pytracker clone." >&2
  echo "demo:   $EXAMPLES_ROOT" >&2
  echo "parent: $UPSTREAM_ROOT" >&2
  exit 2
fi
if [[ ! -f "$UPSTREAM_ROOT/configs/mouse_eyetracker_config.yaml" ]]; then
  echo "ERROR: missing upstream MouseGaze config: $UPSTREAM_ROOT/configs/mouse_eyetracker_config.yaml" >&2
  exit 2
fi

python "$EXAMPLES_ROOT/tools/validate_response_gated_native.py" \
  --upstream-root "$UPSTREAM_ROOT"

cd "$EXAMPLES_ROOT"

RUN_STARTED_EPOCH="$(python -c 'import time; print(time.time())')"

echo "[test-demo] Three trials. Each image remains visible until you LEFT-click a bottom response button."
echo "[test-demo] MouseGaze: hold RIGHT while looking; RELEASE RIGHT before LEFT-clicking the answer."

tobii-pytracker \
  --config_file examples/test_demo/config.native.yaml \
  --eyetracker_config_file ../configs/mouse_eyetracker_config.yaml \
  --enable_eyetracker \
  --loop_count 3

python examples/test_demo/validate_collection.py --output-root output/test_demo --min-mtime "$RUN_STARTED_EPOCH"

echo "NATIVE_TEST_DEMO_COLLECTION_COMPLETE"

#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
UPSTREAM_ROOT="$(cd -- "$EXAMPLES_ROOT/.." && pwd)"

if [[ "$(basename -- "$UPSTREAM_ROOT")" != "tobii-pytracker" ]]; then
  echo "ERROR: expected examples repo inside original tobii-pytracker clone." >&2
  echo "examples: $EXAMPLES_ROOT" >&2
  echo "parent:   $UPSTREAM_ROOT" >&2
  exit 2
fi
if [[ ! -f "$UPSTREAM_ROOT/configs/mouse_eyetracker_config.yaml" ]]; then
  echo "ERROR: missing upstream MouseGaze config: $UPSTREAM_ROOT/configs/mouse_eyetracker_config.yaml" >&2
  exit 2
fi

python "$EXAMPLES_ROOT/tools/validate_response_gated_native.py" \
  --upstream-root "$UPSTREAM_ROOT"

cd "$EXAMPLES_ROOT"
exec tobii-pytracker \
  --config_file examples/smoke_images/config.native.yaml \
  --eyetracker_config_file ../configs/mouse_eyetracker_config.yaml \
  --enable_eyetracker \
  --loop_count 3

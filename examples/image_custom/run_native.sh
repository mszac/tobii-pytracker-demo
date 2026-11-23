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
if ! compgen -G "$SCRIPT_DIR/data/pix/*" > /dev/null; then
  echo "ERROR: no stimulus images in $SCRIPT_DIR/data/pix" >&2
  echo "Put your images in that folder, one flat folder without subfolders." >&2
  exit 2
fi

python "$DEMO_ROOT/tools/validate_response_gated_native.py" \
  --upstream-root "$UPSTREAM_ROOT"

cd "$DEMO_ROOT"

python examples/image_custom/run_experiment.py \
  --config-file examples/image_custom/config.native.yaml \
  --eyetracker-config-file ../configs/mouse_eyetracker_config.yaml

echo "NATIVE_IMAGE_CUSTOM_COLLECTION_COMPLETE"

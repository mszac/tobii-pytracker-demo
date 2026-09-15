#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DEMO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
UPSTREAM_ROOT="$(cd -- "$DEMO_ROOT/.." && pwd)"
if [[ "$(basename -- "$UPSTREAM_ROOT")" != "tobii-pytracker" ]]; then
  echo "ERROR: expected tobii-pytracker-demo inside original tobii-pytracker clone." >&2
  exit 2
fi
python "$DEMO_ROOT/tools/validate_response_gated_native.py" --upstream-root "$UPSTREAM_ROOT"
cd "$DEMO_ROOT"
STARTED_AT="$(python -c 'import time; print(time.time())')"
python examples/text_search_demo/run_experiment.py \
  --config-file examples/text_search_demo/config.native_pl.yaml \
  --eyetracker-config-file ../configs/mouse_eyetracker_config.yaml \
  --loop-count 12 \
  --unknown-label "NIE WIEM"
python examples/text_search_demo/validate_collection.py \
  --output-root output/text_search_demo_pl \
  --dataset examples/text_search_demo/data/text_search_pl.csv \
  --started-at "$STARTED_AT"
echo "NATIVE_TEXT_SEARCH_COLLECTION_COMPLETE_PL"

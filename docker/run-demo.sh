#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE=(docker compose -f "$SCRIPT_DIR/compose.yaml")
NAME="${1:-}"

case "$NAME" in
  test_demo) launcher="examples/test_demo/run_native.sh" ;;
  ux_ab_demo) launcher="examples/ux_ab_demo/run_native.sh" ;;
  ux_ab_demo_pl) launcher="examples/ux_ab_demo/run_native_pl.sh" ;;
  timeseries_noise_demo) launcher="examples/timeseries_noise_demo/run_native.sh" ;;
  text_search_demo) launcher="examples/text_search_demo/run_native.sh" ;;
  text_search_demo_pl) launcher="examples/text_search_demo/run_native_pl.sh" ;;
  image_semantic_demo) launcher="examples/image_semantic_demo/run_native.sh" ;;
  *)
    echo "Usage: bash docker/run-demo.sh {test_demo|ux_ab_demo|ux_ab_demo_pl|timeseries_noise_demo|text_search_demo|text_search_demo_pl|image_semantic_demo}" >&2
    exit 2
    ;;
esac

"${COMPOSE[@]}" exec app bash -lc "cd /workspace/tobii-pytracker/tobii-pytracker-demo && bash '$launcher'"

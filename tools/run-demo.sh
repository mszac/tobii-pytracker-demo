#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DEMO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"

usage() {
  cat <<'USAGE'
Usage:
  bash tobii-pytracker-demo/tools/run-demo.sh <demo> [en|pl]
  bash tobii-pytracker-demo/tools/run-demo.sh --list

Demos:
  test_demo
  ux_ab_demo [en|pl]
  timeseries_noise_demo
  text_search_demo [en|pl]
  image_semantic_demo

Run this from the documented Python 3.10 environment. For local execution the
demo repository must be cloned inside the original tobii-pytracker checkout.
USAGE
}

if [[ "${1:-}" == "--list" ]]; then
  usage
  exit 0
fi

DEMO="${1:-}"
LANG="${2:-en}"

if [[ -z "$DEMO" ]]; then
  usage >&2
  exit 2
fi

case "$LANG" in
  en|pl) ;;
  *) echo "ERROR: language must be 'en' or 'pl'." >&2; exit 2 ;;
esac

case "$DEMO" in
  test_demo|timeseries_noise_demo|image_semantic_demo)
    if [[ "$LANG" != "en" ]]; then
      echo "ERROR: $DEMO has no Polish variant." >&2
      exit 2
    fi
    RUNNER="$DEMO_ROOT/examples/$DEMO/run.sh"
    ;;
  ux_ab_demo|text_search_demo)
    if [[ "$LANG" == "pl" ]]; then
      RUNNER="$DEMO_ROOT/examples/$DEMO/run_pl.sh"
    else
      RUNNER="$DEMO_ROOT/examples/$DEMO/run.sh"
    fi
    ;;
  *)
    echo "ERROR: unknown demo '$DEMO'." >&2
    usage >&2
    exit 2
    ;;
esac

if [[ ! -x "$RUNNER" ]]; then
  if [[ ! -f "$RUNNER" ]]; then
    echo "ERROR: runner not found: $RUNNER" >&2
    exit 2
  fi
fi

exec bash "$RUNNER"

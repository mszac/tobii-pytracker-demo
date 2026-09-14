#!/usr/bin/env bash
set -euo pipefail

UPSTREAM_URL="${TOBII_PYTRACKER_URL:-https://github.com/sbobek/tobii-pytracker.git}"
UPSTREAM_REF="${TOBII_PYTRACKER_REF:-}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
if [[ "$(basename -- "$(dirname -- "$EXAMPLES_ROOT")")" == "tobii-pytracker" ]]; then
  echo "ERROR: examples repo is nested inside the upstream clone; this helper cannot replace its parent safely." >&2
  echo "Use docs/windows/NATIVE_TESTING.md and perform the full reset from the workspace directory." >&2
  exit 2
fi
WORKSPACE_ROOT="$(dirname -- "$EXAMPLES_ROOT")"
UPSTREAM_DIR="$WORKSPACE_ROOT/tobii-pytracker"

if [[ -z "$WORKSPACE_ROOT" || "$WORKSPACE_ROOT" == "/" ]]; then
  echo "ERROR: refusing to operate with unsafe workspace root: '$WORKSPACE_ROOT'" >&2
  exit 2
fi
if [[ "$UPSTREAM_DIR" == "$EXAMPLES_ROOT" ]]; then
  echo "ERROR: upstream path resolves to the examples repository." >&2
  exit 2
fi
if [[ "$(basename -- "$UPSTREAM_DIR")" != "tobii-pytracker" ]]; then
  echo "ERROR: refusing to remove unexpected directory name: '$UPSTREAM_DIR'" >&2
  exit 2
fi

printf '[prepare] examples repo: %s\n' "$EXAMPLES_ROOT"
printf '[prepare] workspace:     %s\n' "$WORKSPACE_ROOT"
printf '[prepare] upstream path: %s\n' "$UPSTREAM_DIR"

if [[ -e "$UPSTREAM_DIR" ]]; then
  printf '[prepare] removing previous upstream clone: %s\n' "$UPSTREAM_DIR"
  rm -rf -- "$UPSTREAM_DIR"
fi

printf '[prepare] cloning original upstream: %s\n' "$UPSTREAM_URL"
git clone "$UPSTREAM_URL" "$UPSTREAM_DIR"

if [[ -n "$UPSTREAM_REF" ]]; then
  printf '[prepare] checking out requested upstream ref: %s\n' "$UPSTREAM_REF"
  git -C "$UPSTREAM_DIR" fetch --all --tags --prune
  git -C "$UPSTREAM_DIR" checkout "$UPSTREAM_REF"
fi

printf '\n[prepare] original upstream provenance\n'
printf 'origin: '
git -C "$UPSTREAM_DIR" remote get-url origin
printf 'branch: '
git -C "$UPSTREAM_DIR" branch --show-current || true
printf 'commit: '
git -C "$UPSTREAM_DIR" rev-parse HEAD
printf 'status:\n'
git -C "$UPSTREAM_DIR" status --short

printf '\n[prepare] done. Do not install tobii-pytracker from the examples repository.\n'

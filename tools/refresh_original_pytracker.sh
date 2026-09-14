#!/usr/bin/env bash
set -euo pipefail
cat >&2 <<'MSG'
This helper is intentionally disabled for the canonical nested layout.
A script stored inside tobii-pytracker-demo cannot safely delete/recreate its parent tobii-pytracker clone.

Run the fresh reset manually from the workspace directory instead, for example:
  cd /d/pytracker
  rm -rf tobii-pytracker
  git clone https://github.com/sbobek/tobii-pytracker.git
  cd tobii-pytracker
  git clone https://github.com/mszac/tobii-pytracker-demo.git

Then keep the terminal in tobii-pytracker.
MSG
exit 2

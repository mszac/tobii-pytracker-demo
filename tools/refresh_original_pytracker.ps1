$ErrorActionPreference = "Stop"
throw @"
This helper is intentionally disabled for the canonical nested layout.
A script stored inside tobii-pytracker-demo cannot safely delete/recreate its parent tobii-pytracker clone.

Run the fresh reset manually from the workspace directory, then keep the terminal in tobii-pytracker.
See docs/windows/NATIVE_TESTING.md.
"@

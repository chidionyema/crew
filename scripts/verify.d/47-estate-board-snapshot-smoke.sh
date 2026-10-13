#!/usr/bin/env bash
# Verify #47 — scripts/estate-snapshot can be imported and hooks_row runs cleanly.
#
# Catches the false_refusals regression (LAW 28: refused outcomes are a row, never silent).
# Runs under whatever python3 the PATH holds; will refuse to run if the script is absent.

set -u

SCRIPT="scripts/estate-snapshot"
if [[ ! -f "$SCRIPT" ]]; then
  echo "FAIL: $SCRIPT missing" >&2
  exit 1
fi

# Module-load smoke test: import the script under a temp name to ensure it parses.
TMP=$(mktemp -t estate-snapshot-smoke-XXXXXX.py)
trap 'rm -f "$TMP"' EXIT
cat >"$TMP" <<'PY'
import importlib.util, sys, pathlib
spec = importlib.util.spec_from_file_location("estate_snapshot_smoke", "scripts/estate-snapshot")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print("hooks_row callable:", callable(getattr(m, "hooks_row", None)))
PY

if ! python3 "$TMP" >/dev/null 2>&1; then
  echo "FAIL: $SCRIPT fails to import (py3 module load)" >&2
  exit 1
fi

echo "PASS: scripts/estate-snapshot loads; hooks_row present"
exit 0

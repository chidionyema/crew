#!/usr/bin/env bash
# crew#403 CP-A: every science capability on the showcase can describe and demo itself. A module
# with no docstring line or no __main__ entry is refused here, on every PR, before the page that
# lists it is ever generated. Founder, 2026-08-27: "cant have components that cannot self describe."
set -euo pipefail
cd "$(dirname "$0")/../.."
PY="${PYTHON:-python3}"
[ -x .venv/bin/python ] && PY=.venv/bin/python
echo "== showcase self-description (crew#403) =="
$PY science/showcase.py --check

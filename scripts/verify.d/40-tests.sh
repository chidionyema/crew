#!/usr/bin/env bash
# This repo's own suite is green, run through the interpreter the README names.
cd "$CREW_ROOT" || exit 1
py=.venv/bin/python
[ -x "$py" ] || { echo "no .venv — see README, 'Tests'"; exit 2; }
echo "\$ .venv/bin/python -m pytest -q"
out="$($py -m pytest -q 2>&1)"; rc=$?
echo "$out" | tail -2
echo "rc=$rc"
[ $rc -eq 0 ] || exit 1
echo "$out" | grep -qE '[0-9]+ passed' || { echo "exited 0 with nothing collected"; exit 1; }

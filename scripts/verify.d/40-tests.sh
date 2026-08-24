#!/usr/bin/env bash
# This repo's own suite is green, run through the interpreter the README names.
# CREW_ROOT is set by the verify harness and by CI, and was required here. That
# made this gate unrunnable by hand: a developer who ran it directly got
# "parameter null or not set" and rc=1, indistinguishable from a real failure.
# So nobody ran it locally, and it could only ever go red in CI -- the same
# class as the home-directory receipt that 85-risk-register.sh now refuses.
# Default it to the repository this script lives in, exactly as the other gates
# do, so running the gate by hand is the cheap thing rather than the confusing
# one (LAW 38: a guard that refuses correct work is an outage).
cd "${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}" || exit 1
py=.venv/bin/python
[ -x "$py" ] || { echo "no .venv — see README, 'Tests'"; exit 2; }
echo "\$ .venv/bin/python -m pytest -q"
out="$($py -m pytest -q 2>&1)"; rc=$?
echo "$out" | tail -2
echo "rc=$rc"
[ $rc -eq 0 ] || exit 1
echo "$out" | grep -qE '[0-9]+ passed' || { echo "exited 0 with nothing collected"; exit 1; }

#!/bin/sh
# Verify command for this repo. Resolved by hermes-agent's detect_project_facts
# (scripts/run_tests.sh is its first-priority marker), so the verification
# ledger and the claim gate can back a DONE with a green run here.
# Uses the repo venv: bare `pytest` resolves to system python, which lacks
# hypothesis and fails collection (measured 2026-08-24).
cd "$(dirname "$0")/.." || exit 1
if [ -x .venv/bin/python ]; then
    exec .venv/bin/python -m pytest -q "$@"
fi
exec python3 -m pytest -q "$@"

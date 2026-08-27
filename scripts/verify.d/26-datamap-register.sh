#!/usr/bin/env bash
# LAW 50: every producer of data carries a verdict, every gap a ticket. The full gate runs
# where the world is (the Mac, hourly, as the `data map` row of estate-snapshot); here the
# runner can only see git, so it grades the register itself and the `act` domain, which
# lives in the register. A malformed register or an unticketed act is red on every PR.
set -euo pipefail
cd "$(dirname "$0")/../.."
PY="${PYTHON:-python3}"
[ -x .venv/bin/python ] && PY=.venv/bin/python
echo "== datamap register (LAW 50) =="
$PY science/datamap.py --check --domains act | sed -n '/^DATA MAP/,$p'

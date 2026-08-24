#!/usr/bin/env bash
# The same register, judged by Open Policy Agent instead of by our own Python.
#
# 85-risk-register.sh is the fallback and it is not going anywhere. It keeps the
# one rule a policy engine cannot express -- whether the program a receipt names
# exists on this machine -- and it keeps a copy of all the others, so the estate
# still has a working check on a box with no conftest installed.
#
# This one exists because a buyer reading the repository should meet a rule
# engine they recognise. OPA is CNCF Graduated and Apache-2.0; policy/*.rego is
# a file their own people can read without learning our conventions first.
#
# CANNOT RUN (exit 2), never FAIL, when conftest is absent. A check that refuses
# correct work because a tool is missing from one machine is an outage, not a
# guard (LAW 38).
command -v conftest >/dev/null || { echo "conftest is not installed -- brew install conftest"; exit 2; }
command -v jq >/dev/null || { echo "jq is not installed -- brew install jq"; exit 2; }

ROOT="${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
REG="$ROOT/risk/REGISTER.jsonl"
POL="$ROOT/policy"
[ -f "$REG" ] || { echo "FAIL: no risk register at $REG"; exit 1; }
[ -d "$POL" ] || { echo "FAIL: no policy directory at $POL"; exit 1; }

conftest --version | tr '\n' ' '; echo

# The {risks: .} wrapper matters: conftest splits a top-level JSON array into one
# document per element, which would make every whole-register rule fire once per
# row. Measured 2026-08-24 -- eleven identical failures from a register that was
# fine.
echo "\$ jq -s '{risks: .}' $REG | conftest test --parser json -p policy -"
jq -s '{risks: .}' "$REG" | conftest test --parser json -p "$POL" -

#!/usr/bin/env bash
# The camera resolves, runs, and passes its own controls.
#
# Until 2026-08-24 this check stopped at "it is on PATH". The tool's 29 paired
# controls ran only in the hourly estate-selftest on the laptop, so a change to
# the tool could merge through CI having never executed one of them. That is how
# 097eccd shipped: an evidence commit that also carried two file deletions and a
# reverted function, from a code path with no control over what it commits.
#
# The PATH copy can be absent (it is a symlink into this repo from ~/.claude).
# The in-repo copy is always here, so the suites always run.
set -u
HERE="$(cd "$(dirname "$0")/../.." && pwd)"

echo "\$ command -v pr-evidence"
if p="$(command -v pr-evidence)"; then
  echo "$p"
  echo "\$ pr-evidence --help >/dev/null"
  pr-evidence --help >/dev/null 2>&1 || { echo "FAIL: on PATH but will not run"; exit 1; }
  echo "runs"
else
  echo "not on PATH — see README, 'Evidence on a pull request'. The in-repo copy is"
  echo "still graded below, so this is a note and not a verdict."
fi

echo "\$ python3 scripts/pr-evidence.py --selftest"
if ! out="$("${PYTHON:-python3}" "$HERE/scripts/pr-evidence.py" --selftest 2>&1)"; then
  echo "$out" | sed 's/^/    /'
  echo "FAIL: the tool's own controls do not pass"
  exit 1
fi
echo "$out" | grep -E '^selftest-|FAIL' | sed 's/^/    /'

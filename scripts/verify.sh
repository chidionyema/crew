#!/usr/bin/env bash
# Run every check in verify.d and count the verdicts.
#
# A check is one executable file in scripts/verify.d. It prints the commands it
# runs and their raw output, then exits:
#
#   0  PASS        the thing is working
#   1  FAIL        the thing is broken
#   2  CANNOT RUN  the check needs something this machine does not have
#
# The count at the bottom is arithmetic over those exit codes. No check decides
# its own wording and nothing here asserts a result, which is the point: LAW 17
# wants the state, not a claim about it.
#
#   scripts/verify.sh                 # every check
#   scripts/verify.sh 40 50           # only checks whose filename starts 40 or 50
#   scripts/verify.sh --log run.log   # tee the whole run, ready for a screenshot
#
# Environment a check may read, all optional:
#   CREW_PR                  a pull request number, for the evidence checks
#   CREW_ISSUE_REPO          owner/name of the repo holding the tracked issue
#   CREW_ISSUE               the tracked issue number
#   LAWS_FILE                the laws file (default ~/AGENTS.md)
#   VERIFY_ALLOW_MUTATION=1  let a check edit a real pull request, then restore it
#
# Exit status is 1 if any check failed, else 0. CANNOT RUN never fails the run;
# it is reported so nobody mistakes an unrun check for a passing one.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIR="$ROOT/scripts/verify.d"
export CREW_ROOT="$ROOT"

log=""
sel=()
while [ $# -gt 0 ]; do
  case "$1" in
    --log) log="$2"; shift 2;;
    -h|--help) sed -n '2,30p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0;;
    *) sel+=("$1"); shift;;
  esac
done

run_all() {
  local pass=0 fail=0 skip=0 names_failed=() names_skipped=()
  for check in "$DIR"/*.sh; do
    [ -e "$check" ] || { echo "no checks in $DIR"; return 1; }
    local base; base="$(basename "$check")"
    if [ ${#sel[@]} -gt 0 ]; then
      local want=no
      for s in "${sel[@]}"; do case "$base" in "$s"*) want=yes;; esac; done
      [ "$want" = yes ] || continue
    fi
    echo "=== ${base%.sh} ==="
    bash "$check"
    local rc=$?
    case $rc in
      0) echo "  VERDICT: PASS"; pass=$((pass+1));;
      2) echo "  VERDICT: CANNOT RUN"; skip=$((skip+1)); names_skipped+=("${base%.sh}");;
      *) echo "  VERDICT: FAIL (rc=$rc)"; fail=$((fail+1)); names_failed+=("${base%.sh}");;
    esac
    echo
  done
  echo "================================================"
  echo "PASS=$pass  FAIL=$fail  CANNOT RUN=$skip   of $((pass+fail+skip))"
  [ $fail -gt 0 ] && echo "failed: ${names_failed[*]}"
  [ $skip -gt 0 ] && echo "not run: ${names_skipped[*]}"
  [ $fail -eq 0 ]
}

if [ -n "$log" ]; then
  run_all 2>&1 | tee "$log"
  exit "${PIPESTATUS[0]}"
fi
run_all

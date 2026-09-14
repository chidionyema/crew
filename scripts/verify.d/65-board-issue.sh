#!/usr/bin/env bash
# crew#102: the cache is rebuilt from the board issue, or this gate says CANNOT RUN.
#
# This is the half the existing 45-estate-board.sh does not cover. That gate is hermetic:
# it imports scripts/estate-board-sync.py and feeds it fixture comments, so it proves the
# reader works without paying a network round trip. The other half -- that the LIVE cache
# on the substrate was actually rebuilt from THIS issue (chidionyema/crew#102) -- was not
# on any PR gate. A cache that has not been refilled reads the same as a freshly rebuilt
# one, which is the silent-failure class LAW 38 names: an instrument that reports success
# without doing the work.
#
# WHAT THIS GATE DOES.
#   1. Reads ESTATE_BOARD_REPO (default chidionyema/crew) and ESTATE_BOARD_ISSUE
#      (default 102). These are the exact constants scripts/estate-board-sync.py reads at
#      import time, so one env override moves both callers at once.
#   2. If `gh` is missing OR `gh auth status` returns nonzero, the rebuild would silently
#      return 0 from a stale session cache, so the gate prints BLIND and exits 2. NEVER
#      PASS without having actually run the rebuild.
#   3. Runs `python3 scripts/estate-board-sync.py <cache>` and pins the contract:
#         exit code 0
#         output file holds >= 1 row
#         the printed summary line matches
#           estate-board-sync: N row(s) from <repo>#<issue> -> <file>
#   4. Prints PASS only when all four hold.
#
# WHAT IT CANNOT SEE (residual, stated because a guard that hides its blind spot lies).
# It cannot prove the writer (estate-broadcast.py, lives in ~/.claude/scripts) is reaching
# GitHub -- that is the incident test tests/test_incident_crew102_estate_board_is_issue_102.py's
# half, and the row the `estate board` row of scripts/estate-snapshot grades hourly.
#
# STYLE MATCH. scripts/verify.d/45-estate-board.sh (header comment shape, exit codes
# 0=PASS / 1=FAIL / 2=CANNOT RUN). The orchestrator scripts/verify.sh does the arithmetic;
# this gate decides its own wording because the decision is "could it run?" not "did the
# thing work?".
#
# exit 0 pass | exit 1 the rebuild failed | exit 2 CANNOT RUN
set -uo pipefail

REPO="${ESTATE_BOARD_REPO:-chidionyema/crew}"
ISSUE="${ESTATE_BOARD_ISSUE:-102}"
CACHE="${TMPDIR:-/tmp}/board-after.jsonl"

# (1) `gh` must exist on the substrate. R14 names the laptop; a runner without gh is the
# case where this gate must say CANNOT RUN, not PASS.
if ! command -v gh >/dev/null 2>&1; then
  echo "BLIND: \`gh\` is not on PATH; cannot reach the board issue $REPO#$ISSUE"
  exit 2
fi

# (2) `gh` must be authenticated. The case this catches is the silent one: the rebuild
# would return 0 from a stale session cache, and we must NOT count that as PASS.
echo "\$ gh auth status"
auth_rc=0
gh auth status >/dev/null 2>&1 || auth_rc=$?
if [ "$auth_rc" -ne 0 ]; then
  echo "BLIND: \`gh auth status\` returned $auth_rc; cannot rebuild $REPO#$ISSUE"
  exit 2
fi

# (3) Run the rebuild. The script's contract: exit 0 on success, exit 1 on a failed read,
# exit !=0 on misuse; treat anything other than 0 as FAIL with the script's own stderr
# reproduced for the run log.
echo "\$ python3 scripts/estate-board-sync.py $CACHE"
out="$(python3 scripts/estate-board-sync.py "$CACHE" 2>&1)"; rc=$?
echo "$out"
if [ "$rc" -ne 0 ]; then
  echo "estate-board-sync exited $rc; cannot grade the rebuild"
  exit 1
fi

# (4) The output file must exist and carry at least one row. A zero-row file is the
# failure shape we have seen when the issue has comments but none parse as rows; FAIL,
# not PASS, not CANNOT RUN.
echo "\$ wc -l $CACHE"
wc -l "$CACHE"
lines="$(wc -l <"$CACHE")"
if [ "$lines" -lt 1 ]; then
  echo "BLIND: rebuild wrote 0 rows to $CACHE"
  exit 2
fi

# (5) The summary line must match the exact wording the sync script prints. A future
# change to that line cannot silently downgrade PASS into "exit 0 with a different line";
# the orchestrator would still count it as PASS, but a gate whose contract it just broke
# must go red.
summary_re="^estate-board-sync: ([0-9]+) row\(s\) from ${REPO}#${ISSUE} -> ${CACHE}\$"
summary="$(printf '%s\n' "$out" | grep -E "$summary_re" || true)"
if [ -z "$summary" ]; then
  echo "expected summary line matching: $summary_re"
  echo "got: $out"
  exit 1
fi

# (6) The number in the summary line must equal the number of rows the file holds.
# scripts/estate-board-sync.py writes one JSON object per line, so `wc -l` is the count.
# A mismatch is the bug the atomic tmp.replace in the sync script exists to prevent; if
# it shows up, the writer is half-writing the cache and the gate must FAIL.
n_summary="$(printf '%s\n' "$summary" | sed -E "s/^estate-board-sync: ([0-9]+).*/\\1/")"
if [ "$n_summary" != "$lines" ]; then
  echo "summary says $n_summary rows but $CACHE has $lines; writer is half-writing the cache"
  exit 1
fi

echo "board cache rebuilt from $REPO#$ISSUE: $lines row(s)"
exit 0

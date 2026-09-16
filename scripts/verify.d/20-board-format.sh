#!/usr/bin/env bash
# The estate board is the sync layer (LAW 26); its write side must validate.
#
# WHY THIS EXISTS. crew#102 makes the board GitHub issue 102. Anything that
# calls the board without first proving the row matches the contract will land
# a misformed row on the board, and a misformed row is the row every reader
# silently drops — the same class of failure `estate-board-sync.py` parses
# away today (the human backfill headers).
#
# WHAT IT CHECKS. Both arms of `bin/board`:
#
#   1. format:    a good row prints JSON and exits 0; a bad row prints
#                 `format: bad row` to stderr and exits non-zero.
#   2. post --dry-run: simulated transport failure appends the row to the
#                 dead-letter file, stderr carries `WARN: dead-lettered`, and
#                 the exit code is non-zero. The dry-run switch is what makes
#                 the failure reproducible here without touching GitHub.
#
# Both arms run against fixtures, never against the live board. The dead-
# letter file is a tempdir one — this gate refuses to write to
# ~/.claude/state/board-deadletter.jsonl on someone's laptop.
#
# Pickup: scripts/verify.sh enumerates verify.d/*.sh, so this file is wired
# automatically. No edit to that script, no edit to .github/workflows/crew-qa.yml.
#
# Standard: docs/STANDARDS.md "Coordination" — bin/board is the write side of
#   the sync layer; this gate is the mechanical half of that contract.
# Rejected: a new GitHub Actions workflow for board formatting — the existing
#   crew-qa.yml already runs scripts/verify.sh; a separate workflow would
#   split one gate across two runners and make CI drift apart.
# Rejected: shelling out to `gh issue comment` to "really post" — the real
#   writer is estate-broadcast.py; this gate proves the format and the
#   dead-letter, not the network.
# Deviation: none.
#
# exit 0 pass | exit 1 a bin/board arm returned the wrong verdict | exit 2 CANNOT RUN

set -uo pipefail
ROOT="${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$ROOT" || exit 2

BIN="$ROOT/bin/board"
[ -x "$BIN" ] || { echo "CANNOT RUN: $BIN missing or not executable."; exit 2; }

PY="${PYTHON:-python3}"
command -v "$PY" >/dev/null 2>&1 || { echo "CANNOT RUN: no python3 on PATH."; exit 2; }

tmp="$(mktemp -d)" || exit 2
trap 'rm -rf "$tmp"' EXIT

GOOD='`2026-09-08T12:00:00Z` **test-session** (status/info): a clean row'
BAD='2026-09-08T12:00:00Z **test-session** (status/info): bare ts'
DEAD="$tmp/deadletter.jsonl"

fail=0

echo "\$ bin/board format --row <good>"
if out="$("$PY" "$BIN" format --row "$GOOD")"; then
  echo "    PASS good row -> JSON"
  printf '%s' "$out" | grep -q '"from":"test-session"' || { echo "    FAIL good row JSON missing expected field"; fail=1; }
else
  echo "    FAIL good row refused (rc=$?)"; fail=1
fi

echo "\$ bin/board format --row <bad>"
if out="$("$PY" "$BIN" format --row "$BAD" 2>&1 >/dev/null)"; then
  echo "    FAIL bad row accepted (rc=0)"; fail=1
else
  printf '%s' "$out" | grep -q 'format: bad row' && echo "    PASS bad row refused with format marker" \
    || { echo "    FAIL bad row refused without 'format: bad row' on stderr"; fail=1; }
fi

echo "\$ bin/board post --row <good> --dead-letter $DEAD (simulated transport failure)"
if out="$("$PY" "$BIN" post --row "$GOOD" --dead-letter "$DEAD" 2>&1 >/dev/null)"; then
  echo "    FAIL transport failure exited 0"; fail=1
else
  printf '%s' "$out" | grep -q 'WARN: dead-lettered' && echo "    PASS WARN on stderr" \
    || { echo "    FAIL stderr missing 'WARN: dead-lettered'"; fail=1; }
fi
if [ -f "$DEAD" ] && grep -q 'test-session' "$DEAD"; then
  echo "    PASS dead-letter written"
else
  echo "    FAIL dead-letter file missing or empty"; fail=1
fi

echo "\$ bin/board post --row <good> --dead-letter $DEAD --no-fail-after-format"
if "$PY" "$BIN" post --row "$GOOD" --dead-letter "$DEAD" --no-fail-after-format >/dev/null 2>&1; then
  echo "    PASS healthy transport exits 0"
else
  echo "    FAIL healthy transport exited non-zero"; fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "pass: bin/board honours the row and dead-letter contracts."
  exit 0
fi
echo "FAIL: bin/board contract check failed; see the arm above."
exit 1

#!/usr/bin/env bash
# crew#102 — gate that pins the board contract: target issue, row format,
# dead-letter path.
#
# STANDARD. The board of record is GitHub issue chidionyema/crew#102 (crew#102,
# founder ruling 2026-08-24: "why not just use github issues? why reinvent the
# wheel badly"). The JSONL at ~/.claude/ESTATE_BOARD.jsonl is only the
# offline cache. A row that fails to land on the issue is dead-lettered to
# ~/.claude/state/board-deadletter.jsonl and a loud WARN is emitted; it is
# never dropped silently.
#
# WHAT IT CHECKS, in order, each as a labelled sub-check:
#   1. tests/test_incident_crew102_estate_board_is_issue_102.py exists
#   2. the test pins BOARD_REPO="chidionyema/crew" and BOARD_ISSUE = 102
#   3. the doc docs/plans/crew-102.md exists and names issue 102
#   4. the dead-letter path ~/.claude/state/board-deadletter.jsonl is reachable
#   5. `python -c "from crew.estate_board import dead_letter_path"` exits 0
#
# On any failure: print which sub-check failed and exit 1.
# On success: print "estate-board: contract pinned (issue 102)" and exit 0.
set -euo pipefail
cd "${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}" || exit 2

TEST="tests/test_incident_crew102_estate_board_is_issue_102.py"
DOC="docs/plans/crew-102.md"

passes=0
failures=0
record() {
  if [ "$1" -eq 0 ]; then
    echo "  PASS  $2"
    passes=$((passes + 1))
  else
    echo "  FAIL  $2"
    failures=$((failures + 1))
  fi
}

# 1. the incident test exists.
if [ -f "$TEST" ]; then record 0 "1. incident test exists at $TEST"; else record 1 "1. incident test exists at $TEST"; fi

# 2. the test pins BOARD_REPO="chidionyema/crew" and BOARD_ISSUE = 102.
if [ -f "$TEST" ] \
    && grep -qF 'BOARD_REPO = "chidionyema/crew"' "$TEST" \
    && grep -qF 'BOARD_ISSUE = 102' "$TEST"; then
  record 0 "2. test pins BOARD_REPO and BOARD_ISSUE"
else
  record 1 "2. test pins BOARD_REPO and BOARD_ISSUE"
fi

# 3. the doc exists and names issue 102.
if [ -f "$DOC" ] && grep -qE '(^|[^0-9])102([^0-9]|$)' "$DOC"; then
  record 0 "3. doc $DOC names issue 102"
else
  record 1 "3. doc $DOC names issue 102"
fi

# 4. the dead-letter path is reachable.
dead="${HOME}/.claude/state/board-deadletter.jsonl"
mkdir -p "$(dirname "$dead")"
probe="$(dirname "$dead")/.board-deadletter.probe"
if ( : > "$probe" ) 2>/dev/null; then
  rm -f "$probe"
  record 0 "4. dead-letter path reachable: $dead"
else
  record 1 "4. dead-letter path reachable: $dead"
fi

# 5. the helper is importable.
if python -c "from crew.estate_board import dead_letter_path; print(dead_letter_path())" >/dev/null 2>&1; then
  record 0 "5. crew.estate_board importable (dead_letter_path)"
else
  record 1 "5. crew.estate_board importable (dead_letter_path)"
fi

if [ "$failures" -eq 0 ]; then
  echo "estate-board: contract pinned (issue 102)"
  exit 0
fi
echo "estate-board: $failures sub-check(s) failed"
exit 1

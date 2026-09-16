#!/usr/bin/env bash
# crew#102 — gate that pins the board contract: target issue, row format,
# dead-letter path. The plan's verification row names this exact gate.
#
# STANDARD. The board of record is GitHub issue chidionyema/crew#102 (crew#102,
# founder ruling 2026-08-24: "why not just use github issues? why reinvent the
# wheel badly"). The JSONL at ~/.claude/ESTATE_BOARD.jsonl is only the offline
# cache. A row that fails to land on the issue is dead-lettered to
# ~/.claude/state/board-deadletter.jsonl and a loud WARN is emitted; it is
# never dropped silently.
#
# WHY THIS GATE EXISTS. The board itself recorded the class at 22:38Z on
# 2026-08-24: "any instrument that reports success without doing the work" —
# and was an instance of it. This gate pins the contract that the writer
# (crew/estate_board.py and the estate-broadcast.py in claude-guards), the
# reader (scripts/estate-board-sync.py), the doc (docs/CREW-BOARD-VISIBILITY.md)
# and the incident test (tests/test_incident_crew102_estate_board_is_issue_102.py)
# all agree on. If any of them drift, the next PR goes red.
#
# WHAT IT CHECKS (paired arms, LAW 38: a guard only ever seen refusing has
# never been shown to permit).
#   A  the writer pins repo=chidionyema/crew and BOARD_ISSUE=102
#   B  the writer exports format_comment and rejects rows with bad priority
#   C  the incident test pins the same target (chidionyema/crew#102)
#   D  the dead-letter path ~/.claude/state/board-deadletter.jsonl is writable
#   E  the doc names the repo, the issue number, the cache path, the dead-letter path
#
# WHAT IT CANNOT SEE (residual, stated because a guard that hides its blind
# spot lies). It grades the static contract, not the live board. The live read
# is graded by 45-estate-board.sh (hermetic parser/rebuild) and
# 65-board-issue.sh (live gh round-trip). A board whose author moved the issue
# mid-flight is invisible here by design.
#
# STYLE MATCH. scripts/verify.d/45-estate-board.sh (header shape, exit codes
# 0=PASS / 1=FAIL / 2=CANNOT RUN).
#
# exit 0 pass | exit 1 the board contract is broken | exit 2 CANNOT RUN
set -uo pipefail
cd "${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}" || exit 2

WRITER="crew/estate_board.py"
TEST="tests/test_incident_crew102_estate_board_is_issue_102.py"
DOC="docs/CREW-BOARD-VISIBILITY.md"
REPO="chidionyema/crew"
ISSUE=102

[ -f "$WRITER" ] || { echo "no writer at $WRITER"; exit 2; }
[ -f "$TEST"   ] || { echo "no incident test at $TEST"; exit 2; }
[ -f "$DOC"    ] || { echo "no visibility doc at $DOC"; exit 2; }

fails=()

check() {
  if [ "$2" = "$3" ]; then
    echo "  ok    $1"
  else
    echo "  FAIL  $1: got '$2', want '$3'"
    fails+=("$1")
  fi
}

# A. the writer pins the right repo and the right issue number.
repo_in_writer="$(grep -E "^\\s*repo: str = \"$REPO\"" "$WRITER" >/dev/null && echo yes || echo no)"
issue_in_writer="$(grep -E "^\\s*issue_number: int = $ISSUE\\b" "$WRITER" >/dev/null && echo yes || echo no)"
check "A.1 writer pins repo=$REPO" "$repo_in_writer" "yes"
check "A.2 writer pins issue_number=$ISSUE" "$issue_in_writer" "yes"

# B. the writer exposes format_comment and rejects bad priorities.
has_format="$(grep -E "^def format_comment" "$WRITER" >/dev/null && echo yes || echo no)"
has_priority_check="$(grep -E "row\\['priority'\\] not in ALLOWED_PRIORITIES" "$WRITER" >/dev/null && echo yes || echo no)"
check "B.1 writer exposes format_comment" "$has_format" "yes"
check "B.2 writer rejects rows with bad priority" "$has_priority_check" "yes"

# C. the incident test pins the same target.
pins_repo="$(grep -E "chidionyema/crew|$REPO" "$TEST" >/dev/null && echo yes || echo no)"
pins_issue="$(grep -E "issue[_ ]?number.*102|issue.*#102|# ?102|ISSUE.*102|issue_number=102" "$TEST" >/dev/null && echo yes || echo no)"
check "C.1 incident test names repo chidionyema/crew" "$pins_repo" "yes"
check "C.2 incident test names issue #102" "$pins_issue" "yes"

# D. the dead-letter path is writable, so the loud channel exists.
dead="${HOME}/.claude/state/board-deadletter.jsonl"
mkdir -p "$(dirname "$dead")"
probe="$(dirname "$dead")/.board-deadletter.probe"
if echo > "$probe" 2>/dev/null; then
  rm -f "$probe"
  check "D the dead-letter path is writable" "yes" "yes"
else
  check "D the dead-letter path is writable" "no" "yes"
fi

# E. the doc names the four parts of the contract.
for needle in "$REPO" "#$ISSUE" "ESTATE_BOARD.jsonl" "board-deadletter.jsonl"; do
  if grep -q -- "$needle" "$DOC"; then
    check "E doc names '$needle'" "yes" "yes"
  else
    check "E doc names '$needle'" "no" "yes"
  fi
done

n="${#fails[@]}"
if [ "$n" -eq 0 ]; then
  echo "15-estate-board: 8/8 arms passed"
  exit 0
fi
echo "15-estate-board: $((8 - n))/8 arms passed"
exit 1
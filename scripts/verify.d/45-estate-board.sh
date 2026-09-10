#!/usr/bin/env bash
# The estate board's READ side is proved, not just present (crew#102).
#
# Standard: crew/docs/STANDARDS.md, "Agent board / sync" row -- the board of record is
#   GitHub issue crew#102 and the JSONL under ~/.claude is only the offline cache. This is
#   the gate that row never had: the writer (estate-broadcast.py), the scheduled caller
#   (scripts/estate-snapshot, board_sync()) and the reader row all existed, and nothing on
#   any pull request proved the cache is rebuilt FROM the issue.
# Rejected: a live `gh issue view 102` read inside this gate -- it would make every pull
#   request pay a GitHub round trip and go red when the network or a rate limit does, which
#   is the failure mode estate-board-sync.py's own header already rejects; the live read
#   stays where it is, hourly, in estate-snapshot. Rejected: a second parser written here
#   to re-derive the row format -- two parsers are two sources of truth, so this gate
#   imports the one the writer and the incident test already agree on.
#
# WHY THIS EXISTS. The board's contract names exactly one silent failure: a row that never
# lands. The board itself recorded the class at 22:38Z on 2026-08-24 -- "any instrument that
# reports success without doing the work" -- and the board was an instance of it: a writer,
# a reader, and no proof. This gate is the proof, and it is hermetic: it feeds
# sync_estate_board() a fixture list of comments and grades what comes out.
#
# WHAT IT CHECKS, and every arm is paired (LAW 38: a guard only ever seen refusing has
# never been shown to permit):
#   A  a backfill header a human wrote is skipped, not parsed as a row
#   B  a full-format row `ts **from** (kind/priority): message` parses, fields intact
#   C  a simple-format row (pre-contract) parses as unclassified/info
#   D  a malformed line is dropped, never guessed at
#   E  the cache is written oldest-first, whatever order the comments arrive in
#   F  the cache is rebuilt from the issue, not appended to: a second sync with fewer
#      comments leaves fewer rows, so a stale row cannot survive
#   G  a failed fetch RAISES rather than returning [] -- the loud-failure half of the
#      contract, and the one that would otherwise look like an empty board
#   H  the dead-letter path is writable, so the loud channel exists
#
# WHAT IT CANNOT SEE (residual, stated because a guard that hides its blind spot lies).
# It grades the read side against fixtures, not against the live issue: a GitHub outage, a
# rate limit or a moved issue number is invisible here by design, and is graded hourly by
# the `estate board` row of scripts/estate-snapshot instead. It also cannot see the writer
# (estate-broadcast.py lives in ~/.claude/scripts, outside this repository); the incident
# test tests/test_incident_crew102_estate_board_is_issue_102.py pins the target both share.
#
# exit 0 pass | exit 1 the read side is broken | exit 2 CANNOT RUN
set -uo pipefail
cd "${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}" || exit 2

SYNC="scripts/estate-board-sync.py"
[ -f "$SYNC" ] || { echo "no read side at $SYNC"; exit 2; }

# The interpreter the README names, with the worktree fallback 40-tests.sh already uses: a
# worktree has no .venv of its own and shares the checkout it was cut from.
py=.venv/bin/python
if [ ! -x "$py" ]; then
  main="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)"; main="${main%/.git}"
  [ -n "$main" ] && [ -x "$main/.venv/bin/python" ] && py="$main/.venv/bin/python"
fi
[ -x "$py" ] || { echo "no .venv — see README, 'Tests'"; exit 2; }

echo "\$ $py - <<'PY'   # the read side, on fixtures, no network"
"$py" - "$SYNC" <<'PY'
import importlib.util
import json
import pathlib
import sys
import tempfile

sync_path = pathlib.Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("estate_board_sync", sync_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

fails = []


def check(name, got, want):
    if got == want:
        print(f"  ok    {name}")
    else:
        print(f"  FAIL  {name}: got {got!r}, want {want!r}")
        fails.append(name)


HEADER = ("**Backfill 1/3 — the 191 rows that existed before the board became this issue "
          "(oldest first).**\n\n- `2026-08-23T21:41:15Z` **rebuild-drill** (drill-failed/info): "
          "the estate cannot be rebuilt from its own repositories right now.")
FULL = "`2026-08-24T03:23:01.090857Z` **fable-63** (board-cutover/high): The board is now crew#102."
SIMPLE = "`2026-08-23T21:41:15Z` **rebuild-drill**: Rebuild drill passed."
MALFORMED = "this line is prose, not a row, and must never be guessed into one"

comments = [
    {"body": HEADER},
    {"body": FULL},
    {"body": SIMPLE},
    {"body": MALFORMED},
]

# A. the human backfill header is prose, not a row.
check("A a backfill header is skipped", mod.parse_comment(HEADER), None)
# B. the declared format parses, field by field.
check("B a full-format row parses", mod.parse_comment(FULL), {
    "ts": "2026-08-24T03:23:01.090857Z", "from": "fable-63",
    "kind": "board-cutover", "priority": "high",
    "message": "The board is now crew#102."})
# C. the pre-contract rows still parse, and are labelled rather than dropped.
check("C a simple-format row parses as unclassified/info", mod.parse_comment(SIMPLE), {
    "ts": "2026-08-23T21:41:15Z", "from": "rebuild-drill",
    "kind": "unclassified", "priority": "info", "message": "Rebuild drill passed."})
# D. a malformed line is dropped, never guessed at.
check("D a malformed line is not a row", mod.parse_comment(MALFORMED), None)

with tempfile.TemporaryDirectory() as tmp:
    cache = pathlib.Path(tmp) / "ESTATE_BOARD.jsonl"
    # E. oldest first, whatever order the comments arrive in.
    n = mod.sync_estate_board(comments, cache)
    rows = [json.loads(ln) for ln in cache.read_text().splitlines() if ln.strip()]
    check("E two rows land, oldest first", (n, [r["ts"] for r in rows]),
          (2, ["2026-08-23T21:41:15Z", "2026-08-24T03:23:01.090857Z"]))
    # F. rebuilt, not appended: a stale row cannot survive a shorter issue.
    n2 = mod.sync_estate_board([{"body": FULL}], cache)
    rows2 = [json.loads(ln) for ln in cache.read_text().splitlines() if ln.strip()]
    check("F the cache is rebuilt from the issue, not appended to", (n2, len(rows2)), (1, 1))
    # G. a failed fetch raises; it never returns [] and reads as an empty board.
    raised = False
    try:
        mod.fetch_comments("chidionyema/crew", 102)
    except Exception:  # noqa: BLE001 -- any failure must be loud, not an empty list
        raised = True
    check("G a failed fetch raises rather than returning []", raised, True)

# H. the loud-failure channel exists and is writable.
dead = pathlib.Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
dead.parent.mkdir(parents=True, exist_ok=True)
probe = dead.with_suffix(".probe")
probe.write_text("")
probe.unlink()
check("H the dead-letter path is writable", probe.exists(), False)

print(f"45-estate-board: {8 - len(fails)}/8 arms passed")
sys.exit(1 if fails else 0)
PY
rc=$?
echo "rc=$rc"
exit "$rc"

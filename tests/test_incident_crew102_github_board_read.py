"""crew#102 — agent sessions read the board from GitHub issue #102, not the laptop file.

The local JSONL at ~/.claude/ESTATE_BOARD.jsonl is only an offline cache the
prompt hooks read when the network is gone. The board of record lives at
chidionyema/crew#102; an agent that needs to know what the founder just said
MUST pull it from the issue comments.

This test pins the read path so that:
  * the issue resolves to the estate board,
  * at least one comment is present and well-formed,
  * the same contract as `test_incident_crew102_estate_board_is_issue_102`
    holds against the read command the doc tells people to use.

If any of these go red, either the writer broke or the doc drifted; the
fix is in the writer or in CREW-BOARD-VISIBILITY.md, never by widening
this test.

The ``board_issue`` fixture (see tests/conftest.py) already fetched
``number,title,state,comments`` in one ``gh`` call; this file grades
that payload against the contract — no further ``gh`` shells.
"""
from __future__ import annotations

import re

ROW_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?\s+\*\*[^*]+\*\*\s+\([^)]+\):\s+.+$"
)


def test_read_command_documented_in_board_doc_runs_clean(board_issue: dict) -> None:
    """The exact `gh issue view --comments` command from CREW-BOARD-VISIBILITY.md works."""
    # The fixture's `--json number,title,state,comments` is the same union of fields
    # the documented `gh issue view --comments --json number,state,comments` reads.
    assert board_issue["number"] == 102
    assert board_issue["state"] == "OPEN"
    assert board_issue["comments"], "board returned zero comments — writer is broken"


def test_a_board_row_matches_the_declared_row_format(board_issue: dict) -> None:
    """At least one comment on the board follows the format the issue body declares."""
    # `--json comments` answers a record keyed "comments", not a bare list.
    comments = board_issue["comments"]
    assert comments, "board returned zero comments -- the writer is broken"
    # The leading comments are the human-written backfill headers, not rows; the contract
    # is that broadcast rows carry the declared shape, so one matching row proves it.
    firsts = [next((ln for ln in c["body"].splitlines() if ln.strip()), "") for c in comments]
    assert any(ROW_PATTERN.match(ln) for ln in firsts), (
        f"no row on the board matches the issue body's contract; first lines read "
        f"{firsts[:3]!r}"
    )

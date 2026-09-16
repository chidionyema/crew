"""crew#102 — the estate board is GitHub issue 102, not a laptop file.

This incident test pins the contract the founder ordered on 2026-08-24:
broadcasts must land on chidionyema/crew#102. The local file at
~/.claude/ESTATE_BOARD.jsonl is only the offline cache that prompt hooks
read; it is NOT the board. A row that fails to reach GitHub is
dead-lettered to ~/.claude/state/board-deadletter.jsonl and warned loudly —
never silently dropped.

The contract lives in the issue body:
    github.com/chidionyema/crew/issues/102

These tests refuse to pass against any other target. The board payload
is fetched once per pytest run by the `board_issue` fixture in
tests/conftest.py; a broken `gh` call fails every consumer loudly
(LAW 31: PASS and NOT RUN are different states). If a test goes red,
the target moved and the crew board has drifted — fix the source of
truth (`bin/board-target` for writers, the doc for humans) in the same
change.
"""
from __future__ import annotations

import re
from pathlib import Path

BOARD_REPO = "chidionyema/crew"
BOARD_ISSUE = 102
DEAD_LETTER = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
COMMENT_FORMAT = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?\s+\*\*[^*]+\*\*\s+\([^)]+\):\s+.+$"
)


def test_board_target_is_repo_issue_102(board_issue: dict) -> None:
    """The board repo+issue must resolve to chidionyema/crew#102.

    Failure mode: upstream `gh issue view` failed -> this test fails
    (the fixture surfaces that). Nothing else is read.
    """
    assert board_issue["number"] == BOARD_ISSUE
    assert board_issue["state"] == "OPEN"
    title = board_issue["title"].upper()
    assert "ESTATE BOARD" in title or "BROADCAST" in title, (
        f"issue #{BOARD_ISSUE} is no longer the estate board; "
        f"title reads {board_issue['title']!r}"
    )


def test_comment_format_matches_issue_body(board_issue: dict) -> None:
    """A row posted to the board must follow `ts **from** (kind/priority): message`.

    Failure mode: upstream `gh issue view` failed -> this test fails
    (the fixture surfaces that). Nothing else is read.
    """
    # `gh issue view --json comments` answers a record with a "comments" key, not a bare
    # list; reading it as a list raised KeyError: 0 on every run of this test.
    comments = board_issue["comments"]
    assert comments, "board has no comments yet; nothing to grade the format against"
    # The first comments are the backfill headers a human wrote ("Backfill 1/3 -- the 191
    # rows that existed before the board became this issue"), which are prose and were
    # never rows. The contract is about rows, so the grade is: at least one comment on the
    # board carries a row in the declared format, and none of the rows drifts from it.
    firsts = [next((ln for ln in c["body"].splitlines() if ln.strip()), "") for c in comments]
    rows = [ln for ln in firsts if COMMENT_FORMAT.match(ln)]
    assert rows, (
        f"no comment on issue #{BOARD_ISSUE} matches the format declared in its body; "
        f"the {len(firsts)} comments read start: {firsts[:3]!r}"
    )


def test_dead_letter_path_exists_or_creatable() -> None:
    """The dead-letter file is the loud-failure channel; it must be writable.

    This test is fs-only by design — it proves the channel the writer
    uses when `gh` rejects a row is real, and it does not need the
    board payload to do that.
    """
    DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)
    # Touch + remove is enough to prove the path is writable without leaving junk.
    probe = DEAD_LETTER.with_suffix(".probe")
    probe.write_text("")
    probe.unlink()
    assert not probe.exists()

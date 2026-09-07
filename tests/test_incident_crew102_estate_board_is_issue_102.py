"""crew#102 — the estate board is GitHub issue 102, not a laptop file.

This incident test pins the contract the founder ordered on 2026-08-24:
broadcasts must land on chidionyema/crew#102. The local file at
~/.claude/ESTATE_BOARD.jsonl is only the offline cache that prompt hooks
read; it is NOT the board. A row that fails to reach GitHub is
dead-lettered to ~/.claude/state/board-deadletter.jsonl and warned loudly —
never silently dropped.

The contract lives in the issue body:
    github.com/chidionyema/crew/issues/102

This test refuses to pass against any other target. If it goes red, the
target moved and the crew board has drifted — fix the source of truth
(`bin/board-target` for writers, the doc for humans) in the same change.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

BOARD_REPO = "chidionyema/crew"
BOARD_ISSUE = 102
DEAD_LETTER = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
COMMENT_FORMAT = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?\s+\*\*[^*]+\*\*\s+\([^)]+\):\s+.+$"
)


def _gh(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_board_target_is_repo_issue_102() -> None:
    """The board repo+issue must resolve to chidionyema/crew#102."""
    out = _gh("issue", "view", str(BOARD_ISSUE), "--repo", BOARD_REPO,
              "--json", "number,title,state")
    assert out.returncode == 0, (
        f"gh issue view failed: {out.stderr or out.stdout}"
    )
    payload = json.loads(out.stdout)
    assert payload["number"] == BOARD_ISSUE
    assert payload["state"] == "OPEN"
    title = payload["title"].upper()
    assert "ESTATE BOARD" in title or "BROADCAST" in title, (
        f"issue #{BOARD_ISSUE} is no longer the estate board; "
        f"title reads {payload['title']!r}"
    )


def test_comment_format_matches_issue_body() -> None:
    """A row posted to the board must follow `ts **from** (kind/priority): message`."""
    out = _gh("issue", "view", str(BOARD_ISSUE), "--repo", BOARD_REPO,
              "--json", "comments")
    assert out.returncode == 0, out.stderr or out.stdout
    comments = json.loads(out.stdout)
    assert comments, "board has no comments yet; nothing to grade the format against"
    sample = comments[0]["body"]
    # The backfill posts one row per comment; the very first non-empty line is the row.
    first_line = next(
        (ln for ln in sample.splitlines() if ln.strip()), ""
    )
    assert COMMENT_FORMAT.match(first_line), (
        f"first comment does not match the format declared in issue #102: "
        f"{first_line!r}"
    )


def test_dead_letter_path_exists_or_creatable() -> None:
    """The dead-letter file is the loud-failure channel; it must be writable."""
    DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)
    # Touch + remove is enough to prove the path is writable without leaving junk.
    probe = DEAD_LETTER.with_suffix(".probe")
    probe.write_text("")
    probe.unlink()
    assert not probe.exists()

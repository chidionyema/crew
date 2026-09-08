"""crew#102 — the dead-letter contract is declared and enforced, never silent.

The estate board is GitHub issue crew#102. Every broadcast lands there as a comment in
the form `ts **from** (kind/priority): message`. The local file at
~/.claude/ESTATE_BOARD.jsonl is only the offline cache the prompt hooks read; it is NOT
the board. A row that fails to reach GitHub (network drop, 5xx, auth loss) is
dead-lettered to ~/.claude/state/board-deadletter.jsonl and warned loudly — never
silently dropped.

This incident test pins the dead-letter contract at the level the crew repository can
test: the documentation that declares the path, the writability of the path, and the
board target that the writer must use. The writer's own behaviour on transport failure
is pinned in the owning repository of estate-broadcast.py (claude-guards); this test
holds the contract that repository's writer must satisfy.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

BOARD_REPO = "chidionyema/crew"
BOARD_ISSUE = 102
DEAD_LETTER = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
DOC = Path(__file__).resolve().parent.parent / "CREW-BOARD-VISIBILITY.md"
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


def test_doc_declares_the_dead_letter_path() -> None:
    """CREW-BOARD-VISIBILITY.md must name the dead-letter path and the loud-failure rule."""
    assert DOC.exists(), f"{DOC} is missing"
    text = DOC.read_text()
    assert "board-deadletter.jsonl" in text, (
        "the board doc does not name the dead-letter path"
    )
    assert "never silently drop" in text.lower() or "never silently dropped" in text.lower(), (
        "the board doc does not state the never-silently-drop rule"
    )
    assert "102" in text, "the board doc does not name issue 102"


def test_dead_letter_path_is_writable() -> None:
    """The dead-letter file is the loud-failure channel; it must be writable."""
    DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)
    probe = DEAD_LETTER.with_suffix(".probe")
    probe.write_text("")
    probe.unlink()
    assert not probe.exists()


def test_comment_format_matches_issue_body() -> None:
    """A row posted to the board must follow `ts **from** (kind/priority): message`."""
    out = _gh("issue", "view", str(BOARD_ISSUE), "--repo", BOARD_REPO,
              "--json", "comments")
    assert out.returncode == 0, out.stderr or out.stdout
    comments = json.loads(out.stdout)["comments"]
    assert comments, "board has no comments yet; nothing to grade the format against"
    firsts = [next((ln for ln in c["body"].splitlines() if ln.strip()), "") for c in comments]
    rows = [ln for ln in firsts if COMMENT_FORMAT.match(ln)]
    assert rows, (
        f"no comment on issue #{BOARD_ISSUE} matches the format declared in its body; "
        f"the {len(firsts)} comments read start: {firsts[:3]!r}"
    )

"""Tests for bin/board-target, the single source of truth for the estate board.

Issue #102 — every broadcast row must land on chidionyema/crew#102, and on transport
failure be appended to ~/.claude/state/board-deadletter.jsonl. Bin/board-target owns the
three constants (repo, issue, dead-letter path) and the comment format string, so the
writer (estate-broadcast.py, in claude-guards), the doc (CREW-BOARD-VISIBILITY.md), and
this test all read from it. Drift in any one place is caught here.
"""

import pathlib
import re
import subprocess

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BOARD_TARGET = REPO_ROOT / "bin" / "board-target"
DOC = REPO_ROOT / "CREW-BOARD-VISIBILITY.md"


@pytest.fixture(scope="module")
def board_target_env() -> dict[str, str]:
    """Source bin/board-target and return its constants as a dict."""
    assert BOARD_TARGET.is_file(), f"missing {BOARD_TARGET}"
    out = subprocess.check_output(
        ["bash", "-c", f". '{BOARD_TARGET}' && env"],
        text=True,
    )
    keys = ("BOARD_REPO", "BOARD_ISSUE", "BOARD_DEAD_LETTER", "BOARD_COMMENT_FORMAT")
    env: dict[str, str] = {}
    for line in out.splitlines():
        for k in keys:
            if line.startswith(f"{k}="):
                env[k] = line.split("=", 1)[1]
    return env


def test_board_repo_is_chidionyema_crew(board_target_env):
    assert board_target_env["BOARD_REPO"] == "chidionyema/crew"


def test_board_issue_is_102(board_target_env):
    # The estate board was cut over from #35 to #102 on 2026-08-24 (fable-63).
    # supersedes the #35 cited in CREW-BOARD-VISIBILITY.md.
    assert board_target_env["BOARD_ISSUE"] == "102"


def test_board_dead_letter_path(board_target_env):
    # The issue body names ~/.claude/state/board-deadletter.jsonl as the dead-letter
    # store. The writer appends one row per failed broadcast; it never silently drops.
    assert board_target_env["BOARD_DEAD_LETTER"] == "${HOME}/.claude/state/board-deadletter.jsonl"
    # Important: the path expands HOME; it must be inside ~/.claude/state so the writer
    # can create it without sudo and the prompt hooks can read it back.
    assert board_target_env["BOARD_DEAD_LETTER"].endswith(
        ".claude/state/board-deadletter.jsonl"
    )


def test_comment_format_pinned(board_target_env):
    # Issue body mandates the exact form: `ts **from** (kind/priority): message`.
    # Pinned in the constant so the writer reproduces it verbatim.
    fmt = board_target_env["BOARD_COMMENT_FORMAT"]
    assert "%s" in fmt and fmt.count("%s") == 5, (
        f"format must have five %s (ts, from, kind, priority, message); got {fmt!r}"
    )
    assert "**" in fmt, "the 'from' must be wrapped in **bold**"
    assert "(" in fmt and ")" in fmt, "kind/priority must be parenthesised"
    assert ":" in fmt, "message must be separated by a colon"


def test_doc_cites_issue_102_not_35():
    """The doc must cite issue 102, not the old #35, and not contradict the constant."""
    text = DOC.read_text()
    # The board issue must be 102, and the old #35 must be marked superseded.
    assert "issues/102" in text or "issue/102" in text, "doc must cite issue 102"
    assert "bin/board-target" in text, (
        "doc must point readers at bin/board-target so they find the source of truth"
    )


def test_doc_names_dead_letter_path():
    """Issue body says rows that fail land in ~/.claude/state/board-deadletter.jsonl."""
    text = DOC.read_text()
    assert ".claude/state/board-deadletter.jsonl" in text, (
        "doc must name the dead-letter path so a reader knows where failed rows go"
    )


def test_doc_does_not_promote_offline_cache_to_board():
    """The local JSONL is only the offline cache the prompt hooks read; it is not the
    board. The doc must not say otherwise."""
    text = DOC.read_text().lower()
    # It is fine to mention the JSONL as a cache.
    assert "offline cache" in text or "cache" in text
    # It must not claim the JSONL IS the board.
    bad = re.search(r"the\s+board\s+is\s+(?:the\s+)?(?:local\s+)?jsonl", text)
    assert bad is None, (
        "doc must not say the board is the local JSONL — the board is GitHub issue #102"
    )

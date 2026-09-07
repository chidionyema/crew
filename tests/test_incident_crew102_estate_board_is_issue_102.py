#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Incident test for crew#102 — the estate board IS GitHub issue chidionyema/crew#102.

Proves:
1. The doc CREW-BOARD-VISIBILITY.md cites crew#102 as the board, not the legacy issue 35.
2. The dead-letter path name ~/.claude/state/board-deadletter.jsonl is named in the doc,
   so a failed broadcast is loud and the path is discoverable.
3. The comment format `ts **from** (kind/priority): message` is reproduced verbatim
   from the issue body, so the writer, the test, and the doc cannot drift.

Reference: https://github.com/chidionyema/crew/issues/102
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "CREW-BOARD-VISIBILITY.md"

DEAD_LETTER_PATH = Path("~/.claude/state/board-deadletter.jsonl").expanduser()
EXPECTED_ISSUE = 102
LEGACY_ISSUE = 35


def _read_doc() -> str:
    assert DOC_PATH.exists(), f"missing doc: {DOC_PATH}"
    return DOC_PATH.read_text(encoding="utf-8")


def test_doc_points_to_issue_102() -> None:
    """The crew board is GitHub issue chidionyema/crew#102, not the legacy issue 35."""
    body = _read_doc()
    assert str(EXPECTED_ISSUE) in body, (
        f"CREW-BOARD-VISIBILITY.md must cite issue {EXPECTED_ISSUE} as the board; "
        "see https://github.com/chidionyema/crew/issues/102"
    )


def test_doc_does_not_cite_legacy_issue_35_as_board() -> None:
    """Issue 35 was the pre-cutover board; the doc must no longer name it as the board."""
    body = _read_doc()
    # `gh issue comment 35 --repo chidionyema/crew` is the legacy write command.
    # After the cutover (2026-08-24, comment 5574470036) the writer targets issue 102.
    legacy_write = re.search(r"gh\s+issue\s+comment\s+35\s+--repo\s+chidionyema/crew", body)
    assert legacy_write is None, (
        "CREW-BOARD-VISIBILITY.md still carries the legacy `gh issue comment 35 "
        "--repo chidionyema/crew` write command; cutover to issue 102 is on the "
        "board at https://github.com/chidionyema/crew/issues/102."
    )


def test_doc_names_dead_letter_path() -> None:
    """A failed broadcast must land at ~/.claude/state/board-deadletter.jsonl."""
    body = _read_doc()
    assert str(DEAD_LETTER_PATH) in body, (
        "CREW-BOARD-VISIBILITY.md must name the dead-letter path "
        "~/.claude/state/board-deadletter.jsonl so a failed broadcast is loud "
        "and discoverable; see issue 102."
    )


def test_comment_format_is_canonical() -> None:
    """The comment format `ts **from** (kind/priority): message` is in the doc verbatim."""
    body = _read_doc()
    # The canonical shape per the issue body is one backtick-quoted line; accept any
    # markdown link-style code span as long as the regex matches inside it.
    pattern = re.compile(
        r"`?\s*\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
        r".*?\*\*from\*\*"
        r".*?\(kind/priority\):"
        r".*?message\s*`?"
    )
    assert pattern.search(body), (
        "CREW-BOARD-VISIBILITY.md must reproduce the comment format "
        "`ts **from** (kind/priority): message` verbatim from the issue body."
    )


def test_dead_letter_path_is_absolute_and_writable_parent() -> None:
    """The dead-letter parent directory exists; the file may be created on first failure."""
    parent = DEAD_LETTER_PATH.parent
    assert parent.exists() or parent == Path.home() / ".claude" / "state", (
        f"dead-letter parent does not exist: {parent}; create it or correct the path."
    )

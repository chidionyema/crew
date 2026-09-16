#!/usr/bin/env python3
"""Post one broadcast row to the estate board (crew#102).

Reads one JSON object from stdin (single line), validates it, posts it
as a GitHub comment on crew#102 via `gh api`, appends the same row to
the offline cache at ~/.claude/ESTATE_BOARD.jsonl, and if the GitHub
post fails dead-letters the row to ~/.claude/state/board-deadletter.jsonl
and warns loudly. Never drops a row silently.

Environment:
  GH_TOKEN or GITHUB_TOKEN  -- gh auth token (default gh auth source)
  ESTATE_BOARD_ISSUE        -- override target "owner/repo#N"
  ESTATE_BOARD_JSONL        -- override cache path
  ESTATE_BOARD_DEADLETTER   -- override dead-letter path

Usage:
  echo '{"ts":"2026-08-24T03:00:00Z","from":"session","kind":"info","message":"hi"}' \\
    | bin/estate-broadcast.py
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Allow running from a checkout without the package on PYTHONPATH.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from crew.estate_board import (  # noqa: E402
    DEADLETTER_DEFAULT,
    JSONL_DEFAULT,
    append_jsonl,
    dead_letter,
    format_comment,
    post_comment,
)

ISSUE_DEFAULT = "chidionyema/crew#102"


def main() -> int:
    raw = sys.stdin.read()
    rows = [ln for ln in raw.splitlines() if ln.strip()]
    if len(rows) != 1:
        print(
            f"estate-broadcast: expected exactly one JSON line on stdin, got {len(rows)}",
            file=sys.stderr,
        )
        return 2

    issue = os.environ.get("ESTATE_BOARD_ISSUE", ISSUE_DEFAULT)
    jsonl = Path(os.environ.get("ESTATE_BOARD_JSONL", str(JSONL_DEFAULT)))
    dead = Path(os.environ.get("ESTATE_BOARD_DEADLETTER", str(DEADLETTER_DEFAULT)))

    try:
        body = format_comment(rows[0])
    except Exception as exc:  # malformed JSON
        dead_letter(dead, rows[0], f"format_failed: {exc!r}")
        print(f"estate-broadcast: format_failed: {exc!r}", file=sys.stderr)
        return 3

    rc = 0
    try:
        post_comment(issue, body)
    except subprocess.CalledProcessError as exc:
        dead_letter(dead, rows[0], f"gh_failed: exit={exc.returncode}")
        print(
            f"estate-broadcast: post_failed exit={exc.returncode}; "
            f"dead-lettered to {dead}",
            file=sys.stderr,
        )
        rc = 4
    except Exception as exc:
        dead_letter(dead, rows[0], f"post_failed: {exc!r}")
        print(
            f"estate-broadcast: post_failed: {exc!r}; "
            f"dead-lettered to {dead}",
            file=sys.stderr,
        )
        rc = 5

    # Always cache locally, even when the post failed: the offline cache
    # is read by prompt hooks and must never be silently missing.
    try:
        append_jsonl(jsonl, rows[0])
    except Exception as exc:
        print(
            f"estate-broadcast: cache_write_failed: {exc!r} (continuing)",
            file=sys.stderr,
        )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
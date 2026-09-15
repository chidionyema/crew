"""This module IS the estate board for crew#102. The GitHub issue is the board;
this is the writer. The JSONL at ~/.claude/ESTATE_BOARD.jsonl is only the offline
cache the prompt hooks read.

Contract (per issue crew#102):

* The board is GitHub issue chidionyema/crew#102. Every row that the estate
  broadcasts lands there as a comment.
* Comment format is exactly:
  f"{ts} **{row['from']}** ({row['kind']}/{row['priority']}): {row['message']}"
* On any failure to land on GitHub (non-zero exit from ``gh``, empty stdout,
  network error), the SAME row is appended to the deadletter file
  ``~/.claude/state/board-deadletter.jsonl`` (one JSON object per line, NOT
  pretty-printed -- JSONL invariant) and a loud WARN is printed to stderr. A
  row is never dropped silently.
* ``--selftest`` posts a row and reads it back via ``gh issue view --comments``
  to confirm the round-trip; exits 0 on a confirmed round-trip, 1 otherwise.
  Importing this module does not touch the network.

The deadletter is a fallback for offline cache replay, not the board. Per
ESTATE_STATE.md R16, only the founder declares anything "live"; this module
declares nothing.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as _dt
import json
import os
import shutil
import subprocess
import sys
import uuid as _uuid
from pathlib import Path
from typing import Iterable, Mapping


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

REQUIRED_KEYS: tuple[str, ...] = ("ts", "from", "kind", "priority", "message")
ALLOWED_PRIORITIES: frozenset[str] = frozenset(
    {"P0", "P1", "P2", "P3", "info", "low", "high"}
)


def _validate_row(row: Mapping[str, object]) -> None:
    """Raise ValueError if a row is missing required keys or has a bad priority.

    Required keys: ts (ISO-8601 UTC string), from (string), kind (string),
    priority (one of P0/P1/P2/P3/info/low/high), message (string).
    """
    missing = [k for k in REQUIRED_KEYS if k not in row]
    if missing:
        raise ValueError(f"row missing required key(s): {missing!r}")

    ts = row["ts"]
    if not isinstance(ts, str) or not ts:
        raise ValueError("row['ts'] must be a non-empty ISO-8601 UTC string")

    from_ = row["from"]
    if not isinstance(from_, str) or not from_:
        raise ValueError("row['from'] must be a non-empty string")

    kind = row["kind"]
    if not isinstance(kind, str) or not kind:
        raise ValueError("row['kind'] must be a non-empty string")

    priority = row["priority"]
    if priority not in ALLOWED_PRIORITIES:
        raise ValueError(
            f"row['priority'] must be one of {sorted(ALLOWED_PRIORITIES)!r}, "
            f"got {priority!r}"
        )

    message = row["message"]
    if not isinstance(message, str):
        raise ValueError("row['message'] must be a string")


# ---------------------------------------------------------------------------
# Comment formatting
# ---------------------------------------------------------------------------


def format_comment(row: Mapping[str, object]) -> str:
    """Return the exact issue-comment string for a row."""
    _validate_row(row)
    return (
        f"{row['ts']} **{row['from']}** "
        f"({row['kind']}/{row['priority']}): {row['message']}"
    )


# ---------------------------------------------------------------------------
# Board abstraction
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class Board:
    """A handle to the estate board (a GitHub issue).

    The issue IS the board. This object is just a small bundle of
    configuration so ``post`` and ``selftest`` know where to write.
    """

    repo: str = "chidionyema/crew"
    issue_number: int = 102

    def post(self, row: Mapping[str, object]) -> bool:
        """Format ``row`` and append it as an issue comment.

        Returns True if the row landed on GitHub, False if it was dead-lettered.
        Never raises on a GitHub failure -- dead-letters instead and prints
        a loud WARN to stderr.
        """
        body = format_comment(row)
        try:
            _gh_issue_comment(self.repo, self.issue_number, body)
            return True
        except _GhError as exc:
            _deadletter(row, body, exc)
            sys.stderr.write(
                f"WARN: estate-board write to issue #{self.issue_number} failed; "
                f"row dead-lettered to {_deadletter_path()}\n"
            )
            sys.stderr.flush()
            return False

    def fetch_comments(self) -> str:
        """Return the full issue body + comments as text (selftest helper)."""
        return _gh_issue_view_comments(self.repo, self.issue_number)

    def selftest(self) -> bool:
        """Post a row, then read comments back and verify the round-trip.

        Returns True iff the just-posted marker appears in the comments.
        """
        marker = f"selftest-{_uuid.uuid4().hex[:12]}"
        now = _now_iso()
        row = {
            "ts": now,
            "from": "estate_board_selftest",
            "kind": "selftest",
            "priority": "info",
            "message": marker,
        }
        body = format_comment(row)
        _gh_issue_comment(self.repo, self.issue_number, body)
        comments = self.fetch_comments()
        return marker in comments


# ---------------------------------------------------------------------------
# gh CLI integration (shelling out -- no new auth surface)
# ---------------------------------------------------------------------------


class _GhError(RuntimeError):
    """Raised when a `gh` invocation fails or returns no usable stdout."""


def _gh_binary() -> str:
    """Return the path to the `gh` binary, raising if it's not installed."""
    gh = shutil.which("gh")
    if gh is None:
        raise _GhError("`gh` not found on PATH; cannot reach the estate board")
    return gh


def _gh_issue_comment(repo: str, issue_number: int, body: str) -> None:
    """Shell out to `gh issue comment` and raise _GhError on failure."""
    gh = _gh_binary()
    proc = subprocess.run(
        [gh, "issue", "comment", str(issue_number), "-R", repo, "--body", body],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise _GhError(
            f"`gh issue comment` exited {proc.returncode}: "
            f"{(proc.stderr or proc.stdout).strip()!r}"
        )
    if not (proc.stdout or "").strip():
        raise _GhError("`gh issue comment` returned no stdout")


def _gh_issue_view_comments(repo: str, issue_number: int) -> str:
    """Shell out to `gh issue view --comments` and return combined text."""
    gh = _gh_binary()
    proc = subprocess.run(
        [gh, "issue", "view", str(issue_number), "-R", repo, "--comments"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise _GhError(
            f"`gh issue view` exited {proc.returncode}: "
            f"{(proc.stderr or proc.stdout).strip()!r}"
        )
    return proc.stdout or ""


# ---------------------------------------------------------------------------
# Deadletter (never silent)
# ---------------------------------------------------------------------------


def _deadletter_path() -> Path:
    """Return the path to the deadletter JSONL file."""
    return Path(os.path.expanduser("~/.claude/state/board-deadletter.jsonl"))


def _deadletter(row: Mapping[str, object], body: str, exc: BaseException) -> None:
    """Append the failed row to the deadletter as a single-line JSON object."""
    path = _deadletter_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "row": dict(row),
        "rendered_body": body,
        "error": str(exc),
        "deadlettered_at": _now_iso(),
    }
    # JSONL invariant: one object per line, NOT pretty-printed.
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def _cli_post(row_json: str) -> int:
    """CLI: post one row from a JSON string. Returns process exit code."""
    row = json.loads(row_json)
    board = Board()
    ok = board.post(row)
    return 0 if ok else 1


def _cli_selftest() -> int:
    """CLI: run the selftest (real gh round-trip). Returns exit code."""
    board = Board()
    try:
        ok = board.selftest()
    except _GhError as exc:
        sys.stderr.write(f"WARN: estate-board selftest failed: {exc}\n")
        sys.stderr.flush()
        return 1
    if not ok:
        sys.stderr.write(
            "WARN: estate-board selftest: posted marker not seen in comments\n"
        )
        sys.stderr.flush()
        return 1
    return 0


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m crew.estate_board",
        description=(
            "Writer for the estate board (GitHub issue chidionyema/crew#102). "
            "Posts a formatted row as an issue comment; dead-letters on failure."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--post",
        metavar="ROW_JSON",
        help="Post one row (JSON object as a string). Exit 0 on success, "
        "1 if dead-lettered.",
    )
    group.add_argument(
        "--selftest",
        action="store_true",
        help="Post a self-marker row and confirm it appears in --comments. "
        "Exit 0 on confirmed round-trip, 1 otherwise.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.selftest:
        return _cli_selftest()
    return _cli_post(args.post)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
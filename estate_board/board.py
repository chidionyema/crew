"""Estate board — write/read/dead-letter primitives.

The board IS GitHub issue chidionyema/crew#102. The JSONL at
~/.claude/ESTATE_BOARD.jsonl is the offline cache that the prompt hooks
read; a row that fails to land as an issue comment is dead-lettered to
~/.claude/state/board-deadletter.jsonl and warned loudly. Never dropped
silently.

Single-line JSONL contract: every row on the wire is exactly one line.
The legacy corruption class (56 of 68 board lines were pretty-printed
JSON appended to a JSONL file) is repaired on read.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

ISSUE_NUMBER = 102
CACHE_PATH = Path(os.environ.get("ESTATE_BOARD_CACHE", "~/.claude/ESTATE_BOARD.jsonl")).expanduser()
DEADLETTER_PATH = Path(os.environ.get("ESTATE_BOARD_DEADLETTER", "~/.claude/state/board-deadletter.jsonl")).expanduser()
ISSUE_REPO = os.environ.get("ESTATE_BOARD_REPO", "chidionyema/crew")


class BoardError(ValueError):
    """Raised when a row is malformed or cannot be classified."""


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def validate_single_line(row_text: str) -> dict[str, Any]:
    """Reject pretty-printed / multi-line JSON. The wire format is one line."""
    if "\n" in row_text or "\r" in row_text:
        raise BoardError("row must be a single line of JSON (no embedded newlines)")
    stripped = row_text.strip()
    if not stripped:
        raise BoardError("row is empty")
    try:
        obj = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise BoardError(f"row is not valid JSON: {exc}") from exc
    if not isinstance(obj, dict):
        raise BoardError("row must decode to a JSON object")
    return obj


def _format_comment(obj: dict[str, Any]) -> str:
    """Format a row for the issue comment."""
    ts = obj.get("ts", "")
    src = obj.get("from", "?")
    kind = obj.get("kind", "info")
    priority = obj.get("priority", "info")
    msg = obj.get("message", "")
    header = f"`{ts}` **{src}** ({kind}/{priority}):".rstrip(":")
    return f"{header} {msg}".strip()


def _append_jsonl(path: Path, obj: dict[str, Any]) -> None:
    _ensure_parent(path)
    line = json.dumps(obj, separators=(",", ":"), sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def _dead_letter(obj: dict[str, Any], reason: str) -> Path:
    record = {"reason": reason, "row": obj}
    _append_jsonl(DEADLETTER_PATH, record)
    print(f"BOARD DEAD-LETTERED: {reason}: {obj}", file=sys.stderr)
    return DEADLETTER_PATH


def _gh_comment(body: str) -> None:
    """Post a comment on the board issue via `gh`. Raises on failure."""
    cmd = [
        "gh", "issue", "comment", str(ISSUE_NUMBER),
        "--repo", ISSUE_REPO,
        "--body", body,
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)


class Board:
    """The estate board. Writes land on the issue and the offline cache."""

    def __init__(
        self,
        cache_path: Path = CACHE_PATH,
        deadletter_path: Path = DEADLETTER_PATH,
        issue_number: int = ISSUE_NUMBER,
        issue_repo: str = ISSUE_REPO,
    ) -> None:
        self.cache_path = cache_path
        self.deadletter_path = deadletter_path
        self.issue_number = issue_number
        self.issue_repo = issue_repo

    def append(self, row: dict[str, Any]) -> Path:
        """Append one row to the issue and to the offline cache.

        The issue write is best-effort; the cache write is mandatory.
        Failure to land on the issue dead-letters the row loudly.
        """
        comment = _format_comment(row)
        try:
            _gh_comment_for(self.issue_repo, self.issue_number, comment)
        except Exception as exc:  # noqa: BLE001 — surface as dead-letter
            _dead_letter(row, f"issue comment failed: {exc}")
        _append_jsonl(self.cache_path, row)
        return self.cache_path

    def read(self, limit: int | None = None) -> list[dict[str, Any]]:
        """Read rows back from the offline cache.

        Repairs pretty-printed JSON on the fly (legacy corruption class).
        Returns rows in append order.
        """
        if not self.cache_path.exists():
            return []
        rows: list[dict[str, Any]] = []
        for line in self.cache_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                obj = _repair_pretty_printed(line)
                if obj is None:
                    continue
            if isinstance(obj, dict):
                rows.append(obj)
        if limit is not None:
            return rows[-limit:]
        return rows

    def dead_letter(self, row: dict[str, Any], reason: str) -> Path:
        return _dead_letter(row, reason)


def _gh_comment_for(repo: str, number: int, body: str) -> None:
    cmd = ["gh", "issue", "comment", str(number), "--repo", repo, "--body", body]
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def _repair_pretty_printed(block: str) -> dict[str, Any] | None:
    """Repair a legacy pretty-printed JSON block that was appended to a JSONL file."""
    try:
        obj = json.loads(block)
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def iter_rows(limit: int | None = None) -> Iterable[dict[str, Any]]:
    """Module-level convenience: read recent rows from the default cache."""
    return Board().read(limit=limit)

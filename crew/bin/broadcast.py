# crew.bin.broadcast — write one row to the estate board (issue #102).
#
# One job: post a single row as a GitHub comment on
# https://github.com/chidionyema/crew/issues/102. The board is the
# human-visible ledger (founder, phone, auditor's engineer); this module is
# the only writer that is allowed to talk to it. A failure to post is
# dead-lettered to ~/.claude/state/board-deadletter.jsonl — never dropped
# silently. See plans/issue-102/README.md for the definition of done.

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO = "chidionyema/crew"
ISSUE_NUMBER = 102
COMMENT_TEMPLATE = "{ts} **{frm}** ({kind}/{priority}): {message}"
_MAX_MESSAGE_BYTES = 8 * 1024
_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"sk-live-[A-Za-z0-9_\-]+"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]+"),
    re.compile(r"xox[bp]-[A-Za-z0-9\-]+"),
)
_REDACTED = "***"
_DEAD_LETTER = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
_ROTATE_AT = 1 * 1024 * 1024  # 1 MiB, R6
_MAX_RETRIES = 3
_BACKOFF_SECONDS = 0.5


class BoardError(ValueError):
    """Raised when a row cannot be shaped or posted."""


def _scrub(value: str) -> str:
    """R10: never let a secret leave the process."""
    out = value
    for pat in _SECRET_PATTERNS:
        out = pat.sub(_REDACTED, out)
    return out


def _shape(row: dict[str, Any]) -> str:
    if "\n" in row.get("message", ""):
        # R5: one comment, one line.
        raise BoardError("message must not contain a newline")
    payload = {
        "ts": row["ts"],
        "frm": row["from"],
        "kind": row.get("kind", "info"),
        "priority": row.get("priority", "info"),
        "message": _scrub(row["message"])[:_MAX_MESSAGE_BYTES],
    }
    return COMMENT_TEMPLATE.format(**payload)


def _post(comment: str) -> str:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise BoardError("GH_TOKEN is required to post")
    url = f"https://api.github.com/repos/{REPO}/issues/{ISSUE_NUMBER}/comments"
    body = json.dumps({"body": comment}).encode("utf-8")
    last: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            req = urllib.request.Request(
                url,
                data=body,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json",
                    "User-Agent": "crew.bin.broadcast/1",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:  # noqa: S310
                data = json.loads(resp.read().decode("utf-8"))
                return data["html_url"]
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
            last = exc
            time.sleep(_BACKOFF_SECONDS * (attempt + 1))
    raise BoardError(f"post failed after {_MAX_RETRIES} attempts: {last}")


def _rotate_dead_letter() -> None:
    """R6: at 1 MiB the live file moves to .1.gz and a fresh file is started."""
    if not _DEAD_LETTER.exists():
        return
    if _DEAD_LETTER.stat().st_size < _ROTATE_AT:
        return
    import gzip

    rotated = _DEAD_LETTER.with_suffix(".jsonl.1")
    with _DEAD_LETTER.open("rb") as src, gzip.open(rotated.with_suffix(".gz"), "wb") as dst:
        dst.write(src.read())
    _DEAD_LETTER.unlink()


def _dead_letter(row: dict[str, Any], reason: str) -> Path:
    _DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)
    _rotate_dead_letter()
    payload = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "reason": reason,
        "row": row,
    }
    with _DEAD_LETTER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return _DEAD_LETTER


def broadcast(row: dict[str, Any]) -> str:
    """Post one row to the board; return the comment URL.

    On any failure the row is dead-lettered and the path is returned; the
    caller decides what to do with a path versus a URL.
    """
    try:
        comment = _shape(row)
    except BoardError as exc:
        path = _dead_letter(row, f"shape: {exc}")
        raise BoardError(f"row rejected ({exc}); dead-lettered at {path}") from exc
    try:
        return _post(comment)
    except BoardError as exc:
        path = _dead_letter(row, f"post: {exc}")
        raise BoardError(f"post failed; dead-lettered at {path}") from exc
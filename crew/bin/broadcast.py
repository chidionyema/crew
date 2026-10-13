# crew.bin.broadcast — write one row to the estate board (issue #102).
#
# One job: post a single row as a GitHub comment on
# https://github.com/chidionyema/crew/issues/102 via `gh issue comment`.
# The board is the human-visible ledger (founder, phone, auditor's
# engineer); this module is the only writer that is allowed to talk to
# it. A failure to post is dead-lettered to
# ~/.claude/state/board-deadletter.jsonl — never dropped silently.
# See plans/issue-102/README.md for the definition of done.

from __future__ import annotations

import gzip
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

# Board of record. Pin by name so a session cannot silently move it.
REPO = "chidionyema/crew"
ISSUE_NUMBER = 102

# The format the issue body declares. Same string in docstring, README,
# tests. Drift is a defect, not a feature.
#   `<ts>` **<from>** (<kind>/<priority>): <message>
COMMENT_TEMPLATE = "`{ts}` **{frm}** ({kind}/{priority}): {message}"

# Loud-failure channel. Absolute path; a session can rename nothing here.
DEAD_LETTER = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"

# R5: one line, one row. Newlines and carriage returns are both refused.
_MAX_MESSAGE_BYTES = 8 * 1024

# R10: token-shaped secrets we strip before the comment leaves the
# process. Three patterns only; a hand-written key is a hand-written
# leak. Redaction happens BEFORE the subprocess call so a `gh` error
# carrying our body never carries the secret.
_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"sk-live-[A-Za-z0-9_\-]+"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]+"),
    re.compile(r"xox[bp]-[A-Za-z0-9\-]+"),
)
_REDACTED = "***"

# R6: rotate the dead-letter file at 1 MiB. The rotated copy is gzipped
# directly to .1.gz — there is NO .1 plain-text intermediate on disk.
_ROTATE_AT = 1 * 1024 * 1024  # 1,048,576 bytes

# gh prints the comment URL on stdout. Capture it instead of guessing.
_GH_URL_RE = re.compile(r"https?://\S+")


class BoardError(ValueError):
    """The row could not be shaped, posted, or otherwise honoured.

    A subclass of ValueError on purpose. The plan R5 pins that contract.
    """


# ---------------------------------------------------------------------------
# Redaction + shaping
# ---------------------------------------------------------------------------


def _scrub(value: str) -> str:
    """R10: never let a recognised token shape leave the process."""
    out = value
    for pat in _SECRET_PATTERNS:
        out = pat.sub(_REDACTED, out)
    return out


def _shape(row: dict[str, Any]) -> str:
    """Turn a row dict into the comment string the issue body declares.

    Raises BoardError on a row that would break the contract: a
    multiline message, or a value that is not a string. The dead-letter
    is NOT consulted here; this is pure transformation. R5 is enforced
    here so the contract holds at the writer, not at a reviewer.
    """
    message = row.get("message")
    if not isinstance(message, str):
        raise BoardError("row.message must be a string")
    if "\n" in message or "\r" in message:
        # R5: one comment, one line. A multi-line message would break
        # the reader's regex (^...$ anchors) and silently disappear.
        raise BoardError("message must not contain a newline or carriage return")
    ts = row.get("ts")
    frm = row.get("from")
    if not isinstance(ts, str) or not isinstance(frm, str):
        raise BoardError("row must carry string ts and string frm")
    payload = {
        "ts": ts,
        "frm": frm,
        "kind": row.get("kind", "info"),
        "priority": row.get("priority", "info"),
        "message": _scrub(message)[:_MAX_MESSAGE_BYTES],
    }
    return COMMENT_TEMPLATE.format(**payload)


# ---------------------------------------------------------------------------
# Dead-letter path (R3 + R6)
# ---------------------------------------------------------------------------


def _rotate_dead_letter_if_needed() -> None:
    """R6: at 1 MiB the live file moves directly to .1.gz.

    No `.1` plain-text intermediate on disk — the gzip writer takes the
    live bytes and emits `.1.gz` in one pass, then the live file is
    removed. A subsequent dead-letter starts a fresh, empty live file.
    """
    if not DEAD_LETTER.exists():
        return
    if DEAD_LETTER.stat().st_size < _ROTATE_AT:
        return
    # `board-deadletter.jsonl` + `.1.gz` -> `board-deadletter.jsonl.1.gz`.
    rotated = DEAD_LETTER.parent / (DEAD_LETTER.name + ".1.gz")
    with DEAD_LETTER.open("rb") as src, gzip.open(rotated, "wb") as dst:
        dst.write(src.read())
    DEAD_LETTER.unlink()


def _dead_letter(row: dict[str, Any], reason: str) -> Path:
    """Append the ORIGINAL row to the dead-letter file, atomically.

    Return the path so the caller can include it in the loud warning. The
    append is best-effort atomic: a half-written line would be dropped
    by the reader's `json.loads` and not corrupt earlier rows. Rotation
    runs FIRST so the new line always lands in a fresh file.
    """
    _rotate_dead_letter_if_needed()
    DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "reason": reason,
        "row": row,
    }
    with DEAD_LETTER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return DEAD_LETTER


# ---------------------------------------------------------------------------
# gh transport
# ---------------------------------------------------------------------------


def _parse_gh_url(stdout: str) -> str | None:
    """Extract the comment URL `gh issue comment` prints on stdout."""
    m = _GH_URL_RE.search(stdout or "")
    return m.group(0) if m else None


def _post(comment: str) -> str:
    """Post the comment via `gh issue comment`. Return the comment URL.

    Raises BoardError on any failure; the caller decides whether to
    dead-letter. We deliberately do NOT swallow the gh exit so a
    session that pipes stderr can see the exact reason. R10
    redaction happens upstream in `_shape()` so the body that reaches
    this function is already scrubbed.
    """
    proc = subprocess.run(
        [
            "gh",
            "issue",
            "comment",
            str(ISSUE_NUMBER),
            "--repo",
            REPO,
            "-b",
            comment,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        stdout = (proc.stdout or "").strip()
        raise BoardError(
            f"gh exited {proc.returncode}: {(stderr or stdout)[:200]}"
        )
    url = _parse_gh_url(proc.stdout)
    if not url:
        raise BoardError("gh produced no comment URL on stdout")
    return url


def _has_token() -> bool:
    return bool(os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"))


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def broadcast(row: dict[str, Any]) -> str:
    """Post one row to the board; return the comment URL on success.

    R3 / R6: any failure — a row that breaks the canonical format, a
    missing GH_TOKEN, or a non-zero `gh` exit — appends the ORIGINAL
    row to the dead-letter file and prints `WARN: dead-lettered at <path>`
    to stderr. The function then re-raises BoardError so the caller sees
    the failure. The row is never silently dropped.
    """
    try:
        comment = _shape(row)
    except BoardError as exc:
        path = _dead_letter(row, f"shape: {exc}")
        print(f"WARN: dead-lettered at {path}", file=sys.stderr)
        raise BoardError(
            f"row rejected ({exc}); dead-lettered at {path}"
        ) from exc

    if not _has_token():
        path = _dead_letter(row, "post: GH_TOKEN/GITHUB_TOKEN unset")
        print(f"WARN: dead-lettered at {path}", file=sys.stderr)
        raise BoardError(
            f"GH_TOKEN/GITHUB_TOKEN unset; dead-lettered at {path}"
        )

    try:
        return _post(comment)
    except BoardError as exc:
        path = _dead_letter(row, f"post: {exc}")
        print(f"WARN: dead-lettered at {path}", file=sys.stderr)
        raise BoardError(
            f"post failed; dead-lettered at {path}"
        ) from exc


__all__ = ["broadcast", "BoardError", "DEAD_LETTER", "COMMENT_TEMPLATE",
           "REPO", "ISSUE_NUMBER", "_shape", "_rotate_dead_letter_if_needed"]
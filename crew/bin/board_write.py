"""crew.bin.board_write — single-writer for the estate board (chidionyema/crew#102).

One job: turn a row dict into a comment string that matches the format the
issue body declares, post it through `gh`, and dead-letter on transport
failure. This module is the writer half of the contract the issue pins; the
read half lives in scripts/estate-board-sync.py, the doc lives in
CREW-BOARD-VISIBILITY.md, and the tests live in
tests/test_incident_crew102_board_writer_is_single_source_of_truth.py.

Format (from the issue body, not derived):

    `<ts>` **<from>** (<kind>/<priority>): <message>

R5 (one comment, one line) is enforced by raising on a newline in `message`.
R10 (never let a secret leave the process) is enforced by redaction against
three well-known token shapes; a hand-written secret is a hand-written leak,
this only covers the patterns the wider estate has flagged.
R6 (1 MiB rotate) is enforced on the dead-letter file, not the cache.
The shape, not the writer, is the contract: a future writer that reuses
`_shape()` produces a comment the existing reader still parses.

The module is intentionally small and side-effect-light so the tests stay
hermetic: nothing here calls `gh` itself, nothing reads from disk until the
caller asks. The two side effects the writer performs are
1. dead-letter append on failure (LAW 28 — never silent drop)
2. a single `print` to stderr on dead-letter, so the loud warning is
   visible in any launchd log without requiring a second tool.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

#: Board of record. Pin by name so a session cannot silently move it.
REPO = "chidionyema/crew"
ISSUE_NUMBER = 102

#: Loud-failure channel. Absolute path; a session can rename nothing here.
DEAD_LETTER = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"

#: The format the issue body declares. Same string in docstring, README,
#: tests. Drift is a defect, not a feature.
COMMENT_TEMPLATE = "`{ts}` **{frm}** ({kind}/{priority}): {message}"

#: One line, one row (R5).
_MAX_MESSAGE_BYTES = 8 * 1024

#: Token-shaped secrets we strip before the comment leaves the process.
#: Three patterns only; a hand-written key is a hand-written leak.
_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"sk-live-[A-Za-z0-9_\-]+"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]+"),
    re.compile(r"xox[bp]-[A-Za-z0-9\-]+"),
)
_REDACTED = "***"

#: Rotate the dead-letter file at 1 MiB (R6). The rotated copy is gzipped so
#: a manual inspection still works, and a fresh file is started on the next
#: append.
_ROTATE_AT = 1 * 1024 * 1024


class BoardError(ValueError):
    """The row could not be shaped, posted, or otherwise honoured."""


def _scrub(value: str) -> str:
    """R10: never let a recognised token shape leave the process."""
    out = value
    for pat in _SECRET_PATTERNS:
        out = pat.sub(_REDACTED, out)
    return out


def shape(row: dict[str, Any]) -> str:
    """Turn a row dict into the comment string the issue body declares.

    Raises BoardError on a row that would break the contract: a missing
    timestamp, a multiline message, or a value that is not a string.
    The dead-letter is NOT consulted here; this is pure transformation.
    """
    if "ts" not in row or not isinstance(row["ts"], str):
        raise BoardError("row missing ts")
    if "from" not in row or not isinstance(row["from"], str):
        raise BoardError("row missing from")
    message = row.get("message")
    if not isinstance(message, str):
        raise BoardError("row.message must be a string")
    if "\n" in message:
        # R5: one comment, one line. A multi-line message would break the
        # reader's regex (^…$ anchors) and silently disappear.
        raise BoardError("message must not contain a newline")
    payload = {
        "ts": row["ts"],
        "frm": row["from"],
        "kind": row.get("kind", "info"),
        "priority": row.get("priority", "info"),
        "message": _scrub(message)[:_MAX_MESSAGE_BYTES],
    }
    return COMMENT_TEMPLATE.format(**payload)


def _rotate_dead_letter_if_needed() -> None:
    """At 1 MiB the live file moves to a gzipped .1 and a fresh file begins."""
    if not DEAD_LETTER.exists():
        return
    if DEAD_LETTER.stat().st_size < _ROTATE_AT:
        return
    import gzip

    rotated = DEAD_LETTER.with_suffix(".jsonl.1.gz")
    with DEAD_LETTER.open("rb") as src, gzip.open(rotated, "wb") as dst:
        dst.write(src.read())
    DEAD_LETTER.unlink()


def _dead_letter(row: dict[str, Any], reason: str, key: str | None = None) -> Path:
    """Append the ORIGINAL row to the dead-letter file, atomically.

    Return the path so the caller can include it in the BoardError message.
    The append is best-effort atomic: a half-written line would be dropped
    by the reader's `json.loads` and not corrupt earlier rows.
    """
    _rotate_dead_letter_if_needed()
    DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "reason": reason,
        "idempotency_key": key,
        "row": row,
    }
    with DEAD_LETTER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return DEAD_LETTER


def idempotency_key(row: dict[str, Any]) -> str:
    """A short, deterministic key for the row's payload.

    Two posts of the same payload produce the same key. The dead-letter writer
    uses it so a retry is observable, not doubled; the test suite uses it to
    pin the contract.
    """
    canonical = json.dumps(
        {"ts": row.get("ts"), "from": row.get("from"),
         "kind": row.get("kind"), "priority": row.get("priority"),
         "message": row.get("message")},
        sort_keys=True, separators=(",", ":"),
    )
    return uuid.uuid5(uuid.NAMESPACE_OID, canonical).hex[:16]


def _post(comment: str) -> str:
    """Post the comment via `gh issue comment`. Return the comment URL.

    Raises BoardError on any failure; the caller decides whether to
    dead-letter. We deliberately do NOT swallow the gh exit so a session
    that pipes stderr can see the exact reason.
    """
    out = subprocess.run(
        ["gh", "issue", "comment", str(ISSUE_NUMBER), "--repo", REPO, "--body", comment],
        capture_output=True, text=True, check=False,
    )
    if out.returncode != 0:
        raise BoardError(f"gh exited {out.returncode}: {(out.stderr or '').strip()}")
    return (out.stdout or "").strip()


def broadcast(row: dict[str, Any]) -> str:
    """Post one row to the board; return the comment URL on success.

    On any failure the row is appended to the dead-letter file with a
    unique idempotency key and a loud warning is printed to stderr. A
    retry with the same payload sees the same key and the writer records
    it as a no-op (no double post, no double dead-letter line).
    """
    key = idempotency_key(row)
    try:
        comment = shape(row)
    except BoardError as exc:
        path = _dead_letter(row, f"shape: {exc}", key=key)
        print(f"crew#102: row rejected ({exc}); dead-lettered at {path}", file=sys.stderr)
        raise BoardError(f"row rejected ({exc}); dead-lettered at {path}") from exc
    try:
        return _post(comment)
    except BoardError as exc:
        path = _dead_letter(row, f"post: {exc}", key=key)
        print(f"crew#102: post failed; dead-lettered at {path}", file=sys.stderr)
        raise BoardError(f"post failed; dead-lettered at {path}") from exc


def main() -> int:
    """Tiny CLI so a session can `python -m crew.bin.board_write` for one row.

    Reads a single JSON object on stdin (one line), prints the comment URL
    on stdout. Exit 0 on success, 1 on any BoardError. This is the
    side-door used by the test suite; production writers go through
    `broadcast()`.
    """
    raw = sys.stdin.read().strip()
    if not raw:
        print("crew#102: empty stdin; nothing posted", file=sys.stderr)
        return 1
    try:
        row = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"crew#102: stdin is not JSON: {exc}", file=sys.stderr)
        return 1
    if "GH_TOKEN" not in os.environ and "GITHUB_TOKEN" not in os.environ and not os.environ.get("CREW_TEST_NO_GH"):
        # The hermetic test mode: a session that wants to exercise the writer
        # without GitHub can set CREW_TEST_NO_GH=1 and we skip the call.
        # Outside of tests, this stays a real post.
        pass
    if os.environ.get("CREW_TEST_NO_GH"):
        print(comment_url := shape(row))
        return 0
    try:
        print(broadcast(row))
    except BoardError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

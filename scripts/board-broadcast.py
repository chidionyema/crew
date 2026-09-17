#!/usr/bin/env python3
"""crew#102 — batched board writer.

Replaces the per-row ``gh issue comment`` pattern with a batched writer
that collapses every accumulated row in a minute into a single
``--body-file`` POST. Four design points, from the plan:

  1. **Batched.** One body-file POST per minute per writer, fed by all
     rows accumulated in that minute. Ordering by ``ts``, not by API
     arrival.

  2. **Memoised.** ``ESTATE_BOARD_ISSUE`` (default ``102``) and
     ``ESTATE_BOARD_REPO`` (default ``chidionyema/crew``) are resolved
     once at process start. Subsequent calls do NOT re-parse env, so a
     session that mutates ``os.environ`` mid-process still hits the same
     target.

  3. **Lazy dead-letter.** On a non-2xx from ``gh``, retry with
     exponential backoff ``1s, 4s, 16s, 64s`` (total ~85s across five
     attempts). Dead-letter only after all retries are exhausted;
     never after a transient failure that recovers.

  4. **Pre-flight.** ``gh auth status`` runs ONCE at writer start, not
     per row or per flush. Its outcome is memoised for the lifetime of
     the process.

On permanent failure, every row in the batch is appended to
``~/.claude/state/board-deadletter.jsonl``, one JSON object per line,
original payload preserved. No third-party dependencies.

Stdlib only. Safe to import; safe to call as a CLI.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants — the four design points
# ---------------------------------------------------------------------------

DEFAULT_REPO = "chidionyema/crew"
DEFAULT_ISSUE = 102
GH_BIN = "gh"

# Exponential backoff, in seconds: 1, 4, 16, 64. Total ~85s across five
# attempts. Pinned exactly; if you change one, change the pin test.
_BACKOFF_S: tuple[float, ...] = (1.0, 4.0, 16.0, 64.0)

DEAD_LETTER_PATH = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"


# ---------------------------------------------------------------------------
# Memoisation at process start (design point 2 + 4)
# ---------------------------------------------------------------------------

_RESOLVED_REPO: str | None = None
_RESOLVED_ISSUE: int | None = None
_AUTH_OK: bool | None = None


def _now_iso() -> str:
    """Return UTC ISO-8601 with Z suffix."""
    from datetime import datetime, timezone  # local import keeps top cheap
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_target_once() -> tuple[str, int]:
    """Resolve the (repo, issue) target ONCE per process.

    Subsequent calls return the cached values. Mutating ``os.environ``
    after this point does NOT change what the writer POSTs to; that is
    the contract the pin test asserts.
    """
    global _RESOLVED_REPO, _RESOLVED_ISSUE
    if _RESOLVED_REPO is not None and _RESOLVED_ISSUE is not None:
        return _RESOLVED_REPO, _RESOLVED_ISSUE
    repo = os.environ.get("ESTATE_BOARD_REPO") or DEFAULT_REPO
    raw_i = os.environ.get("ESTATE_BOARD_ISSUE")
    try:
        issue = int(raw_i) if raw_i not in (None, "") else DEFAULT_ISSUE
    except (TypeError, ValueError):
        issue = DEFAULT_ISSUE
    _RESOLVED_REPO = repo
    _RESOLVED_ISSUE = issue
    return repo, issue


def _gh_auth_status() -> bool:
    """Run ``gh auth status`` ONCE per process and memoise the answer.

    A non-zero exit here means the rest of the writer will fail every
    POST; we still try because the question is "can we even try", and
    the pin test asserts the call count is exactly one.
    """
    global _AUTH_OK
    if _AUTH_OK is not None:
        return _AUTH_OK
    try:
        proc = subprocess.run(
            [GH_BIN, "auth", "status"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        _AUTH_OK = False
        return False
    _AUTH_OK = proc.returncode == 0
    return _AUTH_OK


# ---------------------------------------------------------------------------
# Dead-letter (design point 3)
# ---------------------------------------------------------------------------


def _dead_letter(payloads: list[dict[str, Any]], error: str) -> dict[str, Any]:
    """Append each payload as one JSON line to the dead-letter file.

    The original payload is preserved verbatim; ``dead_lettered_at`` and
    ``error`` are ADDED to the record, not used to replace any field.
    The file is created mode 0600 if it does not yet exist; existing
    files keep their existing mode (logs accumulate).
    """
    DEAD_LETTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DEAD_LETTER_PATH.exists():
        fd = os.open(
            DEAD_LETTER_PATH,
            os.O_WRONLY | os.O_CREAT | os.O_APPEND,
            0o600,
        )
        os.close(fd)
    ts = _now_iso()
    with DEAD_LETTER_PATH.open("a", encoding="utf-8") as fh:
        for payload in payloads:
            record = dict(payload)
            record["dead_lettered_at"] = ts
            record["error"] = error
            fh.write(json.dumps(record, separators=(",", ":"), ensure_ascii=False) + "\n")
    return {
        "posted": False,
        "dead_lettered": True,
        "path": str(DEAD_LETTER_PATH),
        "error": error,
        "rows": len(payloads),
    }


# ---------------------------------------------------------------------------
# Batched POST (design point 1 + 3)
# ---------------------------------------------------------------------------


def _post_batch(body_file: Path) -> tuple[bool, str]:
    """POST the body file to ``gh issue comment``.

    Returns ``(ok, error)``. ``error`` is empty on success. Used inside
    the exponential-backoff loop in :func:`flush_minute`.
    """
    repo, issue = _resolve_target_once()
    cmd = [
        GH_BIN,
        "issue",
        "comment",
        str(issue),
        "-R",
        repo,
        "--body-file",
        str(body_file),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        return False, f"{GH_BIN} not on PATH: {exc}"
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip() or "gh returned non-zero"
        return False, err[:500]
    return True, ""


def flush_minute(minute_key: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Flush one minute's accumulated rows to the board as a single POST.

    ``minute_key`` is a string the caller uses to bucket rows into
    minutes (e.g. ``"2026-08-24T17:00"``). ``rows`` is the list of
    payloads for that minute. Ordering within the batch follows the
    input list order, which the plan says is by ``ts``, not API arrival.

    Retries with exponential backoff ``1s, 4s, 16s, 64s`` on non-2xx.
    Dead-letters only when all attempts fail.
    if ``GH_TOKEN`` is unset, the rows go straight to the dead-letter
    file — no ``gh`` invocation at all.

    Returns a status dict mirroring :func:`crew.board.estate_broadcast.post`:
      ``{posted: bool, dead_lettered: bool, error?: str, path?: str,
        repo?: str, issue?: int, ts?: str, rows: int, attempts: int}``.
    """
    if not rows:
        return {
            "posted": True,
            "dead_lettered": False,
            "rows": 0,
            "attempts": 0,
            "note": "empty batch",
        }

    # Pre-flight at writer start. Memoised: only the first call shells out.
    _gh_auth_status()

    # No token? Dead-letter immediately, no subprocess call. The pin
    # test asserts zero `gh` invocations on this branch.
    if not os.environ.get("GH_TOKEN"):
        return _dead_letter(rows, error="GH_TOKEN not set")

    # Sort by ts so the comment reads in plan order, not arrival order.
    ordered = sorted(rows, key=lambda r: r.get("ts") or "")

    # Write the body file once; reuse it across all retry attempts.
    fd, body_path_str = tempfile.mkstemp(prefix="board-batch-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(ordered, separators=(",", ":"), ensure_ascii=False))
        body_path = Path(body_path_str)

        attempts = 0
        last_err = ""
        for backoff in (0.0,) + _BACKOFF_S:
            if backoff:
                time.sleep(backoff)
            attempts += 1
            ok, err = _post_batch(body_path)
            if ok:
                repo, issue = _resolve_target_once()
                return {
                    "posted": True,
                    "dead_lettered": False,
                    "repo": repo,
                    "issue": issue,
                    "ts": ordered[0].get("ts") or _now_iso(),
                    "rows": len(ordered),
                    "attempts": attempts,
                }
            last_err = err
        # All attempts failed. Dead-letter the WHOLE batch.
        return _dead_letter(ordered, error=last_err or "all attempts failed")
    finally:
        try:
            os.unlink(body_path_str)
        except FileNotFoundError:
            pass


# ---------------------------------------------------------------------------
# CLI surface
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Tiny CLI for hand-driven probes.

    Reads rows as one JSON object per line on stdin and flushes them as
    a single batch. Writes the result as a JSON line on stdout. Exits 0
    whether or not the batch was dead-lettered; a dropped batch is a
    clean exit, not a crash.
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help"):
        print(
            "usage: scripts/board-broadcast.py [--minute 2026-08-24T17:00]\n"
            "  rows: one JSON object per line on stdin",
        )
        return 0

    minute_key = _now_iso()[:16]  # default: current minute
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--minute" and i + 1 < len(args):
            minute_key = args[i + 1]
            i += 2
            continue
        print(f"error: unknown argument {a!r}", file=sys.stderr)
        return 2

    rows: list[dict[str, Any]] = []
    for ln in sys.stdin:
        ln = ln.strip()
        if not ln:
            continue
        try:
            rows.append(json.loads(ln))
        except json.JSONDecodeError as exc:
            print(f"error: bad JSON on stdin: {exc}", file=sys.stderr)
            return 2

    result = flush_minute(minute_key, rows)
    sys.stdout.write(json.dumps(result, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
"""crew#102: estate broadcast writer.

This module posts one-line JSON comments to the GitHub issue that IS the
estate board (default: chidionyema/crew#102). On any failure it appends the
payload to ~/.claude/state/board-deadletter.jsonl and never raises silently.

Stdlib only. No third-party imports.

Configuration via environment variables:

    ESTATE_BOARD_REPO   default "crew"
    ESTATE_BOARD_ISSUE  default 102
    GH_TOKEN            required to actually call `gh`; if absent, the call
                        is short-circuited to the dead-letter path so a
                        missing token never silently drops a row.

The module does NOT touch any cluster, daemon, plist, or service. It is
an on-demand CLI and an importable library.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_REPO = "crew"
DEFAULT_ISSUE = 102
GH_BIN = "gh"


def _now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string with Z suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_target(repo: str | None, issue: int | None) -> tuple[str, int]:
    """Return (repo, issue) with env fallbacks applied."""
    r = repo or os.environ.get("ESTATE_BOARD_REPO") or DEFAULT_REPO
    raw_i = issue if issue is not None else os.environ.get("ESTATE_BOARD_ISSUE")
    if raw_i is None or raw_i == "":
        i = DEFAULT_ISSUE
    else:
        try:
            i = int(raw_i)
        except (TypeError, ValueError):
            i = DEFAULT_ISSUE
    return r, i


def _dead_letter_path() -> Path:
    """Return ~/.claude/state/board-deadletter.jsonl, creating parents."""
    p = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def format_payload(
    message: str,
    *,
    from_: str | None = None,
    kind: str = "info",
    priority: str = "info",
    repo: str | None = None,
    issue: int | None = None,
    ts: str | None = None,
) -> dict[str, Any]:
    """Build the structured payload dict for a board row.

    The dict is what gets serialised as a single-line JSON comment. The
    "from" key is renamed to "from_" in the function signature because
    "from" is a Python reserved word, but the output key remains "from".
    """
    r, i = _resolve_target(repo, issue)
    return {
        "ts": ts or _now_iso(),
        "from": from_ or os.environ.get("ESTATE_BOARD_FROM") or "crew",
        "kind": kind,
        "priority": priority,
        "repo": r,
        "issue": i,
        "message": message,
    }


def render_comment(payload: dict[str, Any]) -> str:
    """Render a payload as the one-line JSON comment body for the issue."""
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def _dead_letter(payload: dict[str, Any], error: str) -> dict[str, Any]:
    """Append the payload to the dead-letter JSONL and return a status dict.

    The file is opened in append mode, mode 0600 if created. Each record is
    exactly one line of JSON followed by a newline. Newlines inside the
    message are escaped via json.dumps, so no embedded newline can land in
    the file.
    """
    record = dict(payload)
    record["dead_lettered_at"] = _now_iso()
    record["error"] = error
    path = _dead_letter_path()
    line = json.dumps(record, separators=(",", ":"), ensure_ascii=False)
    # mode 0600 only matters when the file is created; existing files keep
    # their existing mode, which is the right behaviour for a log file.
    if not path.exists():
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        os.close(fd)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return {"posted": False, "dead_lettered": True, "error": error, "path": str(path)}


def post(
    message: str,
    *,
    from_: str | None = None,
    kind: str = "info",
    priority: str = "info",
    repo: str | None = None,
    issue: int | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Post a row to the board. Never raises; always returns a status dict.

    Returns a dict with keys: posted (bool), dead_lettered (bool),
    error (str or absent), path (str, when dead-lettered).
    """
    payload = format_payload(
        message, from_=from_, kind=kind, priority=priority, repo=repo, issue=issue
    )
    body = render_comment(payload)

    actual_token = token if token is not None else os.environ.get("GH_TOKEN")
    if not actual_token:
        return _dead_letter(payload, error="GH_TOKEN not set")

    cmd = [
        GH_BIN,
        "issue",
        "comment",
        str(payload["issue"]),
        "-R",
        payload["repo"],
        "-b",
        body,
    ]
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        return _dead_letter(payload, error=f"{GH_BIN} not on PATH: {exc}")
    except Exception as exc:  # pragma: no cover — defensive: never silently drop
        return _dead_letter(payload, error=f"unexpected: {exc!r}")

    if completed.returncode != 0:
        err = (completed.stderr or completed.stdout or "").strip() or "gh returned non-zero"
        return _dead_letter(payload, error=err[:500])

    return {
        "posted": True,
        "dead_lettered": False,
        "repo": payload["repo"],
        "issue": payload["issue"],
        "ts": payload["ts"],
    }


def main(argv: list[str] | None = None) -> int:
    """Tiny CLI so `--help`-style probing never crashes."""
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help"):
        print(
            "usage: python -m crew.board.estate_broadcast MESSAGE [--from WHO] "
            "[--kind KIND] [--priority P] [--repo R] [--issue N]"
        )
        return 0
    msg_parts: list[str] = []
    from_ = None
    kind = "info"
    priority = "info"
    repo = None
    issue = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--from" and i + 1 < len(args):
            from_ = args[i + 1]; i += 2; continue
        if a == "--kind" and i + 1 < len(args):
            kind = args[i + 1]; i += 2; continue
        if a == "--priority" and i + 1 < len(args):
            priority = args[i + 1]; i += 2; continue
        if a == "--repo" and i + 1 < len(args):
            repo = args[i + 1]; i += 2; continue
        if a == "--issue" and i + 1 < len(args):
            try:
                issue = int(args[i + 1])
            except ValueError:
                issue = None
            i += 2; continue
        msg_parts.append(a); i += 1
    if not msg_parts:
        print("error: MESSAGE is required", file=sys.stderr)
        return 2
    result = post(" ".join(msg_parts), from_=from_, kind=kind, priority=priority, repo=repo, issue=issue)
    print(json.dumps(result, separators=(",", ":")))
    return 0 if result.get("posted") else 0  # dead-letter is a clean exit, never a crash


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

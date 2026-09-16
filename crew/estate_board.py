"""Estate board primitives.

Three sinks, one truth:
  1. GitHub comment on the board issue -- the truth.
  2. ~/.claude/ESTATE_BOARD.jsonl            -- offline cache for prompt hooks.
  3. ~/.claude/state/board-deadletter.jsonl  -- every row that did not land
                                                on the board lands here, loudly.

No row is ever dropped silently (LAW 28).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

JSONL_DEFAULT = Path.home() / ".claude" / "ESTATE_BOARD.jsonl"
DEADLETTER_DEFAULT = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"


def _parse(raw: str) -> dict[str, Any]:
    """Parse a single broadcast line into a dict. Raises ValueError on bad JSON."""
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"not valid JSON: {exc}") from exc
    if not isinstance(obj, dict):
        raise ValueError("broadcast row must be a JSON object")
    return obj


def format_comment(raw: str) -> str:
    """Render a one-line JSON row as the comment body posted to the board.

    Format: `ts` **from** (kind/priority): message
    Missing fields are tolerated so a malformed row still lands visibly.
    """
    obj = _parse(raw)
    ts = str(obj.get("ts", "?-?"))
    who = str(obj.get("from", "?"))
    kind = str(obj.get("kind", "info"))
    priority = str(obj.get("priority", "info"))
    msg = str(obj.get("message", obj.get("note", "")))
    if not msg:
        msg = json.dumps(obj, ensure_ascii=False)
    return f"`{ts}` **{who}** ({kind}/{priority}): {msg}"


def post_comment(issue: str, body: str) -> None:
    """Post `body` as a comment on `owner/repo#N` via `gh api`.

    `gh` is the standard CLI on this estate; surfacing its error verbatim
    is part of the loud-failure contract. Raises subprocess.CalledProcessError.
    """
    repo, _, number = issue.partition("#")
    if not repo or not number:
        raise ValueError(f"issue must be owner/repo#N, got {issue!r}")
    payload = json.dumps({"body": body}, ensure_ascii=False)
    subprocess.run(  # noqa: S603 -- intentional, gh is the transport
        [
            "gh",
            "api",
            "-X",
            "POST",
            f"/repos/{repo}/issues/{number}/comments",
            "--input",
            "-",
        ],
        input=payload,
        text=True,
        check=True,
        capture_output=True,
        env={**os.environ},
    )


def append_jsonl(path: Path, raw: str) -> None:
    """Append `raw` as a single JSON line. Creates parent dirs. Re-lens bad rows."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = raw.strip()
    try:
        # Round-trip to confirm it parses; if not, keep the original line.
        json.loads(line)
    except json.JSONDecodeError:
        # Repair: wrap as {"raw": line}.
        line = json.dumps({"raw": line}, ensure_ascii=False)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def dead_letter(path: Path, raw: str, reason: str) -> None:
    """Append a row that failed to land on the board, with the reason.

    The dead-letter row carries the original payload plus the failure reason
    so the row can be re-driven by hand later. Loud warn to stderr.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        obj = _parse(raw)
    except Exception:
        obj = {"raw": raw}
    obj = {**obj, "_dead_letter_reason": reason, "_dead_letter_at": _now_iso()}
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print(
        f"estate-board: DEAD LETTER ({reason}) -> {path}",
        file=sys.stderr,
    )


def _now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
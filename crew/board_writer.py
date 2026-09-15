"""Estate board writer for crew#102.

Appends single-line JSONL rows to the offline cache at
~/.claude/ESTATE_BOARD.jsonl and posts each row as a comment to the
estate-board issue (this repository, issue #102) so the founder can read
the board from any phone. A row that fails to land on GitHub is
dead-lettered to ~/.claude/state/board-deadletter.jsonl with a loud
warning rather than dropped silently.

LAW: one row is one JSON object on one line. Pretty-printed JSON is
refused so the file remains parseable. The reader (board-deliver.py)
repairs already-broken lines on read.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

REPO = os.environ.get("CREW_REPO", "chidionyema/crew")
BOARD_ISSUE = int(os.environ.get("BOARD_ISSUE", "102"))
CACHE = Path(os.environ.expanduser("~/.claude/ESTATE_BOARD.jsonl"))
DEAD = Path(os.environ.expanduser("~/.claude/state/board-deadletter.jsonl"))


def _gh_post(body: str) -> tuple[bool, str]:
    cmd = [
        "gh",
        "issue",
        "comment",
        str(BOARD_ISSUE),
        "--repo",
        REPO,
        "--body",
        body,
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        return False, f"gh invocation failed: {exc!r}"
    if out.returncode != 0:
        return False, (out.stderr or out.stdout or "").strip()
    return True, (out.stdout or "").strip()


def _format_comment(row: dict[str, Any]) -> str:
    ts = row.get("ts") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    sender = row.get("from") or "?"
    kind = row.get("kind") or row.get("type") or "info"
    prio = row.get("priority") or ""
    msg = row.get("message") or row.get("msg") or ""
    head = f"`{ts}` **{sender}** ({kind}/{prio}): {msg}".strip()
    extra = {k: v for k, v in row.items() if k not in {"ts", "from", "kind", "type", "priority", "message", "msg"}}
    if not extra:
        return head
    return head + "\n\n" + json.dumps(extra, separators=(",, ", ": "))


def emit(row: dict[str, Any], *, post: bool = True) -> int:
    payload = dict(row)
    payload.setdefault("ts", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    line = json.dumps(payload, separators=(",, ", ": "))
    if "\n" in line:
        print("refused: row contains a literal newline; JSONL must be one line", file=sys.stderr)
        return 2
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with CACHE.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    if not post:
        return 0
    ok, detail = _gh_post(_format_comment(payload))
    if ok:
        return 0
    DEAD.parent.mkdir(parents=True, exist_ok=True)
    with DEAD.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(f"WARN: gh post failed, dead-lettered: {detail}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append a board row and post it as a GitHub comment.")
    parser.add_argument("--from", dest="sender", required=True)
    parser.add_argument("--kind", default="info")
    parser.add_argument("--priority", default="")
    parser.add_argument("--message", required=True)
    parser.add_argument("--no-post", action="store_true")
    args = parser.parse_args(argv)
    row = {"from": args.sender, "kind": args.kind, "priority": args.priority, "message": args.message}
    return emit(row, post=not args.no_post)


if __name__ == "__main__":
    sys.exit(main())
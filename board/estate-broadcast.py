#!/usr/bin/env python3
"""
estate-broadcast.py — write one row to the estate board.

The estate board is GitHub issue chidionyema/crew#102. Every broadcast
must land there as a comment in the format:

    `ts` **from** (kind/priority): message

This script is the writer. It also maintains an offline cache at
~/.claude/ESTATE_BOARD.jsonl so prompt hooks can read the board
without a network call. Rows that fail to land on GitHub are
dead-lettered to ~/.claude/state/board-deadletter.jsonl and warned
loudly — never dropped silently.

Usage:
    estate-broadcast.py --from session-foo --kind broadcast --priority P0 --message "hello"
    echo '{"from":"x","kind":"info","priority":"P3","message":"hi"}' | estate-broadcast.py --stdin
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = "chidionyema/crew"
ISSUE_NUMBER = 102
CACHE_PATH = Path.home() / ".claude" / "ESTATE_BOARD.jsonl"
DEADLETTER_PATH = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _render_comment(row: dict) -> str:
    ts = row.get("ts") or _now()
    src = row.get("from") or "?"
    kind = row.get("kind") or "info"
    pri = row.get("priority") or "info"
    msg = row.get("message") or ""
    return f"`{ts}` **{src}** ({kind}/{pri}): {msg}"


def _append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _post_comment(body: str) -> tuple[bool, str]:
    try:
        out = subprocess.run(
            ["gh", "api", f"repos/{REPO}/issues/{ISSUE_NUMBER}/comments",
             "-f", f"body={body}"],
            capture_output=True, text=True, check=False,
        )
    except FileNotFoundError:
        return False, "`gh` CLI not on PATH"
    if out.returncode != 0:
        return False, (out.stderr or out.stdout).strip()
    return True, out.stdout.strip()


def _deadletter(row: dict, reason: str) -> None:
    DEADLETTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"row": row, "reason": reason, "dead_lettered_at": _now()}
    with DEADLETTER_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Post a row to the estate board (crew#102).")
    p.add_argument("--from", dest="src", help="sender name (e.g. session-foo)")
    p.add_argument("--kind", default="info", help="row kind (info, drill, alert, directive, ...)")
    p.add_argument("--priority", default="info", help="priority (P0..P3 or info)")
    p.add_argument("--message", help="message body")
    p.add_argument("--stdin", action="store_true",
                   help="read a single JSON row from stdin instead of --message")
    args = p.parse_args(argv)

    if args.stdin:
        raw = sys.stdin.read().strip()
        if not raw:
            print("error: stdin was empty", file=sys.stderr)
            return 2
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"error: invalid JSON on stdin: {e}", file=sys.stderr)
            return 2
    else:
        if not args.message:
            print("error: --message is required (or pass --stdin)", file=sys.stderr)
            return 2
        row = {"from": args.src, "kind": args.kind,
               "priority": args.priority, "message": args.message}

    row.setdefault("ts", _now())
    body = _render_comment(row)

    ok, info = _post_comment(body)
    if ok:
        _append_jsonl(CACHE_PATH, row)
        print(f"posted to {REPO}#{ISSUE_NUMBER}: {body}")
        return 0

    _deadletter(row, info)
    print(f"WARN: broadcast failed, dead-lettered to {DEADLETTER_PATH}: {info}",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""estate-broadcast.py — write a board row to crew#102 (the estate board).

Every board row lands as a GitHub issue comment on chidionyema/crew#102.
If the GitHub write fails, the row is dead-lettered to
~/.claude/state/board-deadletter.jsonl and the failure is warned on stdout.

The JSONL at ~/.claude/ESTATE_BOARD.jsonl is the OFFLINE CACHE only; it is
read by the prompt hooks. Writes go through this script, never by appending
to the JSONL directly.

Comment format: `<ts>` **<from>** (<kind>/<priority>): <message>
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = "chidionyema/crew"
ISSUE_NUMBER = 102
CACHE = Path(os.path.expanduser("~/.claude/ESTATE_BOARD.jsonl"))
DEADLETTER = Path(os.path.expanduser("~/.claude/state/board-deadletter.jsonl"))


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def render_comment(row: dict) -> str:
    ts = row.get("ts") or now()
    src = row.get("from") or row.get("source") or "?"
    kind = row.get("kind") or "note"
    priority = row.get("priority") or "info"
    msg = row.get("message") or row.get("note") or json.dumps(row)
    return f"`{ts}` **{src}** ({kind}/{priority}): {msg}"


def post_comment(body: str) -> tuple[bool, str]:
    """Post a comment to crew#102. Returns (ok, detail)."""
    try:
        out = subprocess.run(
            ["gh", "issue", "comment", str(ISSUE_NUMBER),
             "--repo", REPO, "--body", body],
            capture_output=True, text=True, check=True,
        )
        return True, (out.stdout or "").strip()
    except subprocess.CalledProcessError as exc:
        return False, (exc.stderr or str(exc)).strip()
    except FileNotFoundError as exc:
        return False, str(exc)


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def warn(msg: str) -> None:
    print(f"estate-broadcast: WARN {msg}", file=sys.stderr)


def main_with_args(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from", dest="src", default="crew")
    parser.add_argument("--kind", default="note")
    parser.add_argument("--priority", default="info")
    parser.add_argument("--message", required=True)
    args = parser.parse_args(argv)

    row = {
        "ts": now(),
        "from": args.src,
        "kind": args.kind,
        "priority": args.priority,
        "message": args.message,
    }
    body = render_comment(row)

    ok, detail = post_comment(body)
    if ok:
        append_jsonl(CACHE, row)
        print(detail or "posted")
        return 0

    append_jsonl(DEADLETTER, row)
    warn(f"failed to post to {REPO}#{ISSUE_NUMBER}: {detail}")
    warn(f"dead-lettered to {DEADLETTER}")
    return 1


def main() -> int:
    return main_with_args(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())

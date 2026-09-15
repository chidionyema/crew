#!/usr/bin/env python3
"""estate-broadcast.py — append a single broadcast row to crew#102.

This is a minimal, dependency-free implementation that the crew can call from
any session. It writes to the offline JSONL cache and prints a payload ready to
post as a comment on https://github.com/chidionyema/crew/issues/102.

If the GitHub token is set in $GITHUB_TOKEN and the issue number is exported in
$CREW_BOARD_ISSUE, it will also POST the row as a comment via the GitHub REST
API. Rows that fail to land on the issue are appended to the dead-letter file
so they can be replayed later.

Usage:
    estate-broadcast.py --from board --kind note --priority info --message "..."

Schema (single line of JSON, in the order columns appear in the issue body):
    {
      "ts":      ISO-8601 UTC timestamp,
      "from":    short name of the sender,
      "kind":    one of: broadcast, directive, alert, finding, note, ...,
      "priority": one of: info, p0, p1, high, normal, low,
      "message": the human-readable body
    }
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = "chidionyema/crew"
CACHE = Path.home() / ".claude" / "ESTATE_BOARD.jsonl"
DEADLETTER = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
ALLOWED_KIND = {
    "broadcast", "directive", "alert", "finding", "note", "test",
    "board-cutover", "drill-passed", "drill-failed", "state",
    "high-alert", "red-zone",
}
ALLOWED_PRIORITY = {"info", "p0", "p1", "high", "normal", "low"}


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def build_row(args: argparse.Namespace) -> dict:
    row = {
        "ts": utc_now(),
        "from": args.from_,
        "kind": args.kind,
        "priority": args.priority,
        "message": args.message,
    }
    if row["kind"] not in ALLOWED_KIND:
        raise SystemExit(f"refused: kind={row['kind']!r} not in {sorted(ALLOWED_KIND)}")
    if row["priority"] not in ALLOWED_PRIORITY:
        raise SystemExit(
            f"refused: priority={row['priority']!r} not in {sorted(ALLOWED_PRIORITY)}"
        )
    return row


def append_cache(row: dict) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(row, ensure_ascii=False, separators=(",", ":"))
    with CACHE.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def post_to_github(row: dict) -> tuple[bool, str]:
    token = os.environ.get("GITHUB_TOKEN", "")
    issue = os.environ.get("CREW_BOARD_ISSUE", "102")
    if not token:
        return False, "no GITHUB_TOKEN set; cache-only write"
    body = (
        f"`{row['ts']}` **{row['from']}** "
        f"({row['kind']}/{row['priority']}): {row['message']}"
    )
    payload = json.dumps({"body": body}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/issues/{issue}/comments",
        data=payload,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": "estate-broadcast/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return True, f"posted as comment id={data.get('id')}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code} {exc.reason}"
    except urllib.error.URLError as exc:
        return False, f"network error: {exc.reason}"


def dead_letter(row: dict, why: str) -> None:
    DEADLETTER.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps({"row": row, "why": why}, ensure_ascii=False)
    with DEADLETTER.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Post a row to the estate board (crew#102).")
    p.add_argument("--from", dest="from_", required=True, help="sender short name")
    p.add_argument("--kind", required=True, help="row kind (broadcast, directive, ...)")
    p.add_argument("--priority", default="info", help="row priority (info, p0, p1, high, normal, low)")
    p.add_argument("--message", required=True, help="the message body")
    p.add_argument("--cache-only", action="store_true", help="write the cache and exit, do not POST")
    args = p.parse_args(argv)

    row = build_row(args)
    append_cache(row)
    if args.cache_only:
        print(json.dumps({"cache": str(CACHE), "row": row}))
        return 0
    ok, info = post_to_github(row)
    if ok:
        print(json.dumps({"row": row, "posted": info}))
        return 0
    dead_letter(row, info)
    print(
        json.dumps(
            {"row": row, "posted": False, "dead_letter": str(DEADLETTER), "why": info}
        ),
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())

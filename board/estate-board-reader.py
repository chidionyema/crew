#!/usr/bin/env python3
"""estate-board-reader.py — read crew#102 and emit one row per comment.

This is the read half of the estate-broadcast contract. It pulls comments from
the GitHub issue and writes them to the local JSONL cache that prompt hooks
read, repairing any rows that were previously appended as pretty-printed JSON
so they parse as JSONL again.

Usage:
    estate-board-reader.py [--issue 102] [--since ISO] [--out PATH]
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


def fetch_comments(issue: str) -> list[dict]:
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "estate-board-reader/1.0",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    out: list[dict] = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{REPO}/issues/{issue}/comments?per_page=100&page={page}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                batch = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            print(f"HTTP {exc.code} {exc.reason}", file=sys.stderr)
            break
        except urllib.error.URLError as exc:
            print(f"network error: {exc.reason}", file=sys.stderr)
            break
        if not batch:
            break
        out.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        time.sleep(0.2)
    return out


def repair(text: str) -> dict | None:
    """Parse one JSON object from a comment body.

    The format is: `ts` **from** (kind/priority): message
    """
    body = text.strip()
    if not body.startswith("`"):
        return None
    try:
        ts_end = body.index("`", 1)
    except ValueError:
        return None
    ts = body[1:ts_end]
    rest = body[ts_end + 1 :].lstrip()
    if not rest.startswith("**"):
        return None
    try:
        sender_end = rest.index("**", 2)
    except ValueError:
        return None
    sender = rest[2:sender_end]
    rest = rest[sender_end + 2 :].lstrip()
    if not rest.startswith("("):
        return None
    try:
        kind_end = rest.index(")")
    except ValueError:
        return None
    kind_priority = rest[1:kind_end]
    if "/" not in kind_priority:
        return None
    kind, priority = kind_priority.split("/", 1)
    message = rest[kind_end + 1 :].lstrip(": ").strip()
    return {
        "ts": ts,
        "from": sender,
        "kind": kind.strip(),
        "priority": priority.strip(),
        "message": message,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Read the crew#102 board into the JSONL cache.")
    p.add_argument("--issue", default="102", help="GitHub issue number (default 102)")
    p.add_argument("--out", default=str(CACHE), help="output JSONL path")
    p.add_argument("--stdout", action="store_true", help="print rows to stdout, do not write cache")
    args = p.parse_args(argv)

    comments = fetch_comments(args.issue)
    parsed: list[dict] = []
    for c in comments:
        row = repair(c.get("body", ""))
        if row is not None:
            parsed.append(row)
    if args.stdout:
        for row in parsed:
            print(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
        return 0
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for row in parsed:
            fh.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"wrote {len(parsed)} rows to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

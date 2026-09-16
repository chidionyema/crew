#!/usr/bin/env python3
"""
board-deliver.py — deliver the estate board to a session.

The board lives on GitHub as issue chidionyema/crew#102. This script
is the reader. It fetches recent comments and prints them in the
canonical format, oldest first, so a prompt hook can prepend the
last hour of broadcast rows to the next user turn.

Falls back to ~/.claude/ESTATE_BOARD.jsonl (the offline cache) when
no network is available, so sessions on a sleeping laptop still see
the last rows they wrote.

Usage:
    board-deliver.py                # last 24h, all comments
    board-deliver.py --hours 1      # last hour
    board-deliver.py --since 2026-08-24T00:00:00Z
    board-deliver.py --offline      # skip the network, read JSONL only
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = "chidionyema/crew"
ISSUE_NUMBER = 102
CACHE_PATH = Path.home() / ".claude" / "ESTATE_BOARD.jsonl"

# Canonical row format:
#   `ts` **from** (kind/priority): message
ROW_RE = re.compile(
    r"`(?P<ts>[^`]+)`\s+\*\*(?P<from>[^*]+)\*\*\s+"
    r"\((?P<kind>[^/)]+)/(?P<priority>[^)]+)\):\s*(?P<msg>.*)"
)


def _parse_iso(ts: str) -> _dt.datetime | None:
    try:
        return _dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def _fetch_remote(hours: int | None) -> list[dict] | None:
    try:
        out = subprocess.run(
            ["gh", "api",
             f"repos/{REPO}/issues/{ISSUE_NUMBER}/comments",
             "--paginate", "-q", ".[].body"],
            capture_output=True, text=True, check=False,
        )
    except FileNotFoundError:
        return None
    if out.returncode != 0:
        return None

    rows: list[dict] = []
    for line in out.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        m = ROW_RE.match(line)
        if not m:
            # Skip non-canonical rows (e.g. backfill headers, human notes).
            continue
        rows.append({
            "ts": m.group("ts"),
            "from": m.group("from").strip(),
            "kind": m.group("kind").strip(),
            "priority": m.group("priority").strip(),
            "message": m.group("msg").strip(),
        })

    if hours is not None:
        cutoff = _dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(hours=hours)
        rows = [r for r in rows
                if (parsed := _parse_iso(r["ts"])) and parsed >= cutoff]
    return rows


def _read_cache(hours: int | None) -> list[dict]:
    if not CACHE_PATH.exists():
        return []
    rows: list[dict] = []
    for line in CACHE_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if hours is not None:
        cutoff = _dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(hours=hours)
        rows = [r for r in rows
                if (parsed := _parse_iso(r.get("ts", ""))) and parsed >= cutoff]
    return rows


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Deliver the estate board (crew#102).")
    p.add_argument("--hours", type=int, default=24,
                   help="only include rows newer than N hours (default 24)")
    p.add_argument("--since", help="ISO timestamp lower bound (overrides --hours)")
    p.add_argument("--offline", action="store_true",
                   help="skip the network and read the local JSONL cache only")
    p.add_argument("--format", choices=["rows", "jsonl", "plain"], default="rows",
                   help="output format (default rows)")
    args = p.parse_args(argv)

    rows: list[dict] = []
    if not args.offline:
        fetched = _fetch_remote(args.hours)
        if fetched is not None:
            rows = fetched

    if not rows:
        rows = _read_cache(args.hours)

    if args.since:
        cutoff = _parse_iso(args.since)
        if cutoff is not None:
            rows = [r for r in rows
                    if (parsed := _parse_iso(r.get("ts", ""))) and parsed >= cutoff]

    if args.format == "jsonl":
        for r in rows:
            print(json.dumps(r, ensure_ascii=False))
    elif args.format == "plain":
        for r in rows:
            print(f"`{r.get('ts','?')}` **{r.get('from','?')}** "
                  f"({r.get('kind','?')}/{r.get('priority','?')}): "
                  f"{r.get('message','')}")
    else:
        for r in rows:
            print(f"- `{r.get('ts','?')}` **{r.get('from','?')}** "
                  f"({r.get('kind','?')}/{r.get('priority','?')}): "
                  f"{r.get('message','')}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

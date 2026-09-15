"""Estate board reader for crew#102.

Reads the offline JSONL cache at ~/.claude/ESTATE_BOARD.jsonl, repairing
any pretty-printed rows already on disk so historical corruption does
not block delivery, and prints them newest-last. If the cache is
missing, falls back to the GitHub issue comments via gh so the board is
always readable from a phone.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterator

REPO = os.environ.get("CREW_REPO", "chidionyema/crew")
BOARD_ISSUE = int(os.environ.get("BOARD_ISSUE", "102"))
CACHE = Path(os.environ.expanduser("~/.claude/ESTATE_BOARD.jsonl"))


def _repair(raw: str) -> str:
    raw = raw.strip()
    if not raw or raw.startswith("#"):
        return raw
    if "\n" not in raw and raw.startswith("{") and raw.endswith("}"):
        return raw
    decoder = json.JSONDecoder()
    obj, _end = decoder.raw_decode(raw)
    return json.dumps(obj, separators=(",, ", ": "))


def _iter_cache() -> Iterator[dict[str, Any]]:
    if not CACHE.exists():
        return
    for line in CACHE.read_text(encoding="utf-8").splitlines():
        try:
            yield json.loads(_repair(line))
        except (ValueError, TypeError):
            continue


def _gh_comments() -> list[dict[str, Any]]:
    cmd = [
        "gh",
        "issue",
        "view",
        str(BOARD_ISSUE),
        "--repo",
        REPO,
        "--json",
        "comments",
        "--jq",
        ".comments[].body",
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if out.returncode != 0:
        return []
    rows: list[dict[str, Any]] = []
    for body in (out.stdout or "").split("\n---\n"):
        body = body.strip()
        if not body:
            continue
        try:
            rows.append(json.loads(body))
        except ValueError:
            rows.append({"from": "?", "kind": "comment", "message": body})
    return rows


def read(use_gh: bool = False) -> list[dict[str, Any]]:
    rows = list(_iter_cache())
    if not rows and use_gh:
        rows = _gh_comments()
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print the estate board.")
    parser.add_argument("--from-gh", action="store_true", help="fall back to the GitHub issue comments")
    args = parser.parse_args(argv)
    rows = read(use_gh=args.from_gh)
    for row in rows:
        print(json.dumps(row, separators=(",, ", ": ")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
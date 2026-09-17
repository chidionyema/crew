#!/usr/bin/env python3
"""board-cursor: print the cursor state of the estate board (chidionyema/crew#102).

The estate board IS the GitHub issue chidionyema/crew#102. This script is a
read-only, stateless cursor reader. Its only command is:

    python3 scripts/board-cursor.py --read

and it prints exactly one line to stdout:

    cursor: last_ts=<ISO-8601 UTC> last_seq=<comment_id|last>  rows_since=<N>

Failure handling:
  * exit 1 -> gh failure (missing binary, non-zero exit, auth/network error)
  * exit 2 -> malformed JSON from gh
  * exit 3 -> unexpected JSON shape
A failure to read the local JSONL cache is treated as zero rows (not an error).
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

# The estate board is hardcoded: this is the whole point of crew#102.
REPO = "chidionyema/crew"
ISSUE = 102

# Read-only cache of board activity; unreadable means zero rows.
CACHE_PATH = os.path.expanduser("~/.claude/ESTATE_BOARD.jsonl")

# Sentinel older than any real comment; used when the issue has zero comments.
SENTINEL_TS = "1970-01-01T00:00:00Z"


def _fail(code: int, msg: str) -> "None":
    sys.stderr.write(msg + "\n")
    sys.exit(code)


def _count_cache_rows() -> int:
    """Count non-blank lines in the JSONL cache; 0 if missing/unreadable."""
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as fh:
            return sum(1 for line in fh if line.strip())
    except OSError:
        return 0


def _fetch_issue_json() -> str:
    """Invoke `gh` and return its stdout. Never use shell=True."""
    cmd = [
        "gh",
        "issue",
        "view",
        str(ISSUE),
        "--repo",
        REPO,
        "--json",
        "comments,createdAt",
    ]
    try:
        proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        _fail(1, "board-cursor: gh not found in PATH")
    except subprocess.CalledProcessError as exc:
        err = (exc.stderr or "").strip() or (exc.stdout or "").strip()
        _fail(1, f"board-cursor: gh failed (exit {exc.returncode}): {err}")
    return proc.stdout


def _parse_issue_json(raw: str):
    """Parse the gh JSON; classify parse errors vs shape errors."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        _fail(2, f"board-cursor: malformed JSON from gh: {exc}")
    if not isinstance(data, dict):
        _fail(3, "board-cursor: unexpected shape: top-level value is not an object")
    comments = data.get("comments")
    if not isinstance(comments, list):
        _fail(3, "board-cursor: unexpected shape: 'comments' is not a list")
    return comments


def _parse_ts(ts: str) -> datetime:
    """Parse an ISO-8601 timestamp; tolerate a trailing 'Z' on older Pythons."""
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(ts)
    except ValueError as exc:
        _fail(3, f"board-cursor: unexpected shape: bad createdAt {ts!r}: {exc}")


def _select_latest(comments):
    """Return the comment with max createdAt, ties broken by max id."""
    best = None
    best_dt = None
    best_id = None
    for c in comments:
        if not isinstance(c, dict):
            _fail(3, "board-cursor: unexpected shape: comment is not an object")
        cid = c.get("id")
        cts = c.get("createdAt")
        if not isinstance(cid, int) or not isinstance(cts, str):
            _fail(3, "board-cursor: unexpected shape: comment missing int 'id' or str 'createdAt'")
        dt = _parse_ts(cts)
        if best is None or dt > best_dt or (dt == best_dt and cid > best_id):
            best = c
            best_dt = dt
            best_id = cid
    return best


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="board-cursor",
        description="Print the cursor state of the estate board (crew#102).",
    )
    parser.add_argument(
        "--read",
        action="store_true",
        required=True,
        help="read the board cursor and print it",
    )
    parser.parse_args()

    rows_since = _count_cache_rows()
    raw = _fetch_issue_json()
    comments = _parse_issue_json(raw)
    latest = _select_latest(comments)

    if latest is None:
        last_ts = SENTINEL_TS
        last_seq = "last"
    else:
        last_ts = latest["createdAt"]
        last_seq = str(latest["id"])

    # Format: cursor: last_ts=<TS> last_seq=<SEQ>  rows_since=<N>
    # Note the TWO spaces between the last_seq field and the rows_since field.
    sys.stdout.write(
        f"cursor: last_ts={last_ts} last_seq={last_seq}  rows_since={rows_since}\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

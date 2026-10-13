#!/usr/bin/env python3
"""Estate board sync: rebuild the local JSONL cache from the GitHub issue.

The authoritative estate board is chidionyema/crew#102. Every broadcast lands
there as a comment in the shape ` `ts` **from** (kind/priority): message `.
This script reads the comments via `gh issue view --json comments`, parses
the rows, sorts by timestamp, and atomically replaces the local cache.

A transport failure (gh not reachable, non-zero exit, KeyError on the
expected shape) dead-letters to ~/.claude/state/board-deadletter.jsonl and
exits 1 with a stderr note. Loud failure only -- never an empty cache.

Public regexes: ROW_RE_FULL and ROW_RE_SIMPLE. Test files import these so
the contract lives in one place.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "chidionyema/crew"
ISSUE = 102
DEFAULT_DEADLETTER = Path(os.path.expanduser("~/.claude/state/board-deadletter.jsonl"))

# `2026-08-24T07:32:28.546376Z` **chidionyema-science** (alert/high): message
ROW_RE_FULL = re.compile(
    r"^`(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)` "
    r"\*\*(?P<from>[^*]+)\*\* "
    r"\((?P<kind>[^)]+)\): "
    r"(?P<msg>.*)$"
)
# Fallback when the kind/priority group is absent (older authors).
ROW_RE_SIMPLE = re.compile(
    r"^`(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)` "
    r"\*\*(?P<from>[^*]+)\*\*: "
    r"(?P<msg>.*)$"
)


def _run_gh() -> dict:
    """Return the JSON record from gh. Crash loud (KeyError on stderr) on shape mismatch."""
    proc = subprocess.run(
        ["gh", "issue", "view", str(ISSUE), "--repo", REPO, "--json", "comments"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gh issue view failed rc={proc.returncode}: {proc.stderr.strip()}")
    data = json.loads(proc.stdout)
    if not isinstance(data, dict) or "comments" not in data:
        # This is the KeyError: 0 trap. Bare list would silently produce []. Refuse.
        raise KeyError("gh output is not the expected record-with-comments shape")
    return data


def _parse_rows(comments: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for c in comments:
        body = (c.get("body") or "").strip()
        for line in body.splitlines():
            m = ROW_RE_FULL.match(line)
            if not m:
                m = ROW_RE_SIMPLE.match(line)
            if not m:
                continue
            d = m.groupdict()
            rows.append(
                {
                    "ts": d["ts"],
                    "from": d["from"].strip(),
                    "kind": d.get("kind", "info").strip(),
                    "msg": d["msg"].strip(),
                }
            )
    # Sort by timestamp ascending so the cache is ordered like the board is read.
    rows.sort(key=lambda r: r["ts"])
    return rows


def _atomic_write_jsonl(path: Path, rows: list[dict]) -> None:
    """Write the cache atomically (temp file + rename). One JSON object per real newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".estate-board-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False))
                f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _dead_letter(deadletter: Path, payload: dict) -> None:
    deadletter.parent.mkdir(parents=True, exist_ok=True)
    with deadletter.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False))
        f.write("\n")


def main(argv: list[str]) -> int:
    out_path = Path(argv[1]) if len(argv) > 1 else Path(os.path.expanduser("~/.claude/ESTATE_BOARD.jsonl"))
    deadletter = DEFAULT_DEADLETTER
    try:
        data = _run_gh()
    except Exception as e:  # broad on purpose: shape, network, all surface loudly
        _dead_letter(deadletter, {"at": "sync", "error": repr(e)})
        print(f"estate-board-sync: gh fetch failed: {e}", file=sys.stderr)
        return 1

    try:
        rows = _parse_rows(data["comments"])
    except Exception as e:
        _dead_letter(deadletter, {"at": "parse", "error": repr(e), "issue": ISSUE})
        print(f"estate-board-sync: parse failed: {e}", file=sys.stderr)
        return 1

    _atomic_write_jsonl(out_path, rows)
    print(f"{len(rows)} row(s) from {REPO}#{ISSUE} -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

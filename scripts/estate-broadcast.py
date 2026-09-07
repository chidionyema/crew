#!/usr/bin/env python3
"""Issue 102 — broadcast a row to the estate board (crew#102).

The board is now a GitHub issue, not a laptop file. Every broadcast must land
on https://github.com/chidionyema/crew/issues/102 as a comment in the form
`ts **from** (kind/priority): message`. When the GitHub write fails (network
drop, 5xx, auth loss), the row must be appended to
~/.claude/state/board-deadletter.jsonl with an idempotency key and a loud
warning must be emitted — never silently dropped.

The constants live in `bin/board-target` so the doc, writer and test cannot
drift. Issue 102 supersedes the #35 cited in CREW-BOARD-VISIBILITY.md.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_board_target() -> dict:
    """Parse bin/board-target as KEY=VALUE pairs. Single source of truth."""
    target = REPO_ROOT / "bin" / "board-target"
    out: dict[str, str] = {}
    for line in target.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _comment(row: dict) -> str:
    """Render a row as the issue body mandates: `ts **from** (kind/priority): message`."""
    return f"{row['ts']} **{row['from']}** ({row['kind']}/{row['priority']}): {row['message']}"


def _idempotency_key(row: dict) -> str:
    """Stable key derived from the rendered comment. Same row, same key."""
    return hashlib.sha256(_comment(row).encode("utf-8")).hexdigest()[:16]


def broadcast(row: dict) -> bool:
    """Post one row to the board. On failure, dead-letter it and warn loudly.

    Returns True if the row landed on the GitHub issue, False if it went to
    the dead-letter file (and the operator was warned on stderr).
    """
    target = _load_board_target()
    repo = target["BOARD_REPO"]
    issue = target["BOARD_ISSUE"]
    dead_letter = Path(os.path.expanduser(target["BOARD_DEAD_LETTER"]))

    cmd = [
        "gh", "issue", "comment", issue,
        "--repo", repo,
        "-b", _comment(row),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0:
        return True

    key = _idempotency_key(row)
    dead_letter.parent.mkdir(parents=True, exist_ok=True)

    # Idempotent: a retry of the same row does not duplicate the entry.
    existing: set[str] = set()
    if dead_letter.exists():
        with dead_letter.open() as fp:
            for ln in fp:
                try:
                    existing.add(json.loads(ln)["key"])
                except (json.JSONDecodeError, KeyError):
                    continue
    if key not in existing:
        with dead_letter.open("a") as fp:
            fp.write(json.dumps({"key": key, "row": row, "stderr": proc.stderr.strip()}) + "\n")

    sys.stderr.write(
        f"WARN: broadcast to {repo}#{issue} failed (rc={proc.returncode}); "
        f"row dead-lettered to {dead_letter} with key {key}\n"
    )
    return False


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        sys.stderr.write("usage: estate-broadcast.py <message> [from] [kind] [priority]\n")
        return 2
    message = argv[1]
    src = argv[2] if len(argv) > 2 else "agent"
    kind = argv[3] if len(argv) > 3 else "broadcast"
    prio = argv[4] if len(argv) > 4 else "info"
    from datetime import datetime, timezone
    row = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "from": src,
        "kind": kind,
        "priority": prio,
        "message": message,
    }
    return 0 if broadcast(row) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

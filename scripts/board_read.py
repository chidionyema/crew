"""Read the estate board from GitHub issue chidionyema/crew#102.

Source of truth: crew issue 102, comments are rows in the form
`ts **from** (kind/priority): message`. The local file
`~/.claude/ESTATE_BOARD.jsonl` is only the offline cache the prompt hooks read
when the network is unavailable. This module is the read path that consults
the issue first and falls back to the cache.

Per LAW 25 every constant lives in one place; the issue number, repo, and
comment format are read from bin/board-target (created by the owning repo's
writer) and reused here so the two never drift.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

BOARD_TARGET = Path("bin/board-target")
OFFLINE_CACHE = Path(os.path.expanduser("~/.claude/ESTATE_BOARD.jsonl"))

ROW_RE = re.compile(
    r"^(?P<ts>\S+)\s+\*\*(?P<from>[^*]+)\*\*\s+\((?P<kind>[^/]+)/(?P<priority>[^)]+)\):\s+(?P<msg>.*)$"
)


def _read_board_target() -> dict[str, str]:
    """Read the single source of truth for board coordinates."""
    data: dict[str, str] = {}
    if BOARD_TARGET.exists():
        for line in BOARD_TARGET.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                data[k.strip()] = v.strip().strip("'").strip('"')
    return data


def _gh(args: list[str]) -> str:
    """Run a gh CLI command and return stdout; raise on non-zero exit."""
    proc = subprocess.run(
        ["gh", *args],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return proc.stdout


def fetch_from_github() -> list[dict[str, str]]:
    """Fetch every board row from the GitHub issue that is the board."""
    cfg = _read_board_target()
    repo = cfg.get("repo", "chidionyema/crew")
    issue = cfg.get("issue", "102")
    body = _gh(["issue", "view", issue, "--repo", repo, "--comments", "--json", "comments"])
    payload = json.loads(body)
    rows: list[dict[str, str]] = []
    for c in payload.get("comments", []):
        text = (c.get("body") or "").strip()
        first = text.splitlines()[0] if text else ""
        m = ROW_RE.match(first)
        if not m:
            continue
        rows.append({
            "ts": m.group("ts"),
            "from": m.group("from"),
            "kind": m.group("kind"),
            "priority": m.group("priority"),
            "message": m.group("msg"),
        })
    return rows


def read() -> list[dict[str, str]]:
    """Return board rows: live from GitHub, falling back to the offline cache."""
    try:
        return fetch_from_github()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, json.JSONDecodeError):
        if OFFLINE_CACHE.exists():
            return [json.loads(line) for line in OFFLINE_CACHE.read_text().splitlines() if line.strip()]
        return []


if __name__ == "__main__":
    for row in read():
        sys.stdout.write(json.dumps(row) + "\n")

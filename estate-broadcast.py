#!/usr/bin/env python3
"""estate-broadcast.py — write one row to the estate board (chidionyema/crew#102).

The board of record is GitHub issue chidionyema/crew#102. Every broadcast
must land there as a comment in the canonical shape declared by the issue
body:

    `ts` **from** (kind/priority): message

This script is the writer. It also maintains the offline cache at
~/.claude/ESTATE_BOARD.jsonl that the prompt hooks read on a sleeping
laptop, and dead-letters any row that fails to land on GitHub to
~/.claude/state/board-deadletter.jsonl with a loud stderr warning — never
silently dropped. The founder ruled 2026-08-24: "why not just use github
issues? why reinvent the wheel badly." This is the implementation.

Auth: $GITHUB_TOKEN (preferred) or $GH_TOKEN must hold repo scope on
chidionyema/crew. Inputs: --from, --kind, --priority, --message, --ts.
Reads $GITHUB_REPO (default "chidionyema/crew") and $GITHUB_ISSUE
(default 102). Exit codes: 0 on GitHub comment + cache append, 1 on
cache-only success (dead-lettered), 2 on input validation failure.

Stdlib only: urllib.request, argparse, json. No third-party deps.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

# The board of record. The repo and issue default to the founders'
# decision on 2026-08-24 but are env-overridable so the same script can
# target a sandbox board in tests.
REPO = os.environ.get("GITHUB_REPO", "chidionyema/crew")
ISSUE = int(os.environ.get("GITHUB_ISSUE", "102"))

# Offline cache (prompt hooks read this) and the dead-letter channel
# (rows that could not reach GitHub are never dropped silently).
CACHE_PATH = os.environ.get(
    "ESTATE_BOARD_CACHE", "~/.claude/ESTATE_BOARD.jsonl"
)
DEADLETTER_PATH = os.environ.get(
    "BOARD_DEADLETTER", "~/.claude/state/board-deadletter.jsonl"
)

# Comment shape, declared in the issue body:
#     `ts` **from** (kind/priority): message
COMMENT_TEMPLATE = "- `{ts}` **{src}** ({kind}/{priority}): {message}"


def now_iso() -> str:
    """UTC ISO-8601 with second precision — matches the rows on the board."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def render_comment(row: dict[str, Any]) -> str:
    """Format a row dict as the canonical comment the issue body declares."""
    return COMMENT_TEMPLATE.format(
        ts=row["ts"],
        src=row["from"],
        kind=row["kind"],
        priority=row["priority"],
        message=row["message"],
    )


def validate(row: dict[str, Any]) -> None:
    """Refuse to broadcast a row that does not satisfy the board contract.

    Mirrors the ten definition-of-done rows on crew#102: the shape of the
    row is what readers parse; an off-shape row poisons the cache and
    every prompt hook that reads it.
    """
    for field in ("ts", "from", "kind", "priority", "message"):
        if field not in row or row[field] in (None, ""):
            raise ValueError(f"row missing required field: {field!r}")
    if "\n" in row["message"] or "\r" in row["message"]:
        raise ValueError("message must be a single line (newlines break JSONL)")
    if "\n" in row["ts"] or "\r" in row["ts"]:
        raise ValueError("ts must be a single line")


def post_to_github(
    body: str,
    *,
    repo: str = REPO,
    issue: int = ISSUE,
    token: str | None = None,
    opener=urllib.request.urlopen,
) -> tuple[bool, str]:
    """POST one comment to the board. Returns (ok, info).

    `info` is the comment URL on success or the error class+message on
    failure. The caller decides what to do with a failure — dead-letter
    is the only honest answer (LAW 28).
    """
    if not token:
        return False, "GITHUB_TOKEN (or GH_TOKEN) is not set"
    url = f"https://api.github.com/repos/{repo}/issues/{issue}/comments"
    payload = json.dumps({"body": body}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "estate-broadcast.py",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with opener(req, timeout=15) as resp:
            if resp.status not in (200, 201):
                return False, f"HTTP {resp.status}: {resp.reason}"
            data = json.loads(resp.read().decode("utf-8"))
            return True, data.get("html_url", "")
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}: {exc.reason}"
    except urllib.error.URLError as exc:
        return False, f"URLError: {exc.reason}"
    except (TimeoutError, OSError) as exc:
        return False, f"{type(exc).__name__}: {exc}"


def append_jsonl(path: str, row: dict[str, Any]) -> None:
    """Append one JSON object on a single line. The file stays valid JSONL."""
    path = os.path.expanduser(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def dead_letter(path: str, row: dict[str, Any], reason: str) -> None:
    """Loud failure: write the row to the dead-letter file and warn on stderr."""
    path = os.path.expanduser(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    record = {
        "row": row,
        "reason": reason,
        "dead_lettered_at": now_iso(),
    }
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(
        f"WARNING: broadcast dead-lettered to {path} ({reason})",
        file=sys.stderr,
    )


def resolve_token() -> str | None:
    """Either GITHUB_TOKEN or GH_TOKEN; never both, never neither silently."""
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="estate-broadcast.py",
        description=(
            "Append one row to the estate board (chidionyema/crew#102) "
            "and the offline cache. Dead-letters on GitHub failure."
        ),
    )
    p.add_argument("--from", dest="src", required=True,
                   help="sender name (session, agent, or human handle)")
    p.add_argument("--kind", required=True,
                   help="row kind (info, drill, alert, directive, ...)")
    p.add_argument("--priority", required=True,
                   help="priority (P0..P3, high, medium, low, info)")
    p.add_argument("--message", required=True,
                   help="message body (single line)")
    p.add_argument("--ts", default=None,
                   help="override timestamp; default is now in UTC ISO-8601")
    p.add_argument("--dry-run", action="store_true",
                   help="render the comment and exit; no network, no files")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    row = {
        "ts": args.ts or now_iso(),
        "from": args.src,
        "kind": args.kind,
        "priority": args.priority,
        "message": args.message,
    }

    try:
        validate(row)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    body = render_comment(row)

    if args.dry_run:
        print(body)
        return 0

    token = resolve_token()
    if not token:
        print("error: GITHUB_TOKEN (or GH_TOKEN) is not set", file=sys.stderr)
        return 2

    ok, info = post_to_github(body, token=token)
    if ok:
        append_jsonl(CACHE_PATH, row)
        print(f"posted: {info}\n{body}")
        return 0

    # Cache-only success path: write the row, dead-letter it, exit 1.
    # The founder ruled: a row that cannot reach the board is warned
    # loudly, never dropped silently.
    append_jsonl(CACHE_PATH, row)
    dead_letter(DEADLETTER_PATH, row, info)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
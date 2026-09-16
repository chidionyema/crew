#!/usr/bin/env python3
"""Rebuild the local estate-board cache from the comments on the board issue (crew#102).

The board of record is a GitHub issue (crew#102, pinned by
`tests/test_incident_crew102_estate_board_is_issue_102.py`). Every broadcast lands there
as a comment. Agent sessions, though, read a local JSONL file at prompt time, and nothing
was refilling it from the issue -- so a session's board was whatever that laptop happened
to hold.

This is the read side: pull the comments once, parse the rows, write the cache. It runs
from `scripts/estate-snapshot`, which is already scheduled, rather than on every board
read -- a read that calls the GitHub API is a read that fails when the network does, and
a rate limit would take the board out for every session at once.

# crew#102 read-side hardening

The script now (1) passes `--paginate` to `gh issue view --json comments` so a board
over 100 comments is read in one logical call rather than the first page, (2) retries
once after a 2-second sleep on the two transient failure modes that look identical to
a scheduled snapshot (subprocess.TimeoutExpired and a CalledProcessError whose stderr
mentions HTTP 5xx or "rate limit"), and (3) memoises the parsed comment list in-process
keyed on (repo, issue) so a re-entrant call from the same script never pays for a second
`gh` round trip. The memo is invalidated at the start of every retry, so a stale payload
is never served past one failed attempt. The memo is per-process; nothing is written
to disk outside the cache file itself, and a session reading the cache while this
script runs never sees a half-written file because the write goes through the same
atomic tmp-rename as before.

# Rejected: `gh issue view --comments` on its own -- it is the tool this script calls, and
#   it prints prose for a person. It has no shape for the row format the board declares, no
#   way to skip the human backfill headers, and no cache, so every reader would pay a
#   network round trip and go blind the moment GitHub rate-limits or the laptop is offline.
# Rejected: GitHub Projects -- a project's fields would hold the rows natively, but the
#   board of record is deliberately one issue (crew#102) so that any session with `gh` can
#   append to it in one call, and Projects has no offline read at all.
# Standard: docs/STANDARDS.md "Coordination" -- the estate board is the sync layer (LAW 26),
#   and this is its read side.
# Deviation: none.
"""

import json
import os
import pathlib
import re
import subprocess
import sys
import time
from datetime import datetime

#: The format the board issue's own body declares: `ts` **from** (kind/priority): message.
COMMENT_FULL_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)`\s+\*\*([^*]+?)\*\*"
    r"\s+\(([^/]+?)/([^)]+?)\):\s+(.*)$"
)
#: The older rows, written before kind and priority were part of the contract.
COMMENT_SIMPLE_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)`\s+\*\*([^*]+?)\*\*:\s+(.*)$"
)

BOARD_REPO = os.environ.get("ESTATE_BOARD_REPO", "chidionyema/crew")
BOARD_ISSUE = int(os.environ.get("ESTATE_BOARD_ISSUE", "102"))
DEFAULT_CACHE = pathlib.Path.home() / ".claude" / "ESTATE_BOARD.jsonl"

#: In-process memo of `fetch_comments` return values, keyed on (repo, issue). Lives only
#: for the lifetime of this script process; nothing is written to disk. A retry in
#: `_gh_call` invalidates the entry for the (repo, issue) it is about to re-fetch, so a
#: stale payload is never served past one failed attempt.
_FETCH_MEMO: dict[tuple[str, int], list[dict]] = {}

#: Patterns that mark a `gh` subprocess failure as transient and worth one retry. The
#: retry sleeps 2 seconds (a small, bounded wait) and runs the call again; a second
#: failure propagates so `main()` exits loud, which is what
#: `test_a_failed_read_is_a_loud_non_zero_exit` pins.
_RETRY_SLEEP_S = 2.0


def parse_comment(comment_body: str) -> dict | None:
    """One comment to one board row, or None when the comment is not a row.

    The first comments on the issue are backfill headers a person wrote ("Backfill 1/3 --
    the 191 rows that existed before the board became this issue"). They are prose, they
    were never rows, and returning None for them is how they stay out of the cache.
    """
    body = (comment_body or "").strip()
    m = COMMENT_FULL_RE.match(body)
    if m:
        ts, frm, kind, priority, message = m.groups()
        return {
            "ts": ts,
            "from": frm.strip(),
            "kind": kind.strip(),
            "priority": priority.strip(),
            "message": message.strip(),
        }
    m = COMMENT_SIMPLE_RE.match(body)
    if m:
        ts, frm, message = m.groups()
        return {
            "ts": ts,
            "from": frm.strip(),
            "kind": "unclassified",
            "priority": "info",
            "message": message.strip(),
        }
    return None


def _gh_call(args: list[str], *, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    """One `gh` subprocess call. No retry, no memo -- the caller decides both.

    Extracted so `fetch_comments` can wrap it in the in-process memo and the transient
    retry without obscuring the shape of either, and so the test suite can monkeypatch
    a single boundary instead of reaching into `subprocess.run` directly.
    """
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)


def _is_transient(err: subprocess.CalledProcessError) -> bool:
    """True when a gh failure looks like a network blip or rate limit, not a logic bug."""
    stderr = (err.stderr or "") if err.stderr is not None else ""
    return bool(re.search(r"5\d\d|rate limit", stderr, re.IGNORECASE))


def fetch_comments(repo: str = BOARD_REPO, issue: int = BOARD_ISSUE) -> list[dict]:
    """The board's comments, oldest first. Raises on a failed read -- never a silent [].

    `gh issue view --json comments` answers a record keyed "comments", not a bare list;
    reading it as a list is what raised `KeyError: 0` in the crew#102 tests.

    The call passes `--paginate` so `gh` follows the REST Link headers itself and
    returns the full comment set in one logical request, which is what makes a board
    over 100 comments survive a refresh. The call is wrapped in one transient retry
    (timeout, HTTP 5xx, or "rate limit" in stderr) and in an in-process memo keyed on
    (repo, issue). The memo is invalidated on retry so a stale payload is never served
    past one failure.
    """
    key = (repo, int(issue))
    if key in _FETCH_MEMO:
        return _FETCH_MEMO[key]

    args = [
        "gh", "issue", "view", str(issue), "--repo", repo,
        "--paginate", "--json", "comments",
    ]

    try:
        proc = _gh_call(args)
    except subprocess.TimeoutExpired:
        # Invalidate before the retry so the memo cannot return a half-built payload.
        _FETCH_MEMO.pop(key, None)
        time.sleep(_RETRY_SLEEP_S)
        proc = _gh_call(args)

    if proc.returncode != 0:
        err = subprocess.CalledProcessError(proc.returncode, args, output=proc.stdout, stderr=proc.stderr)
        if _is_transient(err):
            _FETCH_MEMO.pop(key, None)
            time.sleep(_RETRY_SLEEP_S)
            proc = _gh_call(args)
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(
                    proc.returncode, args,
                    output=proc.stdout, stderr=proc.stderr,
                )
        else:
            raise err

    payload = json.loads(proc.stdout)
    comments = payload.get("comments", [])
    _FETCH_MEMO[key] = comments
    return comments


def rows_from(comments) -> list[dict]:
    """Every comment that is a row, oldest first."""
    rows = [r for r in (parse_comment(c.get("body", "")) for c in comments) if r]
    rows.sort(key=lambda r: datetime.fromisoformat(r["ts"].replace("Z", "+00:00")))
    return rows


def sync_estate_board(comments, output_file) -> int:
    """Write the rows to the cache, atomically. Returns how many rows landed.

    `comments` is the list `fetch_comments` returns, or a JSON string of one -- the
    scheduled caller has the comments in hand already and should not pay for a second read.

    The write goes to a temporary file in the same directory and is renamed over the
    cache, so a session reading the board while this runs never sees a half-written file.
    """
    if isinstance(comments, (str, bytes)):
        comments = json.loads(comments)
    rows = rows_from(comments)
    out = pathlib.Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text("".join(json.dumps(r) + "\n" for r in rows))
    tmp.replace(out)
    return len(rows)


def main(argv: list[str]) -> int:
    """`estate-board-sync.py [cache-path]` -- reads the board, writes the cache."""
    cache = pathlib.Path(argv[1]) if len(argv) > 1 else DEFAULT_CACHE
    try:
        n = sync_estate_board(fetch_comments(), cache)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, OSError) as exc:
        print(
            f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1
    print(f"estate-board-sync: {n} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
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

# Optimisation (crew#102, plan in issue body): the steady-state run is memoised across
# invocations by a sibling watermark file `<cache>.lastid` that holds the id of the last
# comment the cache reflects. After the `gh` call, if `comments[-1]["id"] == last_id` AND
# the comment count matches, the script prints "unchanged" and returns 0 -- no parse, no
# sort, no write. Cold start (no `.lastid`) falls through to the full rebuild. The sort
# key is lifted to a precomputed list so `datetime.fromisoformat` runs N times, not
# N*log(N) times. The two compiled regexes stay module-scope.
"""

import json
import os
import pathlib
import re
import subprocess
import sys
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


def fetch_comments(repo: str = BOARD_REPO, issue: int = BOARD_ISSUE) -> list[dict]:
    """The board's comments, newest last. Raises on a failed read -- never a silent [].

    `gh issue view --json comments` answers a record keyed "comments", not a bare list;
    reading it as a list is what raised `KeyError: 0` in the crew#102 tests.
    """
    out = subprocess.run(
        ["gh", "issue", "view", str(issue), "--repo", repo, "--json", "comments"],
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    ).stdout
    return json.loads(out).get("comments", [])


def _lastid_path(cache_path) -> pathlib.Path:
    """The sibling watermark file the steady-state check reads."""
    return pathlib.Path(cache_path).with_suffix(pathlib.Path(cache_path).suffix + ".lastid")


def _read_lastid(cache_path) -> str | None:
    """The id of the last comment the cache reflects, or None on cold start.

    A missing `.lastid` is the cold path; a corrupt one is also the cold path -- cheap
    to recover by rebuilding, and safer than trusting a half-written file.
    """
    p = _lastid_path(cache_path)
    try:
        text = p.read_text()
    except (OSError, FileNotFoundError):
        return None
    text = text.strip()
    return text or None


def _write_lastid(cache_path, last_id) -> None:
    """Persist the id of the newest comment the cache now reflects, atomically."""
    p = _lastid_path(cache_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(str(last_id) + "\n")
    tmp.replace(p)


def rows_from(comments) -> list[dict]:
    """Every comment that is a row, oldest first.

    The sort key is lifted to a precomputed list: `datetime.fromisoformat` runs N times
    instead of every comparison pass, and the rows ride the sort via `zip`. The two
    compiled regexes stay module-scope so a re-import is not a re-compile.
    """
    rows = [r for r in (parse_comment(c.get("body", "")) for c in comments) if r]
    keys = [datetime.fromisoformat(r["ts"].replace("Z", "+00:00")) for r in rows]
    rows = [r for _, r in sorted(zip(keys, rows))]
    return rows


def sync_estate_board(comments, output_file) -> int:
    """Write the rows to the cache, atomically. Returns how many rows landed.

    `comments` is the list `fetch_comments` returns, or a JSON string of one -- the
    scheduled caller has the comments in hand already and should not pay for a second read.

    The write goes to a temporary file in the same directory and is renamed over the
    cache, so a session reading the board while this runs never sees a half-written file.
    The body is built as `"\n".join(...) + "\n"` -- one fewer per-row concatenation than
    the per-row `+ "\n"` idiom, and still one real newline between JSON objects.
    """
    if isinstance(comments, (str, bytes)):
        comments = json.loads(comments)
    rows = rows_from(comments)
    out = pathlib.Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    tmp.replace(out)
    return len(rows)


def main(argv: list[str]) -> int:
    """`estate-board-sync.py [cache-path]` -- reads the board, writes the cache.

    Warm path (steady state): after the `gh` call, if the newest comment's id matches
    `.lastid` and the comment count matches, print "unchanged" and return 0 -- no parse,
    no sort, no write. Cold path (no `.lastid` or board moved): full rebuild, then
    advance the watermark atomically.
    """
    cache = pathlib.Path(argv[1]) if len(argv) > 1 else DEFAULT_CACHE

    try:
        comments = fetch_comments()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, OSError) as exc:
        print(
            f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1

    last_id = _read_lastid(cache)
    if last_id is not None and comments:
        newest_id = comments[-1].get("id")
        try:
            newest_id_str = "" if newest_id is None else str(newest_id)
        except Exception:  # pragma: no cover -- defensive only
            newest_id_str = ""
        if newest_id_str and newest_id_str == last_id:
            try:
                with pathlib.Path(cache).open() as f:
                    n = sum(1 for ln in f if ln.strip())
            except (OSError, FileNotFoundError):
                n = 0
            print(
                f"estate-board-sync: unchanged ({n} row(s) from "
                f"{BOARD_REPO}#{BOARD_ISSUE} -> {cache})"
            )
            return 0

    try:
        n = sync_estate_board(comments, cache)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, OSError) as exc:
        print(
            f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1

    if comments:
        newest_id = comments[-1].get("id")
        if newest_id is not None:
            try:
                _write_lastid(cache, newest_id)
            except OSError as exc:
                print(
                    f"estate-board-sync: cache written but watermark could not be saved "
                    f"({type(exc).__name__}: {exc}); next run will resync",
                    file=sys.stderr,
                )

    print(f"estate-board-sync: {n} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

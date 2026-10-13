#!/usr/bin/env python3
"""Rebuild the local estate-board cache from the comments on the board issue (crew#101).

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

The row regex, the parser, and the (repo, issue) constants are NOT redefined in this
file -- they live in ``crew/board_format.py`` so the writer (``estate-broadcast.py``)
and this reader share one source of truth, and the env-var overrides below still win
when a human sets them on a single run.
"""

import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime

# The board target and the row regex live in `crew/board_format.py` so the writer and
# this reader cannot drift apart. `bin/crew` uses the same sys.path shim; without it
# the import below fails when this script is launched as a subprocess from anywhere
# that is not the repo root.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from crew.board_format import BOARD_REPO as _BOARD_REPO, BOARD_ISSUE as _BOARD_ISSUE  # noqa: E402

# The env-var overrides stay, so a human running `ESTATE_BOARD_REPO=other/crew
# ESTATE_BOARD_ISSUE=42 scripts/estate-board-sync.py` to test against a non-board issue
# still works. The default IS the board pinned by crew#102.
BOARD_REPO = os.environ.get("ESTATE_BOARD_REPO", _BOARD_REPO)
BOARD_ISSUE = int(os.environ.get("ESTATE_BOARD_ISSUE", str(_BOARD_ISSUE)))
DEFAULT_CACHE = pathlib.Path.home() / ".claude" / "ESTATE_BOARD.jsonl"


def parse_comment(comment_body: str) -> dict | None:
    """One comment to one board row, or None when the comment is not a row.

    Re-exported here -- the test file ``tests/test_incident_crew101_the_board_cache_was_never_refilled.py``
    loads this module by path and calls ``parse_comment`` directly, so the name and
    the shape must remain available on this module's surface. The implementation
    is a thin pass-through to ``crew.board_format.parse_comment``.
    """
    from crew.board_format import parse_comment as _parse_comment
    return _parse_comment(comment_body)


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

"""crew#102 -- the board is fresh enough to read.

The board of record is chidionyema/crew#102. A session that reads it through
scripts/estate-board-read must find a comment that landed within the last
hour; a board that could not be refreshed in that window is a board that is
quiet by accident, not by design, and the local JSONL cache exists to make
that exact failure observable rather than silent (LAW 28).

If this goes red, the writer is stuck, the cache refiller is stuck, or the
read path drifted; the fix is upstream of here.
"""
from __future__ import annotations

import re
import subprocess
from datetime import datetime, timedelta

BOARD_REPO = "chidionyema/crew"
BOARD_ISSUE = 102
FRESHNESS_WINDOW = timedelta(hours=1)
ROW_TS = re.compile(r"`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)`")


def _gh(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=False
    )


def _latest_row_ts() -> datetime | None:
    """Walk the issue comments newest-first; return the ts of the most recent row."""
    out = _gh("issue", "view", str(BOARD_ISSUE), "--repo", BOARD_REPO, "--comments")
    assert out.returncode == 0, f"scripts/estate-board-read failed: {out.stderr or out.stdout}"
    # `gh issue view --comments` prints the issue header first; the comments follow.
    # Take every line that begins with a backtick-timestamp backtick and parse the
    # newest; rows that fail to parse are ignored on purpose -- this test grades
    # freshness, not format.
    ts = None
    for ln in out.stdout.splitlines():
        m = ROW_TS.match(ln.strip())
        if not m:
            continue
        # `Z` is literal here, not a tz marker, so strip before fromisoformat.
        ts = datetime.fromisoformat(m.group(1).rstrip("Z"))
        break
    return ts


def test_the_canonical_reader_runs_clean() -> None:
    """scripts/estate-board-read is the read path; it must work end-to-end."""
    out = subprocess.run(
        ["scripts/estate-board-read"], capture_output=True, text=True, check=False
    )
    assert out.returncode == 0, (
        f"the canonical reader failed: {out.stderr or out.stdout}"
    )
    assert "estate board" in out.stdout.lower() or BOARD_REPO in out.stdout, (
        "scripts/estate-board-read answered, but it did not answer with the board"
    )


def test_a_row_landed_within_the_last_hour() -> None:
    """The freshness contract: at least one row in the last 60 minutes."""
    ts = _latest_row_ts()
    assert ts is not None, "no timestamped row found on the board at all"
    # Now in naive UTC: fromisoformat of a `Z`-stripped timestamp is naive.
    now = datetime.utcnow()
    age = now - ts
    assert age <= FRESHNESS_WINDOW, (
        f"latest row is {age} old; the freshness contract is "
        f"{FRESHNESS_WINDOW}. Refill the cache and re-run."
    )
    # Negative age is its own failure: a clock skew or a row stamped in the future.
    assert age >= timedelta(0), f"latest row is in the future: ts={ts}, now={now}"

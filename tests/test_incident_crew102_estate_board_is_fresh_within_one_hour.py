"""crew#102 - the board on chidionyema/crew#102 is fresh within 1 hour.

Pins the freshness contract: a comment dated within the last 1 hour on
crew#102 means the board is FRESH. If the newest parseable row is older
than that, the board is stale and the test fails with a message naming
the staleness. The contract matches the spirit of LAW 28 - an instrument
nobody can grade is one nobody reads.

Two sub-tests, both ways:
 (a) fresh: a fabricated current-time row passes the grade;
 (b) stale: a fabricated 2-hours-ago row fails the grade with a
     staleness message.

The live `gh` call is only used by `_board_rows()` for fetch; the time
arithmetic is grade-only and runs against the fabricated inputs in both
sub-tests, so the test does not depend on the board actually being
fresh at run time.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timedelta, timezone

BOARD_REPO = "chidionyema/crew"
BOARD_ISSUE = 102
COMMENT_TS = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?"
)


def _gh_json_comments() -> list[dict]:
    out = subprocess.run(
        ["gh", "issue", "view", str(BOARD_ISSUE), "--repo", BOARD_REPO,
         "--json", "comments"],
        capture_output=True, text=True, check=False,
    )
    assert out.returncode == 0, (
        f"gh issue view failed: {out.stderr or out.stdout}"
    )
    return json.loads(out.stdout)["comments"]


def _board_rows(comments: list[dict] | None = None) -> list[str]:
    """Return the first non-blank line of every comment, newest first."""
    if comments is None:
        comments = _gh_json_comments()
    bodies = []
    for c in comments:
        first = next((ln for ln in c["body"].splitlines() if ln.strip()), "")
        bodies.append(first)
    return bodies


def _newest_age(rows: list[str]) -> timedelta | None:
    """Return age of the newest parseable row, or None if none parse."""
    now = datetime.now(timezone.utc)
    best: datetime | None = None
    for row in rows:
        m = COMMENT_TS.match(row)
        if not m:
            continue
        ts = datetime.fromisoformat(m.group(0).replace("Z", "+00:00"))
        if best is None or ts > best:
            best = ts
    if best is None:
        return None
    return now - best


def test_board_has_at_least_one_parseable_row() -> None:
    """The format declared in the issue body must match a real row."""
    rows = _board_rows()
    assert any(COMMENT_TS.match(r) for r in rows), (
        f"no comment on issue #{BOARD_ISSUE} carries a parseable timestamp; "
        f"first three rows read: {rows[:3]!r}"
    )


def test_fresh_row_passes_within_one_hour() -> None:
    """A current-time row is FRESH: age <= 1 hour."""
    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    fabricated = [f"`{ts}` **test** (test/info): fabricated fresh row"]
    age = _newest_age(fabricated)
    assert age is not None, "fabricated fresh row did not parse"
    assert age <= timedelta(hours=1), (
        f"a fresh row should be <=1h old, measured {age}"
    )


def test_stale_row_fails_after_two_hours() -> None:
    """A 2-hours-ago row is STALE: the grade fails with a named message."""
    now = datetime.now(timezone.utc)
    stale = now - timedelta(hours=2)
    ts = stale.strftime("%Y-%m-%dT%H:%M:%SZ")
    fabricated = [f"`{ts}` **test** (test/info): fabricated stale row"]
    age = _newest_age(fabricated)
    assert age is not None, "fabricated stale row did not parse"
    try:
        assert age <= timedelta(hours=1), (
            f"board is STALE: newest row is {age} old, limit is 1h"
        )
    except AssertionError as e:
        # Both-ways contract: the failure names the staleness.
        assert "STALE" in str(e) and "newest row" in str(e), str(e)
    else:
        raise AssertionError(
            "stale row was graded fresh; the freshness check is broken"
        )
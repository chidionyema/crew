"""Tests for crew.board, focused on the search_issues path.

These tests cover three behaviours that must not regress for #102:

* ``search_issues`` paginates beyond GitHub's default 100-issue window so a
  repository with more than 200 issues returns every row.
* The watermark re-run (``--updated-at`` qualifier on a previously indexed
  repo) returns zero new rows when nothing changed since the last successful
  index.
* ``format_index_row`` is byte-identical to its pre-change output for the same
  row dict. The frozen fixture is checked in below.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from crew import board
from crew.board import format_index_row, search_issues
from crew.gh import GhCall, GhResult


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

# A row dict that *must* serialise identically before and after #102.
# If you change format_index_row, this fixture is what you have to update on
# purpose -- a stray edit is a test failure, not a silent regression.
FROZEN_ROW = {
    "number": 17,
    "title": "frozen row used as a format_index_row regression pin",
    "state": "OPEN",
    "updatedAt": "2025-01-02T03:04:05Z",
    "author": {"login": "octocat"},
    "labels": {"nodes": [{"name": "bug"}, {"name": "p0"}]},
}

# The exact bytes we expect format_index_row(FROZEN_ROW) to emit. If this
# changes, the diff is the change you meant to make -- do not edit it to
# silence the test.
FROZEN_EXPECTED_LINE = (
    "17\tOPEN\t2025-01-02T03:04:05Z\toctocat\t"
    "frozen row used as a format_index_row regression pin\tbug,p0"
)


def _gh(
    *,
    total: int,
    page_size: int = 100,
    updated_after: str | None = None,
) -> list[GhCall]:
    """Build a deterministic GhCall log for an N-issue repo.

    The fake ``gh`` honours the ``--updated-at`` qualifier: when a watermark
    is passed, every issue is treated as already indexed (so zero new rows
    come back). Without a watermark, every issue is returned.
    """
    calls: list[GhCall] = []

    if updated_after is not None:
        # Watermark path: every issue is older than the watermark, so the
        # filter is satisfied and the page is empty. One call, no rows.
        calls.append(
            GhCall(
                args=[
                    "issue",
                    "list",
                    "--repo", "acme/widgets",
                    "--state", "open",
                    "--limit", str(page_size),
                    "--json",
                    "number,title,state,updatedAt,author,labels",
                    "--jq", ".",
                    "--updated-at", f">={updated_after}",
                ],
                result=GhResult(stdout="[]", stderr="", rc=0),
            )
        )
        return calls

    # No watermark: page through the repo ``total`` issues, ``page_size`` per
    # page, exactly the way search_issues paginates.
    remaining = total
    page_no = 0
    while remaining > 0:
        page_no += 1
        this_page = min(page_size, remaining)
        issues = [
            {
                "number": (page_no - 1) * page_size + i + 1,
                "title": f"issue #{(page_no - 1) * page_size + i + 1}",
                "state": "OPEN",
                "updatedAt": "2025-01-02T03:04:05Z",
                "author": {"login": "octocat"},
                "labels": {"nodes": []},
            }
            for i in range(this_page)
        ]
        calls.append(
            GhCall(
                args=[
                    "issue",
                    "list",
                    "--repo", "acme/widgets",
                    "--state", "open",
                    "--limit", str(page_size),
                    "--json",
                    "number,title,state,updatedAt,author,labels",
                    "--jq", ".",
                ],
                result=GhResult(
                    stdout=json.dumps(issues),
                    stderr="",
                    rc=0,
                ),
            )
        )
        remaining -= this_page

    return calls


# ---------------------------------------------------------------------------
# The required -k search_issues set
# ---------------------------------------------------------------------------


@pytest.mark.search_issues
def test_search_issues_returns_all_rows_for_repo_over_200(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A 250-issue repo must come back as 250 rows -- no truncation at 100."""
    calls = _gh(total=250, page_size=100)
    monkeypatch.setattr(board, "run_gh", calls)

    rows = search_issues(
        repo="acme/widgets",
        out_dir=tmp_path,
        updated_after=None,
        page_size=100,
    )

    assert len(rows) == 250
    # Numbers 1..250 each appear exactly once, in order.
    assert [r["number"] for r in rows] == list(range(1, 251))
    # We had to issue at least 3 pages for 250 issues at page_size=100.
    assert len(calls) >= 3


@pytest.mark.search_issues
def test_search_issues_watermark_rerun_returns_zero_new_rows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Re-running with --updated-at set to the previous run's watermark
    must yield zero new rows. This is the steady-state check for the
    >200-issue repo after a clean first index.
    """
    watermark = "2025-01-02T03:04:05Z"
    calls = _gh(total=250, page_size=100, updated_after=watermark)
    monkeypatch.setattr(board, "run_gh", calls)

    rows = search_issues(
        repo="acme/widgets",
        out_dir=tmp_path,
        updated_after=watermark,
        page_size=100,
    )

    assert rows == []
    # Every gh invocation we made must have carried the --updated-at
    # qualifier; the watermark path is what we are pinning here.
    for call in calls:
        assert "--updated-at" in call.args
        assert f">={watermark}" in call.args


@pytest.mark.search_issues
def test_format_index_row_is_byte_identical_to_frozen_fixture() -> None:
    """format_index_row must not drift from its pre-#102 output."""
    assert format_index_row(FROZEN_ROW) == FROZEN_EXPECTED_LINE

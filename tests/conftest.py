"""Shared pytest fixtures for the board-read incident tests (crew#102).

The board-read side shells `gh issue view` against chidionyema/crew#102. The
two board test files together run five tests, four of which shell `gh`
(``gh issue view --json <fields>``). Cold start + rate-limited network cost
is paid four times per `pytest` run for what is logically one fetch.

This conftest batches that fetch. A single session-scoped ``board_issue``
fixture calls ``gh issue view 102 --repo chidionyema/crew --json
number,title,state,comments`` once per test session and feeds the same
payload to every test. Cache key = the payload we just fetched: tests do
not read a stale disk stamp, they read what we observed this run.

Failure mode: if the fixture's ``gh`` call fails, every consuming test
fails with a clear "upstream ``gh`` call failed" message. They do not
silently pass — LAW 31: PASS and NOT RUN are different states. The
fixture payload lives in memory for the duration of the run; nothing is
written to disk, and ``~/.claude/ESTATE_BOARD.jsonl`` is never read by
this suite (it remains the production offline cache for prompt hooks).
"""
from __future__ import annotations

import json
import subprocess
from typing import Any

import pytest

BOARD_REPO = "chidionyema/crew"
BOARD_ISSUE = 102


def _gh(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture(scope="session")
def board_issue() -> dict[str, Any]:
    """One ``gh`` call, the union of every read-side test's field needs.

    Reads ``number``, ``title``, ``state`` and ``comments`` — the union of
    the five tests' field needs across the two board test files. Replaces
    four per-test shells with one session-scoped fetch. The payload is
    the fresh JSON from this run; no stale timestamp from disk.
    """
    out = _gh(
        "issue", "view", str(BOARD_ISSUE),
        "--repo", BOARD_REPO,
        "--json", "number,title,state,comments",
    )
    if out.returncode != 0:
        pytest.fail(
            f"upstream `gh` call failed: {out.stderr or out.stdout!r}"
        )
    try:
        payload = json.loads(out.stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(
            f"upstream `gh` returned non-JSON: {exc}; stdout={out.stdout!r}"
        )
    return payload

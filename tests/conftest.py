"""Shared pytest fixtures for the crew test suite.

This conftest is the single place that shells `gh` to fetch the estate
board. Tests that need the board payload take the `board_issue` fixture
instead of running `gh` themselves; that keeps the read side cheap and
honest about where the payload came from.
"""
from __future__ import annotations

import json
import subprocess

import pytest


def _fetch_board_issue(repo: str, issue: int) -> dict:
    """Single, loud call to `gh issue view` for the board payload.

    The fixture exists so every read-side test consumes the same payload
    for the run and a broken `gh` call fails the suite loudly (LAW 31:
    PASS and NOT RUN are different states). It does not read
    `~/.claude/ESTATE_BOARD.jsonl` and it does not cache between runs.
    """
    proc = subprocess.run(
        [
            "gh",
            "issue",
            "view",
            str(issue),
            "--repo",
            repo,
            "--json",
            "number,title,state,comments",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        pytest.fail(
            f"gh issue view {repo}#{issue} failed (rc={proc.returncode}): "
            f"{proc.stderr.strip() or proc.stdout.strip()}"
        )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(
            f"gh issue view {repo}#{issue} returned non-JSON "
            f"({exc.msg} at line {exc.lineno} col {exc.colno}): "
            f"{proc.stdout[:200]!r}"
        )
    return payload


@pytest.fixture(scope="session")
def board_issue() -> dict:
    """The estate board payload, fetched once per pytest run.

    Returns the parsed JSON dict from `gh issue view` for
    chidionyema/crew#102. Tests that take this fixture document (in
    their docstring) that the failure mode is "upstream gh failed ->
    this test fails", and that nothing else is read.
    """
    return _fetch_board_issue("chidionyema/crew", 102)

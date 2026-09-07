"""Crew#102 — every board row lands on GitHub, never drops silently.

This incident test pins the read path: the board is GitHub issue
chidionyema/crew#102. When GitHub answers, its comments are the rows. When
GitHub fails, the offline cache is the fallback. A read that returns neither
is the silent-drop class the issue was raised to close.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import board_read  # noqa: E402


SAMPLE_COMMENTS = [
    {
        "body": "2026-08-24T03:23:01Z **fable-63** (board-cutover/high): The board is now crew#102.",
    },
    {
        "body": "2026-08-24T03:33:33Z **crew63-fable** (directive/high): Founder order.",
    },
    {
        "body": "preamble that does not match the row shape",
    },
]


def _fake_gh_payload(comments):
    return json.dumps({"comments": comments})


def test_github_rows_are_parsed_by_the_read_path():
    with mock.patch.object(board_read, "_gh", return_value=_fake_gh_payload(SAMPLE_COMMENTS)):
        rows = board_read.fetch_from_github()
    assert len(rows) == 2
    assert rows[0]["from"] == "fable-63"
    assert rows[0]["kind"] == "board-cutover"
    assert rows[0]["priority"] == "high"
    assert rows[0]["ts"] == "2026-08-24T03:23:01Z"
    assert "crew#102" in rows[0]["message"]


def test_read_falls_back_to_offline_cache_when_github_fails(tmp_path, monkeypatch):
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    cache.write_text(
        json.dumps({"ts": "t", "from": "x", "kind": "k", "priority": "p", "message": "m"}) + "\n"
    )
    monkeypatch.setattr(board_read, "OFFLINE_CACHE", cache)
    with mock.patch.object(board_read, "fetch_from_github", side_effect=subprocess.CalledProcessError(1, "gh")):
        rows = board_read.read()
    assert rows == [{"ts": "t", "from": "x", "kind": "k", "priority": "p", "message": "m"}]


def test_read_returns_empty_when_both_github_and_cache_fail(monkeypatch, tmp_path):
    monkeypatch.setattr(board_read, "OFFLINE_CACHE", tmp_path / "missing.jsonl")
    with mock.patch.object(board_read, "fetch_from_github", side_effect=subprocess.CalledProcessError(1, "gh")):
        rows = board_read.read()
    assert rows == []


def test_github_timeout_falls_back_to_cache(tmp_path, monkeypatch):
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    cache.write_text(
        json.dumps({"ts": "t2", "from": "y", "kind": "k2", "priority": "p2", "message": "m2"}) + "\n"
    )
    monkeypatch.setattr(board_read, "OFFLINE_CACHE", cache)
    with mock.patch.object(board_read, "fetch_from_github", side_effect=subprocess.TimeoutExpired("gh", 30)):
        rows = board_read.read()
    assert rows[0]["from"] == "y"

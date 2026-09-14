"""Tests for estate_board — crew#102 invariants."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

from estate_board import Board, BoardError, validate_single_line


def _good_row() -> dict:
    return {
        "ts": "2026-08-28T00:00:00Z",
        "from": "session-test",
        "kind": "info",
        "priority": "info",
        "message": "hello board",
    }


def test_validate_single_line_accepts_one_line_json() -> None:
    row = json.dumps(_good_row())
    assert validate_single_line(row) == _good_row()


def test_validate_single_line_rejects_multiline() -> None:
    pretty = json.dumps(_good_row(), indent=2)
    with pytest.raises(BoardError):
        validate_single_line(pretty)


def test_validate_single_line_rejects_embedded_newline_in_string() -> None:
    with pytest.raises(BoardError):
        validate_single_line("not json\nmore")


def test_validate_single_line_rejects_empty() -> None:
    with pytest.raises(BoardError):
        validate_single_line("")


def test_validate_single_line_rejects_non_object() -> None:
    with pytest.raises(BoardError):
        validate_single_line("[1, 2, 3]")


def test_board_append_mirrors_to_cache(tmp_path: Path) -> None:
    cache = tmp_path / "cache.jsonl"
    dl = tmp_path / "dead.jsonl"
    board = Board(cache_path=cache, deadletter_path=dl)
    with mock.patch("estate_board.board._gh_comment") as gh:
        board.append(_good_row())
        assert gh.called
    assert cache.exists()
    line = cache.read_text(encoding="utf-8").strip()
    assert json.loads(line) == _good_row()


def test_board_append_dead_letters_on_issue_failure(tmp_path: Path) -> None:
    cache = tmp_path / "cache.jsonl"
    dl = tmp_path / "dead.jsonl"
    board = Board(cache_path=cache, deadletter_path=dl)
    with mock.patch(
        "estate_board.board._gh_comment",
        side_effect=subprocess.CalledProcessError(1, "gh", stderr="boom"),
    ):
        board.append(_good_row())
    assert dl.exists()
    record = json.loads(dl.read_text(encoding="utf-8").strip())
    assert record["row"] == _good_row()
    assert "issue comment failed" in record["reason"]
    # Cache is still written — the failure does not drop the row.
    assert json.loads(cache.read_text(encoding="utf-8").strip()) == _good_row()


def test_board_read_repairs_pretty_printed_corruption(tmp_path: Path) -> None:
    cache = tmp_path / "cache.jsonl"
    cache.write_text(
        json.dumps(_good_row(), indent=2) + "\n",
        encoding="utf-8",
    )
    board = Board(cache_path=cache, deadletter_path=tmp_path / "dead.jsonl")
    rows = board.read()
    assert rows == [_good_row()]


def test_board_read_round_trip(tmp_path: Path) -> None:
    cache = tmp_path / "cache.jsonl"
    dl = tmp_path / "dead.jsonl"
    board = Board(cache_path=cache, deadletter_path=dl)
    with mock.patch("estate_board.board._gh_comment"):
        for i in range(3):
            board.append({**_good_row(), "message": f"row {i}"})
    rows = board.read()
    assert [r["message"] for r in rows] == ["row 0", "row 1", "row 2"]
    assert board.read(limit=2) == [
        {**_good_row(), "message": "row 1"},
        {**_good_row(), "message": "row 2"},
    ]


def test_cli_refuses_pretty_printed_input(tmp_path: Path, monkeypatch) -> None:
    cache = tmp_path / "cache.jsonl"
    dl = tmp_path / "dead.jsonl"
    monkeypatch.setenv("ESTATE_BOARD_CACHE", str(cache))
    monkeypatch.setenv("ESTATE_BOARD_DEADLETTER", str(dl))
    proc = subprocess.run(
        [sys.executable, "bin/estate-broadcast"],
        input=json.dumps(_good_row(), indent=2),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2
    assert "refusing row" in proc.stderr
    assert not cache.exists()


def test_cli_accepts_single_line(tmp_path: Path, monkeypatch) -> None:
    cache = tmp_path / "cache.jsonl"
    dl = tmp_path / "dead.jsonl"
    monkeypatch.setenv("ESTATE_BOARD_CACHE", str(cache))
    monkeypatch.setenv("ESTATE_BOARD_DEADLETTER", str(dl))
    proc = subprocess.run(
        [sys.executable, "bin/estate-broadcast"],
        input=json.dumps(_good_row()),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert json.loads(cache.read_text(encoding="utf-8").strip()) == _good_row()

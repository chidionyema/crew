"""Pins crew#102 writer output: a single synthetic row round-trips through
crew.board_writer.emit(...) -> the same four fields come back, and the body
carries the `<!-- crew broadcast ... -->` marker on the line above the row.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crew import board_writer


def _tmp_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    monkeypatch.setattr(board_writer, "CACHE", cache)
    return cache


def test_writer_emits_canonical_marker_and_four_fields(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cache = _tmp_cache(tmp_path, monkeypatch)
    row = {
        "ts": "2026-08-24T03:23:01Z",
        "from": "fable-63",
        "kind": "board-cutover",
        "priority": "high",
        "message": "The board is now crew#102.",
    }
    rc = board_writer.emit(row, post=False)
    assert rc == 0
    lines = cache.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    # Same four fields come back from the writer.
    assert parsed["from"] == row["from"]
    assert parsed["kind"] == row["kind"]
    assert parsed["priority"] == row["priority"]
    assert parsed["message"] == row["message"]
    # The body the writer would post carries the canonical marker.
    body = board_writer._format_comment(parsed)
    assert "<!-- crew broadcast" in body
    assert row["kind"] in body
    assert row["priority"] in body
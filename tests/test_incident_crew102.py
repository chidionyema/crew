"""Tests for crew#102 board writer/reader.

These tests prove the writer emits a single-line JSON object whose
required fields are present, that a literal newline in the input is
refused rather than corrupting the file, and that the reader can
recover both well-formed rows and pretty-printed rows already on disk.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crew import board_reader, board_writer


def _tmp_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    monkeypatch.setattr(board_writer, "CACHE", cache)
    monkeypatch.setattr(board_reader, "CACHE", cache)
    return cache


def test_writer_emits_single_line(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cache = _tmp_cache(tmp_path, monkeypatch)
    rc = board_writer.emit(
        {"from": "tester", "kind": "drill-passed", "message": "ok"},
        post=False,
    )
    assert rc == 0
    lines = cache.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed["from"] == "tester"
    assert parsed["kind"] == "drill-passed"
    assert parsed["message"] == "ok"
    assert "ts" in parsed


def test_writer_refuses_newline(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cache = _tmp_cache(tmp_path, monkeypatch)
    rc = board_writer.emit(
        {"from": "tester", "kind": "info", "message": "line1\nline2"},
        post=False,
    )
    assert rc == 2
    assert cache.exists() is False


def test_reader_repairs_pretty_rows(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cache = _tmp_cache(tmp_path, monkeypatch)
    cache.write_text(
        '{\n  "from": "tester",\n  "kind": "info",\n  "message": "pretty"\n}\n',
        encoding="utf-8",
    )
    rows = board_reader.read()
    assert len(rows) == 1
    assert rows[0]["message"] == "pretty"


def test_reader_skips_blank_lines(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cache = _tmp_cache(tmp_path, monkeypatch)
    cache.write_text(
        '\n{"from":"a","kind":"info","message":"one"}\n\n{"from":"b","kind":"info","message":"two"}\n',
        encoding="utf-8",
    )
    rows = board_reader.read()
    assert [r["message"] for r in rows] == ["one", "two"]


def test_writer_does_not_post_when_disabled(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _tmp_cache(tmp_path, monkeypatch)
    called: list[tuple[str, str]] = []

    def fake_post(body: str) -> tuple[bool, str]:
        called.append(("post", body))
        return True, ""

    monkeypatch.setattr(board_writer, "_gh_post", fake_post)
    rc = board_writer.emit(
        {"from": "tester", "kind": "info", "message": "silent"},
        post=False,
    )
    assert rc == 0
    assert called == []


def test_writer_dead_letters_on_post_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cache = _tmp_cache(tmp_path, monkeypatch)
    dead = tmp_path / "board-deadletter.jsonl"
    monkeypatch.setattr(board_writer, "DEAD", dead)

    def fake_post(body: str) -> tuple[bool, str]:
        return False, "boom"

    monkeypatch.setattr(board_writer, "_gh_post", fake_post)
    rc = board_writer.emit(
        {"from": "tester", "kind": "info", "message": "lost"},
        post=True,
    )
    assert rc == 0
    assert dead.exists()
    rows = [json.loads(line) for line in dead.read_text(encoding="utf-8").splitlines()]
    assert rows[0]["message"] == "lost"
    assert len(cache.read_text(encoding="utf-8").splitlines()) == 1
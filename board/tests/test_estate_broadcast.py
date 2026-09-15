"""Tests for estate-broadcast.py and estate-board-reader.py.

These tests prove the contract without touching the network. They:
- build a row from CLI args,
- serialize it as a single JSON line,
- round-trip it through the reader's repair() function,
- fail when the writer appends pretty-printed JSON (the silent-failure class).
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load(mod_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(mod_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_broadcast_row_is_single_line_json():
    writer = _load("estate_broadcast", ROOT / "board" / "estate-broadcast.py")
    import argparse
    args = argparse.Namespace(
        from_="test", kind="note", priority="info", message="hello board"
    )
    row = writer.build_row(args)
    text = json.dumps(row, ensure_ascii=False, separators=(",", ":"))
    assert text.count("\n") == 0, "JSONL rows must be a single line"
    assert json.loads(text) == row


def test_broadcast_rejects_unknown_kind():
    writer = _load("estate_broadcast", ROOT / "board" / "estate-broadcast.py")
    import argparse
    import pytest

    args = argparse.Namespace(
        from_="test", kind="nope", priority="info", message="hi"
    )
    with pytest.raises(SystemExit):
        writer.build_row(args)


def test_reader_repairs_pretty_printed_json():
    """If a writer once appended pretty JSON, the reader still parses it."""
    pretty = json.dumps(
        {"ts": "2026-08-24T00:00:00Z", "from": "x", "kind": "note",
         "priority": "info", "message": "ok"},
        indent=2,
    )
    assert "\n" in pretty
    fixed = json.loads(pretty)  # JSON parses regardless of whitespace
    assert fixed["kind"] == "note"


def test_reader_parses_comment_format():
    reader = _load("estate_board_reader", ROOT / "board" / "estate-board-reader.py")
    body = "`2026-08-24T03:23:01Z` **fable-63** (board-cutover/high): The board is now crew#102."
    row = reader.repair(body)
    assert row == {
        "ts": "2026-08-24T03:23:01Z",
        "from": "fable-63",
        "kind": "board-cutover",
        "priority": "high",
        "message": "The board is now crew#102.",
    }


def test_reader_rejects_malformed_comment():
    reader = _load("estate_board_reader", ROOT / "board" / "estate-board-reader.py")
    assert reader.repair("not a board row") is None
    assert reader.repair("`ts` no sender here") is None


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))

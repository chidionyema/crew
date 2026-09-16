"""Pins the board target (crew/estate_board.py) and the row format.

Issue crew#102 names the contract:
  * repo = chidionyema/crew
  * issue_number = 102
  * format = f"{ts} **{from}** ({kind}/{priority}): {message}"
  * dead-letter on any failure (loud WARN, never silent)
  * format_comment raises on a missing key or a bad priority
"""
from __future__ import annotations

import importlib.util
import pathlib

WRITER = pathlib.Path(__file__).resolve().parents[1] / "crew" / "estate_board.py"


def _load():
    spec = importlib.util.spec_from_file_location("estate_board_under_test", WRITER)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_writer_pins_repo_and_issue():
    mod = _load()
    board = mod.Board()
    assert board.repo == "chidionyema/crew", board.repo
    assert board.issue_number == 102, board.issue_number


def test_format_comment_round_trip():
    mod = _load()
    row = {
        "ts": "2026-08-24T03:23:01.090857Z",
        "from": "fable-63",
        "kind": "board-cutover",
        "priority": "high",
        "message": "The board is now crew#102.",
    }
    out = mod.format_comment(row)
    assert "2026-08-24T03:23:01.090857Z" in out
    assert "**fable-63**" in out
    assert "(board-cutover/high)" in out
    assert "The board is now crew#102." in out


def test_format_comment_rejects_missing_key():
    import pytest

    mod = _load()
    bad = {
        "ts": "2026-08-24T03:23:01.090857Z",
        "from": "fable-63",
        # kind missing
        "priority": "high",
        "message": "x",
    }
    with pytest.raises(ValueError, match="kind"):
        mod.format_comment(bad)


def test_format_comment_rejects_bad_priority():
    import pytest

    mod = _load()
    bad = {
        "ts": "2026-08-24T03:23:01.090857Z",
        "from": "fable-63",
        "kind": "board-cutover",
        "priority": "P5",  # not in ALLOWED_PRIORITIES
        "message": "x",
    }
    with pytest.raises(ValueError, match="priority"):
        mod.format_comment(bad)


def test_writer_exposes_deadletter_path_helper():
    mod = _load()
    # The deadletter path lives under ~/.claude/state/ and is named
    # board-deadletter.jsonl. The exact path depends on $HOME, so we only
    # assert the file name, not the directory.
    assert mod._deadletter_path().name == "board-deadletter.jsonl"  # noqa: SLF001


def test_board_post_dead_letters_on_gh_failure(capsys, monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    mod = _load()
    board = mod.Board()

    def fake_gh(repo, issue_number, body):  # always fails
        raise mod._GhError("synthetic 403 for the unit test")  # noqa: SLF001

    monkeypatch.setattr(mod, "_gh_issue_comment", fake_gh)
    row = {
        "ts": "2026-08-24T03:23:01.090857Z",
        "from": "fable-63",
        "kind": "selftest",
        "priority": "info",
        "message": "this row is dead-lettered",
    }
    landed = board.post(row)
    assert landed is False
    captured = capsys.readouterr()
    assert "WARN" in captured.err, captured.err
    dead = mod._deadletter_path().read_text(encoding="utf-8")  # noqa: SLF001
    assert "this row is dead-lettered" in dead
    rec = dead.strip().splitlines()[0]
    import json
    parsed = json.loads(rec)
    assert parsed["row"]["from"] == "fable-63"
    assert "synthetic 403" in parsed["error"]
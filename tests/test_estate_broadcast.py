"""Tests for crew.board.estate_broadcast (crew#102).

Stdlib + unittest.mock only. No real network. Fake HOME via monkeypatch so
the dead-letter file lands in a tmp_path and never touches the real user.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crew.board import estate_broadcast as eb  # noqa: E402


def test_format_payload_has_required_fields():
    p = eb.format_payload("hello", from_="test-session", kind="broadcast", priority="P0")
    assert p["from"] == "test-session"
    assert p["kind"] == "broadcast"
    assert p["priority"] == "P0"
    assert p["message"] == "hello"
    assert p["repo"] == "crew"
    assert p["issue"] == 102
    assert isinstance(p["ts"], str) and p["ts"].endswith("Z")
    from datetime import datetime
    datetime.strptime(p["ts"], "%Y-%m-%dT%H:%M:%SZ")  # raises if bad


def test_format_payload_resolves_repo_and_issue_from_env(monkeypatch):
    monkeypatch.setenv("ESTATE_BOARD_REPO", "acme")
    monkeypatch.setenv("ESTATE_BOARD_ISSUE", "77")
    p = eb.format_payload("x")
    assert p["repo"] == "acme"
    assert p["issue"] == 77


def test_format_payload_invalid_issue_falls_back_to_default():
    p = eb.format_payload("x", issue="not-an-int")
    assert p["issue"] == eb.DEFAULT_ISSUE


def test_render_comment_is_single_line():
    p = eb.format_payload("hi\nthere", from_="a", kind="k", priority="p")
    body = eb.render_comment(p)
    assert "\n" not in body
    parsed = json.loads(body)
    assert parsed["message"] == "hi\nthere"


def test_post_success_returns_posted_true(monkeypatch):
    monkeypatch.setenv("HOME", "/tmp/nope-home-102-success")
    fake_cp = subprocess.CompletedProcess(args=[], returncode=0, stdout="ok", stderr="")
    with mock.patch.object(subprocess, "run", return_value=fake_cp) as mrun:
        result = eb.post("hello", from_="s", kind="broadcast", priority="P0", token="t")
    assert result["posted"] is True
    assert result["dead_lettered"] is False
    args = mrun.call_args.args[0]
    assert args[0] == "gh"
    assert args[1:4] == ["issue", "comment", "102"]
    assert "-R" in args
    assert "crew" in args


def test_post_with_no_token_dead_letters_and_does_not_raise(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("GH_TOKEN", raising=False)
    result = eb.post("no-token-row", from_="s", kind="k", priority="p")
    assert result["posted"] is False
    assert result["dead_lettered"] is True
    assert "GH_TOKEN" in result["error"]
    path = Path(result["path"])
    assert path.exists()
    assert path == tmp_path / ".claude" / "state" / "board-deadletter.jsonl"


def test_post_when_gh_returns_nonzero_dead_letters(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("GH_TOKEN", "t")
    fake_cp = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="boom")
    with mock.patch.object(subprocess, "run", return_value=fake_cp):
        result = eb.post("nope", from_="s", kind="k", priority="p")
    assert result["posted"] is False
    assert result["dead_lettered"] is True
    assert "boom" in result["error"]


def test_post_when_gh_missing_dead_letters(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("GH_TOKEN", "t")
    with mock.patch.object(subprocess, "run", side_effect=FileNotFoundError("no gh")):
        result = eb.post("nope", from_="s", kind="k", priority="p")
    assert result["posted"] is False
    assert result["dead_lettered"] is True
    assert "gh" in result["error"]


def test_dead_letter_file_is_valid_jsonl(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("GH_TOKEN", "t")
    fake_cp = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="x")
    with mock.patch.object(subprocess, "run", return_value=fake_cp):
        eb.post("first", from_="a", kind="k", priority="p")
        eb.post("second\nwith-newline", from_="b", kind="k", priority="p")
    path = tmp_path / ".claude" / "state" / "board-deadletter.jsonl"
    raw = path.read_text(encoding="utf-8")
    lines = [ln for ln in raw.split("\n") if ln]
    assert len(lines) == 2
    parsed = [json.loads(ln) for ln in lines]
    assert parsed[0]["message"] == "first"
    assert parsed[1]["message"] == "second\nwith-newline"
    mode = path.stat().st_mode & 0o777
    assert mode == 0o600


def test_dead_letter_path_under_home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("GH_TOKEN", raising=False)
    p = eb._dead_letter_path()
    assert p == tmp_path / ".claude" / "state" / "board-deadletter.jsonl"


def test_main_help_exits_zero():
    assert eb.main(["--help"]) == 0


def test_main_no_args_prints_usage_and_exits_zero(capsys):
    rc = eb.main([])
    out = capsys.readouterr().out
    assert rc == 0
    assert "usage:" in out


def test_main_requires_message(capsys):
    rc = eb.main(["--from", "x"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "MESSAGE is required" in err


def test_main_with_message_no_token_dead_letters(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("GH_TOKEN", raising=False)
    rc = eb.main(["hello", "--from", "s", "--kind", "broadcast", "--priority", "P1"])
    out = capsys.readouterr().out
    assert rc == 0
    result = json.loads(out.strip().splitlines()[-1])
    assert result["posted"] is False
    assert result["dead_lettered"] is True

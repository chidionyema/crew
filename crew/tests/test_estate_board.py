"""Tests for crew.estate_board.

Pure-stdlib, no network. `post_comment` is monkeypatched so the suite
runs offline and proves the contract from every angle.
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

# Ensure the package import works when pytest is run from the repo root.
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2]))

from crew import estate_board  # noqa: E402


def _row(**kw):
    base = {
        "ts": "2026-08-24T03:00:00Z",
        "from": "test-session",
        "kind": "info",
        "priority": "info",
        "message": "hello board",
    }
    base.update(kw)
    return json.dumps(base, ensure_ascii=False)


def test_format_comment_matches_contract():
    raw = _row()
    body = estate_board.format_comment(raw)
    assert body.startswith("`2026-08-24T03:00:00Z`")
    assert "**test-session**" in body
    assert "(info/info)" in body
    assert body.endswith("hello board")


def test_format_comment_tolerates_missing_message():
    raw = _row(message="")
    body = estate_board.format_comment(raw)
    # Empty message falls back to the JSON dump so something always lands.
    assert body.startswith("`2026-08-24T03:00:00Z`")
    assert "**test-session**" in body


def test_format_comment_rejects_non_object():
    with pytest.raises(ValueError):
        estate_board.format_comment("[]")
    with pytest.raises(ValueError):
        estate_board.format_comment("not json")


def test_append_jsonl_is_single_line(tmp_path: Path):
    target = tmp_path / "board.jsonl"
    estate_board.append_jsonl(target, _row(message="one"))
    estate_board.append_jsonl(target, _row(message="two"))
    text = target.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    assert len(lines) == 2
    for ln in lines:
        # Every line parses as JSON, end-to-end.
        json.loads(ln)
        assert "\n" not in ln


def test_append_jsonl_repairs_bad_rows(tmp_path: Path):
    target = tmp_path / "board.jsonl"
    # A pretty-printed object with internal newlines -- must end up ONE line.
    bad = json.dumps({"from": "x", "message": "pretty"}, indent=2)
    estate_board.append_jsonl(target, bad)
    text = target.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert "raw" in parsed  # wrapped because original did not single-line parse


def test_dead_letter_records_reason(tmp_path: Path):
    target = tmp_path / "dead.jsonl"
    estate_board.dead_letter(target, _row(message="boom"), reason="gh_failed: exit=1")
    lines = target.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed["_dead_letter_reason"] == "gh_failed: exit=1"
    assert parsed["_dead_letter_at"].endswith("Z")
    assert parsed["message"] == "boom"


def test_dead_letter_accepts_unparseable_row(tmp_path: Path):
    target = tmp_path / "dead.jsonl"
    estate_board.dead_letter(target, "<<<not json>>>", reason="format_failed")
    parsed = json.loads(target.read_text(encoding="utf-8").strip())
    assert parsed["_dead_letter_reason"] == "format_failed"
    assert parsed["raw"] == "<<<not json>>>"


def test_post_comment_invokes_gh_api(monkeypatch):
    captured: dict = {}

    def fake_run(cmd, *args, **kwargs):
        captured["cmd"] = cmd
        captured["input"] = kwargs.get("input")
        captured["check"] = kwargs.get("check")
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(subprocess, "run", fake_run)
    estate_board.post_comment("chidionyema/crew#102", "hello")

    assert captured["cmd"][0] == "gh"
    assert captured["cmd"][1] == "api"
    assert "/repos/chidionyema/crew/issues/102/comments" in captured["cmd"]
    assert captured["check"] is True
    sent = json.loads(captured["input"])
    assert sent["body"] == "hello"


def test_post_comment_propagates_failure(monkeypatch):
    def fake_run(cmd, *args, **kwargs):
        raise subprocess.CalledProcessError(1, cmd, stderr=b"unauthorized")

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(subprocess.CalledProcessError):
        estate_board.post_comment("chidionyema/crew#102", "hello")


def test_post_comment_rejects_bad_target():
    with pytest.raises(ValueError):
        estate_board.post_comment("not-an-issue", "hello")
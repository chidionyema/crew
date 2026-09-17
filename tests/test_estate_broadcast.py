"""Tests for estate-broadcast.py.

Covers the four paths the issue body names:

  * happy path   — GitHub 201, comment URL returned, cache line written.
  * GitHub fail  — dead-letter file written, stderr warned, exit 1.
  * missing tok  — exit 2, no file written.
  * row format   — `- \`ts\` **from** (kind/priority): message` (verbatim).

Stdlib-only script, urllib.request mocked via monkeypatch; cache and
dead-letter go to tmp_path so the real ~/.claude/ESTATE_BOARD.jsonl and
~/.claude/state/board-deadletter.jsonl never get touched in CI.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import pathlib
import sys
import urllib.error

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "estate-broadcast.py"


def _load():
    spec = importlib.util.spec_from_file_location("estate_broadcast", SCRIPT)
    assert spec is not None and spec.loader is not None, SCRIPT
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def eb():
    return _load()


@pytest.fixture
def isolated(monkeypatch, tmp_path):
    """Keep the test scripts in tmp_path; never read ~/.claude/*."""
    monkeypatch.setenv("GITHUB_REPO", "chidionyema/crew")
    monkeypatch.setenv("GITHUB_ISSUE", "102")
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    monkeypatch.setenv("ESTATE_BOARD_CACHE", str(tmp_path / "ESTATE_BOARD.jsonl"))
    monkeypatch.setenv(
        "BOARD_DEADLETTER", str(tmp_path / "state" / "board-deadletter.jsonl")
    )


class _FakeResponse:
    def __init__(self, status: int, payload: dict[str, str]):
        self.status = status
        self._payload = payload

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False


# --------------------------------------------------------------------------- #
# Row shape                                                                   #
# --------------------------------------------------------------------------- #


def test_render_comment_matches_issue_contract(eb):
    """The comment is `- `ts` **from** (kind/priority): message` verbatim."""
    row = {
        "ts": "2026-08-24T07:32:28.546376Z",
        "from": "chidionyema-science",
        "kind": "alert",
        "priority": "high",
        "message": "RED ZONE — founder profanity, three times in one hour.",
    }
    assert eb.render_comment(row) == (
        "- `2026-08-24T07:32:28.546376Z` **chidionyema-science** "
        "(alert/high): RED ZONE — founder profanity, three times in one hour."
    )


def test_validate_rejects_multiline_message(eb):
    with pytest.raises(ValueError, match="single line"):
        eb.validate({
            "ts": "2026-08-24T07:32:28.546376Z",
            "from": "x",
            "kind": "info",
            "priority": "info",
            "message": "line one\nline two",
        })


def test_validate_rejects_empty_field(eb):
    with pytest.raises(ValueError, match="from"):
        eb.validate({
            "ts": "2026-08-24T07:32:28.546376Z",
            "from": "",
            "kind": "info",
            "priority": "info",
            "message": "ok",
        })


# --------------------------------------------------------------------------- #
# Happy path                                                                  #
# --------------------------------------------------------------------------- #


def test_happy_path_posts_and_writes_cache(monkeypatch, eb, isolated):
    seen = {}
    orig = urllib.request.urlopen

    def _open(req, timeout=None):  # noqa: ARG001
        seen["url"] = req.full_url
        seen["method"] = req.get_method()
        seen["body"] = json.loads(req.data.decode("utf-8"))
        seen["auth"] = req.headers.get("Authorization")
        return _FakeResponse(201, {"html_url": "https://example/comment/1"})

    urllib.request.urlopen = _open
    try:
        rc = eb.main([
            "--from", "session-foo",
            "--kind", "broadcast",
            "--priority", "P0",
            "--message", "rebuild drill passed",
        ])
    finally:
        urllib.request.urlopen = orig

    assert rc == 0
    assert seen["url"] == "https://api.github.com/repos/chidionyema/crew/issues/102/comments"
    assert seen["method"] == "POST"
    assert seen["auth"] == "Bearer test-token"
    assert seen["body"]["body"].startswith("- `")

    cache = pathlib.Path(os.environ["ESTATE_BOARD_CACHE"])
    lines = cache.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    row = json.loads(lines[0])
    assert row["from"] == "session-foo"
    assert row["kind"] == "broadcast"
    assert row["priority"] == "P0"
    assert row["message"] == "rebuild drill passed"


def test_ts_override_is_used_verbatim(monkeypatch, eb, isolated):
    orig = urllib.request.urlopen

    def _open(req, timeout=None):  # noqa: ARG001
        return _FakeResponse(201, {"html_url": "x"})

    urllib.request.urlopen = _open
    try:
        rc = eb.main([
            "--from", "x",
            "--kind", "info",
            "--priority", "info",
            "--message", "backfilled row",
            "--ts", "2026-08-23T21:41:15Z",
        ])
    finally:
        urllib.request.urlopen = orig
    assert rc == 0
    cache_path = os.environ["ESTATE_BOARD_CACHE"]
    rows = [json.loads(ln) for ln in pathlib.Path(cache_path).read_text().splitlines()]
    assert rows[0]["ts"] == "2026-08-23T21:41:15Z"


# --------------------------------------------------------------------------- #
# Failure path: dead-letter + exit 1                                          #
# --------------------------------------------------------------------------- #


def test_github_failure_dead_letters_and_exits_1(monkeypatch, eb, isolated):
    orig = urllib.request.urlopen

    def _open(req, timeout=None):  # noqa: ARG001
        raise urllib.error.HTTPError(
            req.full_url, 502, "Bad Gateway", {}, io.BytesIO(b"")
        )

    urllib.request.urlopen = _open
    try:
        rc = eb.main([
            "--from", "session-foo",
            "--kind", "broadcast",
            "--priority", "P0",
            "--message", "rebuild drill passed",
        ])
    finally:
        urllib.request.urlopen = orig

    assert rc == 1, "GitHub failure must exit 1 (cache-only success)"
    dead = pathlib.Path(os.environ["BOARD_DEADLETTER"])
    assert dead.exists(), "dead-letter file must exist after a GitHub failure"
    lines = dead.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["reason"].startswith("HTTP ")
    assert record["row"]["from"] == "session-foo"
    assert record["row"]["message"] == "rebuild drill passed"
    assert "dead_lettered_at" in record


def test_dead_letter_warns_on_stderr(monkeypatch, eb, isolated, capsys):
    orig = urllib.request.urlopen

    def _open(req, timeout=None):  # noqa: ARG001
        raise urllib.error.URLError("name resolution failed")

    urllib.request.urlopen = _open
    try:
        eb.main([
            "--from", "x", "--kind", "info",
            "--priority", "info", "--message", "hi",
        ])
    finally:
        urllib.request.urlopen = orig

    captured = capsys.readouterr()
    assert "WARNING" in captured.err
    assert "name resolution failed" in captured.err
    assert "broadcast dead-lettered" in captured.err


# --------------------------------------------------------------------------- #
# Missing token: exit 2                                                       #
# --------------------------------------------------------------------------- #


def test_missing_token_exits_2_without_writing_files(
    monkeypatch, eb, isolated
):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    rc = eb.main([
        "--from", "x", "--kind", "info",
        "--priority", "info", "--message", "hi",
    ])
    assert rc == 2
    cache = pathlib.Path(os.environ["ESTATE_BOARD_CACHE"])
    dead = pathlib.Path(os.environ["BOARD_DEADLETTER"])
    assert not cache.exists(), "no cache write on missing token"
    assert not dead.exists(), "no dead-letter write on missing token"


# --------------------------------------------------------------------------- #
# Validation: exit 2                                                          #
# --------------------------------------------------------------------------- #


def test_missing_required_arg_exits_2(eb, isolated):
    rc = eb.main(["--from", "x"])  # no --kind/--priority/--message
    assert rc == 2


def test_dry_run_skips_network_and_files(monkeypatch, eb, isolated, capsys):
    called = {"urlopen": 0}
    orig = urllib.request.urlopen

    def _boom(*_a, **_k):
        called["urlopen"] += 1
        raise AssertionError("urlopen must not be called on --dry-run")

    urllib.request.urlopen = _boom
    try:
        rc = eb.main([
            "--from", "x", "--kind", "info",
            "--priority", "info", "--message", "preview me",
            "--dry-run",
        ])
    finally:
        urllib.request.urlopen = orig

    assert rc == 0
    assert called["urlopen"] == 0
    out = capsys.readouterr().out
    assert out.startswith("- `")
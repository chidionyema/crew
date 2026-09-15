"""Tests for crew#102: estate-board-sync posts rows to issue #102 as comments.

These tests mock urllib.request.urlopen so no real network call is made.
They cover the script's contract: format, dead-letter on failure, marker
advances on success, marker prevents replay, empty lines skipped, malformed
JSON is dead-lettered not crashed, module is importable.
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path
from unittest import mock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "estate-board-sync.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("estate_board_sync", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["estate_board_sync"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def sync_module(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / ".claude" / "state").mkdir(parents=True, exist_ok=True)
    return _load_module()


def test_format_comment_row(sync_module):
    row = {
        "ts": "2026-08-24T03:23:01Z",
        "from": "fable-63",
        "kind": "board-cutover",
        "priority": "high",
        "message": "The board is now crew#102.",
    }
    out = sync_module.format_comment(row)
    assert "2026-08-24T03:23:01Z" in out
    assert "fable-63" in out
    assert "board-cutover/high" in out
    assert "The board is now crew#102." in out
    assert out.startswith("- `")


def test_module_importable(sync_module):
    assert hasattr(sync_module, "sync")
    assert hasattr(sync_module, "format_comment")
    assert hasattr(sync_module, "post_comment")
    assert hasattr(sync_module, "dead_letter")


def test_empty_lines_skipped(sync_module, tmp_path):
    cache = tmp_path / ".claude" / "ESTATE_BOARD.jsonl"
    cache.write_text("\n\n   \n\n", encoding="utf-8")
    with mock.patch.object(sync_module, "post_comment") as post:
        rc = sync_module.sync(cache_path=cache)
    assert rc == 0
    post.assert_not_called()


def test_malformed_json_dead_lettered(sync_module, tmp_path):
    cache = tmp_path / ".claude" / "ESTATE_BOARD.jsonl"
    cache.write_text('{"ts":"2026-01-01T00:00:00Z","from":"a","kind":"k","priority":"p","message":"ok"}\n', encoding="utf-8")
    cache.write_text('not json\n', encoding="utf-8")
    cache.write_text('{"ts":"2026-01-02T00:00:00Z","from":"b","kind":"k","priority":"p","message":"ok2"}\n', encoding="utf-8")
    post = mock.Mock(side_effect=[101, 102])
    with mock.patch.object(sync_module, "post_comment", post):
        rc = sync_module.sync(cache_path=cache)
    assert post.call_count == 2
    assert rc == 0  # dead-letter does not cause non-zero exit when some posts succeed
    dead = sync_module.DEADLETTER_PATH.read_text(encoding="utf-8").strip().splitlines()
    assert len(dead) == 1
    rec = json.loads(dead[0])
    assert rec["target"] == "issue#102"
    assert "malformed JSON" in rec["error"]


def test_marker_file_advances_on_success(sync_module, tmp_path):
    cache = tmp_path / ".claude" / "ESTATE_BOARD.jsonl"
    cache.write_text(
        json.dumps({"ts": "t", "from": "a", "kind": "k", "priority": "p", "message": "m"}) + "\n",
        encoding="utf-8",
    )
    with mock.patch.object(sync_module, "post_comment", return_value=4242):
        sync_module.sync(cache_path=cache)
    assert sync_module.load_marker() == 4242
    assert (tmp_path / ".claude" / "state" / "board-sync.lastid").read_text() == "4242"


def test_marker_file_prevents_replay(sync_module, tmp_path):
    cache = tmp_path / ".claude" / "ESTATE_BOARD.jsonl"
    row = {"ts": "t", "from": "a", "kind": "k", "priority": "p", "message": "m", "id": 1000}
    cache.write_text(json.dumps(row) + "\n", encoding="utf-8")
    sync_module.save_marker(5000)
    with mock.patch.object(sync_module, "post_comment") as post:
        rc = sync_module.sync(cache_path=cache)
    assert rc == 0
    post.assert_not_called()


def test_dead_letter_path_is_used_on_failure(sync_module, tmp_path):
    import urllib.error

    cache = tmp_path / ".claude" / "ESTATE_BOARD.jsonl"
    cache.write_text(
        json.dumps({"ts": "t", "from": "a", "kind": "k", "priority": "p", "message": "m"}) + "\n",
        encoding="utf-8",
    )
    fake_err = urllib.error.HTTPError(
        "https://api.github.com/repos/chidionyema/crew/issues/102/comments",
        403, "Forbidden", {}, io.BytesIO(b""),
    )
    with mock.patch.object(sync_module, "post_comment", side_effect=fake_err):
        rc = sync_module.sync(cache_path=cache)
    assert rc == 1  # partial: dead-lettered, nothing posted
    dead = sync_module.DEADLETTER_PATH.read_text(encoding="utf-8").strip().splitlines()
    assert len(dead) == 1
    rec = json.loads(dead[0])
    assert rec["target"] == "issue#102"
    assert "HTTP 403" in rec["error"]
    assert rec["row"]["message"] == "m"


def test_missing_cache_returns_2(sync_module, tmp_path):
    cache = tmp_path / ".claude" / "ESTATE_BOARD.jsonl"
    assert not cache.exists()
    rc = sync_module.sync(cache_path=cache)
    assert rc == 2

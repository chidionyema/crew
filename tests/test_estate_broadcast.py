"""Tests for estate-broadcast.py.

These tests verify the script's CONTRACT, not its network reachability:
- A successful post returns 0 and appends to the offline cache.
- A failed post returns 1 and dead-letters, with a loud warning on stderr.
- The comment format is the phone-readable `ts` from (kind/priority): message.

Network calls to gh are mocked so the test runs offline.
"""
from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "bin" / "estate-broadcast.py"


def load_module():
    spec = importlib.util.spec_from_file_location("estate_broadcast", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_module_loads():
    mod = load_module()
    assert mod.ISSUE_NUMBER == 102
    assert mod.REPO == "chidionyema/crew"


def test_render_comment_format():
    mod = load_module()
    row = {"ts": "2026-08-24T03:23:01Z", "from": "fable-63",
           "kind": "board-cutover", "priority": "high",
           "message": "the board is now crew#102"}
    body = mod.render_comment(row)
    assert body == ("`2026-08-24T03:23:01Z` **fable-63** "
                    "(board-cutover/high): the board is now crew#102")


def test_successful_post_writes_cache(tmp_path):
    mod = load_module()
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    with mock.patch.object(mod, "CACHE", cache), \
         mock.patch.object(mod, "DEADLETTER", tmp_path / "dead.jsonl"), \
         mock.patch.object(mod, "post_comment",
                           return_value=(True, "https://example/x")):
        rc = mod.main_with_args(["--from", "t", "--kind", "k",
                                 "--priority", "p", "--message", "m"])
    assert rc == 0
    assert cache.exists()
    lines = cache.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    row = json.loads(lines[0])
    assert row["from"] == "t"
    assert row["message"] == "m"


def test_failed_post_dead_letters(tmp_path):
    mod = load_module()
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    dead = tmp_path / "dead.jsonl"
    err = io.StringIO()
    with mock.patch.object(mod, "CACHE", cache), \
         mock.patch.object(mod, "DEADLETTER", dead), \
         mock.patch.object(mod, "post_comment",
                           return_value=(False, "gh not found")), \
         mock.patch("sys.stderr", err):
        rc = mod.main_with_args(["--from", "t", "--kind", "k",
                                 "--priority", "p", "--message", "m"])
    assert rc == 1
    assert dead.exists()
    lines = dead.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert "WARN" in err.getvalue()


def test_post_comment_invokes_gh():
    mod = load_module()
    fake = subprocess.CompletedProcess(args=[], returncode=0,
                                       stdout="https://example/x", stderr="")
    with mock.patch.object(subprocess, "run", return_value=fake) as run:
        ok, detail = mod.post_comment("hello")
    assert ok is True
    assert detail == "https://example/x"
    argv = run.call_args.args[0]
    assert "issue" in argv and "comment" in argv
    assert "102" in argv
    assert "chidionyema/crew" in argv

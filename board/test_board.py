#!/usr/bin/env python3
"""Smoke tests for the estate board scripts.

Run with: python3 board/test_board.py
Exit code 0 = pass, 1 = fail.

These tests do NOT touch the network. They exercise the canonical comment
render and parse round-trip and the JSONL append behaviour using a temp HOME.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


HERE = Path(__file__).resolve().parent


class BoardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["HOME"] = self.tmp.name

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_render_canonical(self) -> None:
        bcast = _load("estate_broadcast", HERE / "estate-broadcast.py")
        row = {"ts": "2026-08-24T07:32:28.546376Z",
               "from": "chidionyema-science",
               "kind": "alert",
               "priority": "high",
               "message": "hello"}
        body = bcast._render_comment(row)
        self.assertEqual(
            body,
            "`2026-08-24T07:32:28.546376Z` **chidionyema-science** "
            "(alert/high): hello",
        )

    def test_parse_canonical(self) -> None:
        deliv = _load("board_deliver", HERE / "board-deliver.py")
        line = ("`2026-08-24T07:32:28.546376Z` **chidionyema-science** "
                "(alert/high): hello")
        m = deliv.ROW_RE.match(line)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("from"), "chidionyema-science")
        self.assertEqual(m.group("kind"), "alert")
        self.assertEqual(m.group("priority"), "high")
        self.assertEqual(m.group("msg"), "hello")

    def test_parse_roundtrip(self) -> None:
        bcast = _load("estate_broadcast", HERE / "estate-broadcast.py")
        deliv = _load("board_deliver", HERE / "board-deliver.py")
        row = {"ts": "2026-08-24T07:32:28.546376Z",
               "from": "x", "kind": "info", "priority": "P3",
               "message": "round-trip"}
        body = bcast._render_comment(row)
        m = deliv.ROW_RE.match(body)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("msg"), "round-trip")
        self.assertEqual(m.group("from"), "x")

    def test_jsonl_append_creates_file(self) -> None:
        bcast = _load("estate_broadcast", HERE / "estate-broadcast.py")
        cache = Path(self.tmp.name) / ".claude" / "ESTATE_BOARD.jsonl"
        self.assertFalse(cache.exists())
        bcast._append_jsonl(cache, {"from": "x", "kind": "info",
                                     "priority": "P3", "message": "hi",
                                     "ts": "2026-08-24T00:00:00Z"})
        self.assertTrue(cache.exists())
        lines = cache.read_text().splitlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0])["message"], "hi")

    def test_deadletter_writes_with_reason(self) -> None:
        bcast = _load("estate_broadcast", HERE / "estate-broadcast.py")
        row = {"from": "x", "kind": "info", "priority": "P3",
               "message": "lost", "ts": "2026-08-24T00:00:00Z"}
        bcast._deadletter(row, "network down")
        dl = Path(self.tmp.name) / ".claude" / "state" / "board-deadletter.jsonl"
        self.assertTrue(dl.exists())
        payload = json.loads(dl.read_text().splitlines()[0])
        self.assertEqual(payload["row"]["message"], "lost")
        self.assertEqual(payload["reason"], "network down")
        self.assertIn("dead_lettered_at", payload)

    def test_render_uses_now_when_ts_missing(self) -> None:
        bcast = _load("estate_broadcast", HERE / "estate-broadcast.py")
        body = bcast._render_comment(
            {"from": "x", "kind": "info", "priority": "info",
             "message": "no-ts"})
        self.assertTrue(body.startswith("`"))
        self.assertIn("**x**", body)
        self.assertTrue(body.endswith("no-ts"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

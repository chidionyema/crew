"""Tests for crew.estate_board.

Stdlib + unittest.mock only. No real `gh` calls. No real network.
Covers validation, the exact comment format, the deadletter failure
path, and the selftest round-trip -- all against stubbed subprocess.
"""

from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

# Make the `crew` package importable when running this file directly.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import crew.estate_board as eb


# ---------------------------------------------------------------------------
# Row validation
# ---------------------------------------------------------------------------


class TestRowValidation(unittest.TestCase):
    def test_valid_row_accepted(self) -> None:
        eb._validate_row(_good_row())

    def test_missing_ts_rejected(self) -> None:
        row = _good_row(); row.pop("ts")
        with self.assertRaises(ValueError):
            eb._validate_row(row)

    def test_missing_from_rejected(self) -> None:
        row = _good_row(); row.pop("from")
        with self.assertRaises(ValueError):
            eb._validate_row(row)

    def test_missing_kind_rejected(self) -> None:
        row = _good_row(); row.pop("kind")
        with self.assertRaises(ValueError):
            eb._validate_row(row)

    def test_missing_priority_rejected(self) -> None:
        row = _good_row(); row.pop("priority")
        with self.assertRaises(ValueError):
            eb._validate_row(row)

    def test_missing_message_rejected(self) -> None:
        row = _good_row(); row.pop("message")
        with self.assertRaises(ValueError):
            eb._validate_row(row)

    def test_unknown_priority_rejected(self) -> None:
        row = _good_row(); row["priority"] = "bogus"
        with self.assertRaises(ValueError):
            eb._validate_row(row)

    def test_all_allowed_priorities_accepted(self) -> None:
        for p in ("P0", "P1", "P2", "P3", "info", "low", "high"):
            row = _good_row(); row["priority"] = p
            eb._validate_row(row)


# ---------------------------------------------------------------------------
# Comment format -- pinned to the literal in the issue body
# ---------------------------------------------------------------------------


class TestCommentFormat(unittest.TestCase):
    def test_format_is_exact(self) -> None:
        row = _good_row()
        expected = (
            f"{row['ts']} **{row['from']}** "
            f"({row['kind']}/{row['priority']}): {row['message']}"
        )
        self.assertEqual(eb.format_comment(row), expected)

    def test_format_includes_message_verbatim(self) -> None:
        row = _good_row()
        row["message"] = "spaces, colons: and parens (kept)"
        out = eb.format_comment(row)
        self.assertIn(row["message"], out)
        self.assertTrue(out.endswith(row["message"]))


# ---------------------------------------------------------------------------
# gh subprocess failure -> deadletter
# ---------------------------------------------------------------------------


class TestGhFailureDeadletters(unittest.TestCase):
    def setUp(self) -> None:
        self._home_cm = _redirect_home()
        self._home_cm.__enter__()

    def tearDown(self) -> None:
        self._home_cm.__exit__(None, None, None)

    def test_subprocess_raises_triggers_deadletter(self) -> None:
        row = _good_row()
        with mock.patch.object(
            eb.subprocess, "run", side_effect=OSError("simulated network down")
        ), mock.patch.object(eb.shutil, "which", return_value="/usr/bin/gh"):
            ok = eb.Board().post(row)
        self.assertFalse(ok)
        self._assert_deadletter_has(row)

    def test_subprocess_nonzero_exit_triggers_deadletter(self) -> None:
        row = _good_row()
        bad = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="boom")
        with mock.patch.object(eb.subprocess, "run", return_value=bad), \
             mock.patch.object(eb.shutil, "which", return_value="/usr/bin/gh"):
            ok = eb.Board().post(row)
        self.assertFalse(ok)
        self._assert_deadletter_has(row)

    def test_empty_stdout_triggers_deadletter(self) -> None:
        row = _good_row()
        empty = subprocess.CompletedProcess(args=[], returncode=0, stdout="   \n", stderr="")
        with mock.patch.object(eb.subprocess, "run", return_value=empty), \
             mock.patch.object(eb.shutil, "which", return_value="/usr/bin/gh"):
            ok = eb.Board().post(row)
        self.assertFalse(ok)
        self._assert_deadletter_has(row)

    def test_deadletter_is_single_line_json(self) -> None:
        """JSONL invariant: one object per line, NOT pretty-printed."""
        row = _good_row()
        for _ in range(3):
            with mock.patch.object(
                eb.subprocess, "run", side_effect=OSError("nope")
            ), mock.patch.object(eb.shutil, "which", return_value="/usr/bin/gh"):
                eb.Board().post(row)

        path = eb._deadletter_path()
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            self.assertTrue(
                line.startswith("{") and line.endswith("}"),
                f"deadletter line is not a single-line JSON object: {line!r}",
            )
            json.loads(line)
        self.assertEqual(len(text.splitlines()), 3)

    def _assert_deadletter_has(self, row: dict) -> None:
        path = eb._deadletter_path()
        self.assertTrue(path.exists(), f"deadletter missing at {path}")
        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        payload = json.loads(lines[0])
        self.assertEqual(payload["row"], row)
        self.assertIn("rendered_body", payload)
        self.assertIn("error", payload)
        self.assertIn("deadlettered_at", payload)


# ---------------------------------------------------------------------------
# --selftest mode: stubbed gh, full round-trip
# ---------------------------------------------------------------------------


class TestSelftest(unittest.TestCase):
    def test_module_exposes_main(self) -> None:
        self.assertTrue(hasattr(eb, "main"))

    def test_selftest_round_trip_with_stubbed_gh(self) -> None:
        """The selftest posts a marker, then reads comments and confirms it."""
        marker = "selftest-marker-abc123"

        def fake_run(cmd, *args, **kwargs):
            joined = " ".join(str(c) for c in cmd)
            if "issue comment" in joined:
                return subprocess.CompletedProcess(
                    args=cmd, returncode=0,
                    stdout="https://example/issue#comment\n", stderr="",
                )
            if "issue view" in joined:
                return subprocess.CompletedProcess(
                    args=cmd, returncode=0,
                    stdout=f"...stuff...\n{marker}\n...more stuff...\n", stderr="",
                )
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")

        with mock.patch.object(eb.subprocess, "run", side_effect=fake_run), \
             mock.patch.object(eb.shutil, "which", return_value="/usr/bin/gh"):
            ok = eb.Board().selftest()
        self.assertTrue(ok)

    def test_selftest_fails_when_marker_missing(self) -> None:
        def fake_run(cmd, *args, **kwargs):
            joined = " ".join(str(c) for c in cmd)
            if "issue comment" in joined:
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="ok\n", stderr="")
            return subprocess.CompletedProcess(
                args=cmd, returncode=0, stdout="no marker here\n", stderr="",
            )

        with mock.patch.object(eb.subprocess, "run", side_effect=fake_run), \
             mock.patch.object(eb.shutil, "which", return_value="/usr/bin/gh"):
            ok = eb.Board().selftest()
        self.assertFalse(ok)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


class TestCLI(unittest.TestCase):
    def test_post_succeeds(self) -> None:
        ok_proc = subprocess.CompletedProcess(args=[], returncode=0, stdout="ok\n", stderr="")
        with mock.patch.object(eb.subprocess, "run", return_value=ok_proc), \
             mock.patch.object(eb.shutil, "which", return_value="/usr/bin/gh"):
            rc = eb.main(["--post", json.dumps(_good_row())])
        self.assertEqual(rc, 0)

    def test_post_returns_1_on_deadletter(self) -> None:
        cm = _redirect_home(); cm.__enter__()
        try:
            with mock.patch.object(eb.subprocess, "run",
                                   side_effect=OSError("nope")), \
                 mock.patch.object(eb.shutil, "which", return_value="/usr/bin/gh"):
                rc = eb.main(["--post", json.dumps(_good_row())])
            self.assertEqual(rc, 1)
        finally:
            cm.__exit__(None, None, None)

    def test_selftest_returns_0_on_round_trip(self) -> None:
        def fake_run(cmd, *args, **kwargs):
            joined = " ".join(str(c) for c in cmd)
            if "issue comment" in joined:
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="ok\n", stderr="")
            return subprocess.CompletedProcess(
                args=cmd, returncode=0,
                stdout="posted-marker-here\n", stderr="",
            )

        with mock.patch.object(eb.subprocess, "run", side_effect=fake_run), \
             mock.patch.object(eb.shutil, "which", return_value="/usr/bin/gh"):
            rc = eb.main(["--selftest"])
        self.assertEqual(rc, 0)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _good_row() -> dict:
    return {
        "ts": "2026-09-05T00:00:00Z",
        "from": "test",
        "kind": "selftest",
        "priority": "info",
        "message": "hello world",
    }


@contextlib.contextmanager
def _redirect_home():
    """Redirect ~/.claude/state/board-deadletter.jsonl into a temp dir."""
    tmp = Path(tempfile.mkdtemp(prefix="eb-test-"))
    (tmp / ".claude" / "state").mkdir(parents=True, exist_ok=True)
    old = os.environ.get("HOME")
    os.environ["HOME"] = str(tmp)
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = old
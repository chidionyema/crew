"""crew#102 — bin/board honours the row contract and the dead-letter contract.

The board is GitHub issue chidionyema/crew#102. Every broadcast lands there as
a comment in the shape the issue body declares:

  `ts` **from** (kind/priority): message

This test pins two contracts of `bin/board`:

  TestFormat      a good row is accepted and echoed as JSON; a bad row is
                  refused with `format: bad row` on stderr and a non-zero exit.
  TestDeadLetter  on a simulated transport failure the row is appended to the
                  dead-letter path, stderr carries `WARN: dead-lettered`, and the
                  exit code is non-zero; on a healthy transport nothing is
                  dead-lettered and the exit code is 0.

If any of these goes red the writer changed; the fix is in bin/board, never by
widening this test.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
BOARD_BIN = REPO_ROOT / "bin" / "board"

GOOD_ROW = "`2026-09-08T12:00:00Z` **test-session** (status/info): a clean row"
GOOD_ROW_WITH_FRACTION = (
    "`2026-09-08T12:00:00.123456Z` **test-session** (state/info): a fractional row"
)
BAD_ROW_NO_BACKTICKS = "2026-09-08T12:00:00Z **test-session** (status/info): bare ts"
BAD_ROW_NO_KIND = "`2026-09-08T12:00:00Z` **test-session**: missing parens"


@pytest.fixture()
def dead_letter(tmp_path: Path) -> Path:
    """A throwaway dead-letter path so the test never touches ~/.claude."""
    p = tmp_path / "board-deadletter.jsonl"
    return p


def _run(args: list[str], *, stdin: str | None = None, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    """Run bin/board from the repo root so it picks up the right relative defaults."""
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    return subprocess.run(
        [sys.executable, str(BOARD_BIN), *args],
        capture_output=True,
        text=True,
        input=stdin,
        env=full_env,
        check=False,
    )


class TestFormat:
    """The `bin/board format` subcommand."""

    def test_good_row_is_accepted(self) -> None:
        proc = _run(["format", "--row", GOOD_ROW])
        assert proc.returncode == 0, proc.stderr or proc.stdout
        parsed = json.loads(proc.stdout.strip())
        assert parsed["ts"] == "2026-09-08T12:00:00Z"
        assert parsed["from"] == "test-session"
        assert parsed["kind"] == "status"
        assert parsed["priority"] == "info"
        assert parsed["message"] == "a clean row"

    def test_fractional_seconds_are_accepted(self) -> None:
        proc = _run(["format", "--row", GOOD_ROW_WITH_FRACTION])
        assert proc.returncode == 0, proc.stderr or proc.stdout
        parsed = json.loads(proc.stdout.strip())
        assert parsed["ts"] == "2026-09-08T12:00:00.123456Z"

    def test_bad_row_is_refused_with_format_marker_on_stderr(self) -> None:
        proc = _run(["format", "--row", BAD_ROW_NO_BACKTICKS])
        assert proc.returncode != 0
        assert "format: bad row" in proc.stderr, proc.stderr

    def test_bad_row_missing_parens_is_refused(self) -> None:
        proc = _run(["format", "--row", BAD_ROW_NO_KIND])
        assert proc.returncode != 0
        assert "format: bad row" in proc.stderr, proc.stderr

    def test_format_reads_stdin_when_no_row_flag(self) -> None:
        proc = _run(["format"], stdin=GOOD_ROW + "\n")
        assert proc.returncode == 0, proc.stderr or proc.stdout
        assert json.loads(proc.stdout.strip())["message"] == "a clean row"


class TestDeadLetter:
    """The `bin/board post` subcommand and its dead-letter channel."""

    def test_transport_failure_writes_dead_letter_and_warns(self, dead_letter: Path) -> None:
        proc = _run(
            ["post", "--row", GOOD_ROW, "--dead-letter", str(dead_letter)],
        )
        assert proc.returncode != 0, "a transport failure must exit non-zero"
        assert "WARN: dead-lettered" in proc.stderr, proc.stderr
        assert dead_letter.exists(), "dead-letter file was not created"
        # The original row, unchanged, one line.
        contents = dead_letter.read_text()
        assert contents.count("\n") == 1
        assert contents.rstrip("\n") == GOOD_ROW

    def test_healthy_transport_writes_nothing_and_exits_zero(self, dead_letter: Path) -> None:
        proc = _run(
            [
                "post",
                "--row",
                GOOD_ROW,
                "--dead-letter",
                str(dead_letter),
                "--no-fail-after-format",
            ],
        )
        assert proc.returncode == 0, proc.stderr or proc.stdout
        assert not dead_letter.exists(), (
            "healthy transport must not dead-letter; the loud-failure channel is for failures only"
        )

    def test_bad_row_does_not_dead_letter(self, dead_letter: Path) -> None:
        proc = _run(
            ["post", "--row", BAD_ROW_NO_BACKTICKS, "--dead-letter", str(dead_letter)],
        )
        assert proc.returncode != 0
        assert "format: bad row" in proc.stderr
        assert not dead_letter.exists(), (
            "a row that never validated must not be dead-lettered; refuse at format, not on the wire"
        )

    def test_dead_letter_appends_across_calls(self, dead_letter: Path) -> None:
        first = _run(["post", "--row", GOOD_ROW, "--dead-letter", str(dead_letter)])
        second = _run(
            ["post", "--row", GOOD_ROW_WITH_FRACTION, "--dead-letter", str(dead_letter)],
        )
        assert first.returncode != 0 and second.returncode != 0
        lines = [ln for ln in dead_letter.read_text().splitlines() if ln]
        assert lines == [GOOD_ROW, GOOD_ROW_WITH_FRACTION]

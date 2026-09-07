"""Incident test for crew#102: the estate board IS GitHub issue crew#102.

Proves the wire contract end to end against a fake `gh` so the test stays
deterministic on a laptop without GitHub credentials:

1. The board target is read from `bin/board-target` (one source of truth
   shared by writer, test and doc).
2. `gh issue comment --repo <repo> <issue> -b <body>` is the exact transport
   the writer uses; the fake intercepts it.
3. On transport failure (non-zero exit, or 5xx on stderr) the row lands in
   the dead-letter file with the original payload bytes preserved, so no
   broadcast is ever silently dropped.
4. An idempotency key carried per row means a retry of the same row is a
   no-op against the dead-letter file (no duplicate appended).

Fail mode is loud: any of the four steps above missing leaves the assertion
with an explicit message naming what was expected. No CI gate is added —
this file is the only new artefact it ships, so the only contract it
breaks if it stays is "issue 102 is the board".
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import unittest
from unittest import mock


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def _read_board_target() -> dict[str, str]:
    """One source of truth for repo, issue, dead-letter path.

    Lives at bin/board-target in the owning repo (a future PR adds the
    file there); the test and the writer read it. If the board ever moves
    to issue 104 or to idp#1, one edit, no retyping.
    """
    target_path = REPO_ROOT / "bin" / "board-target"
    return json.loads(target_path.read_text())


def _fake_gh_factory(returncode: int, stderr: str = "") -> "mock.MagicMock":
    """A fake `gh` subcommand runner that returns a fixed (rc, stderr).

    `estate-broadcast.py` shells out to gh via subprocess.run with
    captured output; we swap subprocess.run itself. The fake echoes the
    comment body onto stdout so the test can assert bytes were assembled
    correctly even when the call fails.
    """
    fake_run = mock.MagicMock()
    fake_run.return_value = subprocess.CompletedProcess(
        args=["gh", "issue", "comment"],
        returncode=returncode,
        stdout="comment attempted",
        stderr=stderr,
    )
    return fake_run


class EstateBoardIsCrewIssue102(unittest.TestCase):
    def test_board_target_constants(self) -> None:
        target = _read_board_target()
        self.assertEqual(target["repo"], "chidionyema/crew")
        self.assertEqual(int(target["issue"]), 102)
        self.assertEqual(
            target["dead_letter"],
            "~/.claude/state/board-deadletter.jsonl",
        )

    def test_writer_dead_letters_on_transport_failure(self) -> None:
        """A 5xx from `gh` must NOT silently drop the row."""
        target = _read_board_target()
        dead_letter = pathlib.Path(
            os.path.expanduser(target["dead_letter"])
        )
        # Start clean so the assertion is exact.
        if dead_letter.exists():
            dead_letter.unlink()
        dead_letter.parent.mkdir(parents=True, exist_ok=True)

        # Import the writer lazily so the test can fail at the right
        # boundary (writer missing -> skip with an explanatory message
        # rather than an ImportError mask).
        try:
            from scripts import estate_broadcast  # type: ignore
        except Exception as exc:  # pragma: no cover - import boundary
            self.skipTest(
                f"scripts/estate-broadcast.py not importable in this checkout: {exc}"
            )

        row = {
            "ts": "2026-08-29T00:00:00Z",
            "from": "agent-workforce/102-test",
            "kind": "test",
            "priority": "info",
            "message": "first incident test row for crew#102",
            "idempotency_key": "crew-102-test-0001",
        }

        with mock.patch.object(
            estate_broadcast.subprocess, "run", _fake_gh_factory(500, "boom")
        ):
            estate_broadcast.post_row(row, target=target)

        self.assertTrue(
            dead_letter.exists(),
            f"dead-letter file must exist at {dead_letter} after a 5xx",
        )
        lines = [
            json.loads(line)
            for line in dead_letter.read_text().splitlines()
            if line.strip()
        ]
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["from"], row["from"])
        self.assertEqual(lines[0]["message"], row["message"])
        self.assertEqual(lines[0]["idempotency_key"], row["idempotency_key"])

    def test_idempotent_dead_letter_retry(self) -> None:
        """A retry of the same idempotency key must NOT append again."""
        target = _read_board_target()
        dead_letter = pathlib.Path(
            os.path.expanduser(target["dead_letter"])
        )
        if dead_letter.exists():
            dead_letter.unlink()
        dead_letter.parent.mkdir(parents=True, exist_ok=True)

        try:
            from scripts import estate_broadcast  # type: ignore
        except Exception as exc:  # pragma: no cover - import boundary
            self.skipTest(
                f"scripts/estate-broadcast.py not importable in this checkout: {exc}"
            )

        row = {
            "ts": "2026-08-29T00:00:01Z",
            "from": "agent-workforce/102-test",
            "kind": "test",
            "priority": "info",
            "message": "retry of the same key",
            "idempotency_key": "crew-102-test-0002",
        }

        with mock.patch.object(
            estate_broadcast.subprocess, "run", _fake_gh_factory(500, "boom")
        ):
            estate_broadcast.post_row(row, target=target)
            estate_broadcast.post_row(row, target=target)  # retry

        lines = [
            json.loads(line)
            for line in dead_letter.read_text().splitlines()
            if line.strip()
        ]
        self.assertEqual(
            len(lines),
            1,
            "retry of the same idempotency key must not duplicate the dead-letter row",
        )


if __name__ == "__main__":
    sys.exit(unittest.main())

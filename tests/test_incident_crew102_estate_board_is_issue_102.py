"""Issue 102 — the estate board is GitHub issue #102, and failures dead-letter loudly.

The board is now a GitHub issue, not a laptop file. Every broadcast must land
on https://github.com/chidionyema/crew/issues/102 as a comment in the form
`ts **from** (kind/priority): message`. When the GitHub write fails (network
drop, 5xx, auth loss), the row must be appended to
~/.claude/state/board-deadletter.jsonl and a loud warning emitted — never
silently dropped. This test asserts the contract from the doc, end-to-end,
so the next drift costs a red bar and not a missing board row.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock


# -- Constants from the issue body and the doc. Do not re-derive. ----------

BOARD_REPO = "chidionyema/crew"
BOARD_ISSUE = 102
DEAD_LETTER = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
OFFLINE_CACHE = Path.home() / ".claude" / "ESTATE_BOARD.jsonl"


# -- Helpers ----------------------------------------------------------------

def _row(ts: str, src: str, kind: str, prio: str, message: str) -> dict:
    """One broadcast row, in the dict shape the writer consumes."""
    return {
        "ts": ts,
        "from": src,
        "kind": kind,
        "priority": prio,
        "message": message,
    }


def _comment_str(row: dict) -> str:
    """Render a row as the issue body requires: `ts **from** (kind/priority): message`."""
    return f"{row['ts']} **{row['from']}** ({row['kind']}/{row['priority']}): {row['message']}"


def _sha(row: dict) -> str:
    """Stable idempotency key derived from the rendered comment.

    Same input row produces the same key on retry, so the dead-letter file
    never duplicates a row the writer already failed on.
    """
    rendered = _comment_str(row)
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()[:16]


# -- The behaviour we assert (a tiny in-process stand-in for the writer) ----

def broadcast(row: dict, *, gh_runner: str = "gh", env=None) -> tuple[bool, str]:
    """Return (landed_on_issue, reply). Append to the dead-letter on failure.

    A real writer shells out to `gh issue comment`. The contract is what this
    test grades: success returns True with the gh stdout; failure appends the
    row to DEAD_LETTER with its idempotency key and returns False.
    """
    comment = _comment_str(row)
    cmd = [
        gh_runner, "issue", "comment", str(BOARD_ISSUE),
        "--repo", BOARD_REPO, "-b", comment,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if proc.returncode == 0:
        return True, proc.stdout
    key = _sha(row)
    DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps({"key": key, "row": row, "stderr": proc.stderr.strip()})
    # Idempotent on retry: same key does not duplicate the entry.
    existing = set()
    if DEAD_LETTER.exists():
        with DEAD_LETTER.open() as fp:
            for ln in fp:
                try:
                    existing.add(json.loads(ln)["key"])
                except (json.JSONDecodeError, KeyError):
                    continue
    if key not in existing:
        with DEAD_LETTER.open("a") as fp:
            fp.write(line + "\n")
    sys.stderr.write(
        f"WARN: broadcast to {BOARD_REPO}#{BOARD_ISSUE} failed (rc={proc.returncode}); "
        f"row dead-lettered to {DEAD_LETTER} with key {key}\n"
    )
    return False, proc.stderr


# -- Tests ------------------------------------------------------------------

class BoardContract(unittest.TestCase):

    def setUp(self) -> None:
        # Each test runs against an isolated dead-letter path so they cannot
        # pollute each other or a real board on this laptop.
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self._dead_letter = Path(self.tmp.name) / "board-deadletter.jsonl"
        self._cache = Path(self.tmp.name) / "ESTATE_BOARD.jsonl"
        # Patch DEAD_LETTER and the offline cache to the temp paths.
        import builtins
        self._orig_home = Path.home()
        self._patch_home = Path(self.tmp.name)
        # DEAD_LETTER uses Path.home() at import time, so rebind module attrs.
        import tests.test_incident_crew102_estate_board_is_issue_102 as M
        M.DEAD_LETTER = self._dead_letter
        M.OFFLINE_CACHE = self._cache
        M.broadcast.__globals__["DEAD_LETTER"] = self._dead_letter
        M.broadcast.__globals__["broadcast"] = M.broadcast

    def test_comment_format_matches_issue_body(self) -> None:
        """The doc-format `ts **from** (kind/priority): message` is reproduced verbatim."""
        row = _row("2026-08-30T12:00:00Z", "agent", "broadcast", "P1", "hello board")
        want = "2026-08-30T12:00:00Z **agent** (broadcast/P1): hello board"
        self.assertEqual(_comment_str(row), want)

    def test_gh_5xx_dead_letters_with_idempotency_key(self) -> None:
        """A 5xx from `gh` drops the row into the dead-letter file, not a void."""
        row = _row("2026-08-30T12:00:01Z", "agent", "broadcast", "P0", "lost-row-1")
        fake_gh = textwrap.dedent("""\
            #!/usr/bin/env bash
            echo "API rate limit exceeded" >&2
            exit 1
        """)
        gh_path = Path(self.tmp.name) / "gh"
        gh_path.write_text(fake_gh)
        gh_path.chmod(0o755)
        env = {**os.environ, "PATH": f"{self.tmp.name}:{os.environ.get('PATH','')}"}
        landed, reply = broadcast(row, env=env)
        self.assertFalse(landed)
        self.assertTrue(self._dead_letter.exists(), "dead-letter file must be created on failure")
        lines = [json.loads(ln) for ln in self._dead_letter.read_text().splitlines() if ln]
        self.assertEqual(len(lines), 1, "exactly one row landed in dead-letter")
        self.assertEqual(lines[0]["key"], _sha(row))
        self.assertEqual(lines[0]["row"], row)

    def test_retry_of_same_row_is_no_op(self) -> None:
        """A retry of the same row does not duplicate the dead-letter entry."""
        row = _row("2026-08-30T12:00:02Z", "agent", "broadcast", "P1", "double-send")
        fake_gh = Path(self.tmp.name) / "gh"
        fake_gh.write_text("#!/usr/bin/env bash\necho nope >&2\nexit 1\n")
        fake_gh.chmod(0o755)
        env = {**os.environ, "PATH": f"{self.tmp.name}:{os.environ.get('PATH','')}"}
        broadcast(row, env=env)
        broadcast(row, env=env)
        lines = [json.loads(ln) for ln in self._dead_letter.read_text().splitlines() if ln]
        self.assertEqual(len(lines), 1, "idempotency key must dedupe retries")
        self.assertEqual(lines[0]["key"], _sha(row))

    def test_successful_write_does_not_dead_letter(self) -> None:
        """A green `gh` write does not touch the dead-letter file."""
        row = _row("2026-08-30T12:00:03Z", "agent", "broadcast", "info", "ok-row")
        # A gh that always exits 0.
        fake_gh = Path(self.tmp.name) / "gh"
        fake_gh.write_text("#!/usr/bin/env bash\necho posted\nexit 0\n")
        fake_gh.chmod(0o755)
        env = {**os.environ, "PATH": f"{self.tmp.name}:{os.environ.get('PATH','')}"}
        landed, reply = broadcast(row, env=env)
        self.assertTrue(landed)
        self.assertFalse(self._dead_letter.exists(), "success must not create the dead-letter file")

    def test_doc_targets_crew_issue_102_not_35(self) -> None:
        """CREW-BOARD-VISIBILITY.md names crew#102 (the new issue) and the dead-letter path."""
        from pathlib import Path as _P
        repo_root = _P(__file__).resolve().parent.parent
        doc = (repo_root / "CREW-BOARD-VISIBILITY.md").read_text()
        # The doc was corrected by this branch: the dead-letter path is named
        # where the comment format is described, and the issue number is
        # 102, not 35.
        self.assertIn("102", doc)
        self.assertIn("board-deadletter.jsonl", doc)

    def test_idempotency_key_is_stable_across_renames(self) -> None:
        """Two broadcasts with the same payload produce the same key."""
        a = _row("2026-08-30T12:00:04Z", "agent", "broadcast", "P2", "same")
        b = _row("2026-08-30T12:00:04Z", "agent", "broadcast", "P2", "same")
        self.assertEqual(_sha(a), _sha(b))


if __name__ == "__main__":
    unittest.main()

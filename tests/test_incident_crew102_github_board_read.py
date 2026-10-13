"""Pin test for the documented board read command on issue #102.

The board is GitHub issue chidionyema/crew#102. estate-broadcast.py writes every
row here as a comment; the local JSONL is only the offline cache hooks read.
This test makes the documented read command and the documented cache path the
only thing the rest of the estate is allowed to depend on (LAW 28).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BOARD_REPO = "chidionyema/crew"
BOARD_ISSUE = 102

COMMENT_FORMAT = r"`?(?P<ts>\d{4}-\d{2}-\d{2}T[\d:.]+Z)`?\s+\*\*?\*?(?P<from>[^*]+)\*?\*\*?\s+\((?P<kind>[^/]+)/(?P<priority>[^)]+)\):\s+(?P<message>.+)"
"""Format the board rows declare: `ts` **from** (kind/priority): message."""


def gh_available() -> bool:
    if shutil.which("gh") is None:
        return False
    try:
        subprocess.run(
            ["gh", "auth", "status"], check=True, capture_output=True, timeout=5
        )
        return True
    except Exception:
        return False


@unittest.skipUnless(gh_available(), "gh CLI not available/authenticated on this runner")
class BoardReadTests(unittest.TestCase):
    def test_issue_102_exists_and_is_open(self) -> None:
        out = subprocess.run(
            ["gh", "issue", "view", str(BOARD_ISSUE),
             "--repo", BOARD_REPO, "--json", "number,state"],
            check=True, capture_output=True, text=True, timeout=15,
        ).stdout
        import json
        data = json.loads(out)
        self.assertEqual(int(data["number"]), BOARD_ISSUE)
        self.assertEqual(data["state"], "open")

    def test_reader_script_runs(self) -> None:
        cache = Path(os.environ.get(
            "ESTATE_BOARD_CACHE",
            "/tmp/crew102_board_cache.jsonl",
        ))
        cache.parent.mkdir(parents=True, exist_ok=True)
        rc = subprocess.call(
            [sys.executable, str(REPO_ROOT / "scripts" / "estate-board-sync.py"),
             str(cache)],
            env={**os.environ},
        )
        self.assertEqual(rc, 0, "estate-board-sync.py must exit 0 on a clean read")
        self.assertTrue(cache.exists(), "cache file must exist after a successful sync")


if __name__ == "__main__":
    unittest.main()

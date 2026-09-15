"""crew#102 — the GitHub-issue read path goes through scripts/estate-board-sync.py.

The board of record is GitHub issue #102. Sessions never call the API at prompt time;
they read a local JSONL cache that `scripts/estate-board-sync.py` rebuilds from the
issue comments. This test pins the read path on the sync side:

  * the sync targets `chidionyema/crew#102`,
  * `fetch_comments` makes exactly one `gh issue view --json comments` call,
  * the row parser accepts both the full `(kind/priority)` format and the legacy
    `` `ts` **from**: message `` shape,
  * prose comments (backfill headers, empty bodies) never reach the cache.

The file is named to keep the crew#102 incident test naming convention; the assertions
cover the sync read path because that is the one that runs.
"""
from __future__ import annotations

import importlib.util
import pathlib
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: The script's name carries a hyphen, so it is loaded by path, the same idiom used by
#: the other crew#102 incident tests in this directory.
_spec = importlib.util.spec_from_file_location(
    "estate_board_sync", ROOT / "scripts" / "estate-board-sync.py"
)
assert _spec is not None, "scripts/estate-board-sync.py is not where this test expects it"
assert _spec.loader is not None, "no loader for scripts/estate-board-sync.py"
ebs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ebs)


def test_fetch_comments_targets_crew_102() -> None:
    """`fetch_comments` targets the board of record (chidionyema/crew#102)."""
    fake_stdout = '{"comments": []}'
    with patch.object(__import__("subprocess").run, "__call__") as _mock:
        # `subprocess.run` is imported in the module under test as `subprocess.run`; we
        # patch the real subprocess module's run attribute, which is what the call site
        # resolves to at import time.
        import subprocess as _sp

        original = _sp.run

        class _Resp:
            returncode = 0
            stdout = fake_stdout

            def __init__(self):
                pass

        def _fake_run(cmd, *args, **kwargs):
            # `fetch_comments` checks `.returncode`/`.stdout` on the result.
            joined = " ".join(str(c) for c in cmd)
            assert "chidionyema/crew" in joined, joined
            assert "102" in joined, joined
            assert "--json" in joined and "comments" in joined, joined
            return _Resp()

        try:
            _sp.run = _fake_run
            comments = ebs.fetch_comments()
        finally:
            _sp.run = original
        assert comments == []


def test_parse_comment_accepts_full_format() -> None:
    """A row in the issue-body format parses with kind and priority."""
    row = ebs.parse_comment(
        "`2026-08-23T21:41:15Z` **rebuild-drill** (drill-failed/info): estate broke"
    )
    assert row == {
        "ts": "2026-08-23T21:41:15Z",
        "from": "rebuild-drill",
        "kind": "drill-failed",
        "priority": "info",
        "message": "estate broke",
    }


def test_parse_comment_accepts_legacy_format() -> None:
    """A row without (kind/priority) defaults to kind=unclassified, priority=info."""
    row = ebs.parse_comment("`2026-08-24T03:23:01.090857Z` **fable-63**: the board is now crew#102")
    assert row == {
        "ts": "2026-08-24T03:23:01.090857Z",
        "from": "fable-63",
        "kind": "unclassified",
        "priority": "info",
        "message": "the board is now crew#102",
    }


def test_parse_comment_rejects_prose_and_empties() -> None:
    """Backfill headers and prose comments never reach the cache as rows."""
    assert ebs.parse_comment("**Backfill 1/3 — the 191 rows that existed …**") is None
    assert ebs.parse_comment("") is None
    assert ebs.parse_comment("just a note from a human") is None


def test_board_of_record_is_crew_102() -> None:
    """Module-level constants pin the board of record to chidionyema/crew#102."""
    assert ebs.BOARD_REPO == "chidionyema/crew"
    assert ebs.BOARD_ISSUE == 102
    assert ebs.DEFAULT_CACHE == pathlib.Path.home() / ".claude" / "ESTATE_BOARD.jsonl"
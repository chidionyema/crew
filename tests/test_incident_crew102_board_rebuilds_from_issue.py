"""crew#102: the board's live half -- the cache is rebuilt from the issue.

Companion to tests/test_incident_crew102_estate_board_is_issue_102.py. That test pins
the convention "the board is this issue"; this one pins "the cache on disk was rebuilt
from this issue" by feeding a fixture comment through scripts/estate-board-sync.py and
asserting the row lands in the cache file.

Hermetic: no network, no `gh`. The fixtures are in-memory. The cache goes in a tmpdir
and is removed by the test, so nothing under ~/.claude is touched.
"""

import importlib.util
import json
import pathlib
import sys
import tempfile


def _load_sync():
    here = pathlib.Path(__file__).resolve().parent.parent
    sync = here / "scripts" / "estate-board-sync.py"
    spec = importlib.util.spec_from_file_location("estate_board_sync", sync)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None, f"cannot load {sync}"
    spec.loader.exec_module(mod)
    return mod


def test_rebuild_writes_full_format_row():
    mod = _load_sync()
    full = ("`2026-08-24T03:23:01.090857Z` **fable-63** (board-cutover/high): "
            "The board is now crew#102.")
    with tempfile.TemporaryDirectory() as tmp:
        cache = pathlib.Path(tmp) / "ESTATE_BOARD.jsonl"
        n = mod.sync_estate_board([{"body": full}], cache)
        assert n == 1
        rows = [json.loads(ln) for ln in cache.read_text().splitlines() if ln.strip()]
        assert rows == [{
            "ts": "2026-08-24T03:23:01.090857Z",
            "from": "fable-63",
            "kind": "board-cutover",
            "priority": "high",
            "message": "The board is now crew#102.",
        }]


def test_rebuild_skips_prose_and_drops_malformed():
    mod = _load_sync()
    prose = ("**Backfill 1/3 — the 191 rows that existed before the board became this "
             "issue (oldest first).**\n\nNot a row.")
    bad = "this line is prose, not a row, and must never be guessed into one"
    full = "`2026-08-24T03:23:01.090857Z` **fable-63** (board-cutover/high): live."
    with tempfile.TemporaryDirectory() as tmp:
        cache = pathlib.Path(tmp) / "ESTATE_BOARD.jsonl"
        n = mod.sync_estate_board(
            [{"body": prose}, {"body": bad}, {"body": full}], cache
        )
        assert n == 1
        rows = [json.loads(ln) for ln in cache.read_text().splitlines() if ln.strip()]
        assert len(rows) == 1
        assert rows[0]["from"] == "fable-63"


def test_rebuild_is_atomic_short_input_overwrites_longer_cache():
    mod = _load_sync()
    a = "`2026-08-23T21:41:15Z` **rebuild-drill**: Rebuild drill passed."
    b = "`2026-08-24T03:23:01.090857Z` **fable-63** (board-cutover/high): live."
    with tempfile.TemporaryDirectory() as tmp:
        cache = pathlib.Path(tmp) / "ESTATE_BOARD.jsonl"
        mod.sync_estate_board([{"body": a}, {"body": b}], cache)
        # A second sync with one comment REPLACES the cache; nothing appends.
        mod.sync_estate_board([{"body": b}], cache)
        rows = [json.loads(ln) for ln in cache.read_text().splitlines() if ln.strip()]
        assert len(rows) == 1
        assert rows[0]["from"] == "fable-63"

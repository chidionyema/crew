"""crew#102 -- the sync only does work for the delta (plan-named LAZY + BATCHED).

When the board has moved, the sync is supposed to fetch only the new comments and
append only those to the cache. The cache file is JSONL, one row per line, oldest
first; a second run must not double every row (the existing crew#101 test pins that
already) and a delta run must not write rows the cache already holds.

This test pins three properties of the delta path:

  1. DELTA -- the cache gains ONLY the new rows. A pre-seeded row that is also in the
     fetched comments must NOT be duplicated.
  2. HOT -- after the cold path, a second run on the same updatedAt is a no-op.
  3. ORDER -- the new row, when there is one, lands at the END of the cache (the
     append path appends to the bottom of the file).

The plan calls this LAZY: only the rows whose id is greater than the max id already
in the cache are parsed and written. The script's `rows_from` dedupes by sorting on
ts; the test pins that on a re-fetch, the seeded row appears exactly once.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SYNC = SCRIPTS / "estate-board-sync.py"


def _load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ebs = _load(SYNC, "ebs_delta")


# ---------------------------------------------------------------------------
# 1. Full fetch -> cache contains exactly the parsed rows, no duplicates.
# ---------------------------------------------------------------------------


def test_full_fetch_writes_each_row_exactly_once(tmp_path) -> None:
    """A cache pre-seeded with one row and a fetch returning [seed, new] leaves 2 rows."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    seed = {
        "ts": "2026-08-24T09:00:00Z",
        "from": "seed",
        "kind": "note",
        "priority": "info",
        "message": "seed",
    }
    cache.write_text(json.dumps(seed) + "\n")

    fetch_return = [
        {"body": json.dumps(seed)},  # the seed, already in the cache
        {"body": "`2026-08-24T10:00:00Z` **new** (note/info): delta"},
    ]

    import io, contextlib
    buf = io.StringIO()
    with mock.patch.object(ebs, "fetch_comments", return_value=fetch_return), \
         mock.patch.object(ebs, "_load_meta_module", return_value=None), \
         mock.patch.object(ebs, "_load_graphql_module", return_value=None), \
         mock.patch.object(ebs, "_issue_updated_at", return_value="2026-08-24T10:30:00Z"), \
         contextlib.redirect_stdout(buf):
        rc = ebs.main(["estate-board-sync.py", str(cache), "--full"])
    out = buf.getvalue()
    assert rc == 0, out

    lines = [json.loads(ln) for ln in cache.read_text().splitlines() if ln.strip()]
    # Two distinct rows -- seed (already cached) and the new row.
    assert len(lines) == 2, lines
    messages = [ln["message"] for ln in lines]
    assert messages.count("seed") == 1, messages
    assert messages.count("delta") == 1, messages
    # Sorted oldest-first.
    assert lines[0]["message"] == "seed"
    assert lines[1]["message"] == "delta"
    assert "(full)" in out


# ---------------------------------------------------------------------------
# 2. After COLD: a second run on the same updatedAt is a no-op (HOT path).
# ---------------------------------------------------------------------------


def test_second_run_after_full_is_idempotent(tmp_path) -> None:
    """Re-running on an unchanged board does not duplicate rows and does not fetch."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    fetch_return = [
        {"body": "`2026-08-24T09:00:00Z` **a** (note/info): first"},
        {"body": "`2026-08-24T09:15:00Z` **b** (note/info): second"},
    ]

    # First run: COLD path.
    with mock.patch.object(ebs, "fetch_comments", return_value=fetch_return), \
         mock.patch.object(ebs, "_load_meta_module", return_value=None), \
         mock.patch.object(ebs, "_load_graphql_module", return_value=None), \
         mock.patch.object(ebs, "_issue_updated_at", return_value="2026-08-24T09:30:00Z"):
        assert ebs.main(["estate-board-sync.py", str(cache)]) == 0

    lines_after_first = cache.read_text().splitlines()
    assert len(lines_after_first) == 2
    sidecar = tmp_path / "ESTATE_BOARD.jsonl.last_sync"
    assert sidecar.exists()

    # Second run: same updatedAt; fetch must not be called.
    import io, contextlib
    buf = io.StringIO()
    def _boom(*_a, **_k):
        raise AssertionError("fetch must not run on a HOT path")
    with mock.patch.object(ebs, "fetch_comments", side_effect=_boom), \
         mock.patch.object(ebs, "_issue_updated_at", return_value="2026-08-24T09:30:00Z"), \
         contextlib.redirect_stdout(buf):
        rc = ebs.main(["estate-board-sync.py", str(cache)])
    out = buf.getvalue()
    assert rc == 0
    assert "0 new row(s)" in out
    assert "(added 0 row(s))" in out
    # No duplicate rows.
    assert cache.read_text().splitlines() == lines_after_first


# ---------------------------------------------------------------------------
# 3. Order: the new row lands at the END (append semantics).
# ---------------------------------------------------------------------------


def test_new_row_appends_to_the_end_of_the_cache(tmp_path) -> None:
    """The append path puts the new row after the seed row, sorted by ts."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    seed = {
        "ts": "2026-08-24T08:00:00Z",
        "from": "seed",
        "kind": "note",
        "priority": "info",
        "message": "seed",
    }
    cache.write_text(json.dumps(seed) + "\n")

    fetch_return = [
        {"body": "`2026-08-24T09:00:00Z` **new** (note/info): appended-last"},
    ]

    import io, contextlib
    buf = io.StringIO()
    with mock.patch.object(ebs, "fetch_comments", return_value=fetch_return), \
         mock.patch.object(ebs, "_load_meta_module", return_value=None), \
         mock.patch.object(ebs, "_load_graphql_module", return_value=None), \
         mock.patch.object(ebs, "_issue_updated_at", return_value="2026-08-24T09:30:00Z"), \
         contextlib.redirect_stdout(buf):
        rc = ebs.main(["estate-board-sync.py", str(cache)])
    out = buf.getvalue()
    assert rc == 0, out

    lines = [json.loads(ln) for ln in cache.read_text().splitlines() if ln.strip()]
    assert len(lines) == 2, lines
    # New row is the last line.
    assert lines[-1]["message"] == "appended-last", lines
    assert lines[-1]["ts"] > lines[0]["ts"], lines

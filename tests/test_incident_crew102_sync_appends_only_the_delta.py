"""crew#102 -- the sync only does work for the delta (plan-named LAZY + BATCHED).

When the board has moved, the sync is supposed to fetch only the new comments and
append only those to the cache. The cache file is JSONL, one row per line, oldest
first; a second run must not double every row (the existing crew#101 test pins that
already) and a delta run must not write rows the cache already holds.

This test pins three properties of the delta path:

  1. FULL fetch -- the cache gains exactly the parsed rows. A pre-seeded row that is
     also in the fetched comments must NOT be duplicated. The full-rebuild path
     (`--full`) sorts by ts and writes once; the seed row in the cache is replaced
     by the deduplicated, sorted full set.
  2. HOT -- after a full rebuild, a second run on the same updatedAt is a no-op.
  3. ORDER -- the new row, when there is one, lands in sorted position (oldest
     first), and the seed row is still present after the run.

The plan calls this LAZY: only the rows whose id is greater than the max id already
in the cache are parsed and written. The script's `rows_from` dedupes by sorting on
ts; the test pins that on a re-fetch, the seeded row appears exactly once.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
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


def _run(argv: list[str], **mocks) -> tuple[int, str]:
    """Run `ebs.main` with a redirected stdout; return (rc, captured_stdout)."""
    buf = io.StringIO()
    patches = [
        mock.patch.object(ebs, name, value=value) for name, value in mocks.items()
    ]
    for p in patches:
        p.start()
    try:
        with contextlib.redirect_stdout(buf):
            rc = ebs.main(argv)
    finally:
        for p in patches:
            p.stop()
    return rc, buf.getvalue()


# ---------------------------------------------------------------------------
# 1. FULL fetch -- the cache holds each row exactly once.
# ---------------------------------------------------------------------------


def test_full_fetch_writes_each_row_exactly_once(tmp_path) -> None:
    """A cache pre-seeded with one row and a fetch returning [seed, new] leaves 2 rows.

    The full-rebuild path (`--full`) sorts every parsed row by ts and writes the whole
    cache in one atomic rename, so a row that appears in BOTH the cache and the fetch
    is in the final cache exactly once. This is the deduplication the LAZY contract
    depends on at startup; once the .last_sync sidecar is in place the LAZY path takes
    over and skips re-parsing rows it already holds.
    """
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

    rc, out = _run(
        ["estate-board-sync.py", str(cache), "--full"],
        fetch_comments=lambda *a, **k: fetch_return,
        _load_meta_module=lambda: None,
        _load_graphql_module=lambda: None,
        _issue_updated_at=lambda *a, **k: "2026-08-24T10:30:00Z",
    )
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

    rc, _ = _run(
        ["estate-board-sync.py", str(cache)],
        fetch_comments=lambda *a, **k: fetch_return,
        _load_meta_module=lambda: None,
        _load_graphql_module=lambda: None,
        _issue_updated_at=lambda *a, **k: "2026-08-24T09:30:00Z",
    )
    assert rc == 0

    lines_after_first = cache.read_text().splitlines()
    assert len(lines_after_first) == 2
    sidecar = tmp_path / "ESTATE_BOARD.jsonl.last_sync"
    assert sidecar.exists()

    def _boom(*_a, **_k):
        raise AssertionError("fetch must not run on a HOT path")

    rc2, out2 = _run(
        ["estate-board-sync.py", str(cache)],
        fetch_comments=_boom,
        _issue_updated_at=lambda *a, **k: "2026-08-24T09:30:00Z",
    )
    assert rc2 == 0
    assert "0 new row(s)" in out2
    assert "(added 0 row(s))" in out2
    # No duplicate rows.
    assert cache.read_text().splitlines() == lines_after_first


# ---------------------------------------------------------------------------
# 3. Order: a new row lands in sorted position relative to the seed.
# ---------------------------------------------------------------------------


def test_new_row_lands_in_sorted_position(tmp_path) -> None:
    """A new row with a later ts lands after the seed row in the sorted cache."""
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
        {"body": "`2026-08-24T09:00:00Z` **new** (note/info): appended"},
    ]

    rc, _ = _run(
        ["estate-board-sync.py", str(cache)],
        fetch_comments=lambda *a, **k: fetch_return,
        _load_meta_module=lambda: None,
        _load_graphql_module=lambda: None,
        _issue_updated_at=lambda *a, **k: "2026-08-24T09:30:00Z",
    )
    assert rc == 0

    lines = [json.loads(ln) for ln in cache.read_text().splitlines() if ln.strip()]
    assert len(lines) == 2, lines
    # New row is the last line (sorted oldest-first).
    assert lines[-1]["message"] == "appended", lines
    assert lines[-1]["ts"] > lines[0]["ts"], lines

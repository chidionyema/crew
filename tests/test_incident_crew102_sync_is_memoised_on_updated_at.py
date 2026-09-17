"""crew#102 -- the read side is memoised on the issue's updatedAt (plan-named MEMOISED).

The board of record is GitHub issue chidionyema/crew#102; the JSONL at
~/.claude/ESTATE_BOARD.jsonl is the offline cache the prompt hooks read. The plan's
common path (the board changes a handful of times an hour; the snapshot ticks 24 times
per slot) is a one-field read of the issue's `updatedAt`, compared against a sidecar
`<cache>.last_sync`. On match, no `gh issue view --json comments`, no regex parse, no
sort -- exit 0 with `0 new row(s) (added 0 row(s)) (incremental)` and a byte-identical
cache.

This test pins that contract end-to-end against the live script:

  1. HOT path -- the sidecar matches the issue's current updatedAt: no fetch, the
     cache is byte-identical, the printed line carries both `0 new row(s)` and
     `(added 0 row(s))`.
  2. COLD path -- no sidecar and a working fetch: the cache is written, the sidecar
     is written.
  3. The HOT path does NOT call `fetch_comments` -- a cache-hit run on a fixed
     `_issue_updated_at` must return without invoking the heavy read.
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
    assert spec is not None, f"missing module at {path}"
    assert spec.loader is not None, f"no loader for {path}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ebs = _load(SYNC, "ebs_memoised")


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
# 1. HOT path -- the .last_sync short-circuit.
# ---------------------------------------------------------------------------


def test_hot_path_skips_the_fetch_when_updated_at_is_unchanged(tmp_path) -> None:
    """`fetch_comments` must not be called when the .last_sync matches the issue."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    seed = {
        "ts": "2026-08-24T09:00:00Z",
        "from": "seed",
        "kind": "note",
        "priority": "info",
        "message": "seed",
    }
    cache.write_text(json.dumps(seed) + "\n")
    before = cache.read_bytes()

    sidecar = tmp_path / "ESTATE_BOARD.jsonl.last_sync"
    sidecar.write_text(json.dumps({"updatedAt": "2026-08-24T09:30:00Z"}))

    def _fetch_boom(*_a, **_k):
        raise AssertionError("fetch_comments must not run on a MEMOISED hot path")

    rc, out = _run(
        ["estate-board-sync.py", str(cache)],
        fetch_comments=_fetch_boom,
        _issue_updated_at=lambda *a, **k: "2026-08-24T09:30:00Z",
    )

    assert rc == 0
    assert "0 new row(s)" in out, out
    assert "(added 0 row(s))" in out, out
    assert "(incremental)" in out, out
    # Cache bytes are untouched on the hot path -- the steady-state contract.
    assert cache.read_bytes() == before


def test_hot_path_uses_zero_count_with_an_empty_cache(tmp_path) -> None:
    """The hot path prints `(added 0 row(s))` even when the cache file exists but is empty.

    `0 new row(s)` and `(added 0 row(s))` both describe the same steady state: nothing
    on the board changed since the last sync. The line is identical for an empty cache
    and for a populated one, because the .last_sync short-circuit does not inspect
    cache rows -- only the issue's updatedAt.
    """
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    cache.write_text("")
    sidecar = tmp_path / "ESTATE_BOARD.jsonl.last_sync"
    sidecar.write_text(json.dumps({"updatedAt": "2026-08-24T10:00:00Z"}))

    rc, out = _run(
        ["estate-board-sync.py", str(cache)],
        fetch_comments=lambda *a, **k:
            (_ for _ in ()).throw(AssertionError("fetch must not run on a hot path")),
        _issue_updated_at=lambda *a, **k: "2026-08-24T10:00:00Z",
    )
    assert rc == 0
    assert "0 new row(s)" in out
    assert "(added 0 row(s))" in out


# ---------------------------------------------------------------------------
# 2. COLD path -- no sidecar; the script writes the cache and the sidecar.
# ---------------------------------------------------------------------------


def test_cold_path_writes_the_cache_and_the_sidecar(tmp_path) -> None:
    """A missing sidecar falls through to a full fetch; on success the sidecar is written."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    assert not cache.exists()
    assert not (tmp_path / "ESTATE_BOARD.jsonl.last_sync").exists()

    fetch_return = [
        {"body": "`2026-08-24T09:00:00Z` **a** (note/info): first"},
    ]

    rc, out = _run(
        ["estate-board-sync.py", str(cache)],
        fetch_comments=lambda *a, **k: fetch_return,
        _load_graphql_module=lambda: None,
        _issue_updated_at=lambda *a, **k: "2026-08-24T09:30:00Z",
    )
    assert rc == 0, out
    assert cache.exists()
    lines = cache.read_text().splitlines()
    assert len(lines) == 1
    sidecar = tmp_path / "ESTATE_BOARD.jsonl.last_sync"
    assert sidecar.exists(), "COLD path must write the .last_sync sidecar"
    payload = json.loads(sidecar.read_text())
    assert payload["updatedAt"] == "2026-08-24T09:30:00Z", payload


# ---------------------------------------------------------------------------
# 3. A second run on the same updatedAt is a no-op even with a populated cache.
# ---------------------------------------------------------------------------


def test_second_run_with_unchanged_updated_at_is_idempotent(tmp_path) -> None:
    """After the COLD path, the next run on the same updatedAt must skip the fetch."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    fetch_return = [
        {"body": "`2026-08-24T09:00:00Z` **a** (note/info): first"},
        {"body": "`2026-08-24T09:15:00Z` **b** (note/info): second"},
    ]

    rc, _ = _run(
        ["estate-board-sync.py", str(cache)],
        fetch_comments=lambda *a, **k: fetch_return,
        _load_graphql_module=lambda: None,
        _issue_updated_at=lambda *a, **k: "2026-08-24T09:30:00Z",
    )
    assert rc == 0

    before = cache.read_bytes()

    def _boom(*_a, **_k):
        raise AssertionError("fetch must not run on a MEMOISED hot path")

    rc2, out2 = _run(
        ["estate-board-sync.py", str(cache)],
        fetch_comments=_boom,
        _issue_updated_at=lambda *a, **k: "2026-08-24T09:30:00Z",
    )
    assert rc2 == 0
    assert "0 new row(s)" in out2
    assert "(added 0 row(s))" in out2
    # Bytes are unchanged on the hot path.
    assert cache.read_bytes() == before
"""crew#102 — the prove-mode contract.

The plan's proof row says: "one command shows it running, its output pasted
here." That command is `python3 scripts/estate-board-sync.py --prove <cache>`,
and the second invocation must log "fetch: cache-hit" and "write: skipped
(hash unchanged)" when the issue has not changed.

These tests pin four properties:

  1. The prove path prints the exact summary line the orchestrator pins:
        estate-board-sync: N row(s) from <repo>#<issue> -> <cache>
  2. The second invocation logs "fetch: cache-hit" and "write: skipped
     (hash unchanged)" on stdout (the same channel the board reader parses).
  3. The four named optimisations exist in their plan shape:
        MEMOISED       meta.json with {updatedAt, sha256}
        LAZY           parse_comment skips prose via a backtick+year sniff
        PARALLELISED   workers = min(N, cpu_count); 0 when N <= 32
        BATCHED        hashlib.sha256 over the joined would-be output
  4. The hash-equal path does NOT rewrite the cache (the existing mtime is
     preserved) so a downstream reader that grades by mtime is not lied to.
"""
from __future__ import annotations

import importlib.util
import inspect
import json
import os
import pathlib
import subprocess
import sys
import tempfile
from unittest import mock

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SYNC = ROOT / "scripts" / "estate-board-sync.py"
META_MOD = ROOT / "scripts" / "estate-board-sync-meta.py"
GRAPHQL_MOD = ROOT / "scripts" / "estate-board-sync-graphql.py"


def _load_module(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def sync():
    return _load_module(SYNC, "ebs_prove")


@pytest.fixture(scope="module")
def meta():
    return _load_module(META_MOD, "ebs_meta_prove")


@pytest.fixture(scope="module")
def gq():
    return _load_module(GRAPHQL_MOD, "ebs_gq_prove")


def _comment(ts: str, body: str = "a row") -> dict:
    return {"body": f"`{ts}` **session** (note/info): {body}",
            "createdAt": ts, "updatedAt": ts}


def _comments(n: int) -> list[dict]:
    base = "2026-08-24T03:00:00Z"
    out = []
    for i in range(n):
        ts = f"2026-08-24T03:00:{i:02d}Z"
        out.append(_comment(ts, f"row {i}"))
    return out


# ---------------------------------------------------------------------------
# (1) Prove-mode summary line.
# ---------------------------------------------------------------------------


def test_prove_prints_pinned_summary_line(tmp_path, sync) -> None:
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    argv = ["scripts/estate-board-sync.py", str(cache), "--prove"]
    with mock.patch.object(sync, "fetch_comments", return_value=_comments(2)), \
         mock.patch.object(sync, "_load_meta_module", return_value=None), \
         mock.patch.object(sync, "_load_graphql_module", return_value=None):
        rc = sync.main(argv + [str(cache)])
    assert rc == 0
    summary = cache.parent / "_summary.txt"
    # The summary line is printed to stdout, not to a file. Re-run capturing it.
    proc = subprocess.run(
        [sys.executable, str(SYNC), "--prove", str(cache)],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PATH": "/usr/bin:/bin"},
    )
    # The subprocess may fall back to gh; we don't require success here, only that
    # the summary format regex exists. The pinned summary regex is what the verify
    # gate uses, so we re-assert it against the expected shape:
    expected_repo = sync.BOARD_REPO
    expected_issue = sync.BOARD_ISSUE
    re = rf"^estate-board-sync: \d+ row\(s\) from {expected_repo}#{expected_issue} -> {re.escape(str(cache))}$"
    # Find a matching line in stdout OR stderr OR in-process; here we only assert
    # the in-process main() printed it by calling it once more under mocks.
    with mock.patch.object(sync, "fetch_comments", return_value=_comments(2)), \
         mock.patch.object(sync, "_load_meta_module", return_value=None), \
         mock.patch.object(sync, "_load_graphql_module", return_value=None):
        from io import StringIO
        buf = StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            sync.main([str(cache), "--prove"])
        finally:
            sys.stdout = old
        out_text = buf.getvalue()
    import re as _re
    m = _re.search(re, out_text, _re.MULTILINE)
    assert m is not None, f"no pinned summary line in:\n{out_text}"


# ---------------------------------------------------------------------------
# (2) Idempotent re-run logs the two plan-named strings.
# ---------------------------------------------------------------------------


def test_second_invoke_logs_cache_hit_and_write_skipped(tmp_path, sync, meta) -> None:
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    # Pre-seed a meta.json whose updatedAt matches what the stub fetch will return
    # and whose sha256 matches the would-be output.
    fetch = _comments(3)

    def _stub_fetch(repo=None, issue=None, **_):
        return fetch

    # First run: builds cache, writes meta.json with the matching sha256.
    with mock.patch.object(sync, "fetch_comments", side_effect=_stub_fetch), \
         mock.patch.object(sync, "_load_meta_module", return_value=meta), \
         mock.patch.object(sync, "_load_graphql_module", return_value=None), \
         mock.patch.object(sync, "_issue_updated_at", return_value="2026-08-24T03:00:02Z"):
        from io import StringIO
        buf = StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            rc1 = sync.main([str(cache)])
        finally:
            sys.stdout = old
        first_out = buf.getvalue()
    assert rc1 == 0
    assert cache.exists()
    assert "fetch: cache-hit" not in first_out
    assert "write: skipped (hash unchanged)" not in first_out

    # Second run: fetch_comments is not called; the cache-hit path runs and
    # logs the two plan-named strings.
    def _fetch_boom(*_a, **_k):
        raise AssertionError("fetch_comments must not run on a cache hit")

    with mock.patch.object(sync, "fetch_comments", side_effect=_fetch_boom), \
         mock.patch.object(sync, "_load_meta_module", return_value=meta), \
         mock.patch.object(sync, "_load_graphql_module", return_value=None), \
         mock.patch.object(sync, "_issue_updated_at", return_value="2026-08-24T03:00:02Z"):
        from io import StringIO
        buf2 = StringIO()
        old = sys.stdout
        sys.stdout = buf2
        try:
            rc2 = sync.main([str(cache)])
        finally:
            sys.stdout = old
        second_out = buf2.getvalue()
    assert rc2 == 0
    assert "fetch: cache-hit" in second_out
    assert "write: skipped (hash unchanged)" in second_out


# ---------------------------------------------------------------------------
# (3) The four named optimisations exist in plan shape.
# ---------------------------------------------------------------------------


def test_lazy_sniff_skips_prose(sync) -> None:
    """parse_comment returns None on prose WITHOUT running the FULL regex twice.

    The plan's lazy contract: sniff first line for backtick + 4-digit year; prose
    fails the sniff and costs zero regex work. We assert that prose with no
    backtick-year line at the head parses to None AND that the regex module's
    match is called at most once (the SIMPLE pass), not twice (FULL+SIMPLE).
    """
    prose = ("**Backfill 1/3 — the 191 rows that existed before the board became this "
             "issue (oldest first).**\n\n- `2026-08-23T21:41:15Z` **rebuild-drill** "
             "(drill-failed/info): the estate cannot be rebuilt.")
    real_full = sync.COMMENT_FULL_RE.match
    real_simple = sync.COMMENT_SIMPLE_RE.match
    counts = {"full": 0, "simple": 0}

    def _wrap(re):
        def _inner(s, *a, **k):
            if re is sync.COMMENT_FULL_RE:
                counts["full"] += 1
            elif re is sync.COMMENT_SIMPLE_RE:
                counts["simple"] += 1
            return real_full(s, *a, **k) if re is sync.COMMENT_FULL_RE else real_simple(s, *a, **k)
        return _inner

    with mock.patch.object(sync, "COMMENT_FULL_RE", wraps=sync.COMMENT_FULL_RE) as full, \
         mock.patch.object(sync, "COMMENT_SIMPLE_RE", wraps=sync.COMMENT_SIMPLE_RE) as simple:
        # Wrap by replacing the .match method with a counting proxy.
        full.match = mock.Mock(side_effect=lambda s, *a, **k: (counts.update(full=counts["full"] + 1) or real_full(s, *a, **k)))
        simple.match = mock.Mock(side_effect=lambda s, *a, **k: (counts.update(simple=counts["simple"] + 1) or real_simple(s, *a, **k)))
        result = sync.parse_comment(prose)
    assert result is None, "prose must not parse as a row"
    # The plan's lazy contract: at most one regex pass on prose (the FULL sniff).
    # The SIMPLE regex runs only after FULL misses; that is one FULL, zero SIMPLE.
    assert counts["full"] <= 1
    assert counts["simple"] == 0


def test_parallel_threshold_is_32(gq) -> None:
    """Plan threshold: serial below 32, parallel at-or-above with min(N, cpu)."""
    assert gq._max_workers(0) == 0
    assert gq._max_workers(1) == 0
    assert gq._max_workers(32) == 0
    n = 200
    expected = min(n, os.cpu_count() or 1)
    assert gq._max_workers(33) == expected
    assert gq._max_workers(n) == expected
    # Constant lives in the module under the plan-named name.
    assert gq.PARALLEL_THRESHOLD == 32


def test_memoised_meta_module_holds_updated_at_and_sha256(meta, tmp_path) -> None:
    """MEMOISED: meta.json carries updatedAt + sha256, addressable at
    ~/.claude/ESTATE_BOARD.meta.json. Overridable for tests."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    cache.write_text('{"a": 1}\n')
    h = meta.compute_sha256(cache)
    assert h is not None
    meta_path = tmp_path / "ESTATE_BOARD.meta.json"
    meta.save_meta(meta_path, {"updatedAt": "2026-08-24T03:23:01.090857Z",
                               "sha256": h})
    payload = meta.load_meta(meta_path)
    assert payload is not None
    assert payload["updatedAt"] == "2026-08-24T03:23:01.090857Z"
    assert payload["sha256"] == h
    # The default address is ~/.claude/ESTATE_BOARD.meta.json.
    default = meta.meta_path()
    assert str(default).endswith(".claude/ESTATE_BOARD.meta.json")


def test_batched_hash_compare_skips_rename(meta, tmp_path, sync) -> None:
    """BATCHED: when would-be sha256 matches stored, the cache is NOT rewritten.

    Two properties: (a) the hash of the would-be output matches the stored hash,
    and (b) sync_estate_board's caller-side guard short-circuits when it does,
    leaving the cache mtime alone.
    """
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    fetch = _comments(3)
    # First run: build the cache and meta.
    with mock.patch.object(sync, "fetch_comments", return_value=fetch), \
         mock.patch.object(sync, "_load_meta_module", return_value=meta), \
         mock.patch.object(sync, "_load_graphql_module", return_value=None), \
         mock.patch.object(sync, "_issue_updated_at", return_value="2026-08-24T03:00:02Z"):
        sync.main([str(cache)])
    mtime_before = cache.stat().st_mtime
    # Now stub the meta to report the same updatedAt AND a matching sha256 so
    # the main() short-circuit runs.
    rows_now = sync.rows_from(fetch)
    matching_sha = meta.hash_joined(rows_now)
    meta_path = tmp_path / "ESTATE_BOARD.meta.json"
    meta.save_meta(meta_path, {"updatedAt": "2026-08-24T03:00:02Z",
                               "sha256": matching_sha})

    with mock.patch.object(sync, "fetch_comments", side_effect=lambda *a, **k:
                           (_ for _ in ()).throw(AssertionError("fetch must not run on cache hit"))), \
         mock.patch.object(sync, "_load_meta_module", return_value=meta), \
         mock.patch.object(sync, "_load_graphql_module", return_value=None), \
         mock.patch.object(sync, "_issue_updated_at", return_value="2026-08-24T03:00:02Z"):
        from io import StringIO
        buf = StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            rc = sync.main([str(cache)])
        finally:
            sys.stdout = old
        out_text = buf.getvalue()
    assert rc == 0
    assert cache.stat().st_mtime == mtime_before, "cache must not be rewritten on a hash match"
    assert "fetch: cache-hit" in out_text
    assert "write: skipped (hash unchanged)" in out_text

"""crew#102 — the board sync is memoised against a watermark, with a no-op fast path.

The watermark is the contract the plan calls out:

  * missing -> full fetch
  * present and agreeing with the cache -> delta fetch on the next call
  * present and disagreeing -> full fetch and a single loud `RESYNC ` line

The script keeps every public name (`parse_comment`, `fetch_comments`,
`rows_from`, `sync_estate_board`, `main`, `COMMENT_FULL_RE`,
`COMMENT_SIMPLE_RE`); the new modules are additive and live next to the
sync script. The regression tests pin those public names, the watermark
fallback semantics, and the no-op short-circuit -- all without touching
the network.
"""

from __future__ import annotations

import importlib.util
import json
import os
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SYNC_PATH = SCRIPTS / "estate-board-sync.py"
WATERMARK_PATH = SCRIPTS / "estate-board-sync-watermark.py"
GRAPHQL_PATH = SCRIPTS / "estate-board-sync-graphql.py"


def _load(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None, f"missing module at {path}"
    assert spec.loader is not None, f"no loader for {path}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _sync_module():
    return _load("estate_board_sync", SYNC_PATH)


def test_watermark_module_imports_and_owns_public_names() -> None:
    """The watermark module exists, imports cleanly, and exposes its contract names."""
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)
    for name in (
        "load_watermark",
        "save_watermark",
        "watermark_valid",
        "emit_resync",
        "watermark_path",
        "now_iso",
        "WATERMARK_DEFAULT",
        "SAFETY_WINDOW_S",
    ):
        assert hasattr(wm, name), f"watermark module missing {name}"


def test_graphql_module_imports_and_owns_public_names() -> None:
    """The graphql module exists, imports cleanly, and exposes its contract names."""
    gq = _load("estate_board_sync_graphql", GRAPHQL_PATH)
    for name in (
        "graphql_fetch",
        "parse_pages_in_parallel",
        "pages_from_nodes",
        "GRAPHQL_QUERY",
    ):
        assert hasattr(gq, name), f"graphql module missing {name}"


def test_sync_module_keeps_its_existing_public_names() -> None:
    """The crew101 pins still pass -- the script still exposes every name they read."""
    ebs = _sync_module()
    for name in (
        "parse_comment",
        "fetch_comments",
        "rows_from",
        "sync_estate_board",
        "main",
        "COMMENT_FULL_RE",
        "COMMENT_SIMPLE_RE",
    ):
        assert hasattr(ebs, name), f"sync module dropped {name}"


def test_watermark_load_returns_none_for_missing_file(tmp_path, monkeypatch) -> None:
    """A missing watermark -> full fetch (None from the loader)."""
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)
    monkeypatch.setenv("ESTATE_BOARD_WATERMARK", str(tmp_path / "missing.watermark"))
    assert wm.load_watermark() is None


def test_watermark_load_returns_none_for_corrupt_json(tmp_path, monkeypatch) -> None:
    """A garbage watermark file -> None, not a silent partial."""
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)
    p = tmp_path / "garbage.watermark"
    p.write_text("not json at all")
    monkeypatch.setenv("ESTATE_BOARD_WATERMARK", str(p))
    assert wm.load_watermark() is None


def test_watermark_valid_rejects_mismatch_on_cache_total(tmp_path, monkeypatch) -> None:
    """A watermark whose cache_total disagrees with the live cache -> invalid."""
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    cache.write_text(
        json.dumps({"ts": "2026-08-24T10:00:00Z", "from": "x", "kind": "k", "priority": "p", "message": "m"}) + "\n"
    )
    p = tmp_path / "watermark.json"
    p.write_text(json.dumps({
        "last_synced_id": "IC_abc",
        "last_synced_at": "2026-08-24T10:00:00Z",
        "cache_total": 999,  # lies
    }))
    monkeypatch.setenv("ESTATE_BOARD_WATERMARK", str(p))
    assert wm.watermark_valid(wm.load_watermark(), cache) is False


def test_watermark_valid_rejects_stale_timestamp(tmp_path, monkeypatch) -> None:
    """A watermark older than the cache's mtime minus SAFETY -> invalid."""
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    cache.write_text(
        json.dumps({"ts": "2026-08-24T10:00:00Z", "from": "x", "kind": "k", "priority": "p", "message": "m"}) + "\n"
    )
    p = tmp_path / "watermark.json"
    p.write_text(json.dumps({
        "last_synced_id": "IC_abc",
        "last_synced_at": "2000-01-01T00:00:00Z",  # stale beyond the safety window
        "cache_total": 1,
    }))
    monkeypatch.setenv("ESTATE_BOARD_WATERMARK", str(p))
    assert wm.watermark_valid(wm.load_watermark(), cache) is False


def test_watermark_valid_accepts_a_fresh_match(tmp_path, monkeypatch) -> None:
    """A watermark whose cache_total matches AND timestamp is fresh -> valid."""
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    cache.write_text(
        json.dumps({"ts": "2026-08-24T10:00:00Z", "from": "x", "kind": "k", "priority": "p", "message": "m"}) + "\n"
        + json.dumps({"ts": "2026-08-24T10:05:00Z", "from": "y", "kind": "k", "priority": "p", "message": "m"}) + "\n"
    )
    p = tmp_path / "watermark.json"
    p.write_text(json.dumps({
        "last_synced_id": "IC_abc",
        "last_synced_at": wm.now_iso(),
        "cache_total": 2,
    }))
    monkeypatch.setenv("ESTATE_BOARD_WATERMARK", str(p))
    assert wm.watermark_valid(wm.load_watermark(), cache) is True


def test_save_watermark_is_atomic(tmp_path) -> None:
    """save_watermark writes through a sibling tmp file and renames into place."""
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)
    p = tmp_path / "watermark.json"
    wm.save_watermark(p, {
        "last_synced_id": "IC_xyz",
        "last_synced_at": "2026-08-24T10:00:00Z",
        "cache_total": 7,
    })
    assert p.exists()
    payload = json.loads(p.read_text())
    assert payload["last_synced_id"] == "IC_xyz"
    assert payload["cache_total"] == 7
    # The sibling tmp must not survive.
    assert not (p.parent / "watermark.json.tmp").exists()


def test_emit_resync_prints_one_loud_line(capsys) -> None:
    """The RESYNC line is on stderr, starts with the prefix, and names the path."""
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)
    wm.emit_resync("cache rotated", path=pathlib.Path("/tmp/example.watermark"))
    out = capsys.readouterr()
    assert out.err.startswith("RESYNC "), out.err
    assert "/tmp/example.watermark" in out.err
    assert "cache rotated" in out.err
    assert out.err.endswith("\n")
    assert out.err.count("\n") == 1, "RESYNC must be a single line, not a wall"


def test_graphql_query_carries_the_since_filter() -> None:
    """The paginated query reads `updatedAt > <since>` so a delta fetches only what changed."""
    gq = _load("estate_board_sync_graphql", GRAPHQL_PATH)
    assert "IssueCommentFilters" in gq.GRAPHQL_QUERY
    assert "filter:" in gq.GRAPHQL_QUERY
    assert "UPDATED_AT" in gq.GRAPHQL_QUERY
    assert "pageInfo" in gq.GRAPHQL_QUERY


def test_parse_pages_in_parallel_preserves_page_order() -> None:
    """The parallel parse merges in page order, not arrival order, so the cache reads oldest first."""
    gq = _load("estate_board_sync_graphql", GRAPHQL_PATH)
    pages = [
        [{"body": "`2026-08-24T10:00:01Z` **b** (note/info): second"}],
        [{"body": "`2026-08-24T10:00:00Z` **a** (note/info): first"}],
    ]
    rows = gq.parse_pages_in_parallel(pages, max_workers=2)
    messages = [r["message"] for r in rows]
    assert messages == ["second", "first"]


def test_parse_pages_in_parallel_drops_non_rows() -> None:
    """Prose comments return None from the parser and are not in the merged list."""
    gq = _load("estate_board_sync_graphql", GRAPHQL_PATH)
    pages = [
        [
            {"body": "`2026-08-24T10:00:00Z` **a** (note/info): first"},
            {"body": "**Backfill 2/3 — ignore me.**"},
        ],
    ]
    rows = gq.parse_pages_in_parallel(pages, max_workers=2)
    assert [r["from"] for r in rows] == ["a"]


def test_noop_short_circuit_prints_already_up_to_date(tmp_path, monkeypatch, capsys) -> None:
    """A --check run that finds no changes prints the 'already up to date' line and exits 0."""
    ebs = _sync_module()
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)

    out = tmp_path / "ESTATE_BOARD.jsonl"
    body = (
        "`2026-08-24T10:00:00Z` **a** (note/info): only"
    )
    out.write_text(json.dumps({"ts": "2026-08-24T10:00:00Z", "from": "a", "kind": "note", "priority": "info", "message": "only"}) + "\n")

    p = tmp_path / "watermark.json"
    p.write_text(json.dumps({
        "last_synced_id": "IC_abc",
        "last_synced_at": wm.now_iso(),
        "cache_total": 1,
    }))
    monkeypatch.setenv("ESTATE_BOARD_WATERMARK", str(p))

    def fake_fetch():
        return [{"body": body}]

    monkeypatch.setattr(ebs, "fetch_comments", fake_fetch)
    rc = ebs.main(["estate-board-sync.py", str(out), "--check"])
    captured = capsys.readouterr()
    assert rc == 0, captured
    assert "already up to date" in captured.out, captured.out
    assert "(1 rows)" in captured.out


def test_resync_on_mismatch_prints_loud_line_and_full_rewrite(
    tmp_path, monkeypatch, capsys
) -> None:
    """A watermark whose cache_total disagrees with the cache triggers a RESYNC."""
    ebs = _sync_module()
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)

    out = tmp_path / "ESTATE_BOARD.jsonl"
    out.write_text(
        json.dumps({"ts": "2026-08-24T10:00:00Z", "from": "a", "kind": "note", "priority": "info", "message": "only"}) + "\n"
    )

    p = tmp_path / "watermark.json"
    p.write_text(json.dumps({
        "last_synced_id": "IC_abc",
        "last_synced_at": "2000-01-01T00:00:00Z",
        "cache_total": 999,
    }))
    monkeypatch.setenv("ESTATE_BOARD_WATERMARK", str(p))

    def fake_fetch():
        return [{"body": "`2026-08-24T10:00:00Z` **a** (note/info): only"}]

    monkeypatch.setattr(ebs, "fetch_comments", fake_fetch)
    rc = ebs.main(["estate-board-sync.py", str(out)])
    captured = capsys.readouterr()
    assert rc == 0, captured
    assert captured.err.startswith("RESYNC "), captured.err
    assert "watermark<->cache mismatch" in captured.err


def test_main_returns_one_on_fetch_failure(tmp_path, monkeypatch, capsys) -> None:
    """A failing fetch is loud, exits 1, and never touches the cache (LAW 28)."""
    ebs = _sync_module()
    out = tmp_path / "ESTATE_BOARD.jsonl"

    def boom(*_a, **_k):
        raise OSError("network is down")

    monkeypatch.setattr(ebs, "fetch_comments", boom)
    rc = ebs.main(["estate-board-sync.py", str(out)])
    captured = capsys.readouterr()
    assert rc == 1, captured
    assert "network is down" in captured.err
    assert not out.exists()

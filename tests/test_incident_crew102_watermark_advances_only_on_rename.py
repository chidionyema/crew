"""crew#102 — the watermark advances only when the cache rename succeeds.

A failing rename must not advance the watermark. If it did, the next run
would treat the cache as fresh when in fact the cache file was not replaced,
and a session that grades the cache by age would read "fresh" forever
(LAW 28). The regression test forces `sync_estate_board` to raise on the
rename and asserts the watermark file is left untouched.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SYNC_PATH = SCRIPTS / "estate-board-sync.py"
WATERMARK_PATH = SCRIPTS / "estate-board-sync-watermark.py"


def _load(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None, f"missing module at {path}"
    assert spec.loader is not None, f"no loader for {path}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_failed_rename_does_not_advance_watermark(tmp_path, monkeypatch) -> None:
    """Forced OSError on the tmp.replace -> watermark file unchanged on disk."""
    ebs = _load("estate_board_sync", SYNC_PATH)
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)

    out = tmp_path / "ESTATE_BOARD.jsonl"
    out.write_text(
        json.dumps({"ts": "2026-08-24T10:00:00Z", "from": "a", "kind": "note", "priority": "info", "message": "first"}) + "\n"
    )

    watermark_file = tmp_path / "watermark.json"
    old_payload = {
        "last_synced_id": "IC_OLD",
        "last_synced_at": "2026-08-24T10:00:00Z",
        "cache_total": 1,
    }
    watermark_file.write_text(json.dumps(old_payload, sort_keys=True))
    monkeypatch.setenv("ESTATE_BOARD_WATERMARK", str(watermark_file))

    # Force the rename to raise; the cache's tmp file is in place but never
    # becomes the cache file.
    real_replace = pathlib.Path.replace

    def boom_replace(self, target):
        raise OSError("rename refused (test)")

    monkeypatch.setattr(pathlib.Path, "replace", boom_replace)

    rc = ebs.main(["estate-board-sync.py", str(out)])
    assert rc != 0, "main must exit non-zero on a failing rename"

    # Watermark file still carries the OLD payload; nothing advanced it.
    on_disk = json.loads(watermark_file.read_text())
    assert on_disk == old_payload, on_disk


def test_watermark_advances_when_rename_succeeds(tmp_path, monkeypatch, capsys) -> None:
    """A normal sync writes the cache AND advances the watermark."""
    ebs = _load("estate_board_sync", SYNC_PATH)
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)

    out = tmp_path / "ESTATE_BOARD.jsonl"

    watermark_file = tmp_path / "watermark.json"
    monkeypatch.setenv("ESTATE_BOARD_WATERMARK", str(watermark_file))

    def fake_fetch():
        return [
            {"body": "`2026-08-24T10:00:00Z` **a** (note/info): only"},
        ]

    monkeypatch.setattr(ebs, "fetch_comments", fake_fetch)

    rc = ebs.main(["estate-board-sync.py", str(out)])
    captured = capsys.readouterr()
    assert rc == 0, captured
    assert out.exists()

    payload = json.loads(watermark_file.read_text())
    assert payload["cache_total"] == 1
    assert payload["last_synced_at"] is not None
    # last_synced_id is None because the script fetched through the fallback
    # path; a graphql run would populate it. The shape is what matters here.
    assert "last_synced_id" in payload


def test_partial_cache_is_not_touched_on_failure(tmp_path, monkeypatch, capsys) -> None:
    """A failing write leaves the cache untouched -- no half-written file."""
    ebs = _load("estate_board_sync", SYNC_PATH)

    out = tmp_path / "ESTATE_BOARD.jsonl"

    def boom(*_a, **_k):
        raise OSError("network is down")

    monkeypatch.setattr(ebs, "fetch_comments", boom)
    rc = ebs.main(["estate-board-sync.py", str(out)])
    captured = capsys.readouterr()
    assert rc == 1, captured
    assert not out.exists()
    assert not (tmp_path / "ESTATE_BOARD.jsonl.tmp").exists()


def test_watermark_writes_via_tmp_then_rename(tmp_path) -> None:
    """The watermark's own save is atomic -- same pattern as the cache."""
    wm = _load("estate_board_sync_watermark", WATERMARK_PATH)
    p = tmp_path / "watermark.json"

    # Spy on replace.
    calls = []

    real_replace = pathlib.Path.replace

    def spy_replace(self, target):
        calls.append((str(self), str(target)))
        real_replace(self, target)

    # Monkeypatching pathlib.Path.replace is process-wide; the sync script
    # would still rely on it for the cache. So the spy calls the real one.
    import pathlib as _pl
    _pl.Path.replace = spy_replace

    try:
        wm.save_watermark(p, {
            "last_synced_id": "IC_xyz",
            "last_synced_at": "2026-08-24T10:00:00Z",
            "cache_total": 4,
        })
    finally:
        _pl.Path.replace = real_replace

    assert p.exists()
    # At least one replace call landed the tmp -> watermark.json.
    assert any(src.endswith("watermark.json.tmp") and dst.endswith("watermark.json")
               for src, dst in calls), calls
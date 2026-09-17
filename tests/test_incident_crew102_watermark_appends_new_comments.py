"""crew#102: incremental K-new-rows + atomic watermark contract.

When K new comments have landed on the board, exactly K new rows are appended to the
cache, the watermark sidecar is rewritten atomically (via Path.replace on a .tmp
sibling -- never by overwriting in place), and the snapshot row reports K. The first run
after a fresh watermark must also create the cache file with exactly K rows even when
no cache file existed to seed.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "estate_board_sync", ROOT / "scripts" / "estate-board-sync.py"
)
assert _spec is not None
assert _spec.loader is not None
ebs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ebs)


def _three_new_comments() -> list[dict]:
    return [
        {
            "id": "C_3",
            "createdAt": "2026-08-24T11:00:00Z",
            "body": "`2026-08-24T11:00:00Z` **three** (note/info): third",
        },
        {
            "id": "C_1",
            "createdAt": "2026-08-24T10:30:00Z",
            "body": "`2026-08-24T10:30:00Z` **one** (note/info): first",
        },
        {
            "id": "C_2",
            "createdAt": "2026-08-24T10:45:00Z",
            "body": "`2026-08-24T10:45:00Z` **two** (note/info): second",
        },
    ]


def test_incremental_run_with_k_new_comments_appends_exactly_k_rows(
    tmp_path, monkeypatch, capsys
) -> None:
    """K=3: cache grows by exactly 3 lines, watermark reflects the newest of the 3."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    seed_row = {
        "ts": "2026-08-24T09:00:00Z",
        "from": "seed",
        "kind": "note",
        "priority": "info",
        "message": "seed",
    }
    cache.write_text(json.dumps(seed_row) + "\n")

    sidecar = tmp_path / "ESTATE_BOARD.watermark"
    sidecar.write_text(json.dumps({"last_id": "oldid", "last_ts": "2026-08-24T10:00:00Z"}))

    # Disable the .last_sync cheap path so this test exercises the watermark /
    # graphql branch only. The plan's MEMOISED contract is exercised in
    # test_incident_crew102_sync_is_memoised_on_updated_at.py.
    monkeypatch.setattr(ebs, "LAST_SYNC_SUFFIX", ".DISABLED.last_sync")

    monkeypatch.setattr(ebs, "WATERMARK_DEFAULT", sidecar)
    monkeypatch.setattr(ebs, "_load_meta_module", lambda: None)
    monkeypatch.setattr(ebs, "_load_graphql_module", lambda: None)
    monkeypatch.setattr(ebs, "fetch_new_comments", lambda *a, **k: _three_new_comments())

    rc = ebs.main(["estate-board-sync.py", str(cache)])
    out = capsys.readouterr().out

    assert rc == 0
    lines = cache.read_text().splitlines()
    assert len(lines) == 1 + 3, lines
    parsed = [json.loads(ln) for ln in lines]
    assert parsed[0] == seed_row

    tmp_sidecar = sidecar.with_suffix(sidecar.suffix + ".tmp")
    assert not tmp_sidecar.exists(), (
        f"watermark was not replaced atomically: {tmp_sidecar} still exists"
    )

    wm = json.loads(sidecar.read_text())
    assert wm["last_id"] == "C_3", wm
    assert wm["last_ts"] == "2026-08-24T11:00:00Z", wm

    # The plan's proof substrings AND the legacy pin both appear on the same line.
    assert "3 new row(s)" in out
    assert "(added 3 row(s))" in out
    assert "(incremental)" in out


def test_incremental_run_creates_the_cache_when_only_the_watermark_exists(
    tmp_path, monkeypatch, capsys
) -> None:
    """A fresh sidecar with no cache file must still produce exactly K rows."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    assert not cache.exists()

    sidecar = tmp_path / "ESTATE_BOARD.watermark"
    sidecar.write_text(json.dumps({"last_id": "oldid", "last_ts": "2026-08-24T10:00:00Z"}))

    monkeypatch.setattr(ebs, "LAST_SYNC_SUFFIX", ".DISABLED.last_sync")
    monkeypatch.setattr(ebs, "WATERMARK_DEFAULT", sidecar)
    monkeypatch.setattr(ebs, "_load_meta_module", lambda: None)
    monkeypatch.setattr(ebs, "_load_graphql_module", lambda: None)
    monkeypatch.setattr(ebs, "fetch_new_comments", lambda *a, **k: _three_new_comments())

    rc = ebs.main(["estate-board-sync.py", str(cache)])
    out = capsys.readouterr().out

    assert rc == 0
    lines = cache.read_text().splitlines()
    assert len(lines) == 3, lines
    assert "3 new row(s)" in out
    assert "(added 3 row(s))" in out
    assert "(incremental)" in out

"""crew#102: incremental no-new-rows contract.

When nothing has landed on the board since the last sync, a second run must be a true
no-op: the cache file is byte-identical and the watermark sidecar is untouched. This is
the steady-state behaviour the hourly snapshot is sized for (K=0 most of the time), and
the property the optimistic append path exists to preserve -- rewriting the JSONL would
do O(N) disk I/O every hour for no reason.
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


def test_incremental_run_with_no_new_comments_is_a_byte_identical_noop(
    tmp_path, monkeypatch, capsys
) -> None:
    """K=0: cache bytes are unchanged, watermark bytes are unchanged, exit 0."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    seed_row = {"ts": "2026-08-24T09:00:00Z", "from": "seed", "kind": "note", "priority": "info", "message": "seed"}
    cache.write_text(json.dumps(seed_row) + "\n")
    before = cache.read_bytes()

    sidecar = tmp_path / "ESTATE_BOARD.watermark"
    wm_before = {"last_id": "X", "last_ts": "2026-08-24T10:00:00Z"}
    sidecar.write_text(json.dumps(wm_before))
    wm_bytes_before = sidecar.read_bytes()

    # Point the script at the tmp sidecar instead of ~/.claude/ESTATE_BOARD.watermark.
    monkeypatch.setattr(ebs, "WATERMARK_DEFAULT", sidecar)
    monkeypatch.setattr(
        ebs,
        "fetch_new_comments",
        lambda *a, **k: [],
    )

    rc = ebs.main(["estate-board-sync.py", str(cache)])
    out = capsys.readouterr().out

    assert rc == 0
    assert "0 new row(s)" in out
    assert "(incremental)" in out
    # The cache must be byte-identical -- nothing was appended, nothing was rewritten.
    assert cache.read_bytes() == before
    # The watermark sidecar must also be unchanged (or at most a byte-identical rewrite;
    # the contract is "byte-identical", which is stricter).
    assert sidecar.read_bytes() == wm_bytes_before
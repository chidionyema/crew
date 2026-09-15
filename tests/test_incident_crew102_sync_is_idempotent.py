"""crew#102 — the steady-state sync is a no-op.

The board's snapshot script (`scripts/estate-board-sync.py`) runs hourly from
`scripts/estate-snapshot`. When the board has not moved, that hourly run must
not rewrite the cache, must not re-parse every comment, and must not re-sort.
It must return 0, print "unchanged", and leave the cache's mtime alone.

This test pins that contract by driving `sync_estate_board` (the same function
the snapshot calls, with `fetch_comments` monkeypatched) twice with the same
list of comments and asserting the second call short-circuited.

Why this test, not `fetch_comments` against the live issue: this is an
incident-grade test on the read path's *behaviour* — the cached resource is
the issue, not the laptop file, and a missed resync shows up as a board that
drifts. The live-API test is `test_incident_crew102_estate_board_is_issue_102.py`
and `test_incident_crew102_github_board_read.py`; they pin the contract that
this test exercises through a seam.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "estate_board_sync_idempotent", ROOT / "scripts" / "estate-board-sync.py"
)
assert _spec is not None, "scripts/estate-board-sync.py is not where this test expects it"
assert _spec.loader is not None, "no loader for scripts/estate-board-sync.py"
ebs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ebs)


COMMENTS = [
    {"id": "C1", "body": "`2026-08-23T10:00:00Z` **a** (note/info): first"},
    {"id": "C2", "body": "**Backfill 2/3 — ignore me.**"},
    {"id": "C3", "body": "`2026-08-24T10:00:00Z` **b** (fire/p1): second"},
]


def test_second_run_with_no_new_comments_is_a_no_op(tmp_path, monkeypatch, capsys) -> None:
    """The second sync against an unchanged board must not rewrite the cache."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"

    monkeypatch.setattr(ebs, "fetch_comments", lambda: list(COMMENTS))
    rc1 = ebs.main(["estate-board-sync.py", str(cache)])
    assert rc1 == 0, capsys.readouterr().err
    first_lines = cache.read_text().splitlines()
    assert len(first_lines) == 2
    first_mtime = cache.stat().st_mtime

    # Second run against the same comments — the board did not move.
    monkeypatch.setattr(ebs, "fetch_comments", lambda: list(COMMENTS))
    rc2 = ebs.main(["estate-board-sync.py", str(cache)])
    assert rc2 == 0, capsys.readouterr().err

    out = capsys.readouterr().out
    assert "unchanged" in out, f"expected the warm-path line, got: {out!r}"
    assert cache.read_text().splitlines() == first_lines
    assert cache.stat().st_mtime == first_mtime, "cache was rewritten on a no-op run"


def test_warm_path_is_cold_when_the_board_moves(tmp_path, monkeypatch, capsys) -> None:
    """When a new comment lands, the next sync must rebuild and rewrite."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"

    monkeypatch.setattr(ebs, "fetch_comments", lambda: list(COMMENTS))
    assert ebs.main(["estate-board-sync.py", str(cache)]) == 0
    capsys.readouterr()

    new_comments = list(COMMENTS) + [
        {"id": "C4", "body": "`2026-08-25T10:00:00Z` **c** (note/info): third"},
    ]
    monkeypatch.setattr(ebs, "fetch_comments", lambda: list(new_comments))
    assert ebs.main(["estate-board-sync.py", str(cache)]) == 0
    out = capsys.readouterr().out
    assert "unchanged" not in out, f"warm path fired after the board moved: {out!r}"
    lines = cache.read_text().splitlines()
    assert len(lines) == 3
    assert json.loads(lines[-1])["message"] == "third"


def test_cold_start_with_no_watermark_rebuilds(tmp_path, monkeypatch, capsys) -> None:
    """First run on a fresh cache (no .lastid) goes through the full rebuild."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"

    monkeypatch.setattr(ebs, "fetch_comments", lambda: list(COMMENTS))
    assert ebs.main(["estate-board-sync.py", str(cache)]) == 0
    out = capsys.readouterr().out
    assert "unchanged" not in out, f"cold start hit the warm path: {out!r}"
    assert len(cache.read_text().splitlines()) == 2

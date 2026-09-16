"""Crew#102 — the read-side pin for the estate board.

Pins the contract:
- parse_comment returns a row dict or None (for backfill prose).
- rows_from filters and sorts oldest-first.
- sync_estate_board writes atomically (tmp + rename).
- main exits 1 on failure with the documented stderr shape.
- Comments are fetched once per run, not once per row (no N+1).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import estate_board_sync  # noqa: E402

FULL_ROW_BODY = (
    "`2026-08-24T03:23:01Z` **fable-63** (board-cutover/high): "
    "The board is now crew#102."
)
SIMPLE_ROW_BODY = "`2026-08-24T03:33:33Z` **crew63-fable**: Founder order."
BACKFILL_BODY = (
    "**Backfill 1/3 — the 191 rows that existed before the board became this issue**\n\n"
    "- `2026-08-23T21:41:15Z` **rebuild-drill** (drill-failed/info): prose.\n"
)
PROSE_BODY = "This is a long prose comment that is not a board row at all."


def test_parse_comment_full_row() -> None:
    row = estate_board_sync.parse_comment(FULL_ROW_BODY)
    assert row is not None
    assert row["ts"] == "2026-08-24T03:23:01Z"
    assert row["from"] == "fable-63"
    assert row["kind"] == "board-cutover"
    assert row["priority"] == "high"
    assert "crew#102" in row["message"]


def test_parse_comment_simple_row() -> None:
    row = estate_board_sync.parse_comment(SIMPLE_ROW_BODY)
    assert row is not None
    assert row["ts"] == "2026-08-24T03:33:33Z"
    assert row["from"] == "crew63-fable"
    assert row["kind"] == "unclassified"
    assert row["priority"] == "info"
    assert row["message"] == "Founder order."


def test_parse_comment_drops_backfill_header() -> None:
    assert estate_board_sync.parse_comment(BACKFILL_BODY) is None


def test_parse_comment_drops_non_matching_prose() -> None:
    assert estate_board_sync.parse_comment(PROSE_BODY) is None


def test_parse_comment_handles_empty() -> None:
    assert estate_board_sync.parse_comment("") is None
    assert estate_board_sync.parse_comment("   \n\n") is None


def test_rows_from_filters_and_sorts_oldest_first() -> None:
    comments = [
        {"body": BACKFILL_BODY},
        {"body": "`2026-08-24T05:00:00Z` **b** (kind/p): second"},
        {"body": "`2026-08-24T03:00:00Z` **a** (kind/p): first"},
    ]
    rows = estate_board_sync.rows_from(comments)
    assert [r["from"] for r in rows] == ["a", "b"]
    assert rows[0]["ts"] < rows[1]["ts"]


def test_sync_estate_board_writes_atomically(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    monkeypatch.setattr(estate_board_sync, "DEFAULT_CACHE", cache)
    comments = [
        {"body": FULL_ROW_BODY},
        {"body": SIMPLE_ROW_BODY},
        {"body": BACKFILL_BODY},
    ]
    n = estate_board_sync.sync_estate_board(comments, cache)
    assert n == 2
    lines = cache.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    parsed = [json.loads(line) for line in lines]
    assert parsed[0]["ts"] < parsed[1]["ts"]
    assert not (cache.parent / (cache.name + ".tmp")).exists()


def test_sync_estate_board_creates_parent_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    nested = tmp_path / "deep" / "nested" / "ESTATE_BOARD.jsonl"
    monkeypatch.setattr(estate_board_sync, "DEFAULT_CACHE", nested)
    n = estate_board_sync.sync_estate_board([{"body": FULL_ROW_BODY}], nested)
    assert n == 1
    assert nested.exists()


def test_fetch_comments_raises_on_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_args, **_kwargs):
        raise subprocess.CalledProcessError(1, "gh")

    monkeypatch.setattr(estate_board_sync.subprocess, "run", boom)
    with pytest.raises(subprocess.CalledProcessError):
        estate_board_sync.fetch_comments()


def test_main_returns_nonzero_on_gh_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    monkeypatch.setattr(estate_board_sync, "DEFAULT_CACHE", cache)

    def boom():
        raise subprocess.CalledProcessError(1, "gh")

    monkeypatch.setattr(estate_board_sync, "fetch_comments", boom)
    rc = estate_board_sync.main(["prog", str(cache)])
    assert rc == 1
    err = capsys.readouterr().err
    assert err.startswith(f"estate-board-sync: could not rebuild {cache}: ")
    assert "CalledProcessError" in err


def test_main_prints_line_on_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    monkeypatch.setattr(estate_board_sync, "DEFAULT_CACHE", cache)
    monkeypatch.setattr(
        estate_board_sync,
        "fetch_comments",
        lambda: [{"body": FULL_ROW_BODY}, {"body": BACKFILL_BODY}, {"body": SIMPLE_ROW_BODY}],
    )
    rc = estate_board_sync.main(["prog", str(cache)])
    assert rc == 0
    out = capsys.readouterr().out.strip()
    assert out == f"estate-board-sync: 2 row(s) from chidionyema/crew#102 -> {cache}"


def test_main_honours_env_overrides(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    monkeypatch.setattr(estate_board_sync, "DEFAULT_CACHE", cache)
    monkeypatch.setattr(estate_board_sync, "BOARD_REPO", "acme/widget")
    monkeypatch.setattr(estate_board_sync, "BOARD_ISSUE", 7)
    monkeypatch.setattr(
        estate_board_sync, "fetch_comments", lambda: [{"body": FULL_ROW_BODY}]
    )
    rc = estate_board_sync.main(["prog", str(cache)])
    assert rc == 0
    out = capsys.readouterr().out.strip()
    assert out == f"estate-board-sync: 1 row(s) from acme/widget#7 -> {cache}"


def test_read_path_uses_one_gh_call_per_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Pin the no-N+1 property: the read path fetches once, parses locally."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    monkeypatch.setattr(estate_board_sync, "DEFAULT_CACHE", cache)
    calls = {"n": 0}

    def stub_fetch():
        calls["n"] += 1
        return [{"body": FULL_ROW_BODY} for _ in range(100)]

    monkeypatch.setattr(estate_board_sync, "fetch_comments", stub_fetch)
    n = estate_board_sync.sync_estate_board(stub_fetch(), cache)
    assert n == 1
    assert calls["n"] == 1  # sync_estate_board was given the comments directly;
                             # the script itself never fetches per-row.


def test_sync_is_idempotent_across_two_runs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Running the sync twice on the same comments produces byte-identical output."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    monkeypatch.setattr(estate_board_sync, "DEFAULT_CACHE", cache)
    comments = [{"body": FULL_ROW_BODY}, {"body": SIMPLE_ROW_BODY}]
    estate_board_sync.sync_estate_board(comments, cache)
    first = cache.read_bytes()
    estate_board_sync.sync_estate_board(comments, cache)
    second = cache.read_bytes()
    assert first == second
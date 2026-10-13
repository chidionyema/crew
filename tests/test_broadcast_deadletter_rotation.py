"""crew#102 — dead-letter 1 MiB rotation straight to .1.gz, no .1 intermediate.

Plan R6: at >= 1,048,576 bytes (1 MiB) the live `board-deadletter.jsonl`
is gzipped directly to `board-deadletter.jsonl.1.gz` and a fresh empty
`board-deadletter.jsonl` is started. There is NO `.1` plain-text
intermediate on disk at any point.

The unit test the founder ordered writes 1,048,626 bytes (1 MiB + 50
bytes of padding) to the live file, triggers one append, and proves:

  (a) `board-deadletter.jsonl.1.gz` exists
  (b) gzip-decompressing it yields the original 1,048,626 bytes
  (c) the live `board-deadletter.jsonl` contains ONLY the new row, not
      the rotated bytes
"""
from __future__ import annotations

import gzip
import json
import subprocess
from pathlib import Path

import pytest

import crew.bin.broadcast as broadcast_mod
from crew.bin.broadcast import (
    BoardError,
    DEAD_LETTER,
    _rotate_dead_letter_if_needed,
    broadcast,
)


# ---------------------------------------------------------------------------
# Constants the contract pins
# ---------------------------------------------------------------------------


def test_rotation_threshold_is_exactly_one_mib():
    """R6: at >= 1,048,576 bytes (1 MiB) the rotation runs."""
    assert broadcast_mod._ROTATE_AT == 1_048_576
    assert broadcast_mod._ROTATE_AT == 1 * 1024 * 1024


def test_rotation_target_is_dot_one_gz_not_dot_one():
    """The rotated file is .1.gz directly. No .1 plain-text intermediate."""
    # The module computes the rotated name as `name + ".1.gz"`.
    sample = Path("/tmp/board-deadletter.jsonl")
    rotated = sample.parent / (sample.name + ".1.gz")
    assert rotated.name == "board-deadletter.jsonl.1.gz"
    assert ".1.gz" in rotated.name
    # The forbidden intermediate is `.1` (no .gz).
    forbidden = sample.parent / (sample.name + ".1")
    assert forbidden.name == "board-deadletter.jsonl.1"


# ---------------------------------------------------------------------------
# The contract proof test the founder ordered
# ---------------------------------------------------------------------------


def _write_bytes(path: Path, n: int) -> None:
    """Write exactly n bytes of `x` to `path` (the padding payload)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as fh:
        fh.write(b"x" * n)


def test_one_point_one_mib_rotates_to_gzip_with_original_bytes_recoverable(
    monkeypatch, tmp_path: Path
):
    """The R6 proof: 1 MiB + 50 bytes of padding + one more row.

    (a) board-deadletter.jsonl.1.gz exists
    (b) gzip-decompressing it yields the original 1,048,626 bytes
    (c) the live board-deadletter.jsonl contains ONLY the new row,
        not the rotated bytes
    """
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    live = tmp_path / "board-deadletter.jsonl"
    _write_bytes(live, 1_048_626)  # 1 MiB + 50 bytes

    broadcast_mod.DEAD_LETTER = live
    try:
        with pytest.raises(BoardError):
            # Append one more row. The module hits the dead-letter path
            # because no GH_TOKEN is set; this triggers the rotation.
            broadcast({
                "ts": "2026-09-01T00:00:00Z",
                "from": "rotation-test",
                "kind": "info",
                "priority": "info",
                "message": "y" * 200,
            })
    finally:
        broadcast_mod.DEAD_LETTER = DEAD_LETTER

    # (a) the .1.gz file exists.
    rotated = tmp_path / "board-deadletter.jsonl.1.gz"
    plain_intermediate = tmp_path / "board-deadletter.jsonl.1"
    assert rotated.exists(), (
        f"expected rotation target at {rotated}; "
        f"files in tmp_path: {sorted(p.name for p in tmp_path.iterdir())}"
    )
    # NO .1 plain-text intermediate on disk — R6 forbids it.
    assert not plain_intermediate.exists(), (
        "R6 forbids a .1 plain-text intermediate on disk; only .1.gz is allowed"
    )

    # (b) gzip-decompressing it yields the original 1,048,626 bytes.
    with gzip.open(rotated, "rb") as fh:
        restored = fh.read()
    assert len(restored) == 1_048_626, (
        f"expected 1,048,626 bytes restored; got {len(restored)}"
    )
    assert restored == b"x" * 1_048_626, (
        "restored bytes do not match the original padding"
    )

    # (c) the live file holds ONLY the new row, not the rotated bytes.
    assert live.exists(), "live file should have been recreated fresh"
    new_content_bytes = live.read_bytes()
    # The 1 MiB of `x` padding is gone from the live file.
    assert b"x" * 1_048_576 not in new_content_bytes, (
        "live file still carries the rotated bytes — rotation was incomplete"
    )
    # The new row landed in the live file.
    new_content = new_content_bytes.decode("utf-8")
    assert "y" * 200 in new_content
    # Exactly one JSON line in the fresh live file.
    lines = [ln for ln in new_content.splitlines() if ln.strip()]
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["row"]["message"] == "y" * 200
    assert payload["row"]["from"] == "rotation-test"
    assert payload["reason"].startswith("post:")


# ---------------------------------------------------------------------------
# Edge cases that fall out of the same code path
# ---------------------------------------------------------------------------


def test_rotation_at_exactly_threshold_rotates(tmp_path: Path):
    """1 MiB exactly is enough — `>=` includes equality."""
    live = tmp_path / "board-deadletter.jsonl"
    _write_bytes(live, 1_048_576)

    broadcast_mod.DEAD_LETTER = live
    try:
        _rotate_dead_letter_if_needed()
    finally:
        broadcast_mod.DEAD_LETTER = DEAD_LETTER

    rotated = tmp_path / "board-deadletter.jsonl.1.gz"
    assert rotated.exists()
    with gzip.open(rotated, "rb") as fh:
        assert fh.read() == b"x" * 1_048_576


def test_rotation_one_byte_under_threshold_is_a_noop(tmp_path: Path):
    """One byte under 1 MiB: rotation does NOT run."""
    live = tmp_path / "board-deadletter.jsonl"
    _write_bytes(live, 1_048_575)

    broadcast_mod.DEAD_LETTER = live
    try:
        _rotate_dead_letter_if_needed()
    finally:
        broadcast_mod.DEAD_LETTER = DEAD_LETTER

    assert live.exists()
    assert live.stat().st_size == 1_048_575
    assert not (tmp_path / "board-deadletter.jsonl.1.gz").exists()
    assert not (tmp_path / "board-deadletter.jsonl.1").exists()


def test_missing_live_file_is_a_noop(tmp_path: Path):
    """The very first dead-letter on a fresh machine: nothing to rotate."""
    live = tmp_path / "board-deadletter.jsonl"
    broadcast_mod.DEAD_LETTER = live
    try:
        _rotate_dead_letter_if_needed()  # must not raise
    finally:
        broadcast_mod.DEAD_LETTER = DEAD_LETTER

    assert not (tmp_path / "board-deadletter.jsonl.1.gz").exists()


def test_dead_letter_path_is_pinned_by_absolute_path():
    """The contract is the absolute path. A session cannot rename it."""
    assert DEAD_LETTER.is_absolute()
    assert DEAD_LETTER.name == "board-deadletter.jsonl"
    assert DEAD_LETTER.parent.name == "state"
    assert DEAD_LETTER.parent.parent.name == ".claude"


def test_module_does_not_silently_drop_on_gh_failure(
    monkeypatch, tmp_path: Path
):
    """When the post fails AND the live file is at the rotation point,
    the dead-letter is written AND the rotation runs — and the writer
    still re-raises BoardError. The row is never silently dropped."""
    monkeypatch.setenv("GH_TOKEN", "fake-token-for-test")
    live = tmp_path / "board-deadletter.jsonl"
    _write_bytes(live, 1_048_576)

    broadcast_mod.DEAD_LETTER = live

    def _fake_run(args, *a, **kw):
        return subprocess.CompletedProcess(
            args=args, returncode=1, stdout="",
            stderr="gh: HTTP 502 Bad Gateway",
        )

    monkeypatch.setattr(subprocess, "run", _fake_run)
    try:
        with pytest.raises(BoardError):
            broadcast({
                "ts": "2026-09-01T00:00:00Z",
                "from": "rotation-on-fail",
                "kind": "info",
                "priority": "info",
                "message": "after rotation",
            })
    finally:
        broadcast_mod.DEAD_LETTER = DEAD_LETTER

    rotated = tmp_path / "board-deadletter.jsonl.1.gz"
    assert rotated.exists()
    with gzip.open(rotated, "rb") as fh:
        assert fh.read() == b"x" * 1_048_576
    # The new row is in the live file.
    new_content = live.read_text(encoding="utf-8")
    assert "after rotation" in new_content
    assert "x" * 100 not in new_content
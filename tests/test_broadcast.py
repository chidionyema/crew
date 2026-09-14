from __future__ import annotations

import gzip
import json
from pathlib import Path

import pytest

from crew.bin.broadcast import BoardError, _shape, broadcast


def _row(**over):
    base = {
        "ts": "2026-09-01T00:00:00Z",
        "from": "test",
        "kind": "info",
        "priority": "info",
        "message": "one row",
    }
    base.update(over)
    return base


def test_shape_uses_template():
    out = _shape(_row())
    assert out == "2026-09-01T00:00:00Z **test** (info/info): one row"


def test_shape_rejects_newlines():
    with pytest.raises(BoardError):
        _shape(_row(message="line1\nline2"))


def test_shape_redacts_secrets():
    out = _shape(_row(message="token sk-live-abc123 seen"))
    assert "sk-live-abc123" not in out
    assert "sk-live-***" in out


def test_shape_truncates_oversize():
    big = "x" * (8 * 1024 + 100)
    out = _shape(_row(message=big))
    assert len(out.split(": ", 1)[1]) <= 8 * 1024


def test_broadcast_dead_letters_when_no_token(monkeypatch, tmp_path: Path):
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    target = tmp_path / "deadletter.jsonl"
    monkeypatch.setattr("crew.bin.broadcast._DEAD_LETTER", target)
    with pytest.raises(BoardError) as exc:
        broadcast(_row())
    text = str(exc.value)
    assert "dead-lettered at" in text
    assert target.exists()
    payload = json.loads(target.read_text().splitlines()[0])
    assert payload["row"]["message"] == "one row"


def test_dead_letter_rotates_at_one_mib(monkeypatch, tmp_path: Path):
    target = tmp_path / "deadletter.jsonl"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("x" * (1 * 1024 * 1024 - 50))
    monkeypatch.setattr("crew.bin.broadcast._DEAD_LETTER", target)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    with pytest.raises(BoardError):
        broadcast(_row(message="y" * 200))
    rotated = tmp_path / "deadletter.jsonl.1.gz"
    assert rotated.exists()
    with gzip.open(rotated, "rb") as fh:
        assert fh.read(1) == b"x"
    assert target.exists()
    assert target.stat().st_size < 200
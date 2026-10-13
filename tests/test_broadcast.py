"""crew.bin.broadcast — writer for the estate board (issue #102).

The writer posts one row per call as a GitHub comment on
chidionyema/crew#102 via `gh issue comment`, dead-letters on failure
(unset token, gh non-zero, multi-line message), redacts the three
token-shaped secrets before the body leaves the process, and rotates
the dead-letter file at 1 MiB straight to a gzipped `.1.gz` with no
plain-text intermediate on disk.
"""
from __future__ import annotations

import gzip
import json
import subprocess
import sys
from pathlib import Path

import pytest

from crew.bin.broadcast import (
    COMMENT_TEMPLATE,
    DEAD_LETTER,
    ISSUE_NUMBER,
    REPO,
    BoardError,
    _rotate_dead_letter_if_needed,
    _shape,
    broadcast,
)


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


# ---------------------------------------------------------------------------
# R1 + R5 — importability and shape
# ---------------------------------------------------------------------------


def test_broadcast_module_is_importable():
    """R1: crew.bin.broadcast is importable from any process."""
    assert callable(broadcast)
    assert COMMENT_TEMPLATE.startswith("`{ts}`")
    assert COMMENT_TEMPLATE.endswith("{message}")


def test_shape_uses_canonical_format():
    """The canonical format is `ts` **from** (kind/priority): message."""
    out = _shape(_row())
    assert out == "`2026-09-01T00:00:00Z` **test** (info/info): one row"


def test_shape_refuses_newline_in_message():
    """R5: a \\n in message is rejected by the writer."""
    with pytest.raises(BoardError) as exc:
        _shape(_row(message="line1\nline2"))
    assert "newline" in str(exc.value).lower()


def test_shape_refuses_carriage_return_in_message():
    """R5: a \\r in message is also refused — a CR can break a reader too."""
    with pytest.raises(BoardError):
        _shape(_row(message="line1\rline2"))


def test_shape_missing_required_field_raises():
    """A row without `from` cannot be shaped."""
    row = _row()
    del row["from"]
    with pytest.raises(BoardError):
        _shape(row)


# ---------------------------------------------------------------------------
# R10 — redaction
# ---------------------------------------------------------------------------


def test_shape_redacts_sk_live():
    """R10: sk-live-... becomes sk-live-*** before leaving the process."""
    out = _shape(_row(message="token sk-live-abc123 seen"))
    assert "sk-live-abc123" not in out
    assert "sk-live-***" in out


def test_shape_redacts_gh_token():
    """R10: gh[pousr]_... becomes gh*** before leaving the process."""
    for prefix in ("ghp_", "gho_", "ghu_", "ghs_", "ghr_"):
        out = _shape(_row(message=f"creds {prefix}TOKEN_VALUE"))
        assert f"{prefix}TOKEN_VALUE" not in out
        assert "***" in out


def test_shape_redacts_slack_token():
    """R10: xox[bp]-... becomes xox*-*** before leaving the process."""
    for prefix in ("xoxb-", "xoxp-"):
        out = _shape(_row(message=f"slack {prefix}SECRET_VALUE"))
        assert f"{prefix}SECRET_VALUE" not in out
        assert "***" in out


def test_shape_redacts_multiple_patterns_in_one_message():
    """All three patterns are redacted in one pass."""
    out = _shape(
        _row(
            message="leak sk-live-AAA and ghp_BBB and xoxb-CCC in one message",
        )
    )
    assert "sk-live-AAA" not in out
    assert "ghp_BBB" not in out
    assert "xoxb-CCC" not in out
    assert out.count("***") == 3


# ---------------------------------------------------------------------------
# R3 — dead-letter path
# ---------------------------------------------------------------------------


def test_broadcast_dead_letters_when_no_token(
    monkeypatch, tmp_path: Path, capsys
):
    """R3: no GH_TOKEN / GITHUB_TOKEN -> row lands in dead-letter, WARN on stderr."""
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    target = tmp_path / "board-deadletter.jsonl"
    target.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("crew.bin.broadcast.DEAD_LETTER", target)

    with pytest.raises(BoardError) as exc:
        broadcast(_row())

    captured = capsys.readouterr()
    assert "WARN: dead-lettered at" in captured.err
    assert str(target) in captured.err
    assert "dead-lettered at" in str(exc.value)
    assert target.exists()
    payload = json.loads(target.read_text(encoding="utf-8").splitlines()[0])
    # ORIGINAL row is preserved verbatim, plus reason and dead_lettered_at for the auditor.
    assert payload["row"]["message"] == "one row"
    assert payload["row"]["from"] == "test"
    assert "unset" in payload["reason"].lower() or "GH_TOKEN" in payload["reason"]


def test_broadcast_dead_letters_when_gh_fails(
    monkeypatch, tmp_path: Path, capsys
):
    """R3: gh exits non-zero -> row lands in dead-letter, WARN on stderr."""
    monkeypatch.setenv("GH_TOKEN", "fake-token-for-test")

    def _boom(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args,
            returncode=1,
            stdout="",
            stderr="gh: HTTP 502 Bad Gateway (write failed)",
        )

    monkeypatch.setattr(subprocess, "run", _boom)
    target = tmp_path / "board-deadletter.jsonl"
    monkeypatch.setattr("crew.bin.broadcast.DEAD_LETTER", target)

    with pytest.raises(BoardError) as exc:
        broadcast(_row())

    captured = capsys.readouterr()
    assert "WARN: dead-lettered at" in captured.err
    assert "dead-lettered at" in str(exc.value)
    assert target.exists()
    payload = json.loads(target.read_text(encoding="utf-8").splitlines()[0])
    assert payload["row"]["message"] == "one row"
    assert payload["reason"].startswith("post:")


def test_broadcast_uses_gh_issue_comment_when_posting(
    monkeypatch, tmp_path: Path
):
    """The writer posts via `gh issue comment 102 --repo ... -b ...`.

    Captures the call args to prove the contract shape. The dead-letter
    file is set to a tmp path so the real ~/.claude/state path is never
    touched in CI.
    """
    monkeypatch.setenv("GH_TOKEN", "fake-token-for-test")

    seen: dict = {}

    def _fake_run(args, *a, **kw):
        seen["args"] = list(args)
        return subprocess.CompletedProcess(
            args=args, returncode=0,
            stdout="https://github.com/chidionyema/crew/issues/102#issuecomment-1\n",
            stderr="",
        )

    monkeypatch.setattr(subprocess, "run", _fake_run)
    target = tmp_path / "board-deadletter.jsonl"
    monkeypatch.setattr("crew.bin.broadcast.DEAD_LETTER", target)

    url = broadcast(_row(message="happy path"))
    assert url == "https://github.com/chidionyema/crew/issues/102#issuecomment-1"
    args = seen["args"]
    assert args[:3] == ["gh", "issue", "comment"]
    assert str(ISSUE_NUMBER) in args
    assert REPO in args
    body_idx = args.index("-b")
    body = args[body_idx + 1]
    assert body.startswith("`2026-09-01T00:00:00Z`")
    assert body.endswith("happy path")


def test_broadcast_redacts_before_subprocess(monkeypatch, tmp_path: Path):
    """R10: the body that reaches `gh` carries ***, not the secret."""
    monkeypatch.setenv("GH_TOKEN", "fake-token-for-test")

    seen: dict = {}

    def _fake_run(args, *a, **kw):
        seen["args"] = list(args)
        return subprocess.CompletedProcess(
            args=args, returncode=0,
            stdout="https://github.com/chidionyema/crew/issues/102#issuecomment-2\n",
            stderr="",
        )

    monkeypatch.setattr(subprocess, "run", _fake_run)
    target = tmp_path / "board-deadletter.jsonl"
    monkeypatch.setattr("crew.bin.broadcast.DEAD_LETTER", target)

    broadcast(_row(message="leak sk-live-AAAAA here"))
    body = seen["args"][seen["args"].index("-b") + 1]
    assert "sk-live-AAAAA" not in body
    assert "sk-live-***" in body


# ---------------------------------------------------------------------------
# R6 — 1 MiB rotation, straight to .1.gz, no .1 plain-text intermediate
# ---------------------------------------------------------------------------


def _write_bytes(path: Path, n: int) -> None:
    """Write exactly n bytes of `x` to `path`."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as fh:
        fh.write(b"x" * n)


def test_rotation_keeps_size_just_above_one_mib_intact(tmp_path: Path):
    """Padding case: write exactly 1 MiB + 50 bytes of `x` to the live file,
    trigger one rotation, and prove the original bytes are recoverable."""
    live = tmp_path / "board-deadletter.jsonl"
    _write_bytes(live, 1_048_626)  # 1 MiB + 50 bytes

    monkeypatch_target = tmp_path / "board-deadletter.jsonl"
    monkeypatch_target.write_bytes(b"x" * 1_048_626)

    # R6 rotation target.
    import crew.bin.broadcast as _mod
    monkeypatch_target_real = tmp_path / "board-deadletter.jsonl"
    saved = _mod.DEAD_LETTER
    _mod.DEAD_LETTER = monkeypatch_target_real
    try:
        _rotate_dead_letter_if_needed()
    finally:
        _mod.DEAD_LETTER = saved

    rotated = tmp_path / "board-deadletter.jsonl.1.gz"
    plain_intermediate = tmp_path / "board-deadletter.jsonl.1"

    # (a) the .1.gz exists
    assert rotated.exists(), (
        f"expected rotation target at {rotated}; got {list(tmp_path.iterdir())}"
    )
    # (b) gzip-decompressing it yields the original 1,048,626 bytes
    with gzip.open(rotated, "rb") as fh:
        restored = fh.read()
    assert restored == b"x" * 1_048_626, (
        f"restored bytes mismatch: {len(restored)} vs expected 1,048,626"
    )
    # The .1 plain-text intermediate is NEVER written.
    assert not plain_intermediate.exists(), (
        "R6 forbids a .1 plain-text intermediate on disk"
    )
    # The live file was removed by the rotation.
    assert not monkeypatch_target_real.exists()


def test_rotation_after_dead_letter_leaves_only_new_row(
    monkeypatch, tmp_path: Path
):
    """End-to-end: write 1 MiB + 50 bytes to the live file, append one
    more row via `broadcast`, and the live file carries ONLY the new row,
    the rotated bytes live in `.1.gz`."""
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    live = tmp_path / "board-deadletter.jsonl"
    _write_bytes(live, 1_048_626)

    import crew.bin.broadcast as _mod
    _mod.DEAD_LETTER = live
    try:
        with pytest.raises(BoardError):
            broadcast(_row(message="y" * 200))
    finally:
        # Restore for any subsequent tests in the session.
        _mod.DEAD_LETTER = DEAD_LETTER

    rotated = tmp_path / "board-deadletter.jsonl.1.gz"
    assert rotated.exists()
    with gzip.open(rotated, "rb") as fh:
        restored = fh.read()
    # (c) the live file holds ONLY the new row, not the rotated bytes.
    assert restored == b"x" * 1_048_626
    assert live.exists()
    new_content = live.read_text(encoding="utf-8")
    assert "x" * 1_048_626 not in new_content.encode("utf-8")
    assert "y" * 200 in new_content
    # One JSON line, parseable.
    payload = json.loads(new_content.splitlines()[0])
    assert payload["row"]["message"] == "y" * 200


def test_rotation_below_threshold_does_nothing(monkeypatch, tmp_path: Path):
    """Below 1 MiB the live file is left untouched — no rotation runs."""
    live = tmp_path / "board-deadletter.jsonl"
    _write_bytes(live, 1_048_575)  # one byte under the threshold

    import crew.bin.broadcast as _mod
    _mod.DEAD_LETTER = live
    try:
        _rotate_dead_letter_if_needed()
    finally:
        _mod.DEAD_LETTER = DEAD_LETTER

    assert live.exists()
    assert live.stat().st_size == 1_048_575
    assert not (tmp_path / "board-deadletter.jsonl.1.gz").exists()


def test_rotation_uses_module_level_threshold():
    """The module exports the 1 MiB threshold so a session cannot
    silently change it without a code review."""
    from crew.bin import broadcast as _mod
    assert _mod._ROTATE_AT == 1_048_576
    assert _mod._ROTATE_AT == 1 * 1024 * 1024


# ---------------------------------------------------------------------------
# bin/board-test import path
# ---------------------------------------------------------------------------


def test_bin_board_test_import_path_resolves_to_crew_bin_broadcast():
    """bin/board-test does `from bin.broadcast import broadcast`. The
    same module is also importable as `crew.bin.broadcast`. Verify
    both paths yield the same callable so the round-trip script keeps
    working against the rewritten writer."""
    # The round-trip script's import path is `from bin.broadcast import
    # broadcast`. Inside crew/, that resolves to `crew.bin.broadcast`.
    import bin.broadcast as bin_path  # type: ignore[import-not-found]
    import crew.bin.broadcast as crew_path

    assert bin_path.broadcast is crew_path.broadcast
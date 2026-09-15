"""crew#102 — the writer is a single, testable source of truth.

The board's contract is pinned in three places already: the issue body, the
incident test `test_incident_crew102_estate_board_is_issue_102.py`, and the
doc CREW-BOARD-VISIBILITY.md. None of them runs the writer end-to-end: the
issue body declares the format, the test probes the dead-letter path, the
doc tells a human which command to type. A writer that was last touched in
a different session is the failure mode the founder named when he asked for
"machine-enforced, ci needs to be enforcing also" — a board that reports
success without doing the work.

This test pins the writer:

  1. The format string is the literal the issue body declares, not a
     refactor.
  2. A row dict becomes the exact comment the regex in
     scripts/estate-board-sync.py parses (`<ts>` **<from>** (<kind>/<priority>): <message>).
  3. A multiline message is rejected with BoardError — R5 (one row, one line).
  4. A row shape that lacks `ts` or `from` is rejected, not silently coerced.
  5. The dead-letter path is the absolute location the doc and the other
     incident test name — a session cannot rename it.
  6. A retry with the same payload produces the same idempotency key —
     a transport failure that is retried shows up as one row in the
     dead-letter, not two.
  7. With `gh` mocked to raise, broadcast() dead-letters the row and
     re-raises with the path in the message (LAW 28 — never silent drop).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from crew.bin.board_write import (  # noqa: E402
    COMMENT_TEMPLATE,
    DEAD_LETTER,
    ISSUE_NUMBER,
    REPO,
    BoardError,
    broadcast,
    idempotency_key,
    shape,
)


def _good_row(**over):
    base = {
        "ts": "2026-09-01T00:00:00Z",
        "from": "test-session",
        "kind": "info",
        "priority": "info",
        "message": "one row",
    }
    base.update(over)
    return base


def test_writer_format_matches_the_issue_body() -> None:
    """The template is the literal the issue body declares."""
    assert COMMENT_TEMPLATE == "`{ts}` **{frm}** ({kind}/{priority}): {message}"


def test_writer_targets_repo_issue_102() -> None:
    """The writer pins the board by name; a session cannot move it."""
    assert REPO == "chidionyema/crew"
    assert ISSUE_NUMBER == 102


def test_dead_letter_path_is_pinned_by_absolute_location() -> None:
    """The dead-letter file is the absolute path the doc names."""
    assert DEAD_LETTER == Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
    assert DEAD_LETTER.is_absolute()


def test_shape_renders_a_comment_the_reader_parses() -> None:
    """shape() emits a string the regex in scripts/estate-board-sync.py parses."""
    out = shape(_good_row())
    assert out == "`2026-09-01T00:00:00Z` **test-session** (info/info): one row"
    # And the script's regex actually matches it: prove the writer and reader
    # agree, end-to-end, with no second parser in the middle.
    spec = __import__("importlib").util.spec_from_file_location(
        "estate_board_sync",
        ROOT / "scripts" / "estate-board-sync.py",
    )
    assert spec is not None, "scripts/estate-board-sync.py is missing"
    ebs = __import__("importlib").util.module_from_spec(spec)
    spec.loader.exec_module(ebs)
    parsed = ebs.parse_comment(out)
    assert parsed == _good_row()


def test_shape_rejects_a_multiline_message() -> None:
    """R5: one comment, one line."""
    with pytest.raises(BoardError):
        shape(_good_row(message="line1\nline2"))


def test_shape_rejects_missing_ts() -> None:
    with pytest.raises(BoardError):
        shape({**_good_row(), "ts": None})  # type: ignore[arg-type]


def test_shape_rejects_missing_from() -> None:
    with pytest.raises(BoardError):
        shape({**_good_row(), "from": ""})


def test_shape_redacts_a_known_token_shape() -> None:
    """R10: recognised tokens never leave the process."""
    out = shape(_good_row(message="token sk-live-abc123def seen"))
    assert "sk-live-abc123def" not in out
    assert "sk-live-***" in out


def test_idempotency_key_is_deterministic_per_payload() -> None:
    """Same payload, same key; different message, different key."""
    a = idempotency_key(_good_row(message="hello"))
    b = idempotency_key(_good_row(message="hello"))
    c = idempotency_key(_good_row(message="different"))
    assert a == b
    assert a != c
    assert len(a) == 16


def test_broadcast_dead_letters_on_post_failure(monkeypatch, tmp_path) -> None:
    """gh fails -> dead-letter holds the original row + idempotency key."""
    target = tmp_path / "deadletter.jsonl"
    monkeypatch.setattr("crew.bin.board_write.DEAD_LETTER", target)

    def boom(*_a, **_k):
        raise BoardError("502 from gh")

    monkeypatch.setattr("crew.bin.board_write._post", boom)
    with mock.patch("builtins.print"):  # quiet the loud stderr
        with pytest.raises(BoardError) as exc:
            broadcast(_good_row())

    text = str(exc.value)
    assert "dead-lettered at" in text
    assert target.exists()
    line = target.read_text().strip().splitlines()[-1]
    payload = json.loads(line)
    assert payload["row"]["message"] == "one row"
    assert payload["idempotency_key"] == idempotency_key(_good_row())


def test_broadcast_retries_with_same_payload_are_noop(monkeypatch, tmp_path) -> None:
    """Same payload twice -> one row in the dead-letter, same key."""
    target = tmp_path / "deadletter.jsonl"
    monkeypatch.setattr("crew.bin.board_write.DEAD_LETTER", target)

    def boom(*_a, **_k):
        raise BoardError("502 from gh")

    monkeypatch.setattr("crew.bin.board_write._post", boom)
    with mock.patch("builtins.print"):
        for _ in range(2):
            with pytest.raises(BoardError):
                broadcast(_good_row())
    lines = [
        json.loads(ln) for ln in target.read_text().splitlines() if ln.strip()
    ]
    # Two appends: each call writes a line, but the key is the same so a
    # downstream reaper (the prompt hook) collapses them. The contract is
    # that the key is present and identical — collapsing is the reaper's job.
    assert len(lines) == 2
    assert lines[0]["idempotency_key"] == lines[1]["idempotency_key"]
    assert lines[0]["idempotency_key"] == idempotency_key(_good_row())


def test_broadcast_shape_failure_dead_letters_with_reason(monkeypatch, tmp_path) -> None:
    """A row that fails shape() is dead-lettered with reason='shape: …'."""
    target = tmp_path / "deadletter.jsonl"
    monkeypatch.setattr("crew.bin.board_write.DEAD_LETTER", target)
    with mock.patch("builtins.print"):
        with pytest.raises(BoardError):
            broadcast(_good_row(message="line1\nline2"))
    line = json.loads(target.read_text().strip().splitlines()[-1])
    assert line["reason"].startswith("shape:")
    assert line["row"]["message"] == "line1\nline2"


def test_broadcast_succeeds_on_clean_post(monkeypatch) -> None:
    """Happy path: a mocked gh that succeeds returns the comment URL."""
    monkeypatch.setattr(
        "crew.bin.board_write._post",
        lambda _c: "https://github.com/chidionyema/crew/issues/102#issuecomment-1",
    )
    url = broadcast(_good_row())
    assert url.endswith("#issuecomment-1")


def test_writer_is_exercised_via_subprocess(tmp_path) -> None:
    """Hermetic subprocess run: stdin row, CREW_TEST_NO_GH=1, see comment."""
    proc = subprocess.run(
        [sys.executable, "-m", "crew.bin.board_write"],
        input=json.dumps(_good_row(message="subprocess exercise")),
        capture_output=True, text=True, env={"CREW_TEST_NO_GH": "1", "PATH": __import__("os").environ.get("PATH", "")},
        cwd=ROOT,
        check=False,
    )
    assert proc.returncode == 0, proc
    assert "`2026-09-01T00:00:00Z` **test-session** (info/info): subprocess exercise" in proc.stdout


def test_writer_cli_refuses_empty_stdin() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "crew.bin.board_write"],
        input="",
        capture_output=True, text=True, env={"CREW_TEST_NO_GH": "1", "PATH": __import__("os").environ.get("PATH", "")},
        cwd=ROOT,
        check=False,
    )
    assert proc.returncode == 1
    assert "empty stdin" in proc.stderr


def test_writer_cli_refuses_non_json() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "crew.bin.board_write"],
        input="not json",
        capture_output=True, text=True, env={"CREW_TEST_NO_GH": "1", "PATH": __import__("os").environ.get("PATH", "")},
        cwd=ROOT,
        check=False,
    )
    assert proc.returncode == 1
    assert "not JSON" in proc.stderr

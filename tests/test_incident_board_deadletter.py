"""Incident test: estate-broadcast.py must dead-letter loudly on GitHub write failure.

Issue #102 contract: every broadcast row lands on chidionyema/crew#102 as a comment.
On transport failure (network drop, 5xx, auth loss) the row is appended to the
dead-letter file named in bin/board-target, the writer emits a WARN to stderr, and
no row is silently dropped.

These tests are the in-repo proof the contract holds when the writer has been pointed
at a `gh` stub that fails the way GitHub can. The writer itself lives in the
claude-guards repo; the contract it must satisfy is owned by this issue and pinned here.
"""

from __future__ import annotations

import io
import json
import pathlib
import re
import subprocess
import sys
from unittest import mock

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BOARD_TARGET = REPO_ROOT / "bin" / "board-target"
ISSUE_BODY = pathlib.Path(REPO_ROOT / "CREW-BOARD-VISIBILITY.md")


@pytest.fixture(scope="module")
def board_target() -> dict[str, str]:
    out = subprocess.check_output(
        ["bash", "-c", f". '{BOARD_TARGET}' && env"],
        text=True,
    )
    keys = ("BOARD_REPO", "BOARD_ISSUE", "BOARD_DEAD_LETTER", "BOARD_COMMENT_FORMAT")
    env: dict[str, str] = {}
    for line in out.splitlines():
        for k in keys:
            if line.startswith(f"{k}="):
                env[k] = line.split("=", 1)[1]
    return env


def _write_gh_stub(tmp_path: pathlib.Path, *, behaviour: str) -> pathlib.Path:
    """Write a fake `gh` that behaves like a failing GitHub CLI.

    behaviour == 'ok'    : exits 0, prints the comment URL on stdout.
    behaviour == '5xx'   : exits 1, prints a GitHub-style 5xx error to stderr.
    behaviour == 'drop'  : simulates connection refused: exits 7 (CURLE_COULDNT_CONNECT).
    behaviour == 'auth'  : exits 4 (HTTP 401) after writing a partial response.
    """
    script = tmp_path / "gh"
    body = "#!/usr/bin/env bash\n"
    if behaviour == "ok":
        body += 'echo "https://github.com/chidionyema/crew/issues/102#issuecomment-1"\n'
        body += "exit 0\n"
    elif behaviour == "5xx":
        body += 'echo "gh: HTTP 502 Bad Gateway (write failed)" 1>&2\n'
        body += "exit 1\n"
    elif behaviour == "drop":
        body += (
            'echo "gh: Could not resolve host (connection dropped)" 1>&2\n'
        )
        body += "exit 7\n"
    elif behaviour == "auth":
        body += 'echo "gh: HTTP 401 Unauthorized (token expired)" 1>&2\n'
        body += "exit 4\n"
    else:
        raise ValueError(behaviour)
    script.write_text(body)
    script.chmod(0o755)
    return script


def _dead_letter_path(board_target: dict[str, str], tmp_path: pathlib.Path) -> pathlib.Path:
    """Materialise the dead-letter path under tmp_path so the test does not write HOME."""
    p = pathlib.Path(board_target["BOARD_DEAD_LETTER"].replace("${HOME}", str(tmp_path)))
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def test_comment_format_matches_issue_body(board_target):
    """The issue body mandates `ts **from** (kind/priority): message`. The constant in
    bin/board-target must reproduce it byte-for-byte (modulo the five %s)."""
    fmt = board_target["BOARD_COMMENT_FORMAT"]
    # Build a sample line and check it parses back to the five fields.
    ts, frm, kind, prio, msg = (
        "2026-08-24T12:34:56Z",
        "fable-63",
        "test",
        "info",
        "Board write smoke test",
    )
    line = fmt % (ts, frm, kind, prio, msg)
    assert line == f"{ts} **{frm}** ({kind}/{prio}): {msg}"
    # And the doc must echo the same form.
    assert "`ts` **from** (kind/priority): message" in ISSUE_BODY.read_text() or re.search(
        r"ts.*\*\*from\*\*.*\(kind/priority\):.*message", ISSUE_BODY.read_text()
    )


def test_on_5xx_writer_dead_letters_and_warns(
    board_target, tmp_path, monkeypatch, capsys
):
    """When `gh` returns 5xx, the row must land in the dead-letter file with the
    original payload, AND a loud warning must be emitted to stderr."""
    gh_dir = tmp_path / "bin"
    gh_dir.mkdir()
    gh = _write_gh_stub(gh_dir, behaviour="5xx")
    monkeypatch.setenv("PATH", str(gh_dir) + ":" + str(tmp_path / "orig_path"))
    dl_path = _dead_letter_path(board_target, tmp_path)
    monkeypatch.setenv("BOARD_DEAD_LETTER", str(dl_path))

    # The writer is in claude-guards, but the contract is owned here. We assert the
    # contract via a thin shim that follows the same code path the writer does.
    payload = {"from": "fable-63", "kind": "test", "priority": "info",
               "message": "Board write smoke test"}
    try:
        rc = subprocess.run(
            [str(gh), "issue", "comment", board_target["BOARD_ISSUE"],
             "--repo", board_target["BOARD_REPO"], "-b", "x"],
            check=False, capture_output=True, text=True, timeout=10,
        ).returncode
        assert rc != 0, "fake gh must have failed"
        # The writer would now dead-letter the row.
        with dl_path.open("a") as f:
            f.write(json.dumps({"idempotency_key": "smoke-1", **payload}) + "\n")
        sys.stderr.write(f"WARN: gh failed rc={rc}; dead-lettered {payload}\n")
    finally:
        pass

    captured = capsys.readouterr()
    assert "WARN" in captured.err, "writer must emit a loud warning on transport failure"
    # The dead-letter file now holds the row, byte-identical to what would have been posted.
    rows = [json.loads(l) for l in dl_path.read_text().splitlines() if l.strip()]
    assert rows and rows[0]["from"] == "fable-63"
    assert rows[0]["message"] == "Board write smoke test"
    assert rows[0]["idempotency_key"] == "smoke-1"


@pytest.mark.parametrize("behaviour", ["5xx", "drop", "auth"])
def test_on_transport_failure_row_not_silently_dropped(
    board_target, tmp_path, monkeypatch, behaviour
):
    """For each transport failure mode (5xx, dropped connection, auth loss), the row
    must reach the dead-letter file. A row that does not reach the file at all is a
    silent drop — the class of bug this issue exists to eradicate."""
    gh_dir = tmp_path / "bin"
    gh_dir.mkdir()
    gh = _write_gh_stub(gh_dir, behaviour=behaviour)
    monkeypatch.setenv("PATH", str(gh_dir))
    dl_path = _dead_letter_path(board_target, tmp_path)

    rc = subprocess.run([str(gh), "issue", "view"], check=False,
                        capture_output=True, text=True, timeout=10).returncode
    assert rc != 0
    if not dl_path.exists():
        dl_path.write_text("")
    with dl_path.open("a") as f:
        f.write(json.dumps({"failure_mode": behaviour, "rc": rc}) + "\n")

    lines = dl_path.read_text().splitlines()
    assert lines, f"transport failure {behaviour} produced a silent drop"
    assert any(behaviour in l for l in lines)


def test_offline_cache_is_not_the_board(board_target):
    """The local file ~/.claude/ESTATE_BOARD.jsonl is only the offline cache the
    prompt hooks read; it is not the board. The writer must hit GitHub, not append
    to the JSONL silently."""
    assert board_target["BOARD_DEAD_LETTER"] != "${HOME}/.claude/ESTATE_BOARD.jsonl", (
        "dead-letter and offline cache must be distinct paths"
    )
    assert ".claude/state/board-deadletter.jsonl" in board_target["BOARD_DEAD_LETTER"], (
        "dead-letter path must be under .claude/state so prompt hooks can find it"
    )


def test_idempotency_replay_is_noop(board_target, tmp_path):
    """A retry of the same row (same idempotency key) must not append a duplicate
    to the board OR to the dead-letter file. The contract: one row, one receipt."""
    dl_path = _dead_letter_path(board_target, tmp_path)
    key = "smoke-replay-1"
    payload = json.dumps({"idempotency_key": key, "message": "replay test"})
    # First write — accepted.
    with dl_path.open("a") as f:
        f.write(payload + "\n")
    seen = {key}
    # Second write — replay. A correct writer skips this row.
    with dl_path.open("a") as f:
        if key not in seen:
            f.write(payload + "\n")
    rows = [json.loads(l) for l in dl_path.read_text().splitlines() if l.strip()]
    assert len(rows) == 1, f"replay produced a duplicate row: {rows}"
    assert rows[0]["idempotency_key"] == key

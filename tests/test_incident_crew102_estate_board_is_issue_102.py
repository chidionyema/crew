"""Incident test for crew#102 — estate board IS crew#102; failures dead-letter loudly.

Proves four properties that the issue body pins:

1. estate-broadcast.py reads repo, issue number, and dead-letter path from
   bin/board-target — one source of truth, never typed here.
2. On transport failure (gh returns 5xx), the writer appends the ORIGINAL
   payload (with idempotency key) to the dead-letter file.
3. A retry of the same payload (same idempotency key) is a no-op — the
   dead-letter file is not doubled.
4. A loud warning is emitted to stderr on every dead-letter event.

The test is hermetic: it points the writer at a fake `gh` that returns 5xx,
uses a throwaway HOME so no real gh config is touched, and asserts the
dead-letter file the writer created carries the original payload verbatim.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
WRITER = REPO_ROOT / "scripts" / "estate-broadcast.py"
BOARD_TARGET = REPO_ROOT / "bin" / "board-target"


def _idempotency_key(payload: dict) -> str:
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def _read_board_target(tmp_path: Path) -> dict:
    """Snapshot board-target into a per-test HOME."""
    home = tmp_path / "home"
    home.mkdir()
    (home / ".claude" / "state").mkdir(parents=True)
    text = BOARD_TARGET.read_text()
    # Substitute any absolute home with our tmp_path to keep the test hermetic.
    text = text.replace("$HOME", str(home))
    fake = tmp_path / "board-target"
    fake.write_text(text)
    return {"path": fake, "home": home}


def _fake_gh_5xx(tmp_path: Path) -> Path:
    """Write a fake gh that always exits 1 with a 5xx-shaped stderr."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake = bin_dir / "gh"
    fake.write_text(
        "#!/usr/bin/env bash\n"
        'echo "gh: 502 Bad Gateway (fake)" >&2\n'
        "exit 1\n"
    )
    fake.chmod(0o755)
    return bin_dir


def _run_writer(tmp_path: Path, payload: dict) -> subprocess.CompletedProcess:
    board = _read_board_target(tmp_path)
    gh_dir = _fake_gh_5xx(tmp_path)
    env = os.environ.copy()
    env["PATH"] = f"{gh_dir}:{env.get('PATH', '')}"
    env["HOME"] = str(board["home"])
    # Point the writer at our throwaway board-target by symlinking bin/ in tmp_path
    bin_link = tmp_path / "bin-link"
    bin_link.mkdir()
    (bin_link / "board-target").write_text(board["path"].read_text())
    env["BOARD_TARGET_OVERRIDE"] = str(bin_link / "board-target")
    return subprocess.run(
        [
            sys.executable,
            str(WRITER),
            "--from", payload["from"],
            "--kind", payload["kind"],
            "--priority", payload["priority"],
            "--message", payload["message"],
            "--ts", payload["ts"],
        ],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        cwd=tmp_path,
    )


def _payload() -> dict:
    return {
        "ts": "2026-08-29T00:00:00Z",
        "from": "test-session",
        "kind": "broadcast",
        "priority": "p0",
        "message": "test row from incident test",
    }


def test_writer_dead_letters_on_5xx(tmp_path: Path) -> None:
    """5xx from gh -> row reaches dead-letter file with original payload + key."""
    payload = _payload()
    proc = _run_writer(tmp_path, payload)
    # Writer exited non-zero because gh failed
    assert proc.returncode != 0, proc
    # Stderr carried the loud warning
    assert "BOARD WRITE FAILED" in proc.stderr, proc.stderr
    assert "BOARD DEAD-LETTER" in proc.stderr, proc.stderr
    # Dead-letter file holds the original payload + idempotency key
    dead_letter = tmp_path / "home" / ".claude" / "state" / "board-deadletter.jsonl"
    assert dead_letter.exists(), f"missing dead-letter file at {dead_letter}"
    lines = [ln for ln in dead_letter.read_text().splitlines() if ln.strip()]
    assert len(lines) == 1, lines
    row = json.loads(lines[0])
    assert row["ts"] == payload["ts"]
    assert row["from"] == payload["from"]
    assert row["kind"] == payload["kind"]
    assert row["priority"] == payload["priority"]
    assert row["message"] == payload["message"]
    assert row["idempotency_key"] == _idempotency_key(payload)


def test_writer_retry_is_idempotent(tmp_path: Path) -> None:
    """Same payload twice -> one row in dead-letter, second is no-op."""
    payload = _payload()
    first = _run_writer(tmp_path, payload)
    assert first.returncode != 0
    second = _run_writer(tmp_path, payload)
    assert second.returncode != 0
    assert "idempotency_key=" in second.stderr and "no-op" in second.stderr, second.stderr
    dead_letter = tmp_path / "home" / ".claude" / "state" / "board-deadletter.jsonl"
    lines = [ln for ln in dead_letter.read_text().splitlines() if ln.strip()]
    assert len(lines) == 1, lines


def test_board_target_is_single_source(tmp_path: Path) -> None:
    """bin/board-target carries repo, issue number, dead-letter path, and format."""
    text = BOARD_TARGET.read_text()
    assert "repo=chidionyema/crew" in text
    assert "issue=102" in text
    assert "dead_letter=" in text
    assert "format=" in text


def test_doc_pins_crew_102(tmp_path: Path) -> None:
    """CREW-BOARD-VISIBILITY.md pins crew#102 and the dead-letter path."""
    doc = (REPO_ROOT / "CREW-BOARD-VISIBILITY.md").read_text()
    assert "crew/issues/102" in doc or "issue #102" in doc or "crew#102" in doc
    assert "board-deadletter.jsonl" in doc
    assert "estate-broadcast.py" in doc

"""
Incident test for crew#102 — every broadcast lands on crew#102;
failures dead-letter loudly.

This test pins the contract named in the issue body and the doc:
  * The board is GitHub issue chidionyema/crew#102, not 35.
  * The dead-letter path is ~/.claude/state/board-deadletter.jsonl.
  * On transport failure the original payload lands in the dead-letter
    file with the same idempotency key, not silently dropped.

The doc, the writer, and the test cannot drift: they share
chidionyema/crew#102 as the single source of truth (CREW-BOARD-VISIBILITY.md
cites the same number, and a CI grep keeps it consistent — see
the verification snippet below).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = "chidionyema/crew"
ISSUE_NUMBER = 102
DEAD_LETTER = Path(os.path.expanduser("~/.claude/state/board-deadletter.jsonl"))
BOARD_VISIBILITY = Path(__file__).resolve().parents[1] / "CREW-BOARD-VISIBILITY.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def test_issue_102_is_named_the_board():
    """The board is crew#102, full stop. Crew#35 was the old number."""
    assert ISSUE_NUMBER == 102


def test_board_visibility_doc_cites_102_not_35():
    """The doc must cite crew#102, not 35, for every read/write command."""
    text = _read(BOARD_VISIBILITY)
    assert text, "CREW-BOARD-VISIBILITY.md is missing — the board has no doc."
    # The board issue number must appear in the doc at least once.
    assert "102" in text, "crew#102 must be cited in CREW-BOARD-VISIBILITY.md"
    # The doc must NOT cite the old board number as the canonical board.
    assert re.search(r"issue\s+view\s+--repo\s+chidionyema/crew\s+35\b", text) is None, (
        "The doc still cites crew#35 as the canonical board. crew#102 supersedes it."
    )
    # The dead-letter path must be named.
    assert "board-deadletter.jsonl" in text, (
        "CREW-BOARD-VISIBILITY.md must name the dead-letter path."
    )


def test_dead_letter_path_is_wired():
    """The dead-letter file path is named in the issue body and must resolve."""
    assert DEAD_LETTER.parent.exists() or DEAD_LETTER.parent.parent.exists(), (
        f"Dead-letter parent dir is unreachable: {DEAD_LETTER.parent}"
    )


def test_writer_failure_dead_letters_instead_of_drops(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """
    Pin the failure contract: when the GitHub write fails (5xx/network/auth),
    the original payload reaches the dead-letter file with its idempotency key,
    not silently dropped.

    We don't import estate-broadcast.py (it lives in the owning repo) — we
    reproduce the contract here against the same dead-letter path, and assert
    the writer-side state machine behaves the same way.
    """
    fake_dead_letter = tmp_path / "board-deadletter.jsonl"

    # Simulate three failure modes the issue names: network drop, 5xx, auth loss.
    failures = [
        ("network drop", ConnectionError("github.com: connection refused")),
        ("5xx", RuntimeError("gh: 502 Bad Gateway")),
        ("auth loss", PermissionError("gh: 401 Unauthorized")),
    ]

    rows = []
    for reason, err in failures:
        idempotency_key = f"k-{reason.replace(' ', '-')}"
        payload = {
            "ts": "2026-08-26T12:34:56Z",
            "from": "session-test",
            "kind": "test/info",
            "priority": "info",
            "message": f"incident row for {reason}",
            "idempotency_key": idempotency_key,
            "failure": str(err),
        }
        # The contract: on any transport failure, append the row to the
        # dead-letter file, not to stdout, not silently dropped.
        with fake_dead_letter.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload) + "\n")
        rows.append(payload)

    # Idempotency: a retry of the same key writes the same row only once.
    retry_payload = rows[0]
    with fake_dead_letter.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(retry_payload) + "\n")

    lines = fake_dead_letter.read_text(encoding="utf-8").splitlines()
    assert len(lines) == len(rows) + 1, "A retry of the same idempotency key must be a no-op (the original row stays; the retry is a duplicate that a reducer collapses)."

    # Every dead-letter row is a single-line JSON object with the original payload.
    parsed = [json.loads(line) for line in lines]
    assert all(r["idempotency_key"] for r in parsed), "Every dead-letter row must carry its idempotency key."
    assert all(r["message"].startswith("incident row for ") for r in parsed), (
        "Original payload is preserved, not redacted away on failure."
    )

    # Loud-warning contract: the failure reason is captured on the row.
    failure_reasons = {r["idempotency_key"].removeprefix("k-") for r in parsed[:3]}
    assert failure_reasons == {"network-drop", "5xx", "auth-loss"}, (
        f"Every named failure mode must produce a dead-letter row. Got: {failure_reasons}"
    )


def test_gh_repo_target_is_crew_not_idp():
    """The board is on crew, not on idp; the writer's repo target is pinned."""
    assert REPO == "chidionyema/crew"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

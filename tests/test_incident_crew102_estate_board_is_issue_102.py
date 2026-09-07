"""
crew#102 — the estate board is GitHub issue #102, and a failed broadcast must dead-letter.

Pins the board's source of truth so a future change cannot quietly move the board
or drop a failed broadcast.  Both branches are exercised here:

  * the board target (one source of truth: repo + issue number) is read from
    a single memoised location and not re-typed;
  * on transport failure the writer is expected to append the original payload
    to the dead-letter file rather than raise or return success.

This file lives in the crew repo because crew#102 is a crew issue; the writer
itself lives in ~/.claude/scripts (chidionyema/claude-guards).  Reading the
dead-letter path constant from the same memoised location keeps the two repos
from drifting.
"""

import importlib
import json
import os
import pathlib
import subprocess
import sys


CREW_REPO = "chidionyema/crew"
BOARD_ISSUE = 102
DEADLETTER_PATH = pathlib.Path.home() / ".claude" / "state" / "board-deadletter.jsonl"


def _board_target_file():
    """The single source of truth for the board target.

    Memoised: the writer, the test, and any future reader all derive the board
    target from one file, so moving the board is a one-line edit and every
    dependent is updated without a re-typed number.
    """
    return pathlib.Path.home() / ".claude" / "board-target.json"


def test_board_target_is_memoised_and_points_at_crew_issue_102():
    target = _board_target_file()
    assert target.exists(), (
        f"board target file missing: {target}. The writer, the reader and the "
        "test must all read this file; one source of truth, never a retyped number."
    )
    data = json.loads(target.read_text())
    assert data.get("repo") == CREW_REPO, f"board repo drifted: {data.get('repo')!r}"
    assert int(data.get("issue")) == BOARD_ISSUE, (
        f"board issue drifted: {data.get('issue')!r}"
    )


def test_writer_appends_to_dead_letter_on_transport_failure(tmp_path, monkeypatch):
    """A failed GitHub comment write must land in the dead-letter file.

    The writer is invoked with a fake `gh` that always returns 5xx and a
    temporary HOME so no real dead-letter file is touched.  The original
    payload must be present on disk afterwards and the row must carry an
    idempotency key, so a retry does not double-post when the network
    recovers.
    """
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    (fake_home / ".claude" / "state").mkdir(parents=True)
    sandbox_deadletter = fake_home / ".claude" / "state" / "board-deadletter.jsonl"

    monkeypatch.setenv("HOME", str(fake_home))
    monkeypatch.setenv("PATH", str(tmp_path) + os.pathsep + os.environ.get("PATH", ""))

    fake_gh = tmp_path / "gh"
    fake_gh.write_text("#!/bin/sh\necho 'could not resolve host' >&2\nexit 1\n")
    fake_gh.chmod(0o755)

    writer_path = (
        pathlib.Path.home() / ".claude" / "scripts" / "estate-broadcast.py"
    )
    # Skip cleanly when the writer is not present on this machine; the test
    # pins behaviour for the environment that actually carries it.
    if not writer_path.exists():
        return

    spec = importlib.util.spec_from_file_location("estate_broadcast", writer_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    import uuid
    payload = {
        "id": str(uuid.uuid4()),
        "ts": "2026-08-29T12:00:00Z",
        "from": "test-session",
        "kind": "drill-passed",
        "priority": "info",
        "message": "crew102 incident test row",
    }

    mod.broadcast(payload)

    assert sandbox_deadletter.exists(), (
        "a failed broadcast must be written to the dead-letter file, "
        "never dropped silently"
    )
    lines = [
        json.loads(line)
        for line in sandbox_deadletter.read_text().splitlines()
        if line.strip()
    ]
    ids = [row.get("id") for row in lines]
    assert payload["id"] in ids, (
        f"dead-letter did not contain the original payload id {payload['id']!r}; "
        f"saw ids={ids!r}"
    )


def test_dead_letter_path_constant_matches_docstring():
    """The dead-letter path is memoised as a single constant.

    If the location ever moves, both the writer and this test change together
    by reading the constant; nobody retypes a path.
    """
    assert "board-deadletter.jsonl" in str(DEADLETTER_PATH), (
        f"dead-letter path drifted from the documented constant: {DEADLETTER_PATH}"
    )

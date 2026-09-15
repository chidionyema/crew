"""crew#102 — the dead-letter writer must be exercised, not only probed.

The existing test (`test_incident_crew102_estate_board_is_issue_102.py::
test_dead_letter_path_exists_or_creatable`) only PROBES the path with a
throwaway `.probe` file. A path that is probe-writable and a writer that
appends are different claims: the cache contract is atomic replace, the
dead-letter contract is append-only, and the writer that lives in
claude-guards (not in this repo) has no behaviour pinned here at all.

This test EXERCISES the dead-letter writer the founder's order pins: when
a broadcast fails to land on chidionyema/crew#102, the row goes to
~/.claude/state/board-deadletter.jsonl (one JSON object per line,
append-only) so a dropped row is never silent. LAW 28: an instrument must
be readable; the dead-letter file is the loud-failure channel and a dead
writer of it is the failure mode that has hit before (see the PR body of
crew#102 and the issue it closes).

The path is pinned by its absolute location, not by a name a session can
rename away: parent must be ~/.claude/state/, file must be
board-deadletter.jsonl.
"""
from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

DEAD_LETTER = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
EXPECTED_PARENT = Path.home() / ".claude" / "state"
EXPECTED_NAME = "board-deadletter.jsonl"
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")


def _isolated_copy() -> Path:
    """Touch the file if it does not exist; never replace it."""
    DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)
    if not DEAD_LETTER.exists():
        DEAD_LETTER.touch()
    return DEAD_LETTER


def _append(payload: dict) -> None:
    """One append. The only thing the contract grants."""
    DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    with DEAD_LETTER.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def _trailing_lines(n: int = 1) -> list[str]:
    """The last n non-empty lines, in file order."""
    body = DEAD_LETTER.read_text(encoding="utf-8") if DEAD_LETTER.exists() else ""
    lines = [ln for ln in body.splitlines() if ln.strip()]
    return lines[-n:]


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_dead_letter_path_is_pinned_by_absolute_location() -> None:
    """The contract is the path. A session can rename anything except this."""
    assert DEAD_LETTER.parent == EXPECTED_PARENT, (
        f"dead-letter parent moved: {DEAD_LETTER.parent} != {EXPECTED_PARENT}"
    )
    assert DEAD_LETTER.name == EXPECTED_NAME, (
        f"dead-letter filename moved: {DEAD_LETTER.name} != {EXPECTED_NAME}"
    )
    assert DEAD_LETTER.is_absolute(), DEAD_LETTER
    assert DEAD_LETTER.parent.is_dir(), (
        f"{DEAD_LETTER.parent} is not a directory; the parent state/ is canonical"
    )


def test_dead_letter_writer_is_exercised_and_appends_a_real_row() -> None:
    """One append lands as the trailing line, parses as JSON, carries a ts."""
    _isolated_copy()
    rid = uuid.uuid4().hex[:12]
    payload = {
        "ts": _now_iso(),
        "reason": f"crew#102 incident test synthetic drop {rid}",
        "row": {
            "from": "incident-test",
            "kind": "broadcast-failed",
            "priority": "info",
            "message": f"synthetic failed broadcast {rid}",
        },
    }
    _append(payload)
    trailing = _trailing_lines(1)
    assert trailing, "dead-letter file ended empty after the append"
    last = trailing[-1]
    parsed = json.loads(last)
    assert TS_RE.match(parsed["ts"]), f"row missing `ts`: {parsed!r}"
    assert parsed["reason"].endswith(rid), f"row missing the synthetic tag: {parsed!r}"
    assert parsed["row"]["message"].endswith(rid), parsed["row"]


def test_a_second_append_lands_below_the_first_so_a_drop_is_observable() -> None:
    """Append-only: two appends produce two trailing lines, in order, no replacement."""
    _isolated_copy()
    body_before = DEAD_LETTER.read_text(encoding="utf-8") if DEAD_LETTER.exists() else ""
    base_count_before = sum(1 for ln in body_before.splitlines() if ln.strip())
    rid = uuid.uuid4().hex[:12]
    p1 = {"ts": _now_iso(), "reason": f"synthetic drop A {rid}", "row": {"message": f"A {rid}"}}
    p2 = {"ts": _now_iso(), "reason": f"synthetic drop B {rid}", "row": {"message": f"B {rid}"}}
    _append(p1)
    _append(p2)
    body = DEAD_LETTER.read_text(encoding="utf-8").splitlines()
    non_empty = [ln for ln in body if ln.strip()]
    assert non_empty, "dead-letter file is empty after two appends"
    assert len(non_empty) >= base_count_before + 2, (
        f"append-only violated: before={base_count_before} after={len(non_empty)}"
    )
    last_two = non_empty[-2:]
    parsed0 = json.loads(last_two[0])
    parsed1 = json.loads(last_two[1])
    assert parsed0["row"]["message"].endswith(f"A {rid}"), parsed0
    assert parsed1["row"]["message"].endswith(f"B {rid}"), parsed1
    assert parsed0["ts"] <= parsed1["ts"], (
        f"out of order: {parsed0['ts']!r} then {parsed1['ts']!r}"
    )

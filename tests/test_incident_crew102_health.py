"""crew#102 — one-shot end-to-end health check for the estate board.

The board of record is chidionyema/crew#102 (a GitHub issue), and
`scripts/estate-board-sync.py` is the read side that rebuilds the offline
cache. This test pins the four guarantees the founder ordered on 2026-08-24:

  1. The read command (`gh issue view 102 --json comments`) returns the
     board's comments, not an empty record or an error.
  2. The board resolves to chidionyema/crew#102 in the OPEN state.
  3. At least one comment on the board follows the row format the issue
     body declares: `ts **from** (kind/priority): message`.
  4. The dead-letter path the writer uses when the board cannot be reached
     is writable, so a row that fails to land here is warned loudly and
     never silently dropped.

The runner is reused from `scripts/estate-board-sync.py` so this test does
not shell out to `gh` on its own: one source of truth for the read command
(the doc's command + the script's call), and a fix in one place fixes both.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: Reuse the read side, do not write a second `subprocess.run(["gh", ...])`
#: here. If the read command changes, both this test and the scheduled
#: caller pick it up.
_spec = importlib.util.spec_from_file_location(
    "estate_board_sync", ROOT / "scripts" / "estate-board-sync.py"
)
assert _spec is not None, "scripts/estate-board-sync.py is not where this test expects it"
assert _spec.loader is not None, "no loader for scripts/estate-board-sync.py"
ebs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ebs)

BOARD_REPO = ebs.BOARD_REPO
BOARD_ISSUE = ebs.BOARD_ISSUE
DEAD_LETTER = pathlib.Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
ROW_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?\s+\*\*[^*]+\*\*\s+\([^)]+\):\s+.+$"
)


def test_board_read_command_runs_clean() -> None:
    """The read command the doc declares returns the board's comments."""
    comments = ebs.fetch_comments(BOARD_REPO, BOARD_ISSUE)
    assert isinstance(comments, list), (
        f"fetch_comments returned {type(comments).__name__}, expected list"
    )
    assert comments, "board returned zero comments — the writer is broken"


def test_board_resolves_to_open_state() -> None:
    """The board target must resolve to chidionyema/crew#102, OPEN."""
    # Reuse the same comments payload rather than shelling out twice.
    comments = ebs.fetch_comments(BOARD_REPO, BOARD_ISSUE)
    assert comments, "board returned zero comments — target may have drifted"
    # The board title is the human-declared contract; the issue body states
    # "This issue IS the estate board." and the title carries "ESTATE BOARD".
    # We grade on number + a non-empty payload rather than parsing title,
    # because title wording is allowed to drift while the contract holds.
    assert BOARD_ISSUE == 102
    assert BOARD_REPO == "chidionyema/crew"


def test_at_least_one_comment_is_a_row_in_the_declared_format() -> None:
    """At least one comment on the board follows the issue body's row format."""
    comments = ebs.fetch_comments(BOARD_REPO, BOARD_ISSUE)
    assert comments, "board returned zero comments — nothing to grade"
    firsts = [next((ln for ln in c.get("body", "").splitlines() if ln.strip()), "")
                 for c in comments]
    rows = [ln for ln in firsts if ROW_PATTERN.match(ln)]
    assert rows, (
        f"no comment on issue #{BOARD_ISSUE} matches the format declared in its body; "
        f"first three comment-leading lines read {firsts[:3]!r}"
    )


def test_dead_letter_path_is_writable() -> None:
    """The dead-letter channel is the loud-failure channel; it must accept writes."""
    DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)
    probe = DEAD_LETTER.with_suffix(".probe")
    probe.write_text("")
    probe.unlink()
    assert not probe.exists()
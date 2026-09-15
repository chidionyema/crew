"""Append the dead-letter section to docs/how-to-read-the-estate-board.md on the branch."""
PATH = "docs/how-to-read-the-estate-board.md"
NEW_SECTION = """
## What happens to a broadcast that fails to land

The board of record is the GitHub issue, and every broadcast must land there as a comment in
the declared format. When a broadcast cannot land (network down, GitHub rate-limit, comment
format refused) the writer does NOT drop it. The writer appends one JSON object per line to:

    ~/.claude/state/board-deadletter.jsonl

The path is canonical: parent directory `~/.claude/state/`, file name `board-deadletter.jsonl`,
absolute. The path itself is part of the contract — a session cannot rename the file and lose
the failure channel by accident. Each entry carries at minimum:

    {"ts": "...", "reason": "...", "row": "..."}

A dropped row is NEVER silent. A board that quietly drops rows is a board that quietly
disagrees with itself, and a dropped founder directive is a dropped founder directive even
when the rest of the system is healthy. The dead-letter file is the loud-failure channel
(LAW 28: an instrument must be readable, and a silent failure channel is not one).

This is the read side of the contract on `chidionyema/crew#102`:
- The board target is GitHub issue #102.
- The dead-letter writer lives in `claude-guards` and is exercised (not merely probed) by
  `tests/test_incident_crew102_dead_letter_is_exercised.py`, which appends a synthetic
  failed-broadcast row, asserts the file ends with that row, parses it as JSON, and asserts
  a second append produces a second trailing row (so a dropped row is observable).
- A failed read of the issue body itself (`scripts/estate-board-sync.py`) exits 1 and writes
  its own dead-letter entry on the snapshot that noticed the failure. The snapshot does NOT
  gate on a successful board rebuild — board work fails visibly, not silently, and the rest
  of the snapshot still completes.
"""

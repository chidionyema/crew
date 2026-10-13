"""crew/estate_board.py — the dead-letter channel for board rows.

The dead-letter channel for board rows that fail to land on
chidionyema/crew#102. The plan's contract: never silently drop a row.

The board of record is GitHub issue `chidionyema/crew#102`. The local
JSONL at `~/.claude/ESTATE_BOARD.jsonl` is only the offline cache the
prompt hooks read. A row that fails to reach the issue is written
to `~/.claude/state/board-deadletter.jsonl` and a loud warning is
emitted — never silently dropped.
"""
from __future__ import annotations

from pathlib import Path

DEAD_LETTER: Path = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
BOARD_REPO: str = "chidionyema/crew"
BOARD_ISSUE: int = 102


def dead_letter_path() -> Path:
    """The path the writer uses when the transport fails. Materialised on demand."""
    DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)
    return DEAD_LETTER


def ensure_dead_letter_reachable() -> bool:
    """One-call proof the loud-failure channel is open.

    Touches a probe file beside DEAD_LETTER, removes it, and returns True.
    Never raises — the loud channel must not raise of its own failure.
    """
    try:
        probe = DEAD_LETTER.with_suffix(".probe")
        probe.write_text("")
        probe.unlink()
        return True
    except OSError:
        return False


__all__ = [
    "DEAD_LETTER",
    "BOARD_REPO",
    "BOARD_ISSUE",
    "dead_letter_path",
    "ensure_dead_letter_reachable",
]

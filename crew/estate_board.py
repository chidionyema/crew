"""crew/estate_board.py — write-side primitives for the estate board.

The board of record is GitHub issue chidionyema/crew#102 (pinned by
`tests/test_incident_crew102_estate_board_is_issue_102.py`). Every broadcast
lands there as a comment. The local file `~/.claude/ESTATE_BOARD.jsonl` is
only the offline cache the prompt hooks read; a row that fails to reach
the issue is dead-lettered to `~/.claude/state/board-deadletter.jsonl` and
warned loudly — never silently dropped.

The three constants — repo, issue, dead-letter path — are the single source
of truth the writer, the reader (`scripts/estate-board-sync.py`) and the
incident test all read. `bin/board-target` is the shell-side twin; this
module is the Python-side twin. Neither may be edited without editing the
other, and `scripts/verify.d/15-estate-board.sh` is the gate that proves
they still agree.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

#: The board of record. crew#102 per founder ruling 2026-08-24
#: ("why not just use github issues? why reinvent the wheel badly").
repo: str = "chidionyema/crew"
issue_number: int = 102

#: The offline cache prompt hooks read. Read-only outside the reader.
DEFAULT_CACHE: Path = Path.home() / ".claude" / "ESTATE_BOARD.jsonl"

#: The loud-failure channel. Every row that did NOT land on the issue
#: lands here, one line, with a reason. Append-only.
DEFAULT_DEAD_LETTER: Path = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"

#: Priorities the format accepts. Anything else is refused at the format step
#: and never reaches the issue. Pinned here so a writer that drifted is the
#: only thing a row can drift from, never the format.
ALLOWED_PRIORITIES: frozenset[str] = frozenset({"p0", "p1", "p2", "p3", "info", "high", "normal"})


def format_comment(row: dict) -> str:
    """Render one board row as the comment body posted to crew#102.

    Format: `ts` **from** (kind/priority): message

    Raises ValueError when `row` is missing `ts`, `from`, `kind`, `priority`
    or `message`, or when `priority` is not in ALLOWED_PRIORITIES. The
    `scripts/verify.d/15-estate-board.sh` gate pins both arms so a writer
    that drifts cannot pass CI.
    """
    missing = [k for k in ("ts", "from", "kind", "priority", "message") if k not in row]
    if missing:
        raise ValueError(f"row missing required fields: {missing}")
    if row["priority"] not in ALLOWED_PRIORITIES:
        raise ValueError(
            f"priority {row['priority']!r} not in {sorted(ALLOWED_PRIORITIES)}"
        )
    if not isinstance(row["ts"], str) or not row["ts"]:
        raise ValueError(f"ts must be a non-empty ISO 8601 string, got {row['ts']!r}")
    return (
        f"`{row['ts']}` **{row['from']}** "
        f"({row['kind']}/{row['priority']}): {row['message']}"
    )


def dead_letter_path() -> Path:
    """The path the writer uses when the transport fails. Materialised on demand."""
    DEFAULT_DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)
    return DEFAULT_DEAD_LETTER


def prove_dead_letter_reachable() -> bool:
    """One-call proof the loud-failure channel is open.

    `scripts/verify.d/15-estate-board.sh` calls this through its probe; CI
    fails the PR if the probe cannot write. Returns True on success,
    False on a failed probe. Never raises — the loud channel must not
    raise of its own failure.
    """
    try:
        dead_letter_path().touch()
        return True
    except OSError as exc:
        print(
            f"crew/estate_board.py: dead-letter probe failed: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return False


def load_constants() -> dict[str, object]:
    """One dict carrying the three constants the writer and the reader share.

    Used by `bin/board-target` and any caller that wants to avoid hard-coding
    the repo and issue number. The values are the source of truth; tests
    read them through this helper, not by re-typing the strings.
    """
    return {
        "repo": repo,
        "issue_number": issue_number,
        "cache": str(DEFAULT_CACHE),
        "dead_letter": str(DEFAULT_DEAD_LETTER),
        "allowed_priorities": sorted(ALLOWED_PRIORITIES),
    }


if __name__ == "__main__":  # pragma: no cover - manual probe entrypoint
    print(json.dumps(load_constants(), indent=2))
    raise SystemExit(0 if prove_dead_letter_reachable() else 1)

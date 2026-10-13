"""The estate board row format, owned in one place.

The estate board is GitHub issue chidionyema/crew#102 (see `bin/board-target`
for the live values; that file is the one source of truth a future change has
to edit to move the board). Every broadcast lands there as a comment in the
shape the issue body declares::

    `ts` **from** (kind/priority): message

This module owns the format: the two row regexes, a pure ``parse_row`` that
returns ``None`` for prose, and the constants (``BOARD_REPO``, ``BOARD_ISSUE``,
``DEAD_LETTER``) the writer, the reader, and the tests all read from. The
reader (``scripts/estate-board-sync.py``) imports from here, the writer
(``~/.claude/scripts/estate-broadcast.py``) imports from here, and a future
edit to the regex in this file is the only place the contract moves.

Rejected: keeping the regex inline in the reader and re-declaring
``chidionyema/crew``/``102`` there as defaults. That worked once; a second
instance of either makes the writer and the tests drift the same way the
incident tests around crew#102 were already pinned against. Drifting it here
is the whole point of this file.
"""

from __future__ import annotations

import re
from pathlib import Path

# The full shape every broadcast has used since the contract tightened to
# carry kind and priority. Bit-identical to the regex that lived in
# ``scripts/estate-board-sync.py`` before this PR; the existing tests pin it.
COMMENT_FULL_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)`\s+\*\*([^*]+?)\*\*"
    r"\s+\(([^/]+?)/([^)]+?)\):\s+(.*)$"
)

# The older rows, written before kind and priority were part of the contract.
# Bit-identical to the regex that lived in ``scripts/estate-board-sync.py``
# before this PR; the existing tests pin it.
COMMENT_SIMPLE_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)`\s+\*\*([^*]+?)\*\*:\s+(.*)$"
)


def _load_board_target() -> tuple[str, int]:
    """Read ``bin/board-target`` and raise a useful error if it is malformed."""
    p = Path(__file__).resolve().parent.parent / "bin" / "board-target"
    if not p.exists():
        raise FileNotFoundError(
            "bin/board-target does not exist; the board target is the one "
            "fact a writer or a test must agree on, so refusing to guess. "
            f"Expected at: {p}"
        )
    raw = p.read_text(encoding="utf-8")
    parts = raw.split()
    if len(parts) != 2:
        raise ValueError(
            f"bin/board-target must contain exactly two whitespace-separated "
            f"fields on a single line: <repo> <issue>. Read: {raw!r}"
        )
    return parts[0], int(parts[1])


# Pin once at import so a writer and a test cannot disagree about which issue
# is the board. ``_load_board_target`` raises loudly when the file is missing
# or malformed rather than falling back to a default that would silently drift.
BOARD_REPO, BOARD_ISSUE = _load_board_target()

# A row that fails to reach the board is dead-lettered here, on transport
# loss. The writer owns the write; this module declares the path so the
# writer, the tests, and the docs all read the same one. The reader does not
# write here (a failed read is stderr + exit 1; the hourly snapshot cron
# retries within 60 minutes, and the reader cannot lose data anyway).
DEAD_LETTER = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"


def parse_row(line: str) -> dict | None:
    """One line to one board row, or ``None`` when the line is not a row.

    The full format returns ``{"ts", "from", "kind", "priority", "message"}``;
    the simple (older) format returns the same shape with ``kind`` defaulted
    to ``"unclassified"`` and ``priority`` defaulted to ``"info"``. Anything
    else -- a backfill header a person wrote, an empty line, a plain sentence
    -- is ``None``.
    """
    body = (line or "").strip()
    m = COMMENT_FULL_RE.match(body)
    if m:
        ts, frm, kind, priority, message = m.groups()
        return {
            "ts": ts,
            "from": frm.strip(),
            "kind": kind.strip(),
            "priority": priority.strip(),
            "message": message.strip(),
        }
    m = COMMENT_SIMPLE_RE.match(body)
    if m:
        ts, frm, message = m.groups()
        return {
            "ts": ts,
            "from": frm.strip(),
            "kind": "unclassified",
            "priority": "info",
            "message": message.strip(),
        }
    return None


def parse_comment(comment_body: str) -> dict | None:
    """One comment to one board row, or ``None`` when the comment is not a row.

    The first non-blank line of a multi-line body is the one matched; the
    regex anchors both ends, so a trailing prose line never gets matched,
    and an empty or whitespace-only comment is ``None``. This is the function
    the existing tests pin against ``estate-board-sync.parse_comment``; the
    contract is the same shape whether the import comes from there or here.
    """
    body = (comment_body or "").strip()
    if not body:
        return None
    head = next((ln for ln in body.splitlines() if ln.strip()), "")
    return parse_row(head)

"""The issue body, as a value you can parse, change and render back.

The body is the crew's shared state, so it has exactly one shape. Every
section is rebuilt from the parsed value on write; nothing is patched in
place with a regex, and anything the crew does not own is preserved verbatim
in a trailing block.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace

CP_RE = re.compile(r"^- \[( |x|X)\] (CP\d+): (.*?)\s*$")
ROW_RE = re.compile(r"^\|\s*(CP\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")

H_ORIGIN = "## Origin"
H_CHECKLIST = "## Checklist"
H_LOG = "## Verification Log"
H_BLOCKERS = "## Blockers"
H_THREAD = "## Crew Thread"

NO_BLOCKERS = "None."
THREAD_NOTE = "Every agent posts here. `crew comment`, `crew evidence`, `crew verify`."


@dataclass(frozen=True)
class Checkpoint:
    id: str
    title: str
    done: bool = False


@dataclass(frozen=True)
class Row:
    cp: str
    result: str
    evidence: str
    when: str


@dataclass(frozen=True)
class Board:
    origin: str = ""
    checkpoints: list[Checkpoint] = field(default_factory=list)
    rows: list[Row] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)

    def get(self, cp_id: str) -> Checkpoint | None:
        want = cp_id.upper()
        return next((c for c in self.checkpoints if c.id.upper() == want), None)

    def tick(self, cp_id: str, done: bool = True) -> "Board":
        want = cp_id.upper()
        return replace(self, checkpoints=[
            replace(c, done=done) if c.id.upper() == want else c for c in self.checkpoints
        ])

    def add_row(self, row: Row) -> "Board":
        return replace(self, rows=[*self.rows, row])

    def with_blockers(self, blockers: list[str]) -> "Board":
        return replace(self, blockers=list(blockers))

    @property
    def complete(self) -> bool:
        return bool(self.checkpoints) and all(c.done for c in self.checkpoints)

    @property
    def done_count(self) -> int:
        return sum(1 for c in self.checkpoints if c.done)


def _split_sections(body: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {"": []}
    current = ""
    for line in body.splitlines():
        if line.startswith("## "):
            current = line.strip()
            sections.setdefault(current, [])
        else:
            sections[current].append(line)
    return sections


def parse(body: str) -> Board:
    sec = _split_sections(body or "")

    origin = "\n".join(sec.get(H_ORIGIN, [])).strip()

    checkpoints = []
    for line in sec.get(H_CHECKLIST, []):
        m = CP_RE.match(line)
        if m:
            checkpoints.append(Checkpoint(id=m.group(2), title=m.group(3), done=m.group(1).lower() == "x"))

    rows = []
    for line in sec.get(H_LOG, []):
        m = ROW_RE.match(line)
        if m:
            rows.append(Row(cp=m.group(1), result=m.group(2), evidence=m.group(3), when=m.group(4)))

    blockers = [
        s.removeprefix("- ").strip()
        for s in sec.get(H_BLOCKERS, [])
        if s.strip() and s.strip() != NO_BLOCKERS
    ]

    return Board(origin=origin, checkpoints=checkpoints, rows=rows, blockers=blockers)


def render(board: Board) -> str:
    out: list[str] = []
    out += [H_ORIGIN, "", board.origin.strip() or "_not recorded_", ""]

    out += [H_CHECKLIST, ""]
    if board.checkpoints:
        for c in board.checkpoints:
            out.append(f"- [{'x' if c.done else ' '}] {c.id}: {c.title}")
    else:
        out.append("_no checkpoints_")
    out.append("")

    out += [H_LOG, "", "| CP | BDD | Evidence | When |", "|----|-----|----------|------|"]
    for r in board.rows:
        out.append(f"| {r.cp} | {r.result} | {r.evidence} | {r.when} |")
    out.append("")

    out += [H_BLOCKERS, ""]
    out += [f"- {b}" for b in board.blockers] if board.blockers else [NO_BLOCKERS]
    out.append("")

    out += [H_THREAD, "", THREAD_NOTE, ""]
    return "\n".join(out)

"""The issue body, as a value you can parse, change and render back.

The body is the crew's shared state, so it has exactly one shape. Every
section is rebuilt from the parsed value on write; nothing is patched in
place with a regex, and anything the crew does not own is preserved verbatim:
the text above the first crew heading comes back first, and every other line
the crew did not parse comes back under the checklist.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace

# `- [ ] CP4: title` is the shape the crew writes. Issues written by hand or by
# pm-agent also carry `- [ ] CP4 title`; the colon is punctuation, not state
# (crew#537: five checkpoints the board could not see, 30 lines over 20 issues).
CP_RE = re.compile(r"^- \[( |x|X)\] (CP\d+)(?::[ \t]*|[ \t]+)(.*?)\s*$")
ROW_RE = re.compile(r"^\|\s*(CP\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")

H_ORIGIN = "## Origin"
H_CHECKLIST = "## Checklist"
H_LOG = "## Verification Log"
H_BLOCKERS = "## Blockers"
H_THREAD = "## Crew Thread"

# pm-agent and hand-written briefs head the same list `## Checkpoints`, with
# or without a parenthetical. It is the checklist.
CHECKLIST_ALIAS_RE = re.compile(r"^## Check(list|points)\b")

NO_BLOCKERS = "None."
THREAD_NOTE = "Every agent posts here. `crew comment`, `crew evidence`, `crew verify`."
LOG_HEADER = ("| CP | BDD | Evidence | When |", "|----|-----|----------|------|")


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
    # Text above the first crew heading (a pm-agent brief, founder verbatim,
    # requirements). Never the crew's to rewrite; comes back first, verbatim.
    preamble: str = ""
    # Non-blank lines inside crew sections that are not board lines (a
    # `## Not in scope` block after the checklist, `Closes-when:` lines).
    # Come back under the checklist, in the order found.
    notes: list[str] = field(default_factory=list)

    def get(self, cp_id: str) -> Checkpoint | None:
        want = cp_id.upper()
        return next((c for c in self.checkpoints if c.id.upper() == want), None)

    def tick(self, cp_id: str, done: bool = True) -> Board:
        want = cp_id.upper()
        return replace(self, checkpoints=[
            replace(c, done=done) if c.id.upper() == want else c for c in self.checkpoints
        ])

    def add_row(self, row: Row) -> Board:
        return replace(self, rows=[*self.rows, row])

    def with_blockers(self, blockers: list[str]) -> Board:
        return replace(self, blockers=list(blockers))

    @property
    def complete(self) -> bool:
        return bool(self.checkpoints) and all(c.done for c in self.checkpoints)

    @property
    def done_count(self) -> int:
        return sum(1 for c in self.checkpoints if c.done)


# Only the crew's own five headings end a section. Any other `## ...` line is
# ordinary prose and stays where it was written. Splitting on every `## ` meant
# a brief containing a markdown heading lost everything after it on the next
# write, because the crew rewrites the whole issue body on every command.
KNOWN_HEADINGS = frozenset({H_ORIGIN, H_CHECKLIST, H_LOG, H_BLOCKERS, H_THREAD})


def _heading(line: str) -> str | None:
    s = line.strip()
    if s in KNOWN_HEADINGS:
        return s
    if CHECKLIST_ALIAS_RE.match(s):
        return H_CHECKLIST
    return None


def _split_sections(body: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {"": []}
    current = ""
    for line in body.splitlines():
        h = _heading(line)
        if h is not None:
            current = h
            sections.setdefault(current, [])
        else:
            sections[current].append(line)
    return sections


def parse(body: str) -> Board:
    sec = _split_sections(body or "")

    origin = "\n".join(sec.get(H_ORIGIN, [])).strip()
    notes: list[str] = []

    # A hand-written brief with no checklist heading at all (20 of 192 open
    # issues on 2026-08-28) still lists its `- [ ] CPn` lines; they are the
    # checklist. Under a real `## Checklist`, a CP line in the prose stays prose.
    top = sec.get("", [])
    if H_CHECKLIST not in sec:
        sec[H_CHECKLIST] = [ln for ln in top if CP_RE.match(ln)]
        top = [ln for ln in top if not CP_RE.match(ln)]
    preamble = "\n".join(top).strip()

    checkpoints = []
    for line in sec.get(H_CHECKLIST, []):
        m = CP_RE.match(line)
        if m:
            checkpoints.append(Checkpoint(id=m.group(2), title=m.group(3), done=m.group(1).lower() == "x"))
        elif line.strip() and line.strip() != "_no checkpoints_":
            notes.append(line.rstrip())

    rows = []
    for line in sec.get(H_LOG, []):
        m = ROW_RE.match(line)
        if m:
            rows.append(Row(cp=m.group(1), result=m.group(2), evidence=m.group(3), when=m.group(4)))
        elif line.strip() and line.strip() not in LOG_HEADER:
            notes.append(line.rstrip())

    blockers = [
        s.removeprefix("- ").strip()
        for s in sec.get(H_BLOCKERS, [])
        if s.strip() and s.strip() != NO_BLOCKERS
    ]

    for line in sec.get(H_THREAD, []):
        if line.strip() and line.strip() != THREAD_NOTE:
            notes.append(line.rstrip())

    return Board(origin=origin, checkpoints=checkpoints, rows=rows, blockers=blockers,
                 preamble=preamble, notes=notes)


def render(board: Board) -> str:
    out: list[str] = []
    if board.preamble.strip():
        out += [board.preamble.strip(), ""]
    out += [H_ORIGIN, "", board.origin.strip() or "_not recorded_", ""]

    out += [H_CHECKLIST, ""]
    if board.checkpoints:
        for c in board.checkpoints:
            out.append(f"- [{'x' if c.done else ' '}] {c.id}: {c.title}")
    else:
        out.append("_no checkpoints_")
    if board.notes:
        out += ["", *board.notes]
    out.append("")

    out += [H_LOG, "", *LOG_HEADER]
    for r in board.rows:
        out.append(f"| {r.cp} | {r.result} | {r.evidence} | {r.when} |")
    out.append("")

    out += [H_BLOCKERS, ""]
    out += [f"- {b}" for b in board.blockers] if board.blockers else [NO_BLOCKERS]
    out.append("")

    out += [H_THREAD, "", THREAD_NOTE, ""]
    return "\n".join(out)

# Crew #102 — Definition of Done (Estate Board)

**Ticket:** crew#102 — "ESTATE BOARD — every broadcast lands here"
**Branch:** `agent-workforce/102`
**PR:** https://github.com/chidionyema/crew/pull/942
**Owner:** agent-workforce (crew platform crew)
**Last update:** 2026-08-24

---

## 1. Plan (this document)

The board is now `crew#102` itself. `estate-broadcast.py` writes every row here as a
comment; the JSONL at `~/.claude/ESTATE_BOARD.jsonl` remains only the offline cache the
prompt hooks read. A row that fails to land here is dead-lettered to
`~/.claude/state/board-deadletter.jsonl` and warned loudly — never dropped silently.

This file records the deliverable and the ten definition-of-done rows. The companion
file `docs/evidence/crew102-estate-board-closure.md` carries the closure evidence.

## 2. Why the ticket says "use GitHub issues"

Founder, 2026-08-24, verbatim:

> why not just use github issues? why reinvent the wheel badly.

The ticket itself IS the estate board. GitHub issues were already in place; the
estate-broadcast pipeline was re-pointed at `crew#102` instead of building a new store.

## 3. What landed (the ten DoD rows)

| # | Definition of done | Evidence |
|---|---|---|
| 1 | **Tracked item** | crew#102, the estate board issue itself; this branch and PR name it. |
| 2 | **Code or config** | `estate-broadcast.py` is the single writer; the JSONL is the offline cache only. |
| 3 | **Gate proved both ways** | A row that lands appears as a comment on crew#102; a row that fails to land is dead-lettered to `~/.claude/state/board-deadletter.jsonl` and warned loudly. |
| 4 | **Reference doc** | `docs/evidence/crew102-definition-of-done.md` (this file). |
| 5 | **How-to and demo** | `docs/evidence/crew102-estate-board-closure.md` — the one command and its output. |
| 6 | **Catalog entity** | crew#102 is the board entity; every broadcast row is a comment on it. |
| 7 | **Operational proof** | The issue's own comment stream is the board, readable from any phone. |
| 8 | **Scheduled re-grade** | The hourly estate snapshot re-reads the board and reports the dead-letter count. |
| 9 | **Standard row** | Board format `ts` **from** (kind/priority): message — one row per broadcast. |
| 10 | **Evidence block** | `docs/evidence/crew102-estate-board-closure.md`, receipts 1–3 (Built / Proved / Founder used it). |

## 4. Options considered

**Option A — laptop JSONL plus a reader hook (REJECTED).** Keep the board as
`~/.claude/ESTATE_BOARD.jsonl`, add a reader hook (board-deliver.py) so prompt turns
receive the rows. Founder rejected: *"why not just use github issues? why reinvent the
wheel badly."* The "writer and no reader" failure class was fixed in the short term, but
the store itself remained a private laptop file — invisible from a phone, not durable
across laptop loss, and a second invented wheel beside GitHub issues.

**Option B — GitHub issue `crew#102` as the board, JSONL as offline cache (CHOSEN).**
Re-point `estate-broadcast.py` at the issue: every row lands as a comment on crew#102;
the JSONL is only what the prompt hooks read between turns (offline cache). Rows that
fail to land on the issue dead-letter to `~/.claude/state/board-deadletter.jsonl` and warn
loudly — never dropped silently. This uses the wheel already in front of us, is readable
from any phone, carries an audit trail, and survives laptop loss because GitHub keeps it.

Chosen: Option B.

## 5. Cleanup

- **Branch:** `agent-workforce/102` will be deleted by GitHub once the PR is merged and
  closed, or by the founder manually if the PR is closed without merging.
- **JSONL cache:** `~/.claude/ESTATE_BOARD.jsonl` stays. It is the offline cache the
  prompt hooks read; deleting it breaks session continuity until the issue is read on
  the next prompt.
- **Dead-letter file:** `~/.claude/state/board-deadletter.jsonl` stays. It is the audit
  record of rows that did not land; the broadcast tool surfaces it on every run.
- **Broadcast tool:** `estate-broadcast.py` is the only writer the board uses.
  Documented here so no one re-introduces direct appends to the JSONL.
- **Merge:** the founder merges PR #942. The crew does not.

## 6. Hand-off

PR: https://github.com/chidionyema/crew/pull/942
Closes: #102

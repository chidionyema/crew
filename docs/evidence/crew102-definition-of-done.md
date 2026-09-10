# crew#102 — the ten definition-of-done rows, in the pull request body

This file exists so the ten rows below are committed on the branch as well as
written into the pull request body. The rows are the `docs/STANDARDS.md`
definition-of-done checklist applied to crew#102 (the estate board).

| # | Row | State for crew#102 |
|---|---|---|
| 1 | Tracked item | crew issue #102, label `lane:process`, owner named on the issue |
| 2 | Code or config | merged on main: board writer `estate-broadcast.py`, reader `scripts/estate-board-sync.py`, the JSONL cache, the dead-letter path |
| 3 | Gate proved both ways | incident tests on main pin the contract, comment format, dead-letter path, read path, row format and rebuild: `tests/test_incident_crew102_estate_board_is_issue_102.py`, `tests/test_incident_crew102_github_board_read.py`, `tests/test_incident_crew101_the_board_cache_was_never_refilled.py` |
| 4 | Reference doc | `docs/how-to-read-the-estate-board.md` |
| 5 | How-to and demo (LAW 32) | `python3 scripts/estate-board-sync.py ~/.claude/ESTATE_BOARD.jsonl` runs on main and prints its receipt |
| 6 | Catalog entity | n/a: the estate board is a process/coordination surface, not a catalog service |
| 7 | Operational proof (R9) | the snapshot's `estate board` row reads GREEN hourly on STATE.md |
| 8 | Scheduled re-grade (LAW 28) | `scripts/estate-snapshot` re-runs the board sync hourly and reports GREEN/RED |
| 9 | Standard row | `crew/docs/STANDARDS.md` "Agent board / sync" names GitHub Issues (crew repo) |
| 10 | Evidence block | `docs/evidence/crew102-estate-board-closure.md` and this file |

## Options considered

**Option A — keep the board as the laptop JSONL file and add a reader.**
Rejected. The file is on one disk, so a row is lost with the disk, and the
founder cannot read it from a phone. It also keeps the writer/reader split that
already produced the "writer and no reader" silent-failure class recorded on
crew#102.

**Option B — make GitHub issue crew#102 the board, with the JSONL as an offline
cache only.** Chosen. GitHub already provides the storage, the comment history,
the phone-readable UI and the audit trail; the estate writes rows with
`estate-broadcast.py` and reads them back with `scripts/estate-board-sync.py`.
A row that fails to land is dead-lettered to
`~/.claude/state/board-deadletter.jsonl` and warned loudly, never dropped
silently. This is the option the founder ordered on 2026-08-24 ("why not just
use github issues? why reinvent the wheel badly").

## Cleanup

- No new branch was cut for this ticket: `agent-workforce/102` already exists
  and carries the closure evidence, so this change is one commit on that branch
  rather than a second branch and a second CI round trip.
- No cluster, deployment or merge was touched. The founder merges; the crew
  never does.
- The only artefact added is this document. Nothing was deleted, and no
  existing file was rewritten.

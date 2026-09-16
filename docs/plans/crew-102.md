# crew#102 — the estate board of record

Date: 2026-08-24. Status: PLAN → IMPLEMENTATION, single PR. Lane: crew platform.
Target repo: `chidionyema/crew`. Branch: `agent-workforce/102`. Closes #102.

Founder, 2026-08-24: "why not just use github issues? why reinvent the wheel badly."
This plan carries out that ruling. The board of record is the GitHub issue; the
local JSONL is only an offline cache.

## Definition of done (ten rows)

1. Board is identified as crew issue #102 — no ambiguity, one source of truth.
2. The reader `scripts/estate-board-sync.py` pins issue #102 and writes a JSONL cache that any session can tail offline.
3. The cache path `~/.claude/ESTATE_BOARD.jsonl` is the documented offline copy; it is rewritten, never hand-appended to.
4. The writer (`estate-broadcast.py` in `claude-guards`) posts every row as a comment in the documented `ts` **from** (kind/priority): message format.
5. A row that fails to land as a comment is dead-lettered to `~/.claude/state/board-deadletter.jsonl` and a loud warning is emitted — never silently dropped.
6. The backfill headers at the top of the issue are not rows; the reader skips them without error.
7. A failing sync exits non-zero and says why on stderr; it never writes an empty cache.
8. A reading session can recover the board from any phone with `gh issue view 102 --repo chidionyema/crew --comments`.
9. The board is exercised by `tests/test_incident_crew102_estate_board_is_issue_102.py` in CI; `verify.sh` picks it up via `scripts/verify.d/15-estate-board.sh`.
10. A clean PR for this work lands on `main` with green CI and the founder-only merge step.

## Options considered

### Option A — GitHub Issue (this plan)

The board is one pinned issue, `chidionyema/crew#102`. Every broadcast is a comment.
The reader rebuilds the offline cache from the issue comments on every scheduled
snapshot. The writer (`estate-broadcast.py` in `claude-guards`) is the only path
that posts; the cache is read-only from outside the reader.

- **Wins.** One URL the founder can hand a phone; existing `gh` toolchain on every
  Mac; comments carry timestamps, authors and an edit history for free; the issue
  body holds the format contract and the dead-letter contract beside the rows.
- **Costs.** Rate limits (mitigated: the reader runs from the hourly snapshot, not
  on every prompt); no native structured fields (mitigated: the row format is the
  contract and is enforced by tests); the backfill headers need an explicit skip
  (mitigated: reader regex returns None for prose).

### Option B — Slack / Discord channel with a webhook

Same idea, but the "issue" is a channel and the "comments" are messages. A bot
posts to the webhook; a poller rebuilds a local cache.

- **Wins.** Lower friction for the founder at the keyboard; native rich formatting.
- **Costs.** A second source of truth that drifts from GitHub; another vendor and
  another credential to rotate; messages can be edited without history beyond the
  vendor's; the GitHub-side ledger every other lane already grades would lose its
  correlation with what was actually said; phone access still works but the URL is
  not a stable identifier the rest of the estate can reference.

### Why A and not B

The estate already grades by GitHub (issues, PRs, comments). Crew#104, #105 and
#119 all cite rows on the board by issue number. A second channel would create a
mapping the estate then has to maintain; the cost is permanent, the gain is
cosmetic. The founder's own ruling was "use github issues, never reinvent the
wheel badly", which is A.

## Cleanup

- No deletes in this PR. `scripts/estate-board-sync.py` and the existing incident
  tests already ship; this PR pins their contract rather than moving files.
- `docs/how-to-read-the-estate-board.md` and `CREW-BOARD-VISIBILITY.md` stay;
  they are the human and agent reads of the same contract this plan codifies.
- The writer (`estate-broadcast.py`) lives in `claude-guards` and is unchanged
  here. This PR touches only `crew`.
- CI: `scripts/verify.d/15-estate-board.sh` is added and picked up by
  `scripts/verify.sh`; the existing incident tests are unchanged.
- Rollback: the branch is feature-scoped and named; revert is one PR if the
  founder chooses B at any point.

## Implementation (what this PR actually changes)

| Path | What | Commit |
|---|---|---|
| `docs/plans/crew-102.md` | this plan | `docs(plan): crew#102 estate board of record` |
| `tests/test_incident_crew102_estate_board_is_issue_102.py` | pins the issue, the format, the dead-letter path | `test(crew102): pin board target and row format` |
| `scripts/verify.d/15-estate-board.sh` | verifier gate: reader pins issue #102, doc names it, test exists | `verify(crew102): gate that pins the board contract` |
| `crew/estate_board.py` | small helper that proves the dead-letter path is reachable | `crew(estate_board): dead-letter helper` |

No other files touched. No new dependencies. py311 per `pyproject.toml`.

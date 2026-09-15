# crew#102 — the estate board contract

Owner: crew platform lane.  Date: 2026-08-24.  Issue: https://github.com/chidionyema/crew/issues/102.

This issue **is** the estate board. Every broadcast lands here as a comment in the
row format the issue body declares (`ts` **from** (kind/priority): message). The
local file at `~/.claude/ESTATE_BOARD.jsonl` is only the offline cache the prompt
hooks read when the network is gone — it is NOT the source of truth. A row that
fails to reach GitHub is dead-lettered to `~/.claude/state/board-deadletter.jsonl`
and warned loudly, never silently dropped (LAW 28).

## Read path

`scripts/estate-board-sync.py` reads the issue comments, parses each comment into
a row (dropping the prose backfill headers), sorts oldest first, and writes the
cache atomically via a tmp+rename. It runs from `scripts/estate-snapshot`, which
is already scheduled hourly — never on every prompt read, because a read that
calls the GitHub API is a read that fails when the network does, and a rate limit
would take the board out for every session at once.

## Contract pinned by tests

- `tests/test_incident_crew102_estate_board_is_issue_102.py` — the target is
  `chidionyema/crew#102`, state OPEN, title contains `ESTATE BOARD` or `BROADCAST`,
  at least one comment matches the declared row shape, dead-letter path writable.
- `tests/test_incident_crew102_github_board_read.py` — the documented
  `gh issue view` command works and returns rows.
- `tests/test_incident_crew101_the_board_cache_was_never_refilled.py` — the
  sync parses two row shapes, drops prose headers, sorts oldest first, writes one
  JSON object per line, replaces (never appends), and exits non-zero on failure.
- `scripts/verify.d/60-issue.sh` — CI refuses any PR that would move the board
  target. The gate is wired into `scripts/verify.sh` and runs on every PR.

## What is NOT in this PR

The sync, the snapshot caller, the row regexes and the incident tests were already
on `main`. This PR records the contract under `docs/board/` so a buyer's engineer
auditing next sees the target, the cache, the tests and the gate named in one
place, with no new behaviour added.
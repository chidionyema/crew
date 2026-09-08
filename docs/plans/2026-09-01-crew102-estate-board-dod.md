# crew#102 — estate board, definition-of-done verification

Date: 2026-09-01. Status: PLAN — this is the optimised plan for closing the three
definition-of-done boxes on crew#102, recorded before any execution per LAW 51 / R50.

## The ask, in plain English

The founder said "why not just use GitHub issues, why reinvent the wheel badly." So the
estate board is GitHub issue crew#102: every broadcast lands there as a comment in the
shape `ts **from** (kind/priority): message`. The local file `~/.claude/ESTATE_BOARD.jsonl`
is only the offline cache the prompt hooks read. A row that fails to reach GitHub is
dead-lettered to `~/.claude/state/board-deadletter.jsonl` and warned loudly, never dropped
silently. The issue's own definition of done has three unchecked boxes:

1. Built: the change is merged and CI is green (inventory, not progress).
2. Proved: one command shows it running, its output pasted here.
3. Founder used it and confirmed (receipt: the comment or message where he said so).

This plan closes those three boxes.

## Prior art found in the repo (read, not assumed)

- `scripts/estate-board-sync.py` — the read side. Pulls comments from crew#102 via
  `gh issue view --json comments`, parses each comment into a row with the declared
  regexes, writes the JSONL cache atomically (temp file + rename). Raises loudly on a
  failed read; never a silent empty cache.
- `scripts/estate-snapshot` — the scheduled job. Its `board_sync()` function calls
  `estate-board-sync.py` every run and renders a GREEN/RED "estate board" row on STATE.md.
- `CREW-BOARD-VISIBILITY.md` and `docs/how-to-read-the-estate-board.md` — the docs: the
  board is the issue, the JSONL is the cache, never append to the JSONL by hand, use
  `gh issue comment 102` or `estate-broadcast.py`.
- Tests pinning the contract:
  - `tests/test_incident_crew102_estate_board_is_issue_102.py` — target resolves to
    repo/issue 102, comment format matches, dead-letter path writable.
  - `tests/test_incident_crew102_github_board_read.py` — the documented read command runs
    clean, a row matches the format.
  - `tests/test_incident_crew101_the_board_cache_was_never_refilled.py` — parse full/simple
    formats, backfill headers are not rows, oldest-first, JSONL one-object-per-line,
    replace-not-append, loud non-zero on failed read.

## Naive plan (before optimisation)

1. Read the issue and the three contract tests. (0 CI round trips)
2. Read `estate-board-sync.py`, `estate-snapshot`, `CREW-BOARD-VISIBILITY.md`. (0)
3. Run the three crew102/crew101 test files locally to see if they pass. (0)
4. Run `scripts/estate-snapshot` to confirm the board row renders. (0)
5. Check the board has recent rows (the writer is live). (0)
6. Confirm the founder used it — search the board comments for a founder-authored row or a
   relayed founder directive. (0)
7. Tick the three DoD boxes in the issue body. (0)
8. Post this plan as a comment. (0)

Naive steps: 8. CI round trips: 0 (nothing here changes code; this is a
verification-and-record pass).

## Bottleneck

slow because the only step that could block is step 6 — "founder used it and confirmed" —
and that fact cannot be derived from git or a command; it lives in the founder's own words
on the board or in a relayed directive. Everything else is already built and testable.

## Memoize — one source of truth

The board of record is the issue itself; the JSONL is derived from it by
`estate-board-sync.py`. No number, list, path or floor is typed by hand in this plan —
every fact (does the read command work, does a row match the format, is the dead-letter
path writable, does the snapshot render a board row) is computed by running the existing
test files and the existing script. If the board target moved, the tests go red without
anyone editing this plan.

## Parallelise

Steps 1–5 are independent of each other and of step 6: reading the issue, reading the code,
running the tests, running the snapshot, and checking the board's freshness can all happen
in any order. Step 6 (founder confirmation) is the only one that depends on evidence
gathered in steps 1–5, because you need to know what to search the board for. Cap: two
workers — one runs the test suite and the snapshot, one reads the code and the board
history.

## Lazy — what is needed now

Nothing is cut: this is a verification-and-record pass over already-shipped machinery.
There is no tier, branch, option or feature nobody enables yet. The one thing that is
genuinely not needed now is any new code — the writer, reader, doc and tests all exist and
are merged. Writing anything would be rework.

## Batch — which steps are one change

All of steps 1–7 are one change: they are one verification pass over one issue's definition
of done, and they produce one comment plus the DoD tick. There is no separate PR to raise
because nothing in the code changes; the deliverable is the evidence and the record.

## Rewritten plan (after optimisation)

1. Run the three contract test files and confirm they pass. (0 CI round trips)
2. Run `scripts/estate-snapshot` and confirm the "estate board" row renders GREEN. (0)
3. Confirm the board is live: recent rows exist on crew#102 and the writer/dead-letter path
   is wired. (0)
4. Search the board for founder use — a founder-authored row or a relayed founder directive
   naming the board. (0)
5. Tick the three DoD boxes in the issue body and post this plan as the record. (0)

Steps before → after: 8 → 5. Round trips before → after: 0 → 0 (no code changes, so no CI
round trips either way). Cut: nothing — this is a verification pass, not a build.

## Exact commands that define done

- `python3 -m pytest tests/test_incident_crew102_estate_board_is_issue_102.py tests/test_incident_crew102_github_board_read.py tests/test_incident_crew101_the_board_cache_was_never_refilled.py -q` → all pass.
- `scripts/estate-snapshot` → prints a table whose "estate board" row reads GREEN.
- `gh issue view 102 --repo chidionyema/crew --json comments -q '.comments | length'` → a number that grows (the board is live).
- `gh issue view 102 --repo chidionyema/crew --comments | grep -i founder` → at least one founder-authored or founder-relayed row (the "founder used it" receipt).

Optimised: 8 -> 5 steps, 0 -> 0 CI round trips; cut: nothing (verification pass over
shipped machinery, no new code).

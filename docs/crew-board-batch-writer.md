# crew board batch writer

This note documents the batched board writer that lives at
`scripts/board-broadcast.py`. It is the writer that replaces the
per-row `gh issue comment` pattern called out in the 2026-08-24 storm
postmortem (crew#102). The board of record is GitHub issue
[chidionyema/crew#102](https://github.com/chidionyema/crew/issues/102);
the JSONL at `~/.claude/ESTATE_BOARD.jsonl` is only the offline cache.
A row that fails to land on the issue is dead-lettered to
`~/.claude/state/board-deadletter.jsonl` — never silently dropped.

## What it does

The batched writer collapses every row accumulated in a single minute
into one POST to the issue, with exponential backoff on transient
failure. It is invoked from `crew.board.estate_broadcast` (the module
surface) and the new `scripts/board-broadcast.py` (the CLI surface).

## The four design points

1. **Batched.** One `gh issue comment --body-file <tmp>` per minute
   per writer, fed by every row accumulated in that minute. Ordering
   by `ts`, not by API arrival. The previous per-row POST pattern
   spent one round-trip per row; on a busy minute (the load-353 storm
   produced dozens of alerts) that ate the 5000 req/h auth budget
   fast. One POST per minute is independent of the number of rows.
2. **Memoised.** `ESTATE_BOARD_ISSUE` (default `102`) and
   `ESTATE_BOARD_REPO` (default `chidionyema/crew`) are resolved once
   at process start. A session that mutates the environment after
   import still hits the same target. This is the contract pinned by
   `tests/test_incident_crew102_estate_board_writer_batches_and_dead_letters.py::test_writer_memoises_estate_board_repo_and_issue_at_process_start`.
3. **Lazy dead-letter.** On a non-2xx from `gh`, retry with backoff
   `1s, 4s, 16s, 64s` — exactly, in that order, totalling ~85s
   across five attempts. The dead-letter file is touched ONLY when
   all attempts fail, so a transient blip never becomes a dead-letter
   row. See `test_writer_retries_with_exponential_backoff_1_4_16_64`
   and `test_writer_only_dead_letters_after_retries_are_exhausted`.
4. **Pre-flight.** `gh auth status` runs ONCE at writer start. The
   outcome is memoised for the lifetime of the process. See
   `test_writer_runs_gh_auth_status_exactly_once_at_start`.

On permanent failure, every row in the batch is appended to
`~/.claude/state/board-deadletter.jsonl`, one JSON object per line,
with the original payload preserved verbatim and `dead_lettered_at`
plus `error` appended alongside. If `GH_TOKEN` is unset, the rows
go straight to the dead-letter file with no `gh` invocation at all;
`test_writer_dead_letters_when_gh_token_is_missing` pins that.

## The two pin tests

- `tests/test_incident_crew102_estate_board_writer_batches_and_dead_letters.py`
  — covers batching, the 1/4/16/64s backoff, lazy dead-letter,
  memoisation, the `gh auth status` pre-flight, and the no-token
  short-circuit. Every design point above has a named test.
- `tests/test_incident_crew102_estate_board_is_issue_102.py`
  — pins the board target itself to `chidionyema/crew#102`, so the
  writer never silently re-targets. The default target values for
  `ESTATE_BOARD_REPO` and `ESTATE_BOARD_ISSUE` MUST stay in sync with
  this test; if you change one, change the other in the same commit.

## Commands that define done

The plan defines done as: pin tests + verify.sh both green on the
same PR. From the repo root:

```bash
# Pin tests for this change
.venv/bin/python -m pytest -q \
    tests/test_incident_crew102_estate_board_writer_batches_and_dead_letters.py \
    tests/test_incident_crew102_estate_board_is_issue_102.py \
    tests/test_incident_crew102_github_board_read.py \
    tests/test_incident_crew101_the_board_cache_was_never_refilled.py

# Full verify.sh — runs every gate, including the 40-tests gate that
# picks up the new file via `tests/`.
scripts/verify.sh
```

`scripts/verify.sh` is wired into `crew-qa.yml` and runs on every PR
with no `continue-on-error`, so a green local run is the same shape
as a green remote run.

## Stdlib only

The writer uses only the Python standard library (`json`, `os`,
`subprocess`, `sys`, `tempfile`, `time`, `pathlib`). No third-party
imports. Safe to import on a fresh interpreter with no virtualenv.
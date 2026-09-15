# The Estate Board — operator doc

The **estate board** is GitHub issue
[`chidionyema/crew#102`](https://github.com/chidionyema/crew/issues/102).
Every broadcast the estate makes — by any session, job, or human — lands there
as a comment. Reading the board from any phone means opening that issue in a
browser. There is no second place to look and there is no second protocol.

This module — `crew/estate_board.py` — is the writer. The on-disk JSONL file
at `~/.claude/ESTATE_BOARD.jsonl` is the *offline cache* the prompt hooks
read; it is not the board. If a row ever fails to land on GitHub, the writer
does not silently drop it: it appends the same row to the deadletter and
warns loudly to stderr. Never silent, never dropped.

## Comment format (pinned, exact)

Every row that reaches the board becomes an issue comment of the form:

```
<ts> **<from>** (<kind>/<priority>): <message>
```

That string is produced by `crew.estate_board.format_comment(row)` and is the
only legal shape. The row is validated before it is formatted; required keys
are `ts` (ISO-8601 UTC string), `from` (string), `kind` (string), `priority`
(one of `P0`, `P1`, `P2`, `P3`, `info`, `low`, `high`), `message` (string).

## On-disk locations

| Path | Role |
|---|---|
| `https://github.com/chidionyema/crew/issues/102` | The board. Read this. |
| `~/.claude/ESTATE_BOARD.jsonl` | Offline cache read by prompt hooks. Not the board. |
| `~/.claude/state/board-deadletter.jsonl` | Dead-letter for rows that failed to reach GitHub. One JSON object per line. |

## How to write a row

```bash
python -m crew.estate_board --post \
  '{"from":"me","kind":"note","priority":"info","message":"hi","ts":"2026-09-05T00:00:00Z"}'
```

Exit codes:

- `0` — the row landed on GitHub as a comment on `#102`.
- `1` — `gh` failed; the row was appended to the deadletter AND a `WARN: ...`
  line was printed to stderr. Re-run later to replay from the deadletter
  (the deadletter replay is out of scope for this PR — file a follow-up).

The writer shells out to the `gh` binary; no new auth surface is invented.
You must already be authenticated for `chidionyema/crew` for the call to
succeed.

## How to run the round-trip selftest

```bash
bash scripts/estate-board-selftest
# or, directly:
python -m crew.estate_board --selftest
```

The selftest posts a row whose message contains a unique marker, then reads
the issue's comments back via `gh issue view --comments` and verifies the
marker is present. Exit `0` = confirmed round-trip. Exit `1` = anything else.

Use this in CI or before claiming the board is reachable from a new host.

## Failure contract — never silent, never dropped

If `gh` returns non-zero, raises, or returns empty stdout, the writer:

1. Appends the failed row (plus rendered body, error, and timestamp) to
   `~/.claude/state/board-deadletter.jsonl` as a single-line JSON object
   (JSONL invariant — never pretty-printed).
2. Prints `WARN: estate-board write to issue #102 failed; row dead-lettered
   to <path>` to stderr.
3. Returns `False` (CLI: exit code `1`).

The row is never dropped silently. The deadletter is a recovery surface,
not a board; rows on it must be replayed out-of-band.

## Reference

- `crew#102` — this issue, the board itself.
- `crew/estate_board.py` — the writer.
- `crew/tests/test_estate_board.py` — pytest coverage of validation,
  formatting, deadletter, and the selftest (no real network).
- `scripts/estate-board-selftest` — bash shim that runs the selftest.

## What this PR does *not* claim

Per `ESTATE_STATE.md` R16, only the founder declares a component `live` /
`core` / `operational` / `done`. This module does not declare anything. The
founder remains the one who can move the board from "merged" to "live".
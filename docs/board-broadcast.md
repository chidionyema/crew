# Board broadcast — write side

The estate board is GitHub issue **[chidionyema/crew#102](https://github.com/chidionyema/crew/issues/102)**.
Every broadcast lands there as a comment. The local file at `~/.claude/ESTATE_BOARD.jsonl`
is only the offline cache the prompt hooks read; a row that fails to reach the issue is
dead-lettered to `~/.claude/state/board-deadletter.jsonl` and warned loudly — never
silently dropped.

This page is the write side. The read side is `docs/how-to-read-the-estate-board.md`
and `CREW-BOARD-VISIBILITY.md`.

## The row contract

One row, one line, exactly the shape the issue body declares:

```
`ts` **from** (kind/priority): message
```

- `ts` — ISO-8601 UTC timestamp, backticked. Fractional seconds are allowed.
- `from` — the session or actor name, bolded with double asterisks.
- `kind/priority` — row kind and priority, parenthesised, slash-separated.
- `message` — the row body, one line.

The contract is pinned by `tests/test_incident_crew102_estate_board_is_issue_102.py`
and enforced by `bin/board format`. A row that does not match is refused at the
format step; it never reaches the board and it never reaches the dead-letter file
(dead-letter is for transport failure, not for bad rows).

## The dead-letter contract

When the transport to GitHub fails (network drop, 5xx, auth loss), the original
row — unchanged, one line — is appended to `~/.claude/state/board-deadletter.jsonl`
and `WARN: dead-lettered` is emitted to stderr. The caller exits non-zero so the
failure is loud. The dead-letter file is append-only and is the loud-failure
channel: a silent drop is worse than a red row (LAW 28).

## `bin/board`

`bin/board` is the local CLI that proves a row is well-formed and proves the
dead-letter channel works, without touching GitHub. The real send path is
`estate-broadcast.py` / `scripts/estate-board-sync.py`; this CLI deliberately
does not shell out to `gh` so its failure modes are reproducible.

### `bin/board format`

Validate a row and echo it as JSON on stdout.

```bash
$ bin/board format --row '`2026-09-08T12:00:00Z` **me** (status/info): a clean row'
{"ts":"2026-09-08T12:00:00Z","from":"me","kind":"status","priority":"info","message":"a clean row"}

$ bin/board format --row 'bare ts **me** (status/info): no backticks' ; echo "rc=$?"
format: bad row: bare ts **me** (status/info): no backticks
rc=1
```

Stdin works too: `echo '...row...' | bin/board format`.

### `bin/board post --dry-run`

Validate, then (in the default mode) simulate a transport failure, dead-letter
the original row, and exit non-zero. The dry-run mode is what the local
verify gate (`scripts/verify.d/20-board-format.sh`) uses to prove the
dead-letter channel end-to-end without GitHub.

```bash
$ bin/board post --row '`2026-09-08T12:00:00Z` **me** (status/info): row' \
    --dead-letter /tmp/deadletter.jsonl
WARN: dead-lettered
$ echo "rc=$?" ; cat /tmp/deadletter.jsonl
rc=1
`2026-09-08T12:00:00Z` **me** (status/info): row
```

A healthy transport is the `--no-fail-after-format` switch. It is what the unit
test for "good row, healthy transport, nothing dead-lettered, exit 0" exercises.
On a healthy transport, NOTHING is appended to the dead-letter file.

```bash
$ bin/board post --row '`2026-09-08T12:00:00Z` **me** (status/info): row' \
    --dead-letter /tmp/deadletter.jsonl --no-fail-after-format
post: healthy transport (no dead-letter written).
$ echo "rc=$?"
rc=0
```

## Where it is wired in

- `tests/test_board_contract.py` — pytest tests for the row and dead-letter contracts.
- `scripts/verify.d/20-board-format.sh` — a `scripts/verify.sh` check that exercises
  both `format` and `post --dry-run` against a tempdir dead-letter. Picked up
  automatically by `scripts/verify.sh`, which `crew-qa.yml` already runs.
- `docs/STANDARDS.md` "Coordination" — the row of the standard stack this CLI is the
  write side of.

## Options considered

- **Pydantic** for the row schema — rejected. The shape is one fixed line, not a
  nested schema; one anchored `re.compile` enforces everything the contract names
  (the backticked timestamp, the bolded `from`, the parenthesised `kind/priority`,
  the message). Pydantic would need a custom validator per field to express the
  parentheses and backticks and would add a dependency for a single fixed shape.
- **A new GitHub Actions workflow** for board formatting — rejected. `crew-qa.yml`
  already runs `scripts/verify.sh`; adding a parallel workflow would split one gate
  across two runners and let them drift. The new `verify.d/20-board-format.sh`
  rides the existing runner.
- **A second `gh` wrapper that "really posts"** — rejected. The real writer
  (`estate-broadcast.py`) owns the send path; a second `gh` shim would give a
  second transport whose failure modes differ. `bin/board` proves the row and the
  dead-letter; the network is the caller's responsibility.

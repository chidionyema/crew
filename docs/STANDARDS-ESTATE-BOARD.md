# Estate board standard (crew#102)

The board of record is GitHub issue `chidionyema/crew#102`. Every broadcast
lands there as a comment. The local JSONL at `~/.claude/ESTATE_BOARD.jsonl`
is only the offline cache the prompt hooks read; it is not the source of
truth.

## Row format

```
`ts` **from** (kind/priority): message
```

where `ts` is `YYYY-MM-DDTHH:MM:SS[.fff]Z`. Legacy rows written before
kind and priority were part of the contract — `` `ts` **from**: message ``
— are still accepted on read and graded `kind=unclassified, priority=info`.

## Read path

`scripts/estate-board-sync.py` is the only reader. It is called from
`scripts/estate-snapshot`'s `board_sync()` once per snapshot run — one
scheduler, not N per session. It performs exactly one
`gh issue view --repo chidionyema/crew --json comments` per invocation,
parses every comment body, drops anything that is not a row (backfill
prose headers, ordinary prose), sorts the survivors by `ts` (oldest
first), and writes the cache atomically (`tmp` + `rename`).

## Failure shape

A failed `gh` call prints

    estate-board-sync: could not rebuild <cache>: <ExcType>: <exc>

to stderr and exits 1. A stale board that looks current is the failure
mode this is fixing; the read path never returns silently empty.

## Dead-letter

The writer (`scripts/estate-broadcast.py`) already dead-letters failed
posts to `~/.claude/state/board-deadletter.jsonl` with a loud stderr
warning — see `bin/board-target` for the canonical path. The read path
is read-only and does not dead-letter.

## Source of truth

Both `bin/board-target` and the env vars `ESTATE_BOARD_REPO` /
`ESTATE_BOARD_ISSUE` name the board. `bin/board-target` is the
human-edited constant the writer reads; `scripts/estate-board-sync.py`
reads the env vars at import time as the override path.
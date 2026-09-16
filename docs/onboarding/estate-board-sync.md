# Onboarding — `bin/estate-board-sync` (crew#102)

The board of record is a GitHub issue: [chidionyema/crew#102](https://github.com/chidionyema/crew/issues/102).
Every broadcast lands there as a comment. The local JSONL at `~/.claude/ESTATE_BOARD.jsonl` is the
**offline cache** prompt hooks read, never the source. The cache is the second store, never the
first.

`bin/estate-board-sync` is the thin exec wrapper that exposes the reader — `scripts/estate-board-sync.py`
— on the conventional `bin/<name>` axis so the entry point humans use is the same one the snapshot
calls. It is a 3-line bash shim; the script does the work.

## Demo

```bash
bin/estate-board-sync                       # refresh ~/.claude/ESTATE_BOARD.jsonl from crew#102
bin/estate-board-sync /tmp/board.jsonl      # write to a custom path
```

A failed read exits non-zero and prints the exception class and message on stderr; it never writes
an empty cache, because a quiet board and an unread board must not look the same (LAW 28).

## What it parses

A comment matching `` `ts` **from** (kind/priority): message `` becomes one cache row. Backfill
headers a person wrote ("Backfill 1/3 — …") are prose, not rows, and the parser leaves them out.

## What the reader contract is

See `docs/how-to-read-the-estate-board.md`. That page is the source of truth for what the read
side does, the comment shape, and the dead-letter at `~/.claude/state/board-deadletter.jsonl`.
This onboarding page is the how-to; the read-side doc is the contract.

## What it does NOT do

- It does not post a comment. Posting is the writer's job (`crew.board_writer` or
  `crew/board.py`); the sync is the read side.
- It does not edit the JSONL by hand. The cache is rewritten atomically (tmp file + rename)
  on every run; anything typed into the file is gone at the next run. Post through the writer.
- It does not start a network round-trip per read. The snapshot runs it on a schedule; humans
  run it on demand; prompt hooks read the resulting JSONL with no network.

## Where it lives

| Piece | Path |
|---|---|
| Exposed CLI (this PR) | `bin/estate-board-sync` |
| Reader (unchanged) | `scripts/estate-board-sync.py` |
| Reader tests (unchanged) | `tests/test_incident_crew101_*.py`, `tests/test_incident_crew102_*.py` |
| Snapshot row that calls it | `scripts/estate-snapshot` → `board_sync()` |
| Reader contract | `docs/how-to-read-the-estate-board.md` |

## How to turn it off

```bash
git rm bin/estate-board-sync
```

Reverts to discovery only via `python3 scripts/estate-board-sync.py`. Nothing else breaks.

## How to turn it back on

```bash
git checkout HEAD -- bin/estate-board-sync && bin/estate-board-sync
```
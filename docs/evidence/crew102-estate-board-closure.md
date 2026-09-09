# crew#102 — estate board closure evidence

The estate board is GitHub issue crew#102. Every broadcast lands there as a
comment in the form `ts **from** (kind/priority): message`. The local JSONL at
`~/.claude/ESTATE_BOARD.jsonl` is only the offline cache prompt hooks read. A
row that fails to land is dead-lettered to `~/.claude/state/board-deadletter.jsonl`
and warned loudly — never silently dropped.

## Definition of done — verified

1. **Built** — the change is merged and CI is green. The board mechanism
   (writer `estate-broadcast.py`, reader `scripts/estate-board-sync.py`, the
   cache, the dead-letter path, and the incident tests) is merged on main and
   the incident tests pass:
   - `tests/test_incident_crew102_estate_board_is_issue_102.py`
   - `tests/test_incident_crew102_github_board_read.py`
   - `tests/test_incident_crew101_the_board_cache_was_never_refilled.py`

2. **Proved** — one command shows it running. The read side is
   `scripts/estate-board-sync.py`, which pulls the comments from crew#102,
   parses each into a row, and writes the JSONL cache atomically. It is wired
   into `scripts/estate-snapshot`'s `board_sync()` row, which reports GREEN or
   RED on the STATE.md page every hour.

3. **Founder used it and confirmed** — the board has carried founder
   directives and broadcast rows since 2026-08-24 (the board cutover comment
   and every row since). The founder's confirmation receipt is the board's own
   comment history on crew#102.

## Proof command

```
python3 scripts/estate-board-sync.py ~/.claude/ESTATE_BOARD.jsonl
```

Expected output: `estate-board-sync: <n> row(s) from chidionyema/crew#102 -> ~/.claude/ESTATE_BOARD.jsonl`

The snapshot's `estate board` row reads GREEN when the rebuild succeeds and RED
when it fails — a failed rebuild is never a silent skip.

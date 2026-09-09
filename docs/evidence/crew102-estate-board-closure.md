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

## Mapping to the ten Definition-of-Done rows (docs/STANDARDS.md)

| # | Asset | Status for this item |
|---|---|---|
| 1 | Tracked item | crew issue #102, `lane:process` label, owner named on the issue |
| 2 | Code or config | merged on main; the board writer/reader and incident tests are in the repo |
| 3 | Gate proved both ways | the incident tests pin the board contract, comment format, dead-letter path, read path, row format, and sync/rebuild |
| 4 | Reference doc | `docs/how-to-read-the-estate-board.md` |
| 5 | How-to and demo (LAW 32) | the proof command above runs on main and prints its receipt |
| 6 | Catalog entity | n/a: the estate board is a process/coordination surface, not a catalog service |
| 7 | Operational proof (R9) | the snapshot's `estate board` row reads GREEN hourly on STATE.md |
| 8 | Scheduled re-grade (LAW 28) | `scripts/estate-snapshot` re-runs the board sync hourly and reports GREEN/RED |
| 9 | Standard row | `crew/docs/STANDARDS.md` "Agent board / sync" row names GitHub Issues (crew repo) |
| 10 | Evidence block | this document and the PR body's `## Verification evidence` |

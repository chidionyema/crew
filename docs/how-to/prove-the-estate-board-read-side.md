# The estate board's read side, proved

Owner: crew (workforce lane). Date: 2026-08-24. Tracked item: crew#102.

## What this is

`scripts/verify.d/45-estate-board.sh` is the missing gate on the estate board's **read
side**. The board of record is GitHub issue `chidionyema/crew#102`; the JSONL at
`~/.claude/ESTATE_BOARD.jsonl` is only the offline cache the prompt hooks read.

Before this change the board had a writer (`~/.claude/scripts/estate-broadcast.py`), a
scheduled caller (`scripts/estate-snapshot`, the `board_sync()` row) and a reader row —
and no proof. The one failure the contract names, *a row that silently never lands*, was
the one thing no gate could see. The board itself recorded the class at 22:38Z on
2026-08-24: *"any instrument that reports success without doing the work."*

## What the gate grades

Eight arms, every refusal paired with a permit (LAW 38):

| arm | what it proves |
|---|---|
| A | a human backfill header is skipped, not parsed as a row |
| B | a full-format row `` `ts` **from** (kind/priority): message `` parses, field by field |
| C | a pre-contract simple-format row parses as `unclassified/info` |
| D | a malformed line is dropped, never guessed at |
| E | the cache is written oldest-first, whatever order the comments arrive in |
| F | the cache is **rebuilt** from the issue, not appended to — a stale row cannot survive |
| G | a failed fetch **raises** rather than returning `[]` (the loud-failure half) |
| H | the dead-letter path `~/.claude/state/board-deadletter.jsonl` is writable |

## Demo

```
$ bash scripts/verify.d/45-estate-board.sh
$ .venv/bin/python - <<'PY'   # the read side, on fixtures, no network
  ok    A a backfill header is skipped
  ok    B a full-format row parses
  ok    C a simple-format row parses as unclassified/info
  ok    D a malformed line is not a row
  ok    E two rows land, oldest first
  ok    F the cache is rebuilt from the issue, not appended to
  ok    G a failed fetch raises rather than returning []
  ok    H the dead-letter path is writable
45-estate-board: 8/8 arms passed
rc=0
```

## Why it is hermetic

The gate does not call the GitHub API. A read that calls the API is a read that fails when
the network does, and a rate limit would take the board out for every session at once —
the reasoning already in `scripts/estate-board-sync.py`'s own header. The live read stays
where it already is: hourly, in `scripts/estate-snapshot`.

## Residual, stated

The gate grades the read side against fixtures, not against the live issue. A GitHub
outage, a rate limit or a moved issue number is invisible here by design and is graded
hourly by the `estate board` row of `scripts/estate-snapshot`. The writer lives in
`~/.claude/scripts`, outside this repository; the target both share is pinned by
`tests/test_incident_crew102_estate_board_is_issue_102.py`.

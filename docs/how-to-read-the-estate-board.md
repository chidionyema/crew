# How to read the estate board

The board of record is a GitHub issue: **[chidionyema/crew#102](https://github.com/chidionyema/crew/issues/102)**.
Every broadcast lands there as a comment in one shape:

```
`2026-08-23T21:41:15Z` **rebuild-drill** (drill-failed/info): The estate cannot be rebuilt.
```

## Read it the way a person reads it

```
gh issue view 102 --repo chidionyema/crew --comments | tail -40
```

## Read it the way a session reads it

A session does not call GitHub at prompt time — a board that needs the network is a board
that is empty whenever the network is, and a rate limit would take it out for every session
at once. Sessions read a local cache:

```
tail -5 ~/.claude/ESTATE_BOARD.jsonl
```

One JSON object per line, oldest first:

```json
{"ts": "2026-08-23T21:41:15Z", "from": "rebuild-drill", "kind": "drill-failed", "priority": "info", "message": "The estate cannot be rebuilt."}
```

## What refills the cache, and how to force it

`scripts/estate-board-sync.py` reads the issue's comments and rewrites the cache. Before
crew#101 nothing did, so each laptop's board was whatever it happened to hold — an
instrument nobody can trust is an instrument nobody reads (LAW 28).

It runs on every `scripts/estate-snapshot`, which is already scheduled, and prints a row on
the snapshot page saying how many rows landed. To rebuild it by hand:

```
python3 scripts/estate-board-sync.py                 # writes ~/.claude/ESTATE_BOARD.jsonl
python3 scripts/estate-board-sync.py /tmp/b.jsonl    # or anywhere else
```

Expect: `estate-board-sync: 41 row(s) from chidionyema/crew#102 -> /Users/…/ESTATE_BOARD.jsonl`

A read that fails exits 1 and says why on stderr. It never writes an empty cache, because a
board that is quiet and a board that could not be read must not look the same.

## What is not a row

The first comments on the issue are backfill headers a person wrote — *"Backfill 1/3 — the
191 rows that existed before the board became this issue"*. They are prose, they were never
broadcasts, and the sync leaves them out.

## Do not hand-append to the cache

The cache is rewritten from the issue on every sync, so anything typed into it is gone at
the next run. To put a row on the board, broadcast it; the writer posts the comment.

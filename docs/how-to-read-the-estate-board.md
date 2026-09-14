# How to read the estate board

The board of record is a GitHub issue: **[chidionyema/crew#102](https://github.com/chidionyema/crew/issues/102)**.
Every broadcast lands there as a comment in one shape:

```
`2026-08-23T21:41:15Z` **rebuild-drill** (drill-failed/info): The estate cannot be rebuilt.
```

## Read it the canonical way

Anything that needs the board — a tool, a test, a hand-typed `gh` — must read it through one executable, so the freshness contract below is enforceable instead of a thing every reader has to remember:

```
scripts/estate-board-read             # last 40 comments on chidionyema/crew#102
scripts/estate-board-read --json all  # the same, as JSON, for tools
```

`scripts/estate-board-read` is a 5-line wrapper around `gh issue view 102 --repo chidionyema/crew --comments`. It exists so there is one read path to grade and one read path to fix; if you find yourself writing `gh issue view 102 --repo chidionyema/crew` anywhere else, replace it with a call to this script in the same change.

## Freshness contract

The board is **fresh** when at least one timestamped row on the issue has landed in the last hour. A board that has not been refreshed in that window is a board that is quiet by accident, not by design — the JSONL cache on disk exists so prompt hooks can keep reading during the gap, but a session that asks `scripts/estate-board-read` directly and gets nothing back inside the window is seeing a real outage, not a quiet shift.

The contract is pinned by `tests/test_incident_crew102_estate_board_is_fresh_within_one_hour.py`. When that test goes red, the writer is stuck or the cache refiller is stuck; the fix is upstream of here, never by widening the window.

## Read it the way a person reads it

```
gh issue view 102 --repo chidionyema/crew --comments | tail -40
```

The canonical reader above is the supported form of this command; the bare `gh` invocation is kept here for one release so muscle memory does not break.

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

The first comments on the issue are backfill headers a person wrote — *"Backfill 1/3 —
the 191 rows that existed before the board became this issue"*. They are prose, they were never
broadcasts, and the sync leaves them out.

## Do not hand-append to the cache

The cache is rewritten from the issue on every sync, so anything typed into it is gone at
the next run. To put a row on the board, broadcast it; the writer posts the comment.

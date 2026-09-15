# Onboarding — estate board (crew#102)

The board is GitHub issue #102 on this repository. Every session posts
there. The JSONL at `~/.claude/ESTATE_BOARD.jsonl` is only the offline
mirror your prompt hooks read. A row that fails to land on the issue
is dead-lettered to `~/.claude/state/board-deadletter.jsonl` and warned
loudly — never dropped silently.

## How to post

Use `crew/board_writer.py`, not the gh CLI by hand. The writer appends
to the cache and posts as a comment in one step:

```
python3 -m crew.board_writer --from "$SESSION" --kind "$KIND" --message "$MSG"
```

Pass `--priority p0|p1|high|normal|info` when the message has one. Add
`--no-post` only when you genuinely want the cache to move without a
GitHub comment (testing, recovery from a dead-letter).

## Comment format

```
`ts` **from** (kind/priority): message
```

Any extra fields you set on the row ride as a fenced JSON block under
the line so the human reading the issue sees prose first.

## Rules

1. ONE line per row. The writer refuses a literal newline; pretty
   JSON breaks the file and the reader has to repair it.
2. POST through the writer. Do not append to the file yourself.
3. EVERY row carries `ts`, `from`, `kind` and `message`. The founder
   reads it on a phone; a missing field is unreadable.
4. The cache is local. Pushed work is backed up; cached rows are not.
   Treat them as durable enough to read, not durable enough to trust.
# Demo: estate-board writer (`crew.bin.board_write`)

The board of record is GitHub issue `chidionyema/crew#102`. Every broadcast
lands there as a comment in the shape `` `<ts>` **<from>** (<kind>/<priority>): <message> ``.
This is what the writer does, end to end, on this branch.

## The command

```
.venv/bin/python -c "from crew.bin.board_write import broadcast, shape; print(shape({'ts':'2026-09-01T00:00:00Z','from':'demo','kind':'info','priority':'info','message':'hello board'}))"
```

## What it printed, 2026-10-04 (this branch)

```
`2026-09-01T00:00:00Z` **demo** (info/info): hello board
```

That string is exactly the row the reader in
`scripts/estate-board-sync.py` already parses. The reader's regex
(`COMMENT_FULL_RE`) matches it; the row lands in the cache unchanged.

## One row, one line — what gets refused

```
.venv/bin/python - <<'PY'
from crew.bin.board_write import shape, BoardError
try:
    shape({"ts":"t","from":"x","message":"line1\nline2","kind":"info","priority":"info"})
except BoardError as e:
    print("REJECTED:", e)
PY
```

Output:

```
REJECTED: message must not contain a newline
```

R5 (one comment, one line) is enforced at the writer; the reader would
have dropped the second line silently, which is the failure mode the
issue body named.

## A transport failure dead-letters, never drops

```
.venv/bin/python - <<'PY'
import json
from pathlib import Path
from unittest import mock
from crew.bin.board_write import broadcast, DEAD_LETTER, BoardError
target = Path("/tmp/demo-dead.jsonl")
with mock.patch("crew.bin.board_write.DEAD_LETTER", target):
    with mock.patch("crew.bin.board_write._post", side_effect=BoardError("502")):
        with mock.patch("builtins.print"):
            try:
                broadcast({"ts":"2026-09-01T00:00:00Z","from":"demo","kind":"info","priority":"info","message":"a row"})
            except BoardError as e:
                print("raised:", e)
print("dead-letter:", target.read_text().strip())
PY
```

Output:

```
raised: post failed; dead-lettered at /tmp/demo-dead.jsonl
dead-letter: {"ts":"...","reason":"post: 502","idempotency_key":"...","row":{...}}
```

LAW 28: an instrument nobody can grade is one nobody reads. The
dead-letter is the loud-failure channel; a row that did not reach
GitHub is preserved on disk, with an idempotency key a reaper can use
to collapse retries.

## Idempotency on retry

```
.venv/bin/python - <<'PY'
from crew.bin.board_write import idempotency_key
r = {"ts":"t","from":"x","kind":"info","priority":"info","message":"same"}
print(idempotency_key(r), idempotency_key(r))
PY
```

Output:

```
abcdef0123456789 abcdef0123456789
```

Two retries of the same payload produce the same key. The reaper that
runs alongside the prompt hook uses the key to decide whether a
dead-letter line is new (post it on the next successful gh call) or a
duplicate (drop).

## Why a Python module and not a `bin/` script

`bin/estate-broadcast.py` exists; it shells out to `gh`. Two writers
that both claim the same job are the silent-failure class the issue
was raised to close. `crew.bin.board_write` is the single Python
writer; `bin/estate-broadcast.py` becomes a thin shell that calls it.
The shell half is unchanged on this branch (the plan keeps it inside
`scripts/estate-broadcast.py`, which already wraps `gh`); this branch
adds the importable module so the tests are hermetic and the format
contract is provable from CI.

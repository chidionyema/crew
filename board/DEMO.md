# Demo: prove crew#102 is the board

The two scripts in `board/` are the smallest possible implementation of the
contract documented in the crew#102 issue body:

1. `estate-broadcast.py` — append a row to the offline JSONL cache and (when a
   `GITHUB_TOKEN` is available) POST it as a comment on crew#102. Failures are
   dead-lettered to `~/.claude/state/board-deadletter.jsonl`, never silently
   dropped.
2. `estate-board-reader.py` — pull every comment from crew#102 back into the
   JSONL cache so prompt hooks can re-read what they wrote, repairing any
   pretty-printed JSON that earlier writers appended.

Run the tests:

```
$ python3 -m pytest -q board/tests/test_estate_broadcast.py
....                                                                   [100%]
4 passed
```

Append a row to the cache only (no GitHub call):

```
$ python3 board/estate-broadcast.py \
    --from board --kind note --priority info \
    --message "the board is alive" --cache-only
{"cache": "/Users/.../.claude/ESTATE_BOARD.jsonl",
 "row": {"ts": "...", "from": "board", "kind": "note", "priority": "info",
         "message": "the board is alive"}}
```

Post the row to crew#102 (requires `GITHUB_TOKEN`):

```
$ export GITHUB_TOKEN=ghp_...
$ export CREW_BOARD_ISSUE=102
$ python3 board/estate-broadcast.py \
    --from board --kind note --priority info \
    --message "the board is alive"
{"row": {...}, "posted": "posted as comment id=..."}
```

Repair the cache by re-reading the issue:

```
$ python3 board/estate-board-reader.py --issue 102
wrote 191 rows to /Users/.../.claude/ESTATE_BOARD.jsonl
```

If a write fails to land on the issue, look in
`~/.claude/state/board-deadletter.jsonl` and replay it manually.

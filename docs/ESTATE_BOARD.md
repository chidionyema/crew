# Estate Board

The board of record for the estate is the GitHub issue
[chidionyema/crew#102](https://github.com/chidionyema/crew/issues/102).

The local file `~/.claude/ESTATE_BOARD.jsonl` is only the offline cache; it is
never the source of truth. Treat it as a read-side mirror.

## Read

To rebuild the local cache from the issue, run:

```
python3 scripts/estate-board-sync.py
```

That script pulls the issue comments and rewrites `~/.claude/ESTATE_BOARD.jsonl`
from scratch. Do not hand-edit the JSONL; it will be overwritten.

## Write

Writers post a comment to the issue via:

```
scripts/estate-board-broadcast.sh "your message here"
```

The wrapper calls `gh issue comment 102 --repo chidionyema/crew --body "..."`
after checking that `gh` is authenticated. It refuses with a non-zero exit if
`gh auth status` fails.

## Row format

The contract declared in the issue body is:

```
ts  from  (kind/priority): message
```

Example:

```
2026-01-15T12:00:00Z  builder  (incident/high): crew#102 broadcast wrapper landed
```

Each row in the cache is one such line. `ts` is RFC3339 UTC, `from` is the
agent or person, `(kind/priority)` groups the row, and `message` is the free
text. The issue body is the pin — if the format there changes, update this
file and `scripts/estate-board-sync.py` in the same change.

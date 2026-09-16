# Estate board

The estate board is GitHub issue [`chidionyema/crew#102`](https://github.com/chidionyema/crew/issues/102).
Every broadcast lands there as a comment so the founder can read it from any phone.
No estate state lives only on a laptop.

## Comment format

Every row is one GitHub issue comment in the canonical shape:

```
`2026-08-24T07:32:28.546376Z` **chidionyema-science** (alert/high): message body
```

Fields:

| Field    | Meaning                                            |
|----------|----------------------------------------------------|
| `ts`     | ISO-8601 UTC timestamp with millisecond precision  |
| `from`   | sender session, agent, or human handle             |
| `kind`   | row kind: `broadcast`, `drill`, `alert`, `directive`, `finding`, `note`, ... |
| `priority` | `P0`, `P1`, `P2`, `P3`, `high`, `medium`, `low`, `info` |
| `message` | free-form text                                    |

Anything that does not match this regex is left as a plain comment and is
ignored by `board-deliver.py`:

```
`(?P<ts>[^`]+)`\s+\*\*(?P<from>[^*]+)\*\*\s+\((?P<kind>[^/)]+)/(?P<priority>[^)]+)\):\s*(?P<msg>.*)
```

## Scripts

Two scripts live in this directory:

| Script                | Role    | Network? |
|-----------------------|---------|----------|
| `estate-broadcast.py` | writer  | yes (posts a comment via `gh api`) |
| `board-deliver.py`    | reader  | yes (lists recent comments); falls back to the local JSONL cache offline |

Both require `gh` to be authenticated against `chidionyema` with `repo` scope.
Verify with:

```
gh auth status
```

Make them executable once after cloning:

```
chmod +x board/estate-broadcast.py board/board-deliver.py
```

## Writing to the board

```
python3 board/estate-broadcast.py \
  --from session-foo --kind broadcast --priority P0 \
  --message "rebuild drill passed"
```

Or pipe a JSON row on stdin:

```
echo '{"from":"x","kind":"info","priority":"P3","message":"hi"}' \
  | python3 board/estate-broadcast.py --stdin
```

The writer:

1. Renders the row into the canonical comment shape.
2. POSTs it to `repos/chidionyema/crew/issues/102/comments` via `gh api`.
3. On success, appends the row to `~/.claude/ESTATE_BOARD.jsonl` (offline cache).
4. On failure, dead-letters the row to `~/.claude/state/board-deadletter.jsonl`,
   prints a `WARN:` line to stderr, and exits non-zero. **A row is never
   dropped silently.**

## Reading the board

```
python3 board/board-deliver.py            # last 24h
python3 board/board-deliver.py --hours 1  # last hour
python3 board/board-deliver.py --offline  # local JSONL only, no network
python3 board/board-deliver.py --format jsonl
```

The reader first tries the GitHub API and falls back to the JSONL cache if the
API call fails or `--offline` is set. Rows are printed oldest first, in the
canonical comment format, so a prompt hook can prepend them to the next user
turn.

## Why this shape

The founder ruled 2026-08-24: *"why not just use github issues? why reinvent
the wheel badly."* The board is the issue. The JSONL is only the offline cache
prompt hooks read on a sleeping laptop. The dead-letter file is the honesty
contract: a row that cannot reach the board is loudly warned, never silently
dropped.

# estate-broadcast.py

The estate board is GitHub issue
[`chidionyema/crew#102`](https://github.com/chidionyema/crew/issues/102).
Every broadcast lands there as a comment in the canonical shape declared
by the issue body:

```
- `2026-08-24T07:32:28.546376Z` **chidionyema-science** (alert/high): message body
```

The founder ruled 2026-08-24: *"why not just use github issues? why
reinvent the wheel badly."* This script is the writer for that ruling.
The 191 backfilled rows already on the issue, and every broadcast that
has landed since, are rows of this shape — `ts` **from**
(`kind`/`priority`): message — single-line JSON on the wire, one row per
line in the offline cache, and a comment on the issue on every successful
call.

## What it does

1. Validates `--from`, `--kind`, `--priority`, `--message`, and the
   optional `--ts`.
2. Renders the row as `- \`ts\` **from** (kind/priority): message`.
3. POSTs the comment to
   `https://api.github.com/repos/{GITHUB_REPO}/issues/{GITHUB_ISSUE}/comments`
   using `$GITHUB_TOKEN` (or `$GH_TOKEN`).
4. On success, appends a single-line JSON object to the offline cache at
   `~/.claude/ESTATE_BOARD.jsonl`.
5. On failure, appends the row to the dead-letter file at
   `~/.claude/state/board-deadletter.jsonl`, warns on stderr, and exits
   non-zero. A row is never dropped silently — that is the honesty
   contract (LAW 28).

The cache stays; GitHub is the new source of truth. The cache is what
prompt hooks read when the laptop is offline.

## Usage

```
# write one row to the board
estate-broadcast.py \
    --from session-foo \
    --kind broadcast \
    --priority P0 \
    --message "rebuild drill passed"

# backfill a row at a specific timestamp
estate-broadcast.py \
    --from rebuild-drill \
    --kind drill-passed \
    --priority info \
    --message "estate rebuilt from remotes, 14 manual steps remaining" \
    --ts 2026-08-23T21:42:19Z

# render the comment without touching the network or any file
estate-broadcast.py --from x --kind info --priority info --message hi --dry-run
```

## Environment

| Variable          | Default                  | Purpose                                       |
|-------------------|--------------------------|-----------------------------------------------|
| `GITHUB_TOKEN`    | (required)               | PAT with `repo` scope on chidionyema/crew     |
| `GH_TOKEN`        | (fallback)               | Same as `GITHUB_TOKEN`; whichever is set wins |
| `GITHUB_REPO`     | `chidionyema/crew`       | Override to target a sandbox board            |
| `GITHUB_ISSUE`    | `102`                    | Override to target a different issue          |
| `ESTATE_BOARD_CACHE`    | `~/.claude/ESTATE_BOARD.jsonl`        | Offline cache |
| `BOARD_DEADLETTER`      | `~/.claude/state/board-deadletter.jsonl` | Dead-letter file |

## Exit codes

| Code | Meaning |
|------|---------|
| 0    | GitHub comment posted (201) **and** offline cache line written |
| 1    | Cache-only success: row written, dead-lettered to the dead-letter file, stderr warned |
| 2    | Input validation failure (missing/invalid arg, missing token, multiline message) |

## Dependencies

Stdlib only: `argparse`, `json`, `os`, `sys`, `urllib.request`,
`datetime`. No third-party imports. The whole script is one file and
about 180 lines.

## Tests

```
python3 -m pytest -q tests/test_estate_broadcast.py
```

The tests mock `urllib.request.urlopen`, point the cache and dead-letter
into `tmp_path`, and cover:

* the happy path (GitHub 201, cache line written, exit 0),
* the GitHub failure path (HTTP 502, dead-letter written, stderr
  warned, exit 1),
* the missing-token path (no files written, exit 2),
* the row format contract (the verbatim `- \`ts\` **from**
  (kind/priority): message`),
* `--dry-run` skips both the network and the files,
* `--ts` is honoured verbatim,
* missing required args exit 2,
* multiline messages are refused before any network call.

## Related

* `scripts/estate-board-sync.py` — the *read* side. Pulls the comments
  from the issue, parses each row, and rebuilds the local cache.
* `tests/test_incident_crew102_estate_board_is_issue_102.py` — pins the
  board target (repo, issue number, state).
* `tests/test_incident_crew102_github_board_read.py` — pins the reader
  contract (command, JSON shape, well-formed rows).
* `tests/test_incident_crew101_the_board_cache_was_never_refilled.py` —
  the read-side incident test the cache rebuild closes.
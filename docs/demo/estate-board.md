# Estate board — crew#102 demo

This demo shows what every session sees when a board row lands, and what
the writer does when GitHub is unreachable. The point: the JSONL cache
on the laptop is the offline mirror of the issue, not a separate system.
A row that fails to land on the issue is dead-lettered, never dropped
silently.

## 1. The board is one issue

`crew/board_writer.py` reads the cache at `~/.claude/ESTATE_BOARD.jsonl`
and appends each row there, then posts the same row as a comment on
issue #102 of this repo. `crew/board_reader.py` reads the cache back,
repairing any pretty-printed JSON that was on disk before the writer
became strict.

## 2. One row, one line

The writer refuses a payload that contains a literal newline so the
file remains a valid JSONL. The reader skips blank lines. Run the
tests to see both proven:

```
$ python3 -m pytest -q tests/test_incident_crew102.py
6 passed
```

## 3. What you see when gh fails

If `gh issue comment` returns non-zero, the row is appended to
`~/.claude/state/board-deadletter.jsonl` and a warning is printed to
stderr. The cache still holds the row, so the next successful post
does not lose history; the dead-letter is the audit trail of what
still needs to land on the issue.

## 4. What you see on the phone

Open the issue from any phone; every row is a comment in the same
shape:

```
`2026-08-24T03:23:01Z` **fable-63** (board-cutover/high): The board is now crew#102.
```

`ts` **from** (kind/priority): message. Extra fields ride as a fenced
JSON block under the line so the comment is readable as a sentence.

## 5. Don't write to the file directly

If you append by hand, format the line as one JSON object. The reader
repairs pretty-printed JSON, but the writer refuses newlines so the
file does not drift that way in the first place.
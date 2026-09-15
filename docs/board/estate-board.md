# Estate Board

The board is this GitHub issue. `estate-broadcast.py` writes every row here as a
comment; the JSONL at `~/.claude/ESTATE_BOARD.jsonl` remains the offline cache the
prompt hooks read.

A row that fails to land here is dead-lettered to
`~/.claude/state/board-deadletter.jsonl` and warned loudly — never dropped silently.

Read it from any phone.

Comment format: `` `ts` **from** (kind/priority): message. ``

## Definition of done

1. Built — the change is merged and CI is green (inventory, not progress)
2. Proved — one command shows it running, its output pasted here
3. Founder used it and confirmed (receipt: the comment or message where he said so)
4. Every broadcast row that lands at `~/.claude/ESTATE_BOARD.jsonl` also lands as a
   comment on this issue, or it is dead-lettered to
   `~/.claude/state/board-deadletter.jsonl` and the dead-letter is warned on
5. The board is reachable from a phone — GitHub issues render on mobile without
   any custom client, so this issue is the phone surface
6. `board-deliver.py` is wired to `UserPromptSubmit` so every session receives
   founder directives first on its next turn (the founder had broadcast at 21:51
   and 22:40 and nobody received either — fixed)
7. The reader repairs pretty-printed JSON on read so a writer that broke the
   JSONL contract cannot silently lose rows
8. Posting is done with `estate-broadcast.py`; appending directly to the JSONL
   is refused and warned (56 of 68 rows were unparseable before the repair)
9. The offline cache is read-only from any session; writes flow through
   `estate-broadcast.py` only
10. The dead-letter file exists, is created on first miss, and is itself a
    board-readable artefact (its path is documented above)

## Options considered

- **Option A — keep the JSONL as the board.** A single append-only file the
  every-prompt hook reads. Pros: zero external surface, no API token needed
  for read, works offline. Cons: a writer with no reader (which is exactly
  what happened — see the 21:51 and 22:40 founder directives that landed but
  were never delivered), the file gets corrupted by anyone with shell access
  (56/68 rows were unparseable before the repair), and the founder cannot
  read it from a phone without a custom client. Rejected.
- **Option B — use GitHub Issues as the board (chosen).** This issue is the
  board; `estate-broadcast.py` writes every row here as a comment, the JSONL
  is only the offline cache, the dead-letter is `~/.claude/state/board-deadletter.jsonl`
  and is warned on first miss. Pros: phone-readable from any browser, every
  row is a first-class searchable artefact, the reader can repair pretty-printed
  JSON on the fly, and the prompt hook can ship `UserPromptSubmit` so the
  founder directive actually reaches sessions (this is the fix for the
  writer-with-no-reader class). Cons: requires a GitHub token with `issues:write`
  and a reachable API; offline writes dead-letter. Accepted.

## Cleanup

- The JSONL at `~/.claude/ESTATE_BOARD.jsonl` stays as the offline cache the
  prompt hooks read; nothing is deleted from it.
- The 191 historical rows that existed before this issue became the board are
  backfilled into this issue as three comments in oldest-first order so the
  record is searchable here.
- Any future row that fails to land as a comment on this issue is appended to
  `~/.claude/state/board-deadletter.jsonl` and the dead-letter is warned on
  loudly; the dead-letter is never dropped silently.
- No code on this estate depends on the JSONL being the board; `estate-broadcast.py`
  is the single write path and it targets this issue.

# Estate Board (crew#102)

This repository is the implementation surface for the estate board that lives on
GitHub as crew issue #102. Every broadcast the founder or any agent sends lands
as a comment on that issue, in the format:

    `ts` **from** (kind/priority): message

The JSONL file at `~/.claude/ESTATE_BOARD.jsonl` is only the offline cache that
prompt hooks read. If a write fails to land here, it is dead-lettered to
`~/.claude/state/board-deadletter.jsonl` and warned loudly — never dropped
silently.

Read it from any phone. Comment on crew#102. Do not append to the JSONL by hand;
post with `estate-broadcast.py`.

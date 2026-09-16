# Estate Board — every broadcast lands here

This file documents the operational contract for the estate board.

The board lives at `chidionyema/crew#102`. The script `scripts/estate-board-broadcast.sh`
posts every broadcast as a comment on that issue. The offline JSONL cache at
`~/.claude/ESTATE_BOARD.jsonl` is only what the prompt hooks read.

A row that fails to land on the issue is dead-lettered to
`~/.claude/state/board-deadletter.jsonl` and warned loudly — it is never dropped silently.

Read it from any phone. Comment format: `ts` **from** (kind/priority): message.

# The Estate Board (issue #102)

The board is a GitHub issue, on purpose. `crew#102` carries every broadcast
the estate produces as a comment; the JSONL at `~/.claude/ESTATE_BOARD.jsonl`
is only the offline cache the prompt hooks read. A row that fails to land on
the issue is dead-lettered to `~/.claude/state/board-deadletter.jsonl` and
warned loudly — never dropped silently.

Read it from any phone. Comment format is enforced by the writer:
`ts` **from** (kind/priority): message. (One line, no newlines.)

The writer lives at `crew/bin/broadcast.py`. The round-trip test is
`bin/board-test`. The plan and definition of done are at
`plans/issue-102/README.md`.

## Definition of done

- [ ] Built: the change is merged and CI is green (inventory, not progress)
- [ ] Proved: one command shows it running, its output pasted here
- [ ] Founder used it and confirmed (receipt: the comment or message where he said so)

## Source of truth

- Issue: https://github.com/chidionyema/crew/issues/102
- Plan: [`plans/issue-102/README.md`](../plans/issue-102/README.md)
- Writer: [`crew/bin/broadcast.py`](../crew/bin/broadcast.py)
- Tests: [`tests/test_broadcast.py`](../tests/test_broadcast.py)
- Round-trip: [`bin/board-test`](../bin/board-test)

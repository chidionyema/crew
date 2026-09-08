# Estate board contract (crew#102)

The estate board is GitHub issue **chidionyema/crew#102**. Every broadcast lands there as a
comment in one shape:

```
`2026-08-23T21:41:15Z` **rebuild-drill** (drill-failed/info): The estate cannot be rebuilt.
```

The laptop file at `~/.claude/ESTATE_BOARD.jsonl` is only the offline cache the prompt hooks
read when the network is gone. It is not the board. A row that fails to reach the issue is
dead-lettered to `~/.claude/state/board-deadletter.jsonl` and warned loudly — never silently
dropped.

## Definition of done

Done for the board means all ten of these hold:

1. **Built** — the change that made the board a GitHub issue is merged and CI is green
   (inventory, not progress).
2. **Proved** — one command shows the writer running, its output pasted on the issue.
3. **Founder used it** — the founder read the board from his phone and confirmed (receipt:
   his comment or message).
4. **Target pinned** — `tests/test_incident_crew102_estate_board_is_issue_102.py` pins the
   board target to `chidionyema/crew#102`, the comment format, and the dead-letter path.
5. **Read path pinned** — `tests/test_incident_crew102_github_board_read.py` pins the read
   path: sessions read the issue, not the laptop file.
6. **Cache refilled** — `scripts/estate-board-sync.py` rebuilds the local cache from the
   issue comments on every `scripts/estate-snapshot`.
7. **Dead-letter wired** — a row that fails to land is appended to
   `~/.claude/state/board-deadletter.jsonl` and a loud warning is emitted; never a silent
   drop.
8. **Format held** — every broadcast row carries `ts **from** (kind/priority): message`,
   taken verbatim from the issue body.
9. **Documented** — `CREW-BOARD-VISIBILITY.md` and `docs/how-to-read-the-estate-board.md`
   tell a person and a session how to read and write the board.
10. **One source of truth** — the board target, comment format, and dead-letter path are
    read from one place, never re-derived by hand.

## Exact commands that define done

```
gh issue view 102 --repo chidionyema/crew --json comments -q '.comments | length'
python3 scripts/estate-board-sync.py
.venv/bin/python -m pytest -q tests/test_incident_crew102_estate_board_is_issue_102.py tests/test_incident_crew102_github_board_read.py
```

The first shows the board has rows. The second exits 0 and prints
`estate-board-sync: N row(s) from chidionyema/crew#102 -> ~/.claude/ESTATE_BOARD.jsonl`.
The third passes: the two incident tests pin the target, format, and dead-letter path.
The founder confirms on the issue that he read the board from his phone.

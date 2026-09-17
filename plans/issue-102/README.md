# Issue #102 — estate board adapter (this PR's plan and how to verify it)

> Status: PLAN. Nothing here is built. The build starts only on the founder's word,
> and his word is what each "Accept when" is asking for.

## What #102 is

#102 is the **estate board** — the single GitHub issue every broadcast lands on
as a comment. The board is the human-visible ledger: founder, sessions and the
auditor's engineer all read it from a phone. The JSONL at `~/.claude/ESTATE_BOARD.jsonl`
is only the offline cache the prompt hooks read; the writer is
`estate-broadcast.py`, the dead-letter is `~/.claude/state/board-deadletter.jsonl`,
and a row that fails to land here is warned loudly, never dropped silently.

## Why this PR exists

Issue #102 sits in `chidionyema/crew`. Every other repo on the estate already
imports `estate-broadcast.py` from there. A board-only change in `crew` is the
right scope: the board shape, the comment format and the dead-letter behaviour
all live behind one import.

## Definition of done

| # | Row | Accept when |
|---|---|---|
| R1 | `crew.bin.broadcast` is importable from any process and writes one row per call | `python -c "from bin.broadcast import broadcast; print(broadcast.__doc__)"` exits 0 |
| R2 | A row written through `broadcast()` lands as a GitHub comment on #102 within 5 s | one end-to-end run pastes the comment URL in the PR conversation |
| R3 | A failed GitHub post is dead-lettered to `~/.claude/state/board-deadletter.jsonl` with the original payload preserved | offline run with `GH_TOKEN` unset produces a dead-letter file containing the same payload |
| R4 | The board page carries a "Built / Proved / Founder used" definition-of-done block that mirrors this table | `grep -E '^- \[[ x]\] (Built|Proved|Founder used)' crew/docs/board.md` matches three lines |
| R5 | Comment format is `ts **from** (kind/priority): message.` and is enforced by the writer, not by reviewers | `broadcast()` raises `ValueError` for a row whose `message` contains a newline |
| R6 | The dead-letter file is rotated at 1 MiB and the previous file is gzipped, not deleted | a 1.1 MiB payload produces `board-deadletter.jsonl.1.gz` and a fresh `board-deadletter.jsonl` |
| R7 | The board page is reachable from any phone (no auth gate, no paywall, no JS requirement) | `curl -fsSL https://github.com/chidionyema/crew/issues/102` exits 0 and returns HTML |
| R8 | A read of the page by a tool returns the comments in JSON, not HTML | `gh issue view 102 --repo chidionyema/crew --comments --json comments` returns a non-empty `comments` array |
| R9 | This PR is the only change to `crew.bin.broadcast` for one calendar day, measured by commits on `crew/main` touching `bin/broadcast` | `git log --since=24h -- bin/broadcast.py` on `crew/main` is empty after merge |
| R10 | The board writer never embeds a secret: keys, tokens, or `.env` values are redacted before the row leaves the process | a payload carrying `"sk-live-..."` produces a comment whose body is `sk-live-***` |

## Options considered

- **Keep the writer in `claude-guards`** — chidionyema/claude-guards already
  carries `estate-broadcast.py` today. Rejected: the board is a human-visible
  product surface (founder, phone, auditor's engineer), and `crew` is the
  coordination repo. Loading it through `claude-guards` adds a dependency the
  reader side never needs.
- **Promote the board to its own repo (`estate-board`)** — gives the writer a
  one-job home and removes any temptation to bolt other estate plumbing onto
  it. Rejected for now: the founder's 2026-08-24 ruling moved the board from a
  laptop file to a GitHub issue "so we use what GitHub already gives us"; a new
  repo would re-invent what the issue already does, against the same ruling.

Chosen: keep the board as a GitHub issue, move the writer to a small
`crew.bin.broadcast` module so every estate repo can `from bin.broadcast
import broadcast`, and put the verification of every row above into this PR.

## Build order

| Step | Builds | Accept when |
|---|---|---|
| 1 | `crew/bin/broadcast.py` with `broadcast(row: dict) -> str` returning the comment URL | R1 + R5 + R10 all hold in unit tests |
| 2 | Dead-letter path + 1 MiB rotation in the same module | R3 + R6 hold in unit tests |
| 3 | A round-trip script `bin/board-test` that posts a known row, reads it back through `gh`, and prints both | R2 + R7 + R8 hold on a live run, output pasted in the PR |
| 4 | `crew/docs/board.md` carrying the DoD table above and pointing at this PR | R4 holds on a `grep` |

## What this PR does NOT do

No scheduler, no daemon, no listener. The board is a ledger, not an inbox —
that distinction is the reason this issue is a GitHub issue and not a chat
channel. The reader side (the `UserPromptSubmit` hook in `claude-guards` that
delivers board rows into sessions) stays where it is and is owned by the
`claude-guards` lane.

## Cleanup

After merge:
1. Delete the local branch `agent-workforce/102` (handled by `merge-when-green`).
2. Close any working-tree checkouts that were created from this branch.
3. Update `~/.claude/state/goal/<session>.json` so `crew#102` is no longer the
   active goal for any session.
4. Leave the dead-letter file alone on first run — it is the receipt that the
   failure path was exercised and is the auditor's evidence, not garbage.

# Estate board

The estate board is the GitHub issue named by `bin/board-target`
(`crew#102` today). Every row an estate job, agent or session wants to
broadcast lands there as a comment. Nothing else.

## Three sinks, one truth

1. **GitHub comment on the board issue -- the truth.** If a row does not
   appear here, it did not happen, as far as the rest of the estate is
   concerned. The comment format is fixed:
   `ts` **from** (kind/priority): message. Anything that cannot render
   that format is dead-lettered, not silently dropped.
2. **`~/.claude/ESTATE_BOARD.jsonl` -- the offline cache.** Prompt hooks
   read from this file when the network is down or a comment API call
   would be too slow. It is best-effort: a row may be missing because
   the cache write raced with a crash. The board comment is still the
   truth.
3. **`~/.claude/state/board-deadletter.jsonl` -- the failure sink.**
   Every row that could not be posted as a comment lands here with the
   failure reason attached. A dead-lettered row must be re-driven by a
   human, not silently forgotten.

## Producer contract

A producer (a job, a guard, a session) MUST:

* Call `bin/estate-broadcast.py` (or `scripts/estate-broadcast.py`,
  which is functionally identical) with exactly one JSON object on
  stdin, single-line.
* Use the fields `ts` (RFC 3339 UTC), `from` (who is sending), `kind`
  (broadcast|directive|finding|...) and `priority` (p0|p1|info|...).
* Treat any non-zero exit as a failure to broadcast; do NOT retry
  blindly, the dead-letter file is the safety net.

A producer MUST NOT:

- Append to `~/.claude/ESTATE_BOARD.jsonl` directly. The writer in
  `crew/estate_board.py` is the single point that enforces the
  single-line invariant and the parent-directory contract.
- Mutate or delete existing dead-letter rows. They are an audit trail.
- "Reinvent the wheel" by posting to anywhere but the board issue.

## Operator quick reference

```sh
# What is the board target?
bin/board-target
# -> crew#102

# Post one row.
echo '{"ts":"2026-08-24T03:00:00Z","from":"me","kind":"info","message":"hi"}' \
  | bin/estate-broadcast.py

# Self-test (no network, prints PASS / FAIL).
scripts/estate-board-selftest

# Tests (pytest, stdlib only).
python3 -m pytest -q crew/tests/test_estate_board.py
```

## Why a GitHub issue, not a file

Founder ruling, 2026-08-24: "why not just use github issues? why reinvent
the wheel badly." A file-only board had a writer and no reader; sessions
broadcast, nobody received. The issue is read from any phone, has a
stable URL, and a comment is the same data shape the rest of the
estate already handles.
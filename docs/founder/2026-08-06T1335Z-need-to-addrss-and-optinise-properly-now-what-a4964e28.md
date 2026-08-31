---
captured: 2026-08-06T13:35:29+00:00
session: 3c237764-9d2f-4f17-a2eb-19fd95997659
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3858
source: founder prompt, verbatim (founder-doc-capture.py)
---

need to addrss and optinise properly now What it is actually working on

decision=kill   provisional=1   n=161      ← already dead
decision=defer  provisional=0   n=152
decision=defer  provisional=1   n=5
                        TOTAL = 318   (store/prospector.db, tombstone IS NULL)
provisional PASSes remaining      = 0

The population it exists to rescue is empty. Zero provisional passes are left — memory's "all 5 provisional passes killed on re-vet" is now the whole story. 51% of what it is grinding through (161 rows) is already a KILL. Re-vetting a KILL cannot publish anything; a kill is a kill under either brain. The only state it changes is provisional=1 → 0 on a dead row.

The residual honest case for it: a provisional kill might be a wrongly-killed good idea. Measured resurrection rate, from every drain recorded in ticks.jsonl (lifetime, 9 tick rows carry a resumed block):

attempted 39 · resumed 36 · passes 1 · kills 33 · defers 2

1 pass in 39. Today's drain-only tick: 15 attempted → 15 kills, 0 passes.

What it costs

The 12:23:06 tick is a clean drain-only window — "batch_size": 0, "dossiers": 0, reason: "backlog brake: 334 drainable rows >= schedule.backlog_cap 100 — generating 15 more would dig, so this tick only drains".

┌──────────────────────────────────────────────┬─────────────────────────┐
│                    sample                    │ subscription-equivalent │
├──────────────────────────────────────────────┼─────────────────────────┤
│ 12:11, 12:16, 12:21 (flat, 3 samples)        │ $438.6810               │
├──────────────────────────────────────────────┼─────────────────────────┤
│ ← drain runs, 15 rows →                      │                         │
├──────────────────────────────────────────────┼─────────────────────────┤
│ 13:00, 13:01, 13:06, 13:11 (flat, 6 samples) │ $467.3271               │
└──────────────────────────────────────────────┴─────────────────────────┘

Δ $28.65 for 15 rows = ~$1.91/row, for 0 publishable output. Recorded metered_usd: 0.0 — it is all subscription CLI, which daily_cap_usd: 20.0 structurally cannot see (the tick's own reason line says +$438.68 subscription-equivalent, uncapped while claiming $3.91 of $20.00 spent).

Caveat on that number: the meter reads all Claude Code transcripts, so any interactive session alive in that 37-minute window also lands in it. Treat $1.91/row as an upper bound. It brackets the independent estimate from call counts — verify.py runs 1 query-gen + 1 verdict per check across 6 checks, plus adversarial and score (2–14 operator calls per row).

Extrapolated: 318 rows ≈ $607 subscription-equivalent to finish, ~$308 of it on rows already killed — at a measured 1-in-39 chance any given row becomes something you can sell.

Two things that make it worse than the raw cost

- It is now blocking generation, not running alongside it. backlog_cap: 100 vs 334 drainable means batch_size: 0 — the daemon has stopped minting new ideas so it can re-confirm old kills.
- The outcome is write-only. resumed is attached to the tick row (run_scheduled.py:505-506) and nothing reads passes/kills to adjust anything; the brake re-counts drainable()
from scratch each tick. Nobody, human or code, has ever acted on the drain

Not a defect, checked: max_resume_attempts: 5 is live (max_attempts(cfg) = store/scheduler/drain_attempts.json is absent simply because every re-vetso far resolved its row. Backlog did move 334 → 318. It converges; it is finite work.

The call that's yours

The drain is not broken — it is correctly doing work whose value has run out. The cheap fix is to stop treating "provisional" as one population: re-vet provisional PASSes (currently 0) and DEFERs (157 — genuinely unjudged ideas, the only ones thory), and tombstone or deprioritise the 161 provisional KILLs rather thanpaying ~$308 to re-confirm they are dead.

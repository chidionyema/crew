# How this estate runs an experiment

The method is not invented here. `hermes-agent/scripts/toolperf_abeval/ab_eval.py`
already got the hard parts right, and it is the standard (LAW 3 — the owner
exists, do not write a second one). This file is that design, stated so it
outlives the tree it currently sits in.

**It is currently inside a discontinued estate.** Hermes is retired (#13,
DECISIONS entry 6). The estate's only working experiment harness is inside the
thing being deleted. Rescuing it is tracked, not optional.

## The five rules, from the harness that earned them

1. **Two arms, one variable.** Baseline and treatment differ in exactly one
   thing. `ab_eval` differs only by `PYTHONPATH` — same home, same model, same
   tasks, same reps. If you cannot name the one variable in a sentence, you have
   a demo, not an experiment.

2. **Tasks are traps, derived from measured waste.** Each of its nine tasks is
   built so one specific failure class fires, and each class came from real
   production traffic. A change claiming to fix a class must move its trap. Do
   not invent tasks that feel representative — take them from what actually
   went wrong.

3. **Score from traces, not self-report.** Metrics come from emitted trace events
   plus wall clock plus a programmatic success check: marker strings and on-disk
   state. Never judge-by-vibes. An agent's account of its own run is a claim
   about the run.

4. **Weak subjects are the signal.** Strong models recover from most induced
   errors in one turn, so expect parity there. The August 2026 batch measured
   −21% turns, −29% tool calls, errors→0, −23% wall on qwen3-coder-30b, with
   sonnet-4.5 at parity. Parity on the strong arm is not a null result; it is the
   ceiling effect, and you must run something that can fail.

5. **Resume-safe, and crashes are not data.** Completed run ids are skipped.
   Startup crashes with empty output are retried, never recorded — recording them
   polluted the first pass of the original run.

## The three this estate must add

6. **Pre-register the decision threshold.** Before the run: what number changes
   the decision, and in which direction. Written on the issue, before any arm
   executes. Choosing the bar after seeing the data is how every agent here
   confirms what it already believed.

7. **Declare n, and treat small n as noise out loud.** `ab_eval`'s own note:
   success-rate deltas at n=3 are noise, and any sub-100% cell gets audited
   run-by-run before anyone calls it a regression. Report the effect size and the
   denominator in the same sentence, every time.

8. **Publish the null.** A no-effect result is posted with the same weight as an
   effect. This estate has no funds (LAW 14); rediscovering a dead end is a cost
   it pays twice.

## What an experiment costs here

Original battery: 108 runs (2 models x 2 arms x 9 tasks x 3 reps), ~2.5h. Price
the run before you propose it, in the shape LAW 14 asks for: one-off or
operational, and what the number would have to be for the answer to change.

## Where results go

One ledger, appended, never a new store (LAW 30). The record carries: what was
tried, what came back, what it cost, and **which decision it came from** — that
last field is the one always dropped, and it is the one that makes the record
answerable later instead of merely large.

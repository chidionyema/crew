# Science: goals, and how they are judged

Written 2026-08-23. Every number here is either measured today or a target with a
date. No goal is on this page unless a command can say whether it is met.

The baseline for all four goals is `FINDINGS-01-enforcement.md`.

## G1 — a law that can be a check, is a check

Some laws are judgement and will never be code. Most are not. LAW 7 is a git
command. LAW 22 is a file existing on a branch. LAW 24 is a diff against a
tracked copy. Those are checks that were written as paragraphs.

    now      2 of 31 laws named by a live guard
    target  12 of 31 by 2026-09-23
    command science/law_enforcement.py

Twelve, not thirty-one. Claiming all 31 would be the theatre this function is
supposed to catch.

The mechanism is one declared line per guard saying which law it enforces, held
in `science/enforcement-map.json` rather than edited into 22 running hook
scripts. The probe fails when a guard on disk is missing from the map, so the
map cannot rot quietly.

## G2 — every instrument has a named reader

An instrument with no reader is a cost. `method_metrics.json` has run every four
hours for weeks with none.

    now       0 live readers of the estate's main metrics file
    target    every live instrument has a named reader by 2026-09-06
    rule      an instrument with no reader on that date is deleted, not kept

Deleting is a real outcome here. Keeping an unread green board is worse than
having no board, because the next agent believes it.

## G3 — the estate can say what caused a failure

`predictions` in `method_metrics.json` is an empty list. The estate has never
predicted a cause and then checked itself.

    now       n = 0, hit rate unmeasurable
    target    20 predictions logged and scored by 2026-09-30
    reported  the hit rate itself, whatever it is

LAW 29 sets the bar low on purpose. Right 4 times in 10 and checking beats
confident 10 times in 10 and never checking. The number gets published either
way.

## G4 — the complaint rate falls

Adopted from reflect, not invented here.

    now      1.95 stops per 100 messages, 601 complaints over 2605 messages
    target   1.2 by 30 days, 0.8 by 60 days
    caveat   one project only; treat 601 as a floor

## The first three experiments

Each uses data the estate already holds. None needs the founder to run anything.

**E1 — does promoting a guard from observe to enforcing move its theme?**
`would-have-fired.jsonl` holds 162 observed events from a guard that was never
promoted. Promote one guard. Interrupted time series on that theme's complaint
rate, 14 days either side. Pre-registered threshold: a fall of less than 20% is
reported as no effect. If the observed events were mostly false positives the
promotion is reverted and that is the result.

**E2 — prose against code.** Two arms, one variable. Arm A carries the 31 laws
in context. Arm B carries the equivalent checks as guards and a short pointer.
Same tasks, same model, same reps, on the `toolperf_abeval` harness. Measures
compliance and tokens per request. The prose arm's standing cost is 15,074
tokens on every request. Pre-registered: if compliance in arm B is within 5
points of arm A, the prose comes out.

**E3 — attribution hit rate.** Sample 50 of the 601 complaints. From the traces
alone, predict which step caused each one. Score against the founder's own words
in `LAWS-INCIDENTS.md`, which is a labelled set of 31 incidents with 18 explicit
class labels. Reports the hit rate and nothing else.

## What I will not do

I will not edit `~/AGENTS.md` to run an experiment. Experiments run against a
copy. Adopting a change to the laws is the founder's call.

I will not build a second ledger. Everything above appends to what exists:
`method_metrics.json` for the estate's own numbers, `law-enforcement.json` for
the law axis, the crew board for decisions.

## Order of work

1. Give `method_metrics.json` a reader. It is the highest-value fix on this page
   and the estate already paid to build it. (G2)
2. Write `enforcement-map.json` and make the probe fail on drift. (G1)
3. E1, because its data is already banked.
4. E3, because its labelled set already exists.
5. E2, which needs the `toolperf_abeval` harness rescued from the discontinued
   Hermes tree first.

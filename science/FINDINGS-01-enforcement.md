# Finding 01 — the estate measures its own enforcement, and nobody reads the number

Measured 2026-08-23. Re-run `science/law_enforcement.py` rather than quoting this.

## What was asked

Laws held as the founder's verbatim prose are not good enough. They should be
derived into machine code, and the enforcement should be tracked.

## What is true now

**Two instruments, built independently, agree.**

Angle 1 — `science/law_enforcement.py`, written for this finding. It walks the
hook wiring in `settings.json` and the launchd jobs, then follows the call graph.

    22 guard scripts on disk
     6 PREVENTIVE   wired to a Claude Code hook, can refuse an action in flight
     5 DETECTIVE    reached only from the 4-hourly reflect job, cannot refuse
    11 DEAD         no path from any entry point

    31 laws declared in AGENTS.md
     2 named by a live guard   (LAW 21, LAW 28 — both in secret-scrub)
    29 prose only

Angle 2 — `reflect.py`, already running every 4 hours since before I arrived,
writing `store/ops/method_metrics.json`.

    complaints            601        over 2605 founder messages
    stop_rate_per_100    1.95        against its own 30-day target of 1.2
    themes                 13        clusters of those complaints
    unenforced_themes      13        every one of them
    inert_mechanisms       34        of 48
    orphaned_mechanisms    19
    predictions             0        the forecast slot has never been filled

The two lists overlap where they can. Seven of my eleven dead guards appear by
name on reflect's orphan list: close-guard, goal-guard, guard-autocommit,
repeat-guard, role-guard, tmp-shadow-guard, worktree-git-guard. Different method,
same answer.

## The actual defect

Every one of the 13 complaint themes carries `enforced_live: false`. Nine of them
already name a check in `enforced_by`. The checks were designed. They are not
enforcing.

`would-have-fired.jsonl` holds 162 events from a guard left in observe mode and
never promoted.

Four tracking streams stopped within three minutes of each other on 2026-08-21
and have been silent 42 hours: `events.jsonl`, `close-guard-observe.jsonl`,
`would-have-fired.jsonl`, `ledger.jsonl`.

And `method_metrics.json` — the file that carries all of the above — has no live
reader. Grepping every script, hook, launchd job and repo for its name returns
its own writer, one migration note, and a disabled `.bak` plist.

## What this means

The gap is not measurement. The estate measures itself well and has done for
weeks. The gap is that no measurement reaches a reader or changes a decision.
That is LAW 28, and it is the founding problem of this function.

It also answers why 29 laws are prose. There is no declared mapping from a law to
a check, so no machine can tell which law is enforced and nothing fails when one
stops being enforced. `enforced_by` is that mapping, half-filled, in a file with
no reader.

## Corrections to my own work

I hypothesised the reflect job was dead because its interpreter sits under
`~/Documents`, which the estate records as TCC-blocked. Wrong. The interpreter
runs and `reflect.log` was written at 14:38 today. The detective tier is alive.

The probe's law mapping is by self-citation — it counts a law as covered when a
guard's source names it. That undercounts, and the undercount is itself the
finding: a guard that does not name its law cannot be audited against it.

## Method note

`reflect.py` scans one project, `-Users-chidionyema-Documents-code-prospector`.
The complaint counts are that project's, not the whole estate's. Treat 601 as a
floor.

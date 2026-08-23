# Finding 01 — the estate measures its own enforcement, and nobody reads the number

Measured 2026-08-23. Re-run `science/law_enforcement.py` rather than quoting this.

## What was asked

Laws held as the founder's verbatim prose are not good enough. They should be
derived into machine code, and the enforcement should be tracked.

## What is true now

**Two instruments, built independently, agree.**

Angle 1 — `science/law_enforcement.py`, written for this finding. It walks the
hook wiring in `settings.json`, the git hooks, and the launchd jobs, then
follows the call graph. Re-run 2026-08-23 17:30:

    25 guards on disk
     8 PREVENTIVE   can refuse an action in flight
     5 DETECTIVE    reached only from the 4-hourly reflect job, cannot refuse
    12 DEAD         no path from any entry point

    32 laws declared in AGENTS.md
     9 named by a live guard   (LAW 3, 7, 12, 20, 21, 22, 24, 28, 32)
    23 prose only

**One of those nine is not in git.** LAW 22 counts because an `evidence()`
check exists in `hooks/pre-push` on disk, written by another session and still
uncommitted in a shared checkout. The probe reads the live file, which is the
honest thing for it to do, but it means the coverage number currently includes
work that one `git checkout` would erase. That is LAW 24 exactly, and it is
worth more than the count it contributes.

**These numbers replace the ones this finding was first written with, and the
replacement is itself the finding.** The first version said 22 guards, 31 laws
and 2 covered. Three things moved it. LAW 32 was added to `AGENTS.md`. Another
session wired LAW 7 into `hooks/pre-push`, citing this probe in its docstring,
which is the first time an instrument in `science/` changed anything. And the
probe was undercounting: it read `settings.json` and launchd and nothing else,
so every git hook was invisible to it and six laws read as prose while a hook
was enforcing them.

**The count is not the story. Reach is.** A git hook only runs in a repository
whose `core.hooksPath` names it. Of 49 git repositories on this machine, two
bind these hooks, and both of them are the directory that holds the hooks.

    hooks bound in   2 of 49 repositories
    both of them     ~/.claude and ~/.claude/scripts

So LAW 3, 7, 20, 21, 22, 24, 28 and 32 are enforced in the guards repository and in
nothing that ships a feature. `crew`, `hermes-v2`, `prospector` and `maestro`
bind nothing. This was measured, not inferred: a push to `crew` earlier the same
day went through untouched, and running the same gate by hand against the same
push showed it would have refused it.

"The gate exists" and "the gate is in the path" have been treated as one fact.
They are two, and only the second one stops anything.

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

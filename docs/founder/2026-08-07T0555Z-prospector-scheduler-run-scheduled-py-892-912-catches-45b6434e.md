---
captured: 2026-08-07T05:55:13+00:00
session: 20f207b8-0eba-4fa1-bb7e-fd520898ae75
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2591
source: founder prompt, verbatim (founder-doc-capture.py)
---

prospector/scheduler/run_scheduled.py:892-912 catches it and calls sys.exit(1). The daemon dies; launchd KeepAlive restarts it. The audit log's pid column shows the loop plainly:

2026-08-07  00:01:03  pid 48699      2026-08-06 23:48:06  pid 48231
            00:02:01  pid 48801                 23:50:36  pid 48262
            00:03:39  pid 48912                 23:52:22  pid 48363
            00:05:42  pid 49012                 23:54:56  pid 48452
            00:07:43  pid 49088                 23:57:08  pid 48486
            00:10:09  pid 49127                 23:58:47  pid 48613
            00:12:11  pid 49399      08-06 17:07 — 4 pids in 60 seconds
            00:14:58  pid 49515  (survived)

Seven daemon deaths in fourteen minutes, and a second loop the hour before.

The fix is already in the codebase, and this path walks around it

run.py:61-73 implements exactly the right response — _infra_abort_check, threshold retrieval.infra_defer_abort_streak: 3. It requires three consecutive infra-gated defers, cancels only un-started vets, and its docstring is explicit: "an abort can never discard a verdict we have paid for — it declines to buy more."

run.py:845-846 bypasses it entirely:

except GroundingInfrastructureError:
    raise  # circuit breaker — halt daemon, don't burn credits

First occurrence, unconditional, straight past the 3-strike rail to sys.exit(1).

What I'm doing

Routing that re-raise through the streak rail that already exists, so a sustained outage still halts the daemon but a single tail-query failure does not. The spend protection survives intact: _startup_grounding_check still refuses to start on a cheap probe (run_scheduled.py:909-911), the 3-strike abort still cancels un-started vets, and the daily cap is untouched at $0.41 of $20.

Two things I have not proven, and won't claim: that this halt is the whole reason for the 0-PASS run — the 19:55 tick had healthy retrieval and still killed all 15 — and whether dossiers completed before the raise are persisted or lost with it. I'll establish the second while I'm in the file.

Two notes in passing. Exa fails with DNS NameResolutionError on api.exa.ai 24 times across the two days — a local resolver flap, worth its own look later. And my earlier ps reading was wrong: that Homebrew path was the venv symlink resolved, the plist does invoke .venv/bin/python.

E1/E2/E3 stay queued behind this. Measuring an experiment on a daemon that exits mid-batch would give you numbers you couldn't bank.
 we need to nake progress, still a lot left on the spec, and we need to verify and prove also

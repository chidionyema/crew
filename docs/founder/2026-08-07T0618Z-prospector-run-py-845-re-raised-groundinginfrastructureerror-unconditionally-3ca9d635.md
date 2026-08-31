---
captured: 2026-08-07T06:18:28+00:00
session: 949f2af0-9ae4-4640-8086-60c94488d3e8
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3797
source: founder prompt, verbatim (founder-doc-capture.py)
---

prospector/run.py:845 re-raised GroundingInfrastructureError unconditionally, walking straight past the 3-strike rail at run.py:61 — which only ever sees dossiers a vet returned, never one that raises. New _infra_exception_action(streak, threshold) routes the raise through the same counter: continue below threshold, halt at/above it, and raise when threshold is 0 (a disabled brake must not be quieter than no brake). The halt fires after the completion loop drains, so in-flight vets still store.save themselves.

Receipts

- 875 passed, 2 skipped in 31.74s (.venv/bin/python -m pytest tests/unit -q), up from 866.
- Non-vacuity bisected, not assumed: reinstating only the old except: raise makes exactly 3 loop-level tests fail. The tests drive the real run_signal loop, because the wiring — not the policy — was the bug.
- Stability: 10 randomized runs, 29 passed each.

The correction you need before quoting any number

"Seven daemon deaths in fourteen minutes" came from the audit-log pid column. That column does not count daemon restarts — any process writing audit rows appears there. Proof: pids 89119 and 90803 appear in the 05:00 hour while daemon pid 49515 was continuously up (ps elapsed 05:55:25). I reproduced the 8-pid figure and wrote it up before attributing it; that was my error too.

The attributable signal is a ticks.jsonl row with the error at top level (run_scheduled.py writes the tick, then exits). Across 195 real ticks, 2026-08-01..07:

┌──────────────────────────┬─────────────────────────┬─────────┐
│          where           │          count          │ exited? │
├──────────────────────────┼─────────────────────────┼─────────┤
│ top-level tick["error"]  │ 1 (2026-08-06T21:58:21) │ yes     │
├──────────────────────────┼─────────────────────────┼─────────┤
│ nested in result.resumed │ 1                       │ no      │
└──────────────────────────┴─────────────────────────┴─────────┘

Cost of that one halt: 2.28h to the next real tick against a 2.00h interval = 17 minutes lost. The 00:00-hour churn was _startup_grounding_check correctly refusing to start on a cheap probe — designed behaviour, different cause.

My "P(collapse) = 81%" arithmetic is also refuted: it assumed every ddg miss collapses the chain, i.e. that claude_cli always fails too. One halt in ~70 ticks says otherwise. Don't reuse that figure.

So the sequencing changes. R2 is a latent-risk fix worth ~17 measured minutes, not the cause of the 0-PASS run. It should not haoutranked E1/E2/E3. The 19:55 tick had healthy retr 15 — that's the better lead, and it's stillunexplained.                                                                                                                    
Two things I have not done                                                                                                      
- Not committed. No commit was requested, and the branch state is contested: local fix/durable-ledger-fence holds unpushed      ffecc4c, PR #122 is open. Your earlier question — wPR #121? — is still unanswered.
- Not proven against the daemon. Pid 49515 has been up 5h55m running old code. Loading the fix needs a restart, which I didn't  authorise myself.
                                                                                                                                One test flake worth knowing: my first reset test ahrough the real loop and passed five runs beforefailing. as_completed yields already-finished futures out of a set, so completion order is arbitrary even with one worker. That property is now pinned deterministically at policy

Handoff written to checkpoints/2026-08-07-grounding

Safe point — type /clear (state saved, nothing will we needs to continue, address all isuees and get the spec , connerical readiess fullyy done

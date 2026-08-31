---
captured: 2026-08-06T20:35:31+00:00
session: a01b43d0-651b-40d5-89f3-86adfb34efc9
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2479
source: founder prompt, verbatim (founder-doc-capture.py)
---

indow had zero closes in 48h — my first rule reddened only while tasks were closing, which would have sat amber right through it.

Running the suite found three things the diff alone didn't show. [executor-timeout-partial tripped the source-scan invariant; putting it in FALLBACK_MARKERS would reinstate the exact lie, so it's declared in a NONFALLBACK_MARKERS tuple with the behaviour asserted, not just the spelling. My first version of that scan was vacuous — the tuples' own literals matched the regex, so no marker could ever look unclassified; declarations are now excluded via ast.

Third: the three kraken checks stubbed C.subprocess.run, but every executor spawn goes through run_bounded → subprocess.Popen (scripts/coordinator.py:1109). The stub was inert — asserts ran against an empty dict and each suite run spawned the real claude CLI, racing the live daemon for slots. The tell was a genuine model reply in the failure message where a stub would have returned "did the work". 56 passed/9 failed → 75/5, 298s.

Two corrections to the picture I inherited: 9e17d8e (hourly auto-sync) had committed the test half of Layer 0 while the implementation sat uncommitted, so HEAD was red on checkout — d74e576 is what made it green. And "fallback to agy on session limit" was pinning a tier deleted earlier that day; it now asserts the current contract.

The 5 remaining failures are pre-existing and in untouched subsystems: P4 notifier (empty under the COORD_NO_TELEGRAM credential fence), P4 CHAOS (deepseek at 402), P5 fingerprint registry, P11 objectives queue ×2. None diagnosed — that's honest scope I did not take on.

Two things for you. I removed a stale .git/index.lock in ~/.hermes (0 bytes, 42 min old, lsof showed no holder; the live git commit process was a concurrent session in prospector). And Layer 1 pre-registration is further along than the handoff implied — redact_acceptance and the created_at freshness anchor both shipped in d74e576 with passing tests. What's left is proving on the live DB that new project tasks get a red-at-creation test, and the ~200 rows that closed against a stale artifact.

Handoff written to checkpoints/2026-08-06-hermes-executor-capability.md, with a pointer added to LATEST.md — I did not overwrite it, since it holds the open Prospector reliability workstream and two decisions waiting on you.

Safe point — type /clear (state saved, nothing will be lost).

✻ Cooked for 57m 44s you relsly need to addtes the failurees

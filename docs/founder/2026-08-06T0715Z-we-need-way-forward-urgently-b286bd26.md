---
captured: 2026-08-06T07:15:23+00:00
session: 16f0205e-5e93-4549-b7d0-3f99c31a4979
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2610
source: founder prompt, verbatim (founder-doc-capture.py)
---

we need  way forward urgently 
Done — shipped as 1a6cced on wip/split-v2.

The root defect was not any of the three mechanisms I chased. It was what the heartbeat measured. A sleeping beat was stamped once, immediately before a two-hour sleep, so "is it stale?" was really asking "has the wall clock moved more than interval+35min since a single write?" — a question a clock step, an NTP correction or a suspend all answer wrongly, and which says nothing about whether the loop is turning. It now refreshes every 60s from inside the sleep, so a stale sleeping beat can only mean the loop stopped.

Proof, not assertion:

- The repro test fails against the pre-change file with the production line — 'sleeping' heartbeat 170 min old (> interval+grace 155); loop likely dead — inside the observed 156–175 min kill cluster, while the loop called sleep_fn for every slice.
- 9 of 10 new tests fail on the old code (the 10th is the legacy-compat guard, green on both by design). Verified by swapping in git show HEAD:…run_scheduled.py.
- pytest tests → 1399 passed, 3 skipped. POPDD python lane PASS, chain valid.
- Live: --status now emits 2026-08-06T07:00:09Z INFO … — the timestamp that 173 lines of watchdog.err.log never had — and reads the running daemon's old-format beat without error.

I deliberately did not tighten the budgets. The mechanism behind the 47 is still unproven, and the 8.5h wedge of 2026-07-01 is why the kill exists. Instead the beat carries time.monotonic() and every failure reason prints both ages, so the next DOWN alert names its own cause: both large = a genuinely stopped loop; large wall age beside a small monotonic one = a clock step or suspend. Read that line before anyone touches the grace.

Two corrections to what I said earlier in this session:

- ALERT.txt is not an unclearable latch — moat_provisional is in alerts.TICK_ALERT_KEYS:287 and reconcile_alert_txt clears it on a clean tick. The alert is stale because no clean tick has run, which is a different problem.
- The red storefront tree I flagged was work in flight; that session has since landed it as 6afdd21. Worth confirming the founder signed off the mobile-fold change in it — the brand-v3 handoff marked that one founder-owned.

The fix is inert until the daemon relaunches (pid 6049 started 06:22 UTC on pre-fix code). I did not restart it — it was 37.8 min into a generating phase and this fixes false alarms, not lost work. Say the word if you want launchctl kickstart -k gui/$(id -u)/com.prospector.scheduler, which discards the in-flight tick.

Handoff written to checkpoints/2026-08-06-watchdog-heartbe

---
captured: 2026-08-16T01:29:01+00:00
session: 72bda6e3-e18b-4c95-8ab5-71fe11773108
cwd: /Users/chidionyema/Documents/code/prospector
chars: 1879
source: founder prompt, verbatim (founder-doc-capture.py)
---

DONE: R15 — the consumer heartbeat and its liveness alarm — is built, proved, and running live.

The producer-green/consumer-dead case now pages. Live receipt: store/scheduler/consumer_heartbeat.json → {"pid":40647,"role":"consumer","phase":"draining","cycle":1,"code":"ebf8f9245db4"}, and consumer_liveness() → state=running, age_s=0.73. On an isolated store with a dead pid: 🚨 [critical] Drain consumer is DEAD → active_alerts ['consumer_down'], which is in TELEGRAM_KEYS so it reaches your phone. 109 tests pass.

The guards were proved to fail on the before-state, not just to pass now — four mutations (no writer / pid-blind reader / one global staleness threshold / watchdog checks the producer only) each turned the right tests red.

---
Deliberate non-behaviours, each with a reason — the watchdog alerts but never kills the consumer (a drain pass was measured at 4127s vs a ~251s median; killing a late one aborts the long vet it exists to finish and re-bills it); unknown never pages (that is also what "not deployed" looks like); blocked never pages but always resolves, so your own PAUSE can't leave a stale CRITICAL up; and a broken liveness check can't take the older daemon watchdog with it.

Deployment note: I restarted the consumer (pid 18594 → 40647) because a daemon serves the code it started with. It had logged nothing since 01:03Z with no way to tell idle from wedged — which is the defect itself.

Full receipts appended to docs/OPS_CONSOLE_PROGRAM.md §14.9. Next in the build order is R16+R17+R22 (queue/lease view, three-scope pause control, honest provider health — provider_health.json currently lists only deleted tiers and has no entry for either live brain).

Unrelated and pre-existing: the live store holds an active stranded_passes alert.

Safe point — type /clear (state saved, nothing will be lost). ok taking way too long, get tthe rest done

---
captured: 2026-08-06T00:35:01+00:00
session: 25fbd0b9-90e7-4bd0-8923-0909042ee1a1
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2499
source: founder prompt, verbatim (founder-doc-capture.py)
---

Deployed. The daemon was serving code older than every fix in the sweep. Restarted at 2026-08-06T00:26:58Z while phase=sleeping (nothing in flight): pid 8308 → 37278, now serving the committed tree through b23b977.

Three things proven live rather than asserted:

1. The backlog drain works in production for the first time — launchd.err.log at 00:29Z:
↻ tick resume pass: {'backlog': 406, 'attempted': 3, 'resumed': 3, 'kills': 3, 'orphaned': 45}
The old build printed 0/3 — dossier JSON missing on the same three rows every tick, forever. That closes the top open item from the handoff.
2. Attribution is live — rows at 00:27:35Z carry "run_id": "80d515348154".
3. New number nobody had: 45 of the 406 backlog rows are orphans — index rows in store/prospector.db with no dossier JSON on disk. Those 45 are what jammed the old drain. Uninvestigated.

The spend rail is intact — that alarm was false. Splitting store/prospector.jsonl the way guard.py:111-155 does: billed spend has never exceeded $6.03 against the $20 cap. Today's independent sum is $0.571869, matching the guard's today_spend_usd: 0.571869 to the last digit — scan_today() re-reads the persistent ledger every evaluation, so a restart cannot zero it. The scary $73.58 on 08-05 was $1.64 billed + $71.94 subscription-equivalent, which is plan allowance, not money.

I was wrong about the dry_run tick rows. I started down the "pytest is writing into the live store" path; a 5s-poll + ps trap caught the actual author: ~/.hermes/scripts/prospector-run.sh runs run_scheduled --once --dry-run and writes a tick by design, and both consumers (run_scheduled.py:379, .state-probe:66) exclude those rows. Harmless. Two Hermes-side discrepancies recorded but not changed — the script calls itself "hourly" and fires every 5 minutes, and ps caught two of its process trees overlapping.

One claim I can't make yet: ALERT.txt still shows the stale 15:29 critical. That's expected — reconciliation runs on tick completion and the tick is mid-generation — but expected isn't proven. Watcher bw7almc9r is polling for the first completed tick and will diff ALERT.txt by md5; if the banner survives a clean completed tick, reconcile_alert_txt is broken. Note that a /clear drops the notification — the exact manual check is in the handoff.

Handoff written to checkpoints/LATEST.md, plus a memory for the Hermes writer so the next session doesn't re-run that investigation.

Safe point — type /clear (state saved, nothing will be lost). hwat next

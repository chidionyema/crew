---
captured: 2026-08-13T06:58:06+00:00
session: 32aee88c-12c8-4b6c-bdc3-0be2ad301d90
cwd: /Users/chidionyema/Documents/code/prospector
chars: 1759
source: founder prompt, verbatim (founder-doc-capture.py)
---

DONE: latest code is merged and green — 79aa357, 2939 passed / 0 failed, branch now 0 behind origin/main.

Both research teams are still running in the background. Their results are durable on disk, and the handoff at checkpoints/LATEST.md records the run IDs, journal paths and resume commands so a fresh session can pick them up without re-running anything.

---
One thing to flag before you clear. The merge brought in docs/ENGINE_AUDIT_2026-08-10.md — a 22-finding engine audit that already existed on main and that this branch never had. 19 are already fixed; only #14 (MOAT_PRIMARY provisional-stamping single-operator gap) and #20 (pricing.py hardcoded fallback price) are still open. The next session's first job is to reconcile the new audit's findings against the merged tree, so nothing gets reported as a blocker that main fixed three days ago. That's step 2 in the handoff.

Two findings that survive independently of either workflow:

1. The daemon hung ~47h inside a single tick. _write_heartbeat (run_scheduled.py:147) only stamps at phase transitions and refreshes during sleep (:863) — nothing bounds tick duration — and com.prospector.watchdog is not running (- in launchctl list). It recovered on its own; cause unknown.
2. k=100 is not a money problem. At the measured $0.051/candidate, 100 candidates/day is ~$5.10 against a $20 cap. The binding constraints are vet_workers=3, claude_concurrency=4, and a 164 MB ledger that takes 108s to read. That reframes the whole scalability story away from cost.

The main checkout is untouched at d4ad901 — the merge lives in the ../prospector-latest worktree and needs a fast-forward to land. Handoff has the exact steps.

Safe point — type /clear (state saved, nothing will be lost). ok continue

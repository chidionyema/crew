---
captured: 2026-08-15T08:10:22+00:00
session: 8bad72b7-f5d1-451d-8ac0-9559c9fa26fa
cwd: /Users/chidionyema/Documents/code/prospector
chars: 1577
source: founder prompt, verbatim (founder-doc-capture.py)
---

stopo reporting and fix 
k=50 is ~2 hours today, not five. The measurement landed: mean 5.07 checks per candidate (n=2044 dossiers), 83.6s per check (n=822 live checks) → 7.1 min per candidate. At vet_workers: 3 that's 118 min for k=50. At 12 workers, ~30 min.

My 5-hour figure extrapolated from one candidate that ran all six checks; 58% stop earlier. Correcting it.

---
Where the time actually is: MODEL 83%, RETRIEVAL 17%. Faster search cannot fix this. The verdict call is already 1 per check — irreducible. Three tails carry the waste:

1. Chain-failover verdicts: 34 calls at 551s mean vs 35s normal — 4% of verdicts burning more wall-clock than the entire retrieval budget. That's claude_cli dying and falling through to MiniMax.
2. The claude_cli search-escalation tier: 11% of searches, 71% of all search time. Booked as retrieval; it's a model call.
3. Six checks sequential (verify.py:990) — right for candidates that die early, 6x latency on the survivors that become products.

On your point about design: two of the three levers are already env-tunable. The one that isn't is the one that matters — MOAT_PRIMARY is welded to claude_cli in a hardcoded frozenset with no config key, which is what makes MiniMax's throughput unusable no matter how wide we run it. That's the poor design, it's costing exactly what you said, and it's a one-line fix plus two call sites.

Handoff written with every number and the ordered plan, so the next session starts at the commit and doesn't re-derive any of this.

Safe point — type /clear (state saved, nothing will be lost).

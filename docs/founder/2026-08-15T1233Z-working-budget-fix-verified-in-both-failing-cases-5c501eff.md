---
captured: 2026-08-15T12:33:33+00:00
session: 015c5900-24bb-446f-b760-58a1f213c467
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2051
source: founder prompt, verbatim (founder-doc-capture.py)
---

WORKING: budget fix verified in both failing cases; full suite running to confirm, then I commit.

Correcting myself once: my first fix (swapping monotonic for process_time) was wrong — it changed the clock when the problem was the margin, and it broke the test in a case that had been passing.

The measured truth, taken inside pytest where conftest applies:

┌───────────────────────┬────────────────────────────────────────────────────────┐
│         case          │                         result                         │
├───────────────────────┼────────────────────────────────────────────────────────┤
│ warm, mid-file, idle  │ CPU 0.371-0.391s vs a 0.5s budget                      │
├───────────────────────┼────────────────────────────────────────────────────────┤
│ cold, run alone       │ over budget — first call pays warmup nothing amortised │
├───────────────────────┼────────────────────────────────────────────────────────┤
│ full suite at -n auto │ over budget — 12-way memory contention                 │
└───────────────────────┴────────────────────────────────────────────────────────┘

A 22% margin over a 0.39s cost was never guarding an algorithm; it was reporting how busy the machine was. It only looked stable because it always ran mid-file on an idle box. Now: process_time and a 2.0s budget, with the failure message quoting the measured baseline. The defect it exists to catch — an O(n²) window scan re-tokenising at every offset — regresses by multiples, not by 25%, so the looser budget loses nothing real.

Both previously-failing cases now pass (cold-alone, and the whole file).

---
Still on your question about the engine: generation has produced 0 candidates for ~4 hours while the drain works fine, and there are 7 finished PASSes nobody can buy. That's the one costing money. Say the word and I'll take it next — but it's a fresh investigation and this session is at ~115K resident context, so it's cheaper for you if I commit this, hand off, and start it clean. ok is generation working, eed realtine debugging

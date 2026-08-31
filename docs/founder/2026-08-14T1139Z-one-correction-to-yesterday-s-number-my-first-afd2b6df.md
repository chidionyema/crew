---
captured: 2026-08-14T11:39:46+00:00
session: b1bb43c8-b9bc-4d72-95b4-f5c2178c923b
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3928
source: founder prompt, verbatim (founder-doc-capture.py)
---

One correction to yesterday's number: my first registrable() treated service.gov.uk and gov.uk as two publishers. Fixed, and the measurement script now imports the same function the gate uses. The headline moves 434 → 470 single-publisher rulings (15.4% → 16.7%). The cost is unchanged: 1 pass of 75 flips.

Two reds in the tree are the other session's, not mine — they removed buyer_intent from UGC_ADMISSIBLE without updating tests/unit/test_admissibility.py:104, and ruff flags unsorted imports in bridge.py. Both will block a commit gate until they fix them.

---
What landed:

┌────────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────┐
│                  file                  │                                     change                                      │
├────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
│ prospector/admissibility.py            │ corroboration_reason(), registrable(), publishers(), CORROBORATION_EXEMPT_TIERS │
├────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
│ prospector/verify.py                   │ the gate, inside the existing demotion chain in verdict_for — SUPPORTED only    │
├────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
│ prospector/config.py                   │ corroboration_min_domains: 2, corroboration_exempt_tiers + loud validation      │
├────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
│ config.yaml                            │ both keys under admissibility:, measurement in the comments                     │
├────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
│ tests/unit/test_corroboration_floor.py │ new, 40 tests                                                                   │
├────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
│ tools/experiments/d5_corroboration.py  │ new, the measurement                                                            │
├────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
│ docs/RETRIEVAL_PROGRAM.md §D5          │ corrected and marked shipped                                                    │
└────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────┘

Three design calls I made and why:

- SUPPORTED only. A refutation from a single source still kills. Corroborating kills was never measured, and weakening kills is not this programme's business.
- gov.uk collapses, ac.uk does not. assets.publishing.service.gov.uk and www.gov.uk are one state; ox.ac.uk and cam.ac.uk are two universities. A site must not be able to corroborate itself from a second subdomain.
- corroboration_min_domains: 1 is the off switch, mirroring policy: off — the change is reversible by config alone, no code edit.

Two existing tests needed their fixtures given a second publisher (test_source_or_die.py, test_figure_check.py). Each still asserts its original property; the reason is written into the test so nobody later reads it as an arbitrary fixture.

The live pack b94760e86e62585a is not delisted by this — the gate rules at verdict time, not over stored dossiers. It will demote when vet --resume next reaches it, and that is when to choose delist or re-ground.

Handoff written. Safe point — type /clear (state saved, nothing will be lost).

✻ Churned for 10m 57s · 1 shell still running fair, however we are still focused on uk narket when us shold be doninant and not just california

---
captured: 2026-08-08T12:27:28+00:00
session: df788473-4339-4349-92bc-a1829f81884a
cwd: /Users/chidionyema/Documents/code/prospector
chars: 1641
source: founder prompt, verbatim (founder-doc-capture.py)
---

te, payback anchor, Could you run this?. On a 9-check pack the reconciliation reads lane ran 3 more on top, for 9 in all.

Two things worth knowing about how it got out:

Admin merge was impossible. python is a required status check and repo rules reject --admin outright, so the red gate had to be fixed, not bypassed. That made your "fix the tests first" answer the only available path regardless.

The claim-lock failure was a real defect, not a flake. _is_stale() returns True for a missing file — correct for claim(), which retries the create; wrong inside _expire(), which unlinks. So a steal arriving while the path was momentarily empty deleted whichever lock a peer had just created, and both threads held the claim. Measured 2 failures in 400 before, 0 in 1,200 after, both under 8-way load. The caller is health.py's half-open probe, so two winners meant two callers re-probing one dead brain — the exact double-spend the lock exists to prevent. It had been failing on main independently of my work.

Still open, in the handoff: the TestLoadJobs pollution (one CI run, passed on merge, would not reproduce locally in 25 attempts — I could not explain it and did not invent a fix), and the fact that "How it scores" is dead for all 15 packs sampled, so that lever needs an engine change in bridge.py plus a republish, not a storefront one. The four brainstorm items you asked me to find middle ground for are written up there with the specific middle ground for each — I had designed them but hadn't started implementing when you called ship, so nothing half-built went out you need to conclude the brainstorn ideas and no ui tests

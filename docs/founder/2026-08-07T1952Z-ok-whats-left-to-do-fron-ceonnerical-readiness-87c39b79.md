---
captured: 2026-08-07T19:52:48+00:00
session: d6619fd9-7786-4c0f-9393-e662ece6ac10
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3585
source: founder prompt, verbatim (founder-doc-capture.py)
---

ok whats left to do fron ceonnerical readiness for engine  across 9 test directories, not just tests/unit — so my current run (unit + behavioural) is narrower than the gate's scope. I'll widen it to full scope once this finishes.

Current state:

Commit: BLOCKED, nothing lost. ruff passed; pytest hit the 600s wall and was killed. HEAD unmoved at a946435, 29 files still staged, lock released. The cause is the contention I flagged, not a regression — the HHEM sidecar is still at 290% CPU, 11m41s in.

All six edits are applied:

┌─────┬─────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────┐
│  #  │                  file                   │                                    change                                    │
├─────┼─────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ 1   │ prospector/verify.py:665                │ citations filtered against {s.source_id for c in checks for s in c.sources}; │
│     │                                         │  dangling ids logged and dropped before the decisive guard                   │
├─────┼─────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ 2   │ tests/behavioural/test_source_or_die.py │ _check_holding() helper; fixed the vacuous checks=[] test; +2 new tests      │
│     │                                         │ (dangling → downgraded, mixed → keeps only the resolver)                     │
├─────┼─────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ 3   │ prospector/artifacts.py:292,300,359     │ score kwarg, fed into the stand-in Dossier                                   │
├─────┼─────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ 4   │ prospector/run.py:480                   │ passes score=score                                                           │
├─────┼─────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ 5   │ config.yaml:1113                        │ pack_data.enabled: true                                                      │
├─────┼─────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ 6   │ config.yaml:1065                        │ numeric_citation.enabled: true (shadow_mode: true retained)                  │
└─────┴─────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────┘

Two things I have not done and want to name rather than bury:
- tools/publish_passes.py:169 calls generate_artifacts with a real dossier in scope but doesn't pass it, so the republish path will also emit score_available: false even now. That's a second call site the register never counted. It's a one-line dossier=dossier and I'll add it.
- Nothing has re-verified yet. pack_data.enabled: true is live in config but no test run has confirmed the bundle actually builds with it on. That's the next receipt, not an assumption.

⏺ Running 1 shell command…
  ⎿  $ cd /Users/chidionyema/Documents/code/prospector; SP=/private/tmp/claude-501/-Users-chidionyema-Documents-code-prospector/2a751c3a-53b3-4e58-8f3a-9cff7e26480c/scratchpad; echo "=== run state ==="; grep -c . "$SP/unit2.log" 2>/dev/null; tail -5 "$SP/unit2.log" 2>&1; echo; echo "=== publish_passes: …

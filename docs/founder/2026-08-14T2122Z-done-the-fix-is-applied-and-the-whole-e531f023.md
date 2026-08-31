---
captured: 2026-08-14T21:22:24+00:00
session: 70f17edf-b4f2-41d1-921d-499750b18c97
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2456
source: founder prompt, verbatim (founder-doc-capture.py)
---

DONE: the fix is applied and the whole suite is green — 903 passed, 5 skipped, PYTEST EXIT=0 (exit captured before any pipe).

63 panels now have a way back. nav_stack.py was dead code since creation — zero importers, while its own docstring claimed nav() read it and added ← / →. Wired at the single funnel, so no panel was edited.

The adoption meter is live — floors that only rise (compose=4 group=3 glyphs=1 nav=39), a ceiling that only falls (raw_glyphs=33), and failure output that prints the migration queue.

Two things need you:

1. Restart ai.hermes.gateway (pid 84403) — none of this is live until you do; it serves the code it started with.
2. §11 decision 0 is now answered by measurement: don't rebuild, raise adoption. U7 migrates panels onto compose() in defect-rank order.

Nothing committed.

---
What the measurement changed. I proposed building Screen(...). Measuring first showed panel_chrome.compose() already is that renderer — it emits body and grid together and guarantees every legend line has buttons under it. It's just optional, and the parts that create coherence have 6% / 5% / 2% uptake against 64% for the decorative nav row. That's the entire diagnosis, and it makes the fix incremental instead of a rewrite.

Defects fixed in passing, each real:
- nav_stack read HERMES_HOME at import time — the test suite would have written your live ~/.hermes/state/nav-stack.json on every run (tests-polluted-the-production-audit-log).
- Its write was non-atomic; a crash mid-write reads back as char-0, not bad JSON.
- except: bare — it swallowed KeyboardInterrupt.
- handle_estate_action's docstring sat below code, so __doc__ was None.
- History records only view.ok renders, so ← never walks you back into an error card.

The gate that caught me: test_every_button_dispatches failed my first draft with estate:back — 1 button(s): panel_chrome.py:98. Its scanner derives handlers by reading action == "x" / action in (...) against the variable literally named action; I'd branched on a normalised local it couldn't see. Fixed by writing the branch in the dispatcher's own contract form — not by adding back to _UNBUILT.

Handoff: checkpoints/2026-08-14-ops-console-programme.md (your LATEST.md was overwritten at 21:40 by the concurrent US-money-path session).

Safe point — type /clear (state saved, nothing will be lost).

✻ Worked for 47s ok you need to conclude, nergee and ship and also audit log files to enure isues ae fied

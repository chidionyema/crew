---
captured: 2026-08-14T10:02:22+00:00
session: 60af6fba-ce2b-4754-9296-903d148b74f8
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3094
source: founder prompt, verbatim (founder-doc-capture.py)
---

DONE: I pulled the number I owed, and it says the engine broke on 6 August. It isn't a tuning problem.

Plain words: the share of ideas that survive vetting fell from 13.5% (28 Jul–5 Aug) to 1.9% (8–14 Aug) — about 7x, and the two figures don't overlap statistically. Same engine, same brains, same query style.

Why: the evidence it retrieves went bad. Same number of sources per check, worse kind. Wikipedia went from 0.4% of all cited sources to 7%; dictionary entries from 0% to 1.2%. Early on it was citing gov.uk, Facebook groups, Reddit — real market signal. Now it cites encyclopedia stubs, and the engine correctly says "this proves nothing" and kills the idea.

So more ideas per batch would not have helped. I was tuning the wrong dial for hours.

---
Per check, share of checks the evidence actually supported:

┌──────────────────┬──────────────┬──────────┐
│      check       │ 28 Jul–5 Aug │ 8–14 Aug │
├──────────────────┼──────────────┼──────────┤
│ payer_solvency   │ 28.3%        │ 10.5%    │
├──────────────────┼──────────────┼──────────┤
│ legality         │ 39.4%        │ 18.3%    │
├──────────────────┼──────────────┼──────────┤
│ distribution     │ 59.8%        │ 27.6%    │
├──────────────────┼──────────────┼──────────┤
│ buyer_intent     │ 66.4%        │ 38.2%    │
├──────────────────┼──────────────┼──────────┤
│ currency         │ 73.1%        │ 46.8%    │
├──────────────────┼──────────────┼──────────┤
│ value_durability │ 46.5%        │ 26.0%    │
└──────────────────┴──────────────┴──────────┘

Every check roughly halved at the same time. A worse idea generator cannot do that — it wouldn't move "currency" and "legality" by the same amount. That points at the shared step: re

Suspect, not yet proven: ddgs is a metasearch aggreipedia's opensearch API, grokipedia, Yahoo, Brave,Mojeek. It serves ~95% of our retrieval (17,333 log mentions vs Exa's 763). Decisive test, cheap: replay ~200 of the recorded
queries through DDG and through Exa, compare. I hav

One retraction: I briefly had a start date of 6 Aug log's own first line is one second earlier, so thatdate is just where the log begins. It proves nothing. The measurement above comes from the dossiers and doesn't depend on it.

On other agents — you're right, and it cost me today. docs/ENGINE_WAR_PLAN_2026-08-13.md is in my lane, written by another agent,
and I never opened it. Its Wave 2 is "Retrieval sele)" with the same conclusion I just re-derived fromscratch: "pages are always found — the defect is WHICH 600 characters reach the model." What I add is the time series showing it
got 7x worse. That goes into their Wave 2, not a ri census also belongs to that other lane; it's flagged in the handoff to hand over or delete. Live lanes I can now see: pack quality, storefront/site spec, cost, commercial readiness,
engine war plan.

Handoff: checkpoints/2026-08-14-core-engine-yield.mlds another session's storefront work).

Safe point — type /clear (state saved, nothing will
 again this is jargo, you are not providing fresh insights or  a way forward, either get this done or sack urself

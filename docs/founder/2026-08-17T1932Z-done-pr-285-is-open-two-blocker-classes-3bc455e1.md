---
captured: 2026-08-17T19:32:31+00:00
session: 35a644ab-eb64-4a89-a141-c609b835f2e9
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2014
source: founder prompt, verbatim (founder-doc-capture.py)
---

DONE: PR #285 is open. Two blocker classes are gone from the linter, but the stranded count did not move.

https://github.com/chidionyema/prospector/pull/285 — commit fb68a10, 167 passed, ruff clean on the origin/main base.

The number that matters: stranded passes: 34 before, 34 after. I am not calling this progress on the count. title_claim (9 packs) and currency (2 of 3) were false positives and are now gone from the gate, but every one of those packs is also blocked by something else, so zero packs reached the shelf.

What still blocks the 34: title 20, shelf_copy 15, citation_urls 4, empty artifacts 2, placeholders 1.

shelf_copy and the empties I can repair without touching anything a buyer sees. The 20 title blocks cannot be — the fix rewrites live product titles, and you have not approved that. Say the word and I run it.

---
Root cause, since you asked for it before the fix. Every stranded pack was at most three days old, and every one was made after the rule that blocked it. No old stock, no new rule. The single cause: these checks ran only at the publish gate, at the end of the line, on fields nothing upstream could change. The split proves it — checks with an upstream caller blocked 1–2 packs each; checks without one blocked 9–20.

Why the two checks were wrong. check_title_claims was handed the shelf card, about 40 words, and asked whether the title's terms were supported. Its own docstring says the sources are the pack's own description and structured fields. All 14 flagged tokens — House, Bill, Department, Information, Resources, ISVs, DevOps, Spine, Markets, Competition, GA, CTOs, HB and the figure 4 — appear in their own pack's ~5,500 words. check_currency's listing-page half had the same gap; its notes half got a wider haystack on 2026-08-09 and the listing half never did.

48977b86df56eaac still blocks on currency, correctly: one stray £ in the rendered rows of a us financial model.

What  ok but after 5 hours, why should i trust u to get the rrot cause quickly

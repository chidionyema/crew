---
captured: 2026-08-16T04:46:36+00:00
session: 53cdf64e-9f6d-4b28-ac12-ad882c8b90b3
cwd: /Users/chidionyema/Documents/code/prospector
chars: 4610
source: founder prompt, verbatim (founder-doc-capture.py)
---

DONE: one real bug found and shipped as PR #233, and my headline claim corrected.

Grounding is not our problem. I reported 36% of figures trace to no source. That was my measuring tool. numeric_citation.py was reading our own citation markers as numbers — 459782dc95f977cf became the figure 459782. That was 205 of 698 "figures" across 87 packs. The real rate is 2.7% overall, 2.1% on packs since 13 August, and most of those are our own price or arithmetic the text shows in full.

Item 1 also turned out not to be a defect: config.yaml:579-581 switches off incumbency and value_durability for the side_hustle lane on purpose, because a commoditised niche is a good sign there.

Six items remain live. The next one is well specified and I stopped rather than half-start it.

---
Verified state of all eight

┌─────┬──────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────────┐
│  #  │             Item             │                                        Verdict                                         │
├─────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ 1   │ Packs skip the competition   │ Not a defect. Deliberate lane design. Item 8 is the real version.                      │
│     │ check                        │                                                                                        │
├─────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ 2   │ price_comparables returns    │ Live. 9 of the last 29 packs, from 17–42 fetched pages on 3 queries, rejecting         │
│     │ nothing                      │ nothing. The extractor, not retrieval.                                                 │
├─────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ 3   │ No bottom-up money model     │ Live. No market-sizing code anywhere in prospector/.                                   │
├─────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ 4   │ why_now is unchecked         │ Live, and blocked. See below.                                                          │
├─────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ 5   │ Figures not traced to source │ Fixed — PR #233. Was mostly a measuring bug.                                           │
├─────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ 6   │ One-shot adversarial review  │ Live. critique.py exposes only critique_revise.                                        │
├─────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ 7   │ Composite cannot rank        │ Live. Last 29 packs span 2.50–3.55, avg 2.87. A killed idea scored 3.60.               │
├─────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ 8   │ Wrong ambition tier          │ Live. Last 29: 11 side_hustle, 11 smb, 5 untagged, 2 venture.                          │
└─────┴──────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────┘

All of items 2, 7 and 8 were re-checked on the last 29 packs, not the back catalogue — you were right that the old data misleads. July read 18% untraceable and August 38%, purely from engine changes.

The next task, specified

Nothing records when our evidence was published. 97% of source rows have no published_at. retrieval.py:268 only copies a date the search provider returned, and DuckDuckGo doesn't return one. Nothing reads a date out of the page we already fetched and parsed.

That blocks item 4 — a why_now check needs a dated trigger — and undated evidence is its own weakness in front of an investor. The change is contained: fetch_page_text returns a bare string today, so it needs a sibling returning (text, published_at), reading article:published_time, meta[name=date], JSON-LD datePublished and <time datetime>. Deterministic, no model call. The raw HTML is in hand at retrieval.py:565.

Handoff written to checkpoints/2026-08-16-research-quality.md, with the remaining order: dates → item 2 → item 3 → item 6 → item 8 → item 7. PR #233 is open against main and needs your merge.
 ok what next

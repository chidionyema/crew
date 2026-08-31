---
captured: 2026-08-16T03:13:37+00:00
session: 9ddde4bb-7cfc-445d-b504-bf96307acbd4
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2630
source: founder prompt, verbatim (founder-doc-capture.py)
---

streanlit is broken did u test 
Telegram: closed. Merge: fixes done, suite still running (~84%). Research: first real number in hand.

---
Merge — both red tests were real defects in the uncommitted work, both fixed:

1. routing_problems/routing_advisories crashed on a config with no moat_primary — _chain(list(None)). _chain already documents "a bare string, a list, or nothing"; the list() defeated it. prospector/ops/routing.py:79,107.
2. Fixing that exposed a realer one: the roster fence then refused every unrelated edit to a config missing that key — you couldn't move confidence_floor until you'd fixed a roster the write doesn't touch. Now it subtracts problems the on-disk config already has and blocks only what the write introduces; set_moat_primary keeps the unfiltered fence.
3. Swallow ratchet: 8 new tier-1 sites. Narrowed the except at 5 sites where the condition is known, used the tool's own counted # swallow-ok: waiver at the 3 that are best-effort by contract and already render or log the failure. Waiver baseline 1→5, which that test explicitly requires be argued in the commit message.

Targeted re-run: 304 passed, 1 skipped. The first full run reported green and wasn't — | tail handed back tail's exit 0. Full suite is re-running with the real status captured.

Research — the number, from 84 PASS dossiers / 8,407 pooled passages, zero network (dossiers store the retrieved passage inline, so figures resolve offline):

55.4% of distinct quantitative figures we assert appear literally in a passage we cited. But the split is the finding, not the headline: verdict surfaces are 87–93% grounded (check.rationale 89.7%, marketing 93.0%); the artifacts a buyer actually reads are 53.5%. Reading the misses, most aren't fabrications — they're our own prices, margins and projections (£49, 40% COGS, £50 × 50 orders = £2,500), which no web passage can corroborate. The defect is that artifacts don't mark which figures are retrieved fact, which are our assumptions, and which are arithmetic on the two. One dossier already does it right — "the $3,000 lawyer cost and the $499 price are both assumptions — unverified" — so the generator can; it just isn't required to.

I got 33.2% on the first pass and it was wrong: SVG polygon coordinates and 16-hex citation IDs were being read as claims. Both fixed before I quoted anything.

Next step there is to split the 1,242 ungrounded figures into our-decisions / derived / genuinely-unsupported — the 55.4% must not be quoted as a fabrication rate before that split exists.

Handoff written with the full merge path, the commit split, and both extractor traps.

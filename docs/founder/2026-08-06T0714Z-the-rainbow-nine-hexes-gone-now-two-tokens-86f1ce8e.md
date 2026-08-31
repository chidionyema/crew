---
captured: 2026-08-06T07:14:20+00:00
session: a496bbba-cbdc-496e-bd35-05e746983d2c
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3171
source: founder prompt, verbatim (founder-doc-capture.py)
---

The rainbow. Nine hexes gone, now two tokens (bg-subtle tagged, bg-border-strong untagged). You framed the counterweight as "the dots are a genuine discovery affordance across 61 cards" — that turned out not to survive counting. Twelve sectors were mapped onto eight palettes, so four pairs collided outright: employment_pay/creative_rights both violet, housing_rental/energy_planning both teal, trades_construction/retail_inventory both amber, professional_services/other both slate. A hue that can't separate those isn't identifying a category, so there was no affordance to trade away. Verified on the rendered shelf: 61 dots, 2 distinct colours, both tokens. New noArbitraryHex.test.ts scans the whole tree — proved non-vacuous by reintroducing bg-[#E11D48] and watching it fail by name.

The fold. Panel moved below the shelf on mobile only; desktop keeps it beside the claim. Card positions after the change, measured on the built page: 390×844 → 140px visible, 360×780 → 51px, 430×932 → 267px, desktop unchanged. This reinstates the hidden lg:block/lg:hidden pair that index.tsx:692 had recorded as a bug, so I dealt with that recorded reason rather than ignoring it: the objection was that display:none doesn't stop effects running twice, and LiveKillCard.tsx now has no useEffect, useState, fetch or timer — with the timer independently forbidden by an existing assertion that reads its source.

Worth knowing why this reached you as a review finding rather than a test failure: the suite runs one Playwright project at 1280×720, so a mobile regression was structurally invisible. Guarded now at three widths — 360×780 was the worst case and the one a single 390×844 check would have missed widest.

Gates: vitest 751/51 files, playwright 27 passed/1 skipped, tsc clean, POPDD PASS chain valid.

Shipped: branch pushed, PR #111 open → main (169 files, +13302/−3670 since the merged #110). CI only fires on PRs to main, so the PR is the evidence; I'm watching the checks and will report the verdict. I did not merge — that's yours, and it needs gh pr merge --squash --admin since main requires signed commits.

Three things for you:

1. Two copy claims in the PR are false and I deliberately did not rewrite them — they need a wording decision, not a code change. "Every pack clears the six checks" is untrue for the 21 lane-variant packs, where value_durability and incumbency never run; it appears in 12+ files. And the pack page prints the engine's real denominator, which varies: across 61 live packs, 40× "6/6", 14× "8/8", 3× "7/8", 3× "9/9", 1× "6/8" — so a buyer reads "survived all 8 checks" on the money page while every other page says six.
2. PR #111 carries the concurrent dynamic-pricing session's work too, per your "take in all the work". It's not a single-topic PR and shouldn't be reviewed as one. That session has since added two more commits on top of mine (1a6cced, ac6c5e1) that are unpushed — theirs to push, not mine. Their commit also absorbed the em-dash fix I'd made in client.ts, so that loose end closed itself.
3. The prod server is still up on :3111 (node PID 11593). Leaving it — the other session address all properly and carefully

---
captured: 2026-08-09T01:15:12+00:00
session: c30f7b1d-73dd-4989-b211-68dfd489bbf0
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2056
source: founder prompt, verbatim (founder-doc-capture.py)
---

3 files changed, all verified:

1. MarketingLayout.tsx — footer "Legal" links (Terms/Privacy/Refund) and the support email link had zero padding; the "Store" column beside them had already been fixed to 44px targets and this one was missed. Applied the identical treatment. Measured before/after: 15–17px → 41.6px / 45.6px.
2. index.tsx (featured card) — the "New this week" heading and the space around the card had no opaque background of their own, only the card did, so ticker text showed through around it. Wrapped the whole slot in bg-surface (the same token the card already uses). Measured: heading's nearest ancestor background is now rgb(255,255,255) (opaque) — confirmed by screenshot, no bleed-through.
3. index.tsx (method band) — a section was drawing 3 rules where it should draw 1: the shared band system already gives every section a full-bleed bottom border, and this one also set an explicit border-y at content-width (1280px) directly against it — a doubled, offset hairline at any width over 1280px. Removed the redundant explicit border.
4. faq.tsx — root cause of "FAQ centered, rest left-aligned": FAQ ran its content at 896px (4xl) while every other content page runs 1152–1280px (6xl/7xl). Widened FAQ's band to 6xl (matching how-it-works/kill-log/pack-detail, its closest sibling page type) to fix the left-edge mismatch — but a 2026-08-06 comment in the same file documented that this exact width was previously tried and reverted because it pushed answer text to a ~110-character line. So I kept the band at 6xl for alignment and separately capped the search/filter/accordion content at max-w-3xl for reading measure — same band-sets-the-edge / inner-div-sets-the-line-length split the codebase already uses for PageHero. Measured: hero title, search box, and accordion now share x=184 (same left edge), and the answer measure is back under control.

Screenshots of both pages at 1440px are at .../scratchpad/shots-after/. Nothing committed — sitting as local changes per your standing rule (commit only when asked). full sweep

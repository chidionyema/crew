---
captured: 2026-08-14T08:38:23+00:00
session: d2ba2ba0-a9a9-44e0-8af4-a9f6f386d331
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2305
source: founder prompt, verbatim (founder-doc-capture.py)
---

DONE: /pack/[id] is on the instrument system — commit 0a5b9a1, POPDD PASS, web: PASS 842 passed 0 failed, tsc 0. Step 4 of 6 closed.

The headline finding is not a design change. The Buy button has never stayed on screen.

sticky top-24 has been on the checkout rail for months. It computes as sticky, the class is in the DOM, the source reads correct — but SectionBand's wrapper was overflow-hidden, which makes it a scroll container and therefore the containing block for every descendant sticky. Probed at scroll 2,200: railTop -2007 inside a parent 4,082px tall. On a 5,190px money page the buy panel left the screen after one scroll and the right half of the page was white for ~3,400px. One word — overflow-clip — clips identically without creating a scroll container. Now pinned at top: 96 at every depth, bottomInView true at both 900px and 768px tall.

Two features came back for free, built and invisible for the same reason: /sample's contents rail including its scrollspy highlight, and the same rail on /privacy, /terms, /refund.

Also on the page:
- 94.5% was unlabelled, in the largest type on the page, sitting immediately left of "This one came through the filter" — which reads as the share that came through. It's the share that was killed. It now says so.
- "Could you run this?" was three cards faking a grid — two of three carried sm:col-span-3, so Market and Who pays each sat alone in a 976px box holding one line. 390px and three borders for three fields → one spec sheet with an aligned label column, 220px.
- The masthead plate now carries the same radial every other instrument surface has; it was the widest band on the site and the only flat fill.

Swept 13 routes × 2 viewports: all 200, no horizontal overflow. No test needed updating.

I've written the sticky trap to memory — it's the kind that survives source review and passes every static check.

---
Next is step 5: /kill-log, /how-it-works, /sample. Note /kill-log renders a 26,875px page at desktop and 36,847px on mobile, so it needs a different treatment from the others.

Two files on that list — kill-log.tsx and sample.tsx — currently carry uncommitted edits from the concurrent session, so I'll work around their hunks or wait for them to land.

Safe point — type /clear (state saved, nothing will be lost).ok

---
captured: 2026-08-14T19:41:59+00:00
session: ecb8fc72-2b08-47a7-8ed2-9a85a575930e
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2263
source: founder prompt, verbatim (founder-doc-capture.py)
---

also Here’s the thing to fix first: you’re describing feelings (“looks shabby”), and the agent needs symptom + location + expected. Below is a paste-ready report.

Paste this to your agent:

Pack list page, mobile viewport (~390px, iOS Safari). Screenshots attached. Fix at the container/layout level, not with per-row hacks.

Meta row children overlap instead of laying out. The count number renders on top of the adjacent element — “48” over “US rules” renders as “48S rules”; “9” over the sparkline. Same on rows 3, 4, 5. Expected: category, count, and badge sit in a row with real gaps, no collision.
Sparkline overflows the card. It runs past the card’s right padding to the viewport edge and gets clipped. Expected: constrained to the card, fixed max-width.
Titles truncate far too early. “Court case dige…” cuts at ~50% of available width while empty space remains. Likely a missing min-width: 0 on the flex text column. Expected: title uses all space up to the price, then ellipses.
Meta row schema is inconsistent between rows. Some rows show category + count + sparkline; others show count + “US rules” and no category or sparkline. Expected: one field order for every row, with empty slots collapsing gracefully.
Price formatting inconsistent. “£49” next to “£49.99”. Expected: always 2dp.
Thumbnails render as solid black blocks on every row — images missing or failing to load. Expected: real image or a designed placeholder.
Sticky “Narrow it down” pill overlaps card content, hiding the price on the Life insurance row. Expected: it should not cover content — add bottom padding to the list equal to the pill height.
Bottom CTA “Show the other 35 UK packs” is clipped by the viewport.
Data bug: rows in the UK list are tagged “US rules”.
Two things that make this land better: attach both screenshots and state the viewport width, and tell it to reproduce at 390px before and after. Otherwise it’ll fix at desktop width and declare victory.

Items 1–3 are almost certainly one root cause — a flex row without min-width: 0 and without flex-shrink control. Worth telling it to look for that specifically rather than patching each symptom., address the colour audit also and other fidingss and lastly this needss to be done super fast, no ui tests etc

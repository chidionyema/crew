---
captured: 2026-08-16T04:39:45+00:00
session: 0f781f13-a5de-4e5e-bfb1-40786b5420b0
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2088
source: founder prompt, verbatim (founder-doc-capture.py)
---

The one lint error (kill-log.tsx:94, direct fetch) is pre-existing — the same line is on origin/main, and CI's nextjs job runs typecheck, vitest and build only, no lint fix it, alo Good news first — the category labels have moved to caps sans, which is the single biggest improvement so far. The colour is still per-category, but the ransom-note effect is largely gone.

The truncation is a layout problem wearing a text-length costume. Phrasing for the agent:

1. The title column is being squeezed by a fixed price column.

“The row splits into a title column and a price column at a fixed ratio, so titles get roughly 55% of the row while the price column sits mostly empty — there is a full title’s worth of dead space under every price. Change the price column to flex: 0 0 max-content so it takes only the width the price needs, and let the title column take the remainder.”

2. Titles are being cut by character count, not clamped by line.

“Titles are truncated with a JS substring at a fixed character count, so they cut mid-word with room still left on the line. Replace with CSS -webkit-line-clamp: 2 on the full string, so the browser fills each line completely and only cuts where it must.”

3. The description clamps to one line.

“Descriptions clamp at one line. Set two.”

4. The “seen” badge is inside the title block.

“The seen badge sits top-right inside the title’s own column, forcing the title to wrap early around it. Move it into the meta row alongside the category label.”

5. Worth raising separately — every title ends in the same place. “Freelance pay benchmarks for UK…”, “Weekly judgment brief for UK…”, “HMRC £100 late-filing penalty appeals for UK…”. Three consecutive rows truncating at the identical word makes the list look like one repeated item. Even with the layout fixed, that pattern will persist because the titles share a construction. Consider stripping the trailing “for UK [audience]” clause at render time in list contexts and showing it in full only on the pack page — the audience is already implied by the category label directly beneath.

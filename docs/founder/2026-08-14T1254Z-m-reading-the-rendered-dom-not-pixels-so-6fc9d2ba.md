---
captured: 2026-08-14T12:54:02+00:00
session: ecb8fc72-2b08-47a7-8ed2-9a85a575930e
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3312
source: founder prompt, verbatim (founder-doc-capture.py)
---

’m reading the rendered DOM, not pixels — so I can’t judge your type scale, colour or spacing directly. But most of what reads as “shabby” here isn’t taste, it’s inconsistent data shapes rendering through the same component. That’s diagnosable from markup, and it’s the thing you can hand an agent.

The card grid is the main offender

Descriptions truncate mid-word with no ellipsis, at different lengths: “…vendors in their stack”, “…lock in today’s material prices for a”, “…priced, dated change”. A grid of sentences that stop randomly looks broken before anyone reads it. Fix: hard character budget, enforced at write time, not CSS clamp.
Cards carry different fields. Some have a category chip, some don’t (NHS care fee reclaim, Business rates challenge, Retention chasing, Holiday pay). Some show a source count, most don’t. Some render “View pack”, most don’t. Three card variants masquerading as one.
Titles mix registers: brand names (SunsetLedger, TipperWatch, TopCoat) sit next to descriptive sentences (“Business rates challenge service for UK shop owners”). One wraps to a line, the other to three. Ragged card heights read as amateur even when spacing is perfect.
Prices mix £149.99, £79, £49, £199, £29.99. Adjacent in a grid, that inconsistency is visible as texture.
Structural problems

The homepage is a landing page and a store index welded together: hero → featured pack → stats → grid → filter quiz interrupting the grid → more grid → US section → email capture → kill ticker → what’s inside → sample evidence → closing CTA. Eleven full-width bands with no rhythm change. Nothing tells the eye which section matters. That’s your “worst on desktop” — wide viewports expose flat hierarchy mercilessly.
Four competing filter mechanisms: search, sort, category list, and the “tick what you’re good at” quiz. Pick one primary.
The kill-count (1,364 / 1,444) appears four times. Your best asset, spent to exhaustion by the second screen.
SunsetLedger renders twice. “Browse the packs” twice. “Read the kill log” three times.
The logo string comes through as “MumchimpMumchimp” in header and footer — likely an image plus an unhidden text node. Check that; it may be visible.
Count math doesn’t reconcile: 62 packs, ~45 shown, “Show the other 37”.
The one I’d act on first

Your deliverable is 8 .md files in a zip, presented as an ASCII directory tree with ├── and └──. Your buyers, per your own packs, are mobile nail techs, tipper drivers, family carers, dog walkers. A terminal file tree and Markdown are a developer’s artefacts. The whole visual register — near-black chrome, “the engine”, “kill log”, evidence records — is dev-tools/YC. If the actual buyer is an indie hacker, the pack subjects are the mismatch. If it’s the sole trader, the design is. Right now the site can’t tell me which, and that ambiguity is doing more damage than any spacing issue.

Smaller

“14-day money back / Every claim sourced / One-time payment” sits below the final CTA. Those belong beside the first price the eye lands on.
US packs priced in £, with $295 inside the description. Fix or it undermines the sourcing claim.
Nav: logo, “Catalogue” and the homepage are all /. Two of three are redundant.
Email capture appears to render two buttons (“Email me if a pack survives” / “Tell me when one survives”).

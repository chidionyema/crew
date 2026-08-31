---
captured: 2026-08-15T19:56:07+00:00
session: 42f418ad-8bc6-4e2b-aa8b-a40da39a0308
cwd: /Users/chidionyema/Documents/code/prospector
chars: 1569
source: founder prompt, verbatim (founder-doc-capture.py)
---

In the audience filter tiles, the count sits as an inline sibling of the label rather than in its own right-aligned column. Single-digit counts therefore have no fixed slot, so ‘4’ lands hard against the end of ‘Suits an audience’ while ‘15’, ‘32’ and ‘24’ sit clear of their labels. Nothing aligns vertically across the 2×2 grid. Fix: make each tile a flex row with justify-content: space-between, put the count in a slot with min-width: 2.5ch, text-align: right, and font-variant-numeric: tabular-nums. Counts should share the label’s typeface and use one weight and one grey across all tiles.”

The tabular-nums bit matters — proportional figures make ‘1’ narrower than ‘3’, so even matched digit counts won’t line up.

On “Suits”:

Worth flagging that the pattern is already broken, which is probably part of why it grates. “Suits builders” means suits people who build. “Suits an audience” means the pack requires you to have an audience. Two different grammatical relationships wearing the same label, so the row reads as a mistake even before you get to the word itself.

The section already speaks first person — “Show me packs I could actually run”, “Tick what you’re good at”. Match it:

I can build · I can sell · I can run operations · I have an audience

That fixes the grammar collision (the fourth is now honestly a different kind of claim), matches the surrounding voice, and drops a word that’s doing no work. If you want them shorter for the tile width: Building · Selling · Operating · Have an audience — though the mixed lengths there are less tidy.

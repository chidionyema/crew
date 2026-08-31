---
captured: 2026-08-15T18:02:21+00:00
session: 0c5421cf-3f28-415a-99ac-a6381ae54271
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2243
source: founder prompt, verbatim (founder-doc-capture.py)
---

Navy button, black price — that’s landed correctly.

For the new issues, the phrasing that works on an agent names the mechanism, not the symptom. “The card looks squashed” gets you a padding tweak; the versions below get you the actual fix.

Compounding container padding — pack sample card, image 2. “The excerpt is nested three levels deep (outer grey frame → stacked-card wrapper → inner card), each contributing its own horizontal padding. The effective text column is roughly 55% of viewport width, so the excerpt wraps at four words per line. Collapse to a single padded container on viewports under 640px.”

Measure/leading mismatch — same card. “Line-height is set for a 65-character measure but the actual measure is ~25 characters. Short lines with generous leading read as disconnected fragments. Tie line-height to the realised measure.”

Over-truncation — same card, tab row. “The tab label truncates to ‘The S…’, which carries no information, while the sibling tab ‘Everything we read, once’ renders in full. Tabs are sharing width by content length rather than by equal fraction or minimum legible width.”

Edge-bleeding carousel with no scroll-snap — “Narrow it down” section, image 1. “The category chip carousel clips items at both viewport edges mid-scroll (’…efits claims’, and a partial card on the right). No scroll-snap alignment and no start/end gutter, so no scroll position is ever visually resolved.”

Off-palette accent reappearing — same carousel. “The chip icons render in mustard/gold, which is outside the palette and reintroduces the per-category colouring we removed from the catalogue cards.”

Redundant filtering affordances — image 1, whole section. “Three separate filter mechanisms stack vertically: a search field, a horizontal category carousel, and a ‘Show me packs I could actually run’ checkbox grid. Same job, three interaction models, no stated relationship between them.”

Orphaned grid item — checkbox grid, image 1. “The tick grid is two-up but has an odd item count, leaving ‘Suits ope…’ alone on the final row with a trailing gap.”

And the persistent one: the “Narrow it down” pill is still floating over content — now sitting on top of the source citation at the bottom of the sample card.

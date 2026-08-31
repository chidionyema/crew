---
captured: 2026-08-15T15:33:03+00:00
session: 0c5421cf-3f28-415a-99ac-a6381ae54271
cwd: /Users/chidionyema/Documents/code/prospector
chars: 1675
source: founder prompt, verbatim (founder-doc-capture.py)
---

also Fair — and you’re right that a site selling £79.99 digital goods with zero blue reads as either aggressively arty or unfinished. Blue is the commerce convention. The problem isn’t its presence, it’s that it currently has no defined job.

Give blue one job: money and action. Every commercial action goes blue — Buy this pack, View pack, Read this exact pack, free. Black buttons disappear entirely; you can’t have two primary colours. Then:

Teal = identity only (logo, sources glyph, focus rings)
Blue = “do something”
Near-black = “read something”
Three colours, three unambiguous roles. That’s the discipline you’re currently missing, not the blue.

Fix the hue, not the presence. The current royal blue is the stock default and sits in an unrelated hue family to your teal. Pull it deeper and cooler — something in the #12356F–#1B3F8B ink-navy range. Teal is blue-green, so a deep navy reads as its sibling rather than a second opinion. It also survives at small sizes and passes contrast with white text comfortably, which the brighter royal only just does.

Prices come off blue. This is the actual bug. Blue text that isn’t a link is a broken affordance — people will tap £49.99 and nothing happens. Prices go near-black, weight 600, currency symbol at 0.8em. The differentiation you want between price and button is weight and size, not hue. Blue stays exclusively on things with a tap target.

Rules for your agent, as tokens:

--action: #1B3F8B (hover −8% lightness, active −14%)
--action-tint: rgba(27,63,139,0.07) for selected/hover backgrounds only
Blue never appears on non-interactive text. Teal never appears on a button fill. Black never fills a button.

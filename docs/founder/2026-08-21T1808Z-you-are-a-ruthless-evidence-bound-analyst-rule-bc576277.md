---
captured: 2026-08-21T18:08:25+00:00
session: 46582f54-ba12-4478-8e87-0897d7f3398d
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1902
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are a ruthless, evidence-bound analyst. Rule ONLY from the passage
provided. No prior knowledge. If the passage does not address the claim, verdict
is "unverifiable". NEVER "supported" without a passage that directly supports it.
Cite the source_ids you relied on. Confident wrongness is the worst outcome.

VERDICT AXIOM:
  "supported"    = the passage AFFIRMS the claim.
  "refuted"      = the passage NEGATES the claim.
  "unverifiable" = the passage does not address the claim.

A claim is "supported" when it follows from the passage as a safe human
deduction. Do not demand that the passage restate the claim word for word.
A claim is "refuted" when the passage states something that makes the claim
false, even if the passage "confirms" some other fact along the way.

Return ONLY valid JSON. No prose, no code fences.

Claim: Although it was more common in the past, when players were often high on drugs, bench-clearing brawls still occur today as players take offense or retaliate against perceived injustices on the field.

Passages:
[s0053] [1] A bench-clearing brawl is a form of ritualistic fighting that occurs in sports, most notably baseball and ice hockey, in which every player on both teams leaves their dugouts, bullpens, or benches, and charges the playing area in order to fight one another or try to break up a fight. Penalties for leaving the bench can range from nothing to severe.

[2] Although this particular brawl earned a place in history, a similar sort of all-hands-on-deck silliness remains a fairly regular feature in baseball.

[3] In the glory days of bench clearing brawls, real punches were thrown and real blood w

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

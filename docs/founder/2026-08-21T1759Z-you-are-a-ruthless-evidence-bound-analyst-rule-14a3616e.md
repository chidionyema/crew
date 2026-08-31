---
captured: 2026-08-21T17:59:38+00:00
session: 17e1cac9-8533-4203-8dce-5678ec6965a6
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1812
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

Claim: Actor Jon Cryer recreated his iconic dance scene from the 1986 film "Pretty in Pink" on the "Late Late Show."

Passages:
[s0042] Duckie's still got moves. On Tuesday night's "Late Late Show" on CBS, actor Jon Cryer reprised the character's record-store dance to Otis Redding's "Try a Little Tenderness," right down to the wall-dancing, the counter-bashing and, of course, the trademark white shoes. In the original scene, one of the best-loved bits from the 1986 John Hughes film, Cryer dances around a record store, lip-syncing the song as he tries to win the affection of Molly Ringwald's Andie. In Tuesday's recreation, he dances in tandem with host James Corden, who tweeted that he'd "fulfilled a childhood dream" by re-crea

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

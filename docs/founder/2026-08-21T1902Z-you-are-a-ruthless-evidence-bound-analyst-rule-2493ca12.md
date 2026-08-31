---
captured: 2026-08-21T19:02:47+00:00
session: fda97c24-c99b-4006-89ab-54531f8a2f39
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1539
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

Claim: Currently, Geranium is the most expensive restaurant in Copenhagen.

Passages:
[s0156] Within 4 blocks Copenhagen Restaurants Most Expensive Restaurant Top 10 Best Most Expensive Restaurant Near Copenhagen Sort: Recommended All Price Open Now Good for Dessert 1 . Noma 4.5 (51 reviews) Modern European Danish Scandinavian $$$$ Christianshavn This is a placeholder Upscale “this restaurant so long as he remains active at Noma. The service is unparalleled.”

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

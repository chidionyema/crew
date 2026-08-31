---
captured: 2026-08-21T18:56:58+00:00
session: 0a22eb12-a60a-4ed3-bf67-220c82dc6a26
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1845
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

Claim: Total cooking time will depend on the thickness of the tuna steaks, but it should take around 15-20 minutes for a 1-inch (2.5 cm) thick steak.

Passages:
[s0145] {'question': 'how to cook the perfect tuna steak', 'passages': 'passage 1:Bake the tuna. Place the baking dish in the preheated oven and bake until the skin is no longer pink and flakes when poked with a fork, about 10 to 12 minutes. The actual cooking time will depend upon on how thick your steaks are.hi tuna steaks are mostly grilled or seared to bring out the best in their flavour, but you can also bake them to reach a different texture. In case you are buying a piece of sushi-grade tuna, you can forego cooking and serve it raw. 1  Prep time (Searing): 10 minutes. 2  Cook time: 4-5 minutes.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

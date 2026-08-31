---
captured: 2026-08-21T18:57:19+00:00
session: 90541c2a-9bf6-4224-84ea-b272d2a5fb8c
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3061
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
[s0145] {'question': 'how to cook the perfect tuna steak', 'passages': 'passage 1:Bake the tuna. Place the baking dish in the preheated oven and bake until the skin is no longer pink and flakes when poked with a fork, about 10 to 12 minutes. The actual cooking time will depend upon on how thick your steaks are.hi tuna steaks are mostly grilled or seared to bring out the best in their flavour, but you can also bake them to reach a different texture. In case you are buying a piece of sushi-grade tuna, you can forego cooking and serve it raw. 1  Prep time (Searing): 10 minutes. 2  Cook time: 4-5 minutes. 3  Total time: 15 minutes.\n\npassage 2:1 Place the tuna steaks in the marinade and turn to coat. 2  Cover, and refrigerate for at least 30 minutes. 3  Preheat grill for high heat. 4  Lightly oil grill grate. 5  Cook the tuna steaks for 5 to 6 minutes, then turn and baste with the marinade.6  Cook for an additional 5 minutes, or to desired doneness. In a large non-reactive dish, mix together the orange juice, soy sauce, olive oil, lemon juice, parsley, garlic, oregano, and pepper. 2  Place the tuna steaks in the marinade and turn to coat. 3  Cover, and refrigerate for at least 30 minutes. 4  Preheat grill for high heat. 5  Lightly oil grill grate.\n\npassage 3:1 Preheat grill for high heat. 2  Lightly oil grill grate. 3  Cook the tuna steaks for 5 to 6 minutes, then turn and baste with the marinade. 4  Cook for an additional 5 minutes, or to desired doneness.5  Discard any remaining marinade. In a large non-reactive dish, mix together the orange juice, soy sauce, olive oil, lemon juice, parsley, garlic, oregano, and pepper. 2  Place the tuna steaks in the marinade and turn to coat. 3  Cover, and refrigerate for at least 30 minutes. 4  Preheat grill for high heat. 5  Lightly oil grill grate.\n\n'}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

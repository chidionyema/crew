---
captured: 2026-08-21T17:46:44+00:00
session: 50c24060-3d37-4998-a323-f2c6b20e9639
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3156
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

Claim: Turn the ribs, brush again, and bake for an additional 10 minutes.

Passages:
[s0024] {'question': 'how to cook marinated beef ribs', 'passages': 'passage 1:Preheat oven to 350F. Season ribs with salt and pepper. Lay across a rack in a roasting pan or baking sheet and bake 10 minutes. In a small bowl, combine water, lemon juice, and red pepper flakes.Brush over top side of ribs and bake an additional 10 minutes. Turn, brush again, and bake 10 minutes more.Set aside to cool. Combine marinade ingredients in a large bowl.Add roasted ribs and toss to coat. Cover with plastic wrap and refrigerate a minimum of 4 hours or as long as 24. Preheat grill or broiler. Grill ribs for 2 minutes per side and serve immediately.urn, brush again, and bake 10 minutes more. Set aside to cool. Combine marinade ingredients in a large bowl. Add roasted ribs and toss to coat. Cover with plastic wrap and refrigerate a minimum of 4 hours or as long as 24. Preheat grill or broiler. Grill ribs for 2 minutes per side and serve immediately.\n\npassage 2:Serve ribs with remaining barbecue sauce on the side. For the barbecue sauce. In a small saucepan, melt butter over medium heat. Add remaining ingredients, whisking to combine. Bring to a boil, then reduce heat to a simmer.Allow to cook until thick, approximately 10 minutes.erve ribs with remaining barbecue sauce on the side. For the barbecue sauce. In a small saucepan, melt butter over medium heat. Add remaining ingredients, whisking to combine. Bring to a boil, then reduce heat to a simmer.\n\npassage 3:1 Preheat the oven to 325°F. 2  Drain the ribs (reserving the sauce), and place them in a large roasting pan, bone-side down. 3  Brush with sauce, and bake for 30 minutes. 4  Remove from oven, and turn the ribs over, brush with additional sauce, bake for another 30 minutes. Drain the ribs (reserving the sauce), and place them in a large roasting pan, bone-side down. 2  Brush with sauce, and bake for 30 minutes. 3  Remove from oven, and turn the ribs over, brush with additional sauce, bake for another 30 minutes.\n\n'}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

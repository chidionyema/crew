---
captured: 2026-08-21T19:11:41+00:00
session: 484537c1-3b9d-4e83-9d72-d88b0a616e13
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2349
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

Claim: Keep it covered with plastic wrap.

Passages:
[s0173] {'question': 'how to cook rack of lamb on the grill', 'passages': 'passage 1:1 You can season to taste but this rack of lamb recipe is quite good with ample salt, if you like that kind of thing.  Next, put the herbs and garlic in a small bowl and add enough dry white wine to make a slurry or paste. Rub this garlic/herb mixture thickly over all the exposed surfaces of meat on the rack of lamb.\n\npassage 2:How to make the grilled rack of lamb recipe: 1  After trimming your rack of lamb and chopping the herbs and garlic, rub coarse salt and black pepper into all the surfaces of the meat.  Next, put the herbs and garlic in a small bowl and add enough dry white wine to make a slurry or paste. Rub this garlic/herb mixture thickly over all the exposed surfaces of meat on the rack of lamb. Place it in a shallow dish or bowl, pour over the remaining bit of wine and cover. Marinate about 2 to 4 hours.\n\npassage 3:Remove the rack of lamb from the refrigerator 90 minutes before you want to cook it to warm up to room temperature. Keep the meat covered with plastic wrap the whole time. Preheat a gas grill to 400 degrees Fahrenheit. If you are using a charcoal grill, preheat the grill for 20 minutes.\n\n'}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

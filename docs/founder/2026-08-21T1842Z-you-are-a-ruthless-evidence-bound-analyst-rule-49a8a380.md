---
captured: 2026-08-21T18:42:19+00:00
session: 889403f4-b671-44fd-bc1c-53e8520e7724
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1777
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

Claim: Note that if you prefer a creamier soup, you can also add cream in step 2.

Passages:
[s0117] {'question': 'how to make potato leek soup', 'passages': 'passage 1:Heat the olive oil in a large, heavy soup pot over medium heat and add the onion, leeks and a pinch of salt. Cook, stirring, until tender, about 5 minutes. Add the garlic and cook, stirring, until fragrant, 30 seconds to a minute. Add the turnips, potatoes, water or stock, salt to taste, and the bouquet garni.\n\npassage 2:Method. 1  Heat the oil in a large pan and add the onions, potatoes and leeks. Cook for 3-4 minutes until starting to soften. 2  Add the vegetable stock and bring to the boil. Season well and simmer until th

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

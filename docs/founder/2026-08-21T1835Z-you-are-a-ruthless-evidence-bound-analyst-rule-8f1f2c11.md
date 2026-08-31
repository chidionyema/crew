---
captured: 2026-08-21T18:35:26+00:00
session: ff41d549-4772-40cd-b3fe-fd35a4f13808
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1821
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

Claim: The driver's seat is positioned on the side of the car to allow the driver to see traffic coming from both directions.

Passages:
[s0102] When you are driving in a foreign country, it can be confusing to know which side of the road the driver should be on. In some countries, like the United States, the driver sits on the left and stays on the right side of the road unless overtaking.
In other countries, like England, the drivers sit on the right and keep left in traffic unless overtaking.
The driver sits on the left side of the car on the American continents, continental Europe, Africa, and parts of Asia, making up roughly two-thirds of world countries. In Britain and its former colonies, the driver sits on the right side of the

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

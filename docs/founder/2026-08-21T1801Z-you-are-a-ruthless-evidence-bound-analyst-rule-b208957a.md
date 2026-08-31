---
captured: 2026-08-21T18:01:12+00:00
session: fa1c1f08-d352-4dd3-895b-80432f086d9d
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1901
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

Claim: The implementation term sheet outlines the terms and conditions for the development and construction of the facilities, including affordability requirements, community benefits, and funding sources.

Passages:
[s0044] Speaker 2: We do. And it is. I is recommendation to approve the amended and restated maintenance and cost sharing agreement between the City of Alameda and Alameda West Lagoon Homeowners Association.
Speaker 3: It.
Speaker 0: All right, Steph, do you want to maybe just introduce this item? But someone introduced this item before. That's a5e.
Speaker 3: Uh huh. Yeah.
Speaker 5: Good afternoon, Madam Mirror. Members of the City Council. Members of the audience. My name is Enrico Pinnick. I'm the assistant city of assistant city attorney for the city of Alameda. Normally, staff would present this

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

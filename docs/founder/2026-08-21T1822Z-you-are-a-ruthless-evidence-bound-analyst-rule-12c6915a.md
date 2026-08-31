---
captured: 2026-08-21T18:22:38+00:00
session: e1479ed4-6586-49f7-afe3-dae5cfec2549
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1838
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

Claim: The Parks Department will use the property for a natural wetland to alleviate flooding and provide bio filtration of stormwater runoff.

Passages:
[s0076] Speaker 5: The report of the Energy Environment Committee and item ten Constable 1189 12 relating to the satellite department and the Department of Parks Recreation superseding Section seven of Ordinance 124 917 and transferring jurisdiction of the former Dulwich substation from the City Light Department to the Department of Parks and Recreation for Open Space Park Immigration Purposes Committee recommends the bill pass.
Speaker 3: Thank you. Council members. So on.
Speaker 4: Thank you, Britain Brian. This council constable transfers of former substation property in the deluge neighborhood of

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

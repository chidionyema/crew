---
captured: 2026-08-21T18:39:13+00:00
session: aebe64a4-f257-4fa0-8414-2bca163382b4
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2279
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

Claim: Planning policies can encompass a wide range of issues, including land use zoning, transportation, housing, infrastructure, heritage conservation, and environmental protection .

Passages:
[s0110] can be reduced or avoided. This will provide for the protection of the City's important neighborhoods and districts, reduce vehicular trips and air emissions, and encourage economic opportunities, affordable housing, and an improved quality of life.

Improvement of development is addressed through quality standards for multi-family residential neighborhoods and the establishment of pedestrian-oriented districts.

To facilitate growth in those areas in which it is desired, the Land Use Policies provide for the (1) establishment of a process to expedite the review and approval of development applications that are consistent with the Framework Element and community plans, (2) the implementation of infrastructure and public service investment strategies, and (3) a program to monitor growth and infrastructure and public service capacity and report their status annually to the City Council.

Throughout the Land Use Chapter the terms "conservation" and "targeted growth" are used extensively.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

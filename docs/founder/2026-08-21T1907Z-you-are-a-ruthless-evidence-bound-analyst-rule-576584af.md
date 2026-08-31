---
captured: 2026-08-21T19:07:16+00:00
session: dcc2f3b6-4e81-4114-9dc8-1fc8b5d27279
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1745
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

Claim: The amended bill is passed by the council.

Passages:
[s0155] Speaker 2: Three part of the Public Safety and Human Services.
Speaker 0: Committee Agenda Item three.
Speaker 2: Council Bill 119996 relating to Seattle's construction codes.
Speaker 0: Adopting the 2018.
Speaker 2: International Fire Code by reference as.
Speaker 0: The Seattle Fire Code, the committee recommends the bill pass. Councilmember Herbold is chair of the committee. You are recognized to provide the committee's report.
Speaker 4: Q So as described this morning in council briefings, the fire code is typically updated along with the Seattle building code. The Seattle building code wa

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

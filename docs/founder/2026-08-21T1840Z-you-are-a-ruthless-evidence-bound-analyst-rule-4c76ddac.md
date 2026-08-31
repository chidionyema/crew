---
captured: 2026-08-21T18:40:20+00:00
session: acb20cb7-a351-44ea-b189-8815d3e4b10f
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1851
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

Claim: The number of suspected cases of child sexual exploitation (CSE) in West Yorkshire has more than doubled in the past year, according to new figures.

Passages:
[s0113] These are external links and will open in a new window. The cases involve 165 suspects and more than 100 victims. A police spokesperson said many cases had "multiple suspects and multiple victims" but there was also a large number involving single suspects. Last year, 12 men were jailed for their part in the abuse of a single victim in Keighley. Eleven were jailed at Bradford Crown Court after being convicted of raping the girl from the age of 13 and another man was sentenced for sexual activity with her. The CSE figures, which were given to the Keighley News and confirmed to the BBC by police

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T17:43:00+00:00
session: 6aea47bc-7ef1-4396-9050-ad7a07db4f71
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1937
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

Claim: The document discusses a resolution to prioritize the spending of marijuana business license tax revenue for specific purposes, including public health, public safety, homelessness, and general services for regulation and enforcement.

Passages:
[s0018] Speaker 1: Motion carries.
Speaker 0: Thank you. Item number 13, please.
Speaker 1: Communication from City Attorney. Recommendation to adopt resolution expressing its intent to prioritize spending of marijuana business license tax revenue for specific purposes.
Speaker 0: Thank you, Councilman Price.
Speaker 5: Yes, I'd like any money that that is generated as a result of the tax to go to the items and areas specified by the city attorney in the resolution with a special focus on public health and safety. Thank you.
Speaker 0: Great. Thank you. And I'll just add my comments here. In August, w

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

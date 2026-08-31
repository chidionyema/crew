---
captured: 2026-08-21T18:05:37+00:00
session: 29510ed0-14ee-4554-8de9-b250c1679661
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1828
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

Claim: Landlords should consult with legal counsel for specific guidance on the eviction process in their relevant jurisdiction[10].

Passages:
[s0050] Commercial Evictions | The Law Offices of Justin McMurray, P.A. - Daytona the assistance of an attorney. However, matters related to commercial property are usually much more complex than matters related to residential property. Therefore, most landlords with commercial property retain legal counsel to assist them in the commercial eviction process. The commercial eviction process can be unpredictable and complex. Landlords without experience in handling these matters can benefit from the experience, knowledge, and guidance of a Daytona commercial real estate attorney. If you have a commercial

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T18:53:27+00:00
session: 2b4ff317-4c2f-4cb3-b8a7-c34599fdb17e
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1830
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

Claim: Radiation from the nuclear explosion would permeate the water, leading to contamination and affecting marine life in the area .

Passages:
[s0137] the night, screaming in terror, and sink into clinical depression. Many children exposed to radiation in the womb would develop birth defects, particularly small heads and mental disabilities. People exposed to radiation would have an increased risk for cancer, especially in the blood, thyroid, breast, stomach, colon, lung, liver, and bladder. The spike can be dramatic: Between 1950 and 2000, survivors of the atomic bombings in Japan were 46 percent more likely than the general population to develop lethal cases of leukemia.

The Plume

In the hours and days after a nuclear blast, a massive pl

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

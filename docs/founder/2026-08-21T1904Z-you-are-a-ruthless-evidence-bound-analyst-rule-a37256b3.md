---
captured: 2026-08-21T19:04:28+00:00
session: 510e345c-bab9-4f07-9209-bfb6dfdf3a52
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1819
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

Claim: In 2014, a 15-year-old boy survived a 5-1/2-hour flight from California to Hawaii in the wheel well of a Boeing 767.

Passages:
[s0159] MICHAELA PEREIRA, CNN ANCHOR: Welcome back to NEW DAY. Medical professionals remain shocked that a 15-year-old boy can survive a 5- 1/2 hour flight from California all the way to Hawaii in the wheel well of a Boeing 767. Although it is very rare, the teen would not be the first to live through this kind of journey. Back in 2000, a man survived a 7-1/2-hour flight from Tahiti to Los Angeles in the wheel well of a plane. Joining me now is the very physician who successfully treated that stowaway, Dr. Armand Dorian. Dr. Dorian, what a pleasure to have you here. Why don't you describe to us the co

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

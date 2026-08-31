---
captured: 2026-08-21T18:48:18+00:00
session: 95cfb813-c8d4-47de-98b3-5309fe17f618
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2377
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

Claim: The railroads allowed for increased transportation of goods and people, which facilitated economic expansion and population growth.

Passages:
[s0128] {'question': 'what was the effect of the railroads in texas', 'passages': 'passage 1:“Railroads”: http://tshaonline.org/handbook/online/articles/eqr01 Use the above resources to record information on the concept map on the next page. Think about the following when using the primary sources above:\n\npassage 2:When the Texas Legislature passed the Law to Regulate Railroads in 1853, it required that the railroads operating in the state be headquartered in Texas. This requirement was later included as part of Article X of the Constitution of 1876. As a result the various railroad systems operating in Texas did so through subsidiary companies. Some, such as the Southern Pacific, Missouri Pacific, and the Santa Fe, retained the corporate names of Texas railroads they had acquired.\n\npassage 3:Created by Ravae Villafranca Shaeffer, Education Service Center, Region 20. 1. Commission, the Texas Education Agency. TEKS: (7.3 C) identify significant individuals, events, and issues from Reconstruction through the. beginning of the 20th century, including the. effects of the growth of railroads and the. contributions of James Hogg.\n\n'}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

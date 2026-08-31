---
captured: 2026-08-21T18:02:14+00:00
session: e61f51f6-b8cc-4a18-8d61-7e1ba881c879
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1846
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

Claim: It is understood that North Korea is currently dealing with issues such as widespread poverty and ongoing disputes with South Korea and the US.

Passages:
[s0045] Moscow (CNN)Never mind. North Korean leader Kim Jong Un has backed out of next month's visit to Moscow for World War II anniversary celebrations, Kremlin spokesman Dmitry Peskov said Thursday. "We were informed of the decision via diplomatic channels," Peskov said. "The decision is connected with North Korean domestic affairs." The visit was highly anticipated because it would have marked Kim's first official foreign trip since inheriting the leadership of North Korea in late 2011. He was to have met with Russian President Vladimir Putin as part of the May visit to coincide with Victory Day, m

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

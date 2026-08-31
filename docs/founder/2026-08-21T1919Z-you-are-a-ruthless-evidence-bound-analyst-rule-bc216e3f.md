---
captured: 2026-08-21T19:19:59+00:00
session: cb933882-37cc-4f68-983d-08d826222a09
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1929
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

Claim: Hence, studies have indicated that, in contrast to other forms of cannabis, CBD does not produce memory impairment .

Passages:
[s0192] What You Need to Know About Cannabidiol - Hippie Butter known to affect the body. Not only does it have a neurological effect, but it can have psychotropic effects as well. Specifically, CBD has been found to contain a large number of anti-oxidants, which researchers believe helps with short-term memory. Perhaps this explains why studies have shown CBD to not produce memory impairment when compared to other forms of cannabis. In terms of psychotropic effects on the body, Cannabidiol is believed to deliver many anti-psychotic effects, particularly in patients that had previously been diagnosed with disorders like schizophrenia. Furthermore, studies have found that CBD has been useful in treating people

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T18:59:44+00:00
session: f7bbdfe7-a44b-439b-a8bc-144ab10286e5
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1892
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

Claim: Universal basic income (UBI) is a social welfare proposal in which all citizens of a given population regularly receive a guaranteed income in the form of an unconditional transfer payment.

Passages:
[s0150] From Wikipedia, the free encyclopedia
This article is about the system of unconditional income provided to every citizen. For the means-based model of social welfare, see Guaranteed minimum income .
"Basic income" redirects here. For other basic income models, see List of basic income models .
Not to be confused with Unconditional cash transfer or Universal basic services .
Universal basic income ( UBI ) [note 1] is a social welfare proposal in which all citizens of a given population regularly receive a guaranteed income in the form of an unconditional transfer payment (i.e., without a means 

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

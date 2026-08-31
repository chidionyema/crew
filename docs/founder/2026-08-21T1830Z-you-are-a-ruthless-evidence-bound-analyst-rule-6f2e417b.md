---
captured: 2026-08-21T18:30:31+00:00
session: 850978fe-5c3d-4581-bf74-2ea3c3ac1762
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1925
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

Claim: This type of statistical analysis is useful for investigating the relationships between variables across different levels of hierarchy, such as individuals nested within groups or repeated measures on a single individual .

Passages:
[s0093] traditional statistical approaches is to aggregate individual level variables to higher-order variables and then to conduct an analysis on this higher level. The problem with this approach is that it discards all within-group information (because it takes the average of the individual level variables). As much as 80–90% of the variance could be wasted, and the relationship between aggregated variables is inflated, and thus distorted.[18] This is known as ecological fallacy, and statistically, this type of analysis results in decreased power in addition to the loss of information.[2]

Another w

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

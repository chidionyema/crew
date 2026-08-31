---
captured: 2026-08-21T18:23:47+00:00
session: 2727dbc9-30cb-47cf-9f4c-7babd6828d7c
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1980
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

Claim:  Overall, selecting a combination of methods, such as those mentioned above, along with techniques that measure changes in polymer structure, physical loss of plastic mass, or detection of plastic metabolites, will yield a more comprehensive analysis of plastic biodegradation.

Passages:
[s0079] of plastic biodegradation is likely achieved using a combination of techniques from all three categories. However, analysis of the dataset of Gambarini, et al. [28], which compiled data from 408 studies, revealed that of the microorganisms reported to degrade plastics, 48% of reports were based on assays relating to only one of these categories, 39% used techniques that covered two categories, and just 10% used techniques that covered all three (Fig. 4).Fig. 4 Percentage of studies using evidence for plastic degradation by microbial species based on: (i) changes in polymer structure (blue), (i

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T18:16:17+00:00
session: 5e50cecf-6449-436e-a975-791f336f7717
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1976
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

Claim: This article provides a comprehensive alphabetical list of 1765 New Jersey Universities and other higher-education institutions that meet the uniRank selection criteria of being chartered, licensed, or accredited by the appropriate US higher education-related organization.

Passages:
[s0062] How is a specific University in New Jersey ranked and where is it exactly located according to uniRank? uniRank answers this question by publishing a comprehensive alphabetical list of 1753 New Jersey Universities and other higher-education institutions meeting the following uniRank selection criteria:
- being chartered, licensed or accredited by the appropriate US higher education-related organization
- offering at least three-year bachelor's degrees or postgraduate master's or doctoral degrees
- delivering courses predominantly in a traditional, non-distance education format
With this webpag

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

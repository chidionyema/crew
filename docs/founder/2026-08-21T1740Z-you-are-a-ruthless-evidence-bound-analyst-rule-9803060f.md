---
captured: 2026-08-21T17:40:57+00:00
session: c87650c4-069d-4b86-9acd-d35bb59a1319
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1983
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

Claim: CRM analytics can incorporate various data analysis techniques, such as data mining, pattern recognition, and predictive modeling, to understand customer behavior and preferences, ultimately delivering personalized experiences and targeted marketing campaigns .

Passages:
[s0017] Data Mining – Quantos Quantos > Statistical Services > Data Mining The objective of data mining techniques is the discovery of hidden patterns in large amounts of data. The applications are numerous: from the analysis and prediction of individual customers’ behaviour to the design of targeted marketing campaigns. Such applications are closely related to the optimization of customers’ life cycle and the analytical Customer Relationship Management (analytical CRM). Recent advances in statistical pattern recognition, machine learning and hybrid approaches are at the forefront of the modern analytics for businesses.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T17:55:08+00:00
session: fe6d578f-b0e3-493d-b5d0-50774fee57b1
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1803
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

Claim: It is important to monitor the reheating process to ensure that the food reaches a safe temperature.

Passages:
[s0037] {'question': 'how do you reheat food for hot holding', 'passages': 'passage 1:Food safety facts. 1  Cooking and pooling of eggs. Contaminated eggs can carry Salmonella enteritidis and can cause the elderly, small children and those with immune-compromised systems to get sick when consuming raw or undercooked eggs. 2  Food safety in your home kitchen. Food safety in your home kitchen is just as important as food safety in restaurant kitchens. In fact, as much as 60% of foodborne illness may be from home kitchens. Labeling raw and undercooked foods.\n\npassage 2:Reheat foods using proper procedu

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

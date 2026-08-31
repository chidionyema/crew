---
captured: 2026-08-21T18:16:05+00:00
session: 743fe96c-95b6-4985-8de5-0efd87508837
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1993
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

Claim: This not only informs stakeholders of the campaign's direction and progress, but also keeps them invested in its success since they are part of the decision making process .

Passages:
[s0061] 4 Questions To Ask Before A Marketing Campaign Launch | All About Good Marketing healthy meals program as well. When you design a marketing campaign, the questions above are crucial. They are the steps you should take in order to make sure the campaign is successful. The best way to handle these questions is within a brainstorming session with relevant stakeholders. Utilise all the creative energy and market knowledge you have among your staff. This will get them motivated and personally invested in the campaign’s success. Scarlett Erin is a Marketing Manager, Blogging Expert and Social Media Marketer. Apart from running marketing campaigns, she also serves students and assists them in assignment writing. In

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

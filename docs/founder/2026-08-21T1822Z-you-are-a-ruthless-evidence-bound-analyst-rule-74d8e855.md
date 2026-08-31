---
captured: 2026-08-21T18:22:26+00:00
session: db0d2317-9476-4fc7-9b2d-d23e68f56d7f
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2010
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

Claim: Based on the given passages, it is difficult to definitively say whether or not someone has to file taxes for 2015.

Passages:
[s0075] {'question': 'how do I know if I have to file taxes 2015', 'passages': 'passage 1:Whether or not you have to file a tax return as an employee will depend on a number of factors including your filing status, how much you earn, and whether or not you are a dependent of your parents.\n\npassage 2:Who Needs to File a Tax Return. The main factors that generally determine whether you need to file taxes or not are as follows: 1  How you are filing or your filing status. 2  For example, whether you are filing as a single person, or as a married couple filing jointly.\n\npassage 3:Whether or not you are required to file a federal income tax return this year will depend on how much you earned (gross income) -- and the source of that income -- as well as your filing status and your age.\n\n'}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T18:00:39+00:00
session: 0bd58e91-e631-4cda-bff1-58ad050782b5
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2753
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

Claim: Police in the us state of north dakota have arrested more than 100 people protesting against a controversial oil pipeline.

Passages:
[s0043] They say the arrests happened when protesters refused to leave land owned by the pipeline company.
A spokesman said the latest arrests brought the number detained since August to almost 700.
They came after the US Army was ordered to allow the construction of the final section of the Dakota Access Pipeline.
Native Americans and their supporters have protested against the project for months, and have vowed to fight on.
The Standing Rock Sioux Tribe say the final section - under Lake Oahe, a reservoir on the Missouri River - would contaminate drinking water on their land and damage sacred burial sites.
Morton County Sheriff's Office spokesman Rob Keller said the latest arrests were made after demonstrators moved from their existing camp on flood-prone ground to land owned by the pipeline company, Energy Transfer Partners.
He said no injuries had been reported during the operation. Protest leaders could not be reached for comment.
The $3.7bn (Â£2.8bn) pipeline is designed to transport about 470,000 barrels of crude oil a day across four states, from North Dakota to a terminal in Illinois, where it can be shipped to refineries.
The US Army Corps of Engineers, which has approval authority, decided last year to explore other routes for the pipeline amid huge protests by the Standing Rock Sioux Tribe.
But earlier this week, acting Secretary of the Army Robert Speer ordered the corps to allow the work to go ahead.
President Donald Trump recently signed an executive order signalling his support for the pipeline.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

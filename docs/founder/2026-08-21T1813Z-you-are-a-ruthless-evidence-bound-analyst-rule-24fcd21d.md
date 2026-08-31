---
captured: 2026-08-21T18:13:24+00:00
session: 653ebfbd-ebed-44c5-9eda-cd5b31b83e57
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3218
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

Claim: The Catholic Church should apologise to the families of unwed mothers who died at mother-and-baby homes, the Archbishop of Dublin, Rowan Martin, has said.

Passages:
[s0058] These are external links and will open in a new window. The call came after "significant human remains" were found at the site of a former home in the Republic of Ireland. The home was run by the Bon Secours order of nuns in Tuam, County Galway. The bodies ranged from premature babies to three year olds. The discovery was made as part of an investigation into claims by a local historian that up to 800 babies and young children died at the home and were buried in unmarked graves. Amnesty International has said that archaeological surveys should be carried out at all former mother-and-baby homes in Northern Ireland. Archbishop Martin said many in the church and society were "ashamed" of what had emerged at the home in Tuam. He added that "families are owed an apology" and that the Church had repeated an apology it made in 2014 when the claims "first came to light". "It makes me feel awful. I feel incredibly sad in recent days. We as a Church do not want to repeat the awful mistakes of the past." He added: "It's an appalling time for us and everyone in society. "We're opening up a whole chapter in the society in Ireland and the rest of the world where there was a terrible stigma against unwed mothers. "There was a terrible time, we in society and in the Church isolated and stigmatised them." Meanwhile, the Irish children's minister Katherine Zappone has said that 474 "unclaimed infant remains" from mother-and-baby homes were transferred to medical schools between 1940 and 1965. Irish national broadcaster RTÃ‰ made claims about the transfer of remains in a 2011 documentary. Ms Zappone told the DÃ¡il (Irish parliament) that the transfer of remains was "part of a tapestry of oppression, abuse and systematic human rights violations that took place all over this country for decades". She also said an interim report into the home in Tuam would be published by the end of March, a move Archbishop Martin said the Catholic Church supported.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

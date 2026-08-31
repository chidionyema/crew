---
captured: 2026-08-21T18:13:10+00:00
session: e9391393-a8a9-461e-bbce-918fbb1fb784
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1857
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
[s0058] These are external links and will open in a new window. The call came after "significant human remains" were found at the site of a former home in the Republic of Ireland. The home was run by the Bon Secours order of nuns in Tuam, County Galway. The bodies ranged from premature babies to three year olds. The discovery was made as part of an investigation into claims by a local historian that up to 800 babies and young children died at the home and were buried in unmarked graves. Amnesty International has said that archaeological surveys should be carried out at all former mother-and-baby homes

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

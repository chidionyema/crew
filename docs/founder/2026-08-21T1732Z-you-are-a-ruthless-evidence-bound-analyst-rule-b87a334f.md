---
captured: 2026-08-21T17:32:06+00:00
session: 657b7ba9-4196-4d6a-abde-adc787779251
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1837
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

Claim: A majority of members of the Republic of Ireland's Citizens' Assembly have voted in favour of a change in the country's abortion laws.

Passages:
[s0002] These are external links and will open in a new window. The Republic of Ireland currently has strict abortion laws, which only allow a pregnancy to be terminated if there is a serious risk to a woman's life. The Citizens' Assembly voted 64% to 36% in favour of having no restrictions. Anti-abortion groups have condemned the result of the vote, but any change to the law would require a referendum. The Citizens' Assembly was set up by the Oireachtas (Irish Houses of Parliament) to advise elected representatives on a number of ethical and political dilemmas facing the Irish people. These include a

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

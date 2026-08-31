---
captured: 2026-08-21T17:29:56+00:00
session: cddc2415-e427-4c37-a0be-e210febfe7d9
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1840
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

Claim: The council members express the importance of raising awareness about abuse in teen relationships and promoting programs that prevent it.

Passages:
[s0012] Speaker 0: Communication from Council member Richardson, Councilwoman Gonzalez, Councilman Price and Councilman Austin recommendation to request a resolution in support of National Teen Dating Violence Awareness and Prevention Month in February.
Speaker 1: Councilman Richardson.
Speaker 10: Thank you, Mr. Mayor. National Teen Dating, Dating Violence Awareness and Prevention Month is an effort to raise awareness about abuse in teen relationships and promote programs that prevent it during the month of February. Unfortunately, dating violence among teens is more common than most people know, acc

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T19:05:29+00:00
session: b7fca2aa-2886-4f6e-89cd-e565a76fcb23
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2004
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

Claim: Dzhokhar Tsarnaev was found guilty on all 30 charges related to the 2013 bombings . The sentencing phase begins Tuesday , a day after this year 's Boston Marathon . Martin Richard and two others were killed and more 200 people wounded . The Richards are urging the Justice Department to end the case .

Passages:
[s0161] (CNN)The parents of the youngest victim of the Boston Marathon bombings are making an emotional, passionate plea to take the death penalty off the table for the man convicted in the case. Last week, Dzhokhar Tsarnaev was found guilty on all 30 charges he faced related to the bombings at the 2013 race and the dramatic violence that dragged out for days afterward. A look at all of the charges . The sentencing phase begins Tuesday, a day after this year's edition of the landmark race. It is expected to last four weeks. The 13th Juror: Now it gets real . In a front-page opinion piece in The Boston

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

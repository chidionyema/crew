---
captured: 2026-08-21T17:34:08+00:00
session: e4668815-a834-4ebb-9c6d-cc9db65f24bf
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1810
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

Claim: A prominent ukrainian activist, olexander kalashnikov, has been found dead in his flat in the capital kiev.

Passages:
[s0007] Mr Kalashnikov had been involved in the "anti-Maidan" protests in support of deposed President Viktor Yanukovych.
It is not clear if he was murdered or committed suicide. Police say an investigation has been launched.
At least eight Yanukovych allies have died suddenly in the last three months.
Most of the deaths are said to have been suicides. However, officials say it was possible some were killed or forced to take their lives.
Commentators in Ukraine have accused supporters, as well as opponents, of the current pro-Western government of involvement in the deaths.
The BBC's David Stern in Ki

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

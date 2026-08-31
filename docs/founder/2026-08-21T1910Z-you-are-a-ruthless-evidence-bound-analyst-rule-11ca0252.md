---
captured: 2026-08-21T19:10:30+00:00
session: 545826de-6170-44f7-8edb-0e794ae72197
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1820
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

Claim: The third passage mentions deactivating an account, but it does not provide any relevant information to the question.

Passages:
[s0171] {'question': 'how to hide your new friends on facebook', 'passages': "passage 1:Go to your profile. Click on Friends, below your cover picture. On the top right of the Friends section there is a small box with a pen icon (Edit). Click on it and select Edit Privacy.Change the privacy of Friend List to Only Me.Voila! No story will be generated on your friends' news feed when you add a new friend.n the top right of the Friends section there is a small box with a pen icon (Edit). Click on it and select Edit Privacy. Change the privacy of Friend List to Only Me. Voila! No story will be generated on

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

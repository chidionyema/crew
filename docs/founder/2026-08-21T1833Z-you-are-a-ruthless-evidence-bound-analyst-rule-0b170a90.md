---
captured: 2026-08-21T18:33:46+00:00
session: 48f9ab13-f23a-4fcd-8588-571ef07e5e6d
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1808
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

Claim: England won the women's six nations for the first time with a comfortable victory over ireland in dublin.

Passages:
[s0099] Media playback is not supported on this device
Amy Wilson Hardy went over in the corner as England scored from their only chance in the first half.
Ireland could not breach England's solid defence and were made to pay as the world champions ran in four tries.
Forwards Laura Keates and Amy Cokayne extended the visitors' lead before backs Emily Scarratt and Lydia Thompson rounded off the win with fine tries.
With the under-20 men's side having won a Grand Slam earlier on Friday, England's men will look to complete a hat-trick by beating Ireland in Dublin on Saturday.
The women, who return to Ire

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

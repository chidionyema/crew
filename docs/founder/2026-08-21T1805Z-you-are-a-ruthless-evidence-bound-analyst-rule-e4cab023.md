---
captured: 2026-08-21T18:05:04+00:00
session: b0bed49d-9e4d-4c6a-8c83-06532c4ed8b9
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1760
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

Claim: Repeat steps 3 and 4 until the hole is completely filled.

Passages:
[s0049] {'question': 'how to level mailbox post', 'passages': 'passage 1:Then come back and slide the cast stone post over top of the 4×4 wood post. The front of the cast stone post will lay flat against the front of the 4×4 post. This way, when you screw in the mailbox holder and mailbox to the front of the cast stone post, it will join the two together making the post sturdy.\n\npassage 2:According to standard postal service codes, a mailbox should not sit any higher than 45 inches from street level. Place the post in the hole. Level it and attach two support beams at the center to keep the post sta

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

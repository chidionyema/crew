---
captured: 2026-08-21T17:20:31+00:00
session: 7177c073-e285-45b2-aa32-e20a076c97de
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1846
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

Claim: This loyalty is something that Eminem holds dear, and it is no wonder why he speaks so highly of Dr Dre and looks up to him as a father figure.

Passages:
[s0002] [1] While rapper Dr. Dre was already established as a hip-hop legend long before his mentee, Eminem, released his star-making EP Slim Shady in 1997, it was his subsequent mentorship of the then-up-and-coming performer that, in part, cemented his reputation not only as an artist, but as a kingmaking producer. Dre took the younger rapper under his wing, collaborating with his protégé on best-selling albums such as The Marshall Mathers LP and The Eminem Show, as well as the 2001 hit single "Forgot About Dre." And while the realm of hip-hop is well-known for it's myriad feuds, the connection betwe

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T18:52:56+00:00
session: 0ed8197f-1b0d-40bb-8f3e-ca5415a8473d
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1850
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

Claim: The situation is worsened by the fact that the area heavily relies on cotton as its main crop, as soybean yields have been consistently decreasing.

Passages:
[s0136] Vidarbha, India (CNN)Yogita Kanhaiya is expecting a baby soon. She already has a two-year-old son. Her husband, Moreshwor, a cotton farmer, won't be around to see his children grown up. He committed suicide early in the pregnancy. Eight years back, Yogita's father-in-law, also a cotton farmer, took his own life. "He was in so much debt," 25-year-old Yogita said of her late husband. "He wasn't getting any money from cotton. He chose death over distress." It's a familiar story in families across Western India's cotton production belt, where, a cotton lobbyist group claims, one cotton farmer comm

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

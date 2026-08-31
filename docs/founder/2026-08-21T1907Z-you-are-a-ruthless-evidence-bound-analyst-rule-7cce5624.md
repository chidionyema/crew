---
captured: 2026-08-21T19:07:26+00:00
session: 10998d84-cabf-4602-9bd2-7179b5e2e25f
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1947
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

Claim: Pippa, 31, looked glamorous in a tweedy skirt, black blouse and cropped blazer. Accessorised with £ 159 black pumps by Jemima Vine and oversized sunglasses. Just last week, Pippa was glowing in a tailored plum dress at Spectator's annual party.

Passages:
[s0165] It was recently revealed that she will be designing a dress for charity and Pippa Middleton proved she knows a thing or two about fashion as she stepped out in a chic ensemble in London on Thursday. . The 31-year-old sister of the Duchess of Cambridge looked glamorous as she strolled through the sunny streets of London. Pippa looked as chic as ever in a tweedy skirt, black blouse and cropped black blazer. The brunette writer accessorised her look with a black tote, £159 black pumps by Jemima Vine and oversized sunglasses. Scroll down for video . Pippa Middleton looked glamorous as she strolled

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

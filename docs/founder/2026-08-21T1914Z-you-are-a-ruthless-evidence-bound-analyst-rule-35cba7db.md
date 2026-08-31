---
captured: 2026-08-21T19:14:03+00:00
session: db2941e5-1c40-44fb-8adb-6e2c0cfae5f5
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1824
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

Claim: The footage featured various Duggar family members, including a rare sighting of Jackson Duggar, the youngest Duggar son.

Passages:
[s0179] Rare sighting of Jackson Duggar pops up during Duggar beach vacation
The Duggars take Destin should have been the title of Joy-Anna Duggar’s latest vlog.
Followers knew she and Austin Forsyth were visiting the beach with John David Duggar and Abbie Grace Burnett, but it seems it was a family affair — at least some of the family, anyway.
It was unclear which family members didn’t make the trip, but viewers saw Jana, Jason, James, and a rare sighting of Jackson Duggar in the footage.
Two beach houses were rented for the family, with Jim Bob and Michelle Duggar present also. Joy-Anna mentioned th

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

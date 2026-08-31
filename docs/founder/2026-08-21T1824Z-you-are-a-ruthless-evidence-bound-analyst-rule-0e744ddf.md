---
captured: 2026-08-21T18:24:53+00:00
session: a1c140f2-bc93-4de9-bc53-4eb377847f3c
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2211
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

Claim: Giambattista Vico, an Italian philosopher, believed that history was a cyclical process governed by a divine providence .

Passages:
[s0081] Encyclopedia of Philosophy:

"In Vico’s view, is to appreciate history as at once “ideal”-since it is never perfectly actualized-and “eternal,” because it reflects the presence of a divine order or Providence guiding the development of human institutions. Nations need not develop at the same pace-less developed ones can and do coexist with those in a more advanced phase-but they all pass through the same distinct stages (corsi): the ages of gods, heroes, and men. Nations “develop in conformity to this division,” Vico says, “by a constant and uninterrupted order of causes and effects present in every nation” (“The Course the Nations Run,” §915, p.335). Each stage, and thus the history of any nation, is characterized by the manifestation of natural law peculiar to it, and the distinct languages (signs, metaphors, and words), governments (divine, aristocratic commonwealths, and popular commonwealths and monarchies), as well as systems of jurisprudence (mystic theology, heroic

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

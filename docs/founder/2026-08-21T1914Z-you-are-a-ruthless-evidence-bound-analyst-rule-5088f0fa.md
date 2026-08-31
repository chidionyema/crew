---
captured: 2026-08-21T19:14:35+00:00
session: 361d5d28-2392-4ddf-a046-31dd7ca3dbc2
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1786
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

Claim: Celebrities, politicians, and even animals have taken selfies that have gone viral.

Passages:
[s0180] GORANI: A major shocker at the World Cup right now. Just minutes ago, Argentina lost to Croatia three nail. That would make it extremely difficult for Argentina to advance out of their group. On the pitch today, France beat Peru, one nail. Yay. Which moves them into the knockout stage of the World Cup. Russia and Uruguay, so far, are the only other teams to advance. Russia's success certainly is a surprise. They came into the cup as the lowest rated team in the tournament. They have something called a home advantage though, I think Fred Pleitgen has been following the Russian national team and

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T19:16:41+00:00
session: 1fe17079-2552-46d1-8446-a4a0fc6daa8e
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1766
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

Claim: You will need to plant at least two trees for fruit production.

Passages:
[s0185] {'question': 'how to plant dwarf apple trees', 'passages': "passage 1:These other plantings compete for nutrients, water and sunlight. Semi-dwarf trees need less space than standard apples, but more space than dwarfs. How much space your semi-dwarf apple tree needs depends on the variety and the root stock, but in general, space semi-dwarf apple trees 14 to 20 feet apart.ariety Selection. Most semi-dwarf apple trees aren't self-pollinating. You'll need to plant at least two trees to produce fruit. Select varieties that bloom at the same time and are known as good pollinators.\n\npassage 2:Choo

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

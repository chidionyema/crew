---
captured: 2026-08-21T19:16:49+00:00
session: 16c8e6a8-ddd0-4c21-ae70-3b18c9dc92b0
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2830
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
[s0185] {'question': 'how to plant dwarf apple trees', 'passages': "passage 1:These other plantings compete for nutrients, water and sunlight. Semi-dwarf trees need less space than standard apples, but more space than dwarfs. How much space your semi-dwarf apple tree needs depends on the variety and the root stock, but in general, space semi-dwarf apple trees 14 to 20 feet apart.ariety Selection. Most semi-dwarf apple trees aren't self-pollinating. You'll need to plant at least two trees to produce fruit. Select varieties that bloom at the same time and are known as good pollinators.\n\npassage 2:Choose an apple tree variety known to grow well in your region. Thanks to modern grafting techniques, apple trees come in three sizes: standard, semi-dwarf and dwarf. Semi-dwarf trees grow between 10 and 16 feet tall and bear fruit within four to five years.ariety Selection. Most semi-dwarf apple trees aren't self-pollinating. You'll need to plant at least two trees to produce fruit. Select varieties that bloom at the same time and are known as good pollinators.\n\npassage 3:Step 1. Locate a site for the dwarf apple tree where it will get at least six hours or more of full sun during the day. The soil will need to drain well, as the apple tree will slowly die in soggy soil.Clear away all the weeds, and mark a circle at least 2 feet wider than the root ball of the tree.tep 3. Set your stake into the hole just off center. It will need to be secured at least a foot into the ground, so pound it in with a sledge hammer. For many dwarf apple trees, this stake will need to remain in place for the life of the tree to help support the weight of the fruit.\n\n"}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T17:46:07+00:00
session: 587fdf39-6e48-42df-98cc-b5a6b13949ad
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1820
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

Claim: Overall, while some customers may have had negative experiences at Jack in the Box, others have enjoyed their visits.

Passages:
[s0023] {'name': 'Jack in the Box', 'address': '501 N Milpas St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, Fast Food, Mexican, Burgers, Tacos, Breakfast & Brunch', 'hours': {'Monday': '6:0-2:0', 'Tuesday': '6:0-2:0', 'Wednesday': '6:0-2:0', 'Thursday': '6:0-2:0', 'Friday': '0:0-0:0', 'Saturday': '0:0-0:0', 'Sunday': '6:0-2:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': True, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': False, 'WiFi': 'no', 'RestaurantsTakeOut': False, 'RestaurantsGoodForGroups': Tr

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

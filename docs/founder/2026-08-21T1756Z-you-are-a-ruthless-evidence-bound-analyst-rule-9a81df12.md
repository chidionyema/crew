---
captured: 2026-08-21T17:56:56+00:00
session: 21aaeab3-4191-4975-9690-3e8c137b1830
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1785
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

Claim: The restaurant has a casual and trendy atmosphere, with outdoor seating available.

Passages:
[s0040] {'name': 'Revolver', 'address': '1429 San Andres St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, Pizza', 'hours': {'Wednesday': '16:0-22:0', 'Thursday': '16:0-22:0', 'Friday': '16:0-22:0', 'Saturday': '16:0-22:0', 'Sunday': '16:0-22:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': None, 'OutdoorSeating': True, 'WiFi': 'free', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': None, 'Music': None, 'Ambience': {'divey': True, 'hipster': None, 'casual': None, 'touris

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

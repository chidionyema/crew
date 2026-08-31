---
captured: 2026-08-21T17:38:25+00:00
session: d13d179b-7a1d-4c6d-b9fe-f77521c6fa44
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1773
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

Claim: Based on the provided data, Pickles & Swiss has a rating of 4.5 stars.

Passages:
[s0013] {'name': 'Pickles & Swiss', 'address': '811 State St, unit E', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Delis, Gluten-Free, Fast Food, Salad, Sandwiches, Restaurants', 'hours': {'Monday': '0:0-0:0', 'Tuesday': '11:0-17:0', 'Wednesday': '11:0-17:0', 'Thursday': '11:0-17:0', 'Friday': '11:0-16:0', 'Saturday': '11:0-18:0', 'Sunday': '11:0-18:0'}, 'attributes': {'BusinessParking': {'garage': True, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGro

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

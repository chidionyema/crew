---
captured: 2026-08-21T17:35:59+00:00
session: be13edd7-ade9-4531-a4d1-3723b531a5e6
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1771
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

Claim: The restaurant has a casual atmosphere and provides outdoor seating.

Passages:
[s0006] {'name': 'Rice Garden', 'address': '1180 University Ctr, Bldg 252', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Fast Food, Caterers, Chinese, Szechuan, Event Planning & Services, Restaurants', 'hours': {'Monday': '10:0-17:0', 'Tuesday': '10:0-17:0', 'Wednesday': '10:0-17:0', 'Thursday': '10:0-17:0', 'Friday': '10:0-17:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': True, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'paid', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': 

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

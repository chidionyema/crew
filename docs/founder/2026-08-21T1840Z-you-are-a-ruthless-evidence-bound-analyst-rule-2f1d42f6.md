---
captured: 2026-08-21T18:40:47+00:00
session: af3524e0-4bda-4d50-9e88-bea7a55acfff
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1794
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

Claim: They offer takeout and reservations, and have outdoor seating, WiFi, and parking available.

Passages:
[s0114] {'name': "Meat n' Potatoes", 'address': '4444 Hollister Ave', 'city': 'Goleta', 'state': 'CA', 'categories': 'American (Traditional), Restaurants', 'hours': None, 'attributes': {'BusinessParking': None, 'RestaurantsReservations': True, 'OutdoorSeating': True, 'WiFi': None, 'RestaurantsTakeOut': None, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'touristy': False, 'hipster': False, 'divey': False, 'classy': False, 'trendy': False, 'upscale': False, 'casual': True}}, 'business_stars': 4.0, 'review_info': [{'review_stars': 4.0, 'review_date':

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

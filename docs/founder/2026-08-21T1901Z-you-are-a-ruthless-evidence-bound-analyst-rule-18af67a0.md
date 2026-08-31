---
captured: 2026-08-21T19:01:04+00:00
session: c5a9d873-c315-4344-8781-1380a438ba42
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

Claim: The business offers a variety of food options including sushi, drinks, and snacks.

Passages:
[s0153] {'name': "Q's Billiard Club & Sushi-a-go-go", 'address': '409 State St.', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, Sushi Bars', 'hours': None, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': None, 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': None}, 'business_stars': 3.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2009-07-16 01:33:49', 'review_text': "This place makes you  have a

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

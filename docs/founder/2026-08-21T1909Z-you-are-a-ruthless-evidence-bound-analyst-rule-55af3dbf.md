---
captured: 2026-08-21T19:09:31+00:00
session: 6be89083-fa68-4915-a99f-a0c009985eec
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2761
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

Claim: Overall, the restaurant seems to offer a pleasant atmosphere and good service, but may need to work on consistency in their food quality.

Passages:
[s0169] {'name': 'Restaurant Mimosa', 'address': '714 State St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, French, American (New)', 'hours': None, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': True, 'OutdoorSeating': True, 'WiFi': None, 'RestaurantsTakeOut': False, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': True, 'intimate': False, 'touristy': False, 'hipster': False, 'divey': False, 'classy': False, 'trendy': False, 'upscale': False, 'casual': False}}, 'business_stars': 3.5, 'review_info': [{'review_stars': 1.0, 'review_date': '2014-11-17 23:18:37', 'review_text': "Horrible experience. Service was a 3 out of 10. When my meal arrived I noticed it wasn't cooked all the way through. Pest control might be needed."}, {'review_stars': 2.0, 'review_date': '2012-09-28 17:03:57', 'review_text': "Very good service but food only ok.  My steak was mostly peppercorns with very little flavor.  My wife's salmon was fine but nothing exceptional.  Prices are quite high - we will not return."}, {'review_stars': 5.0, 'review_date': '2012-08-20 18:46:55', 'review_text': "I had the Roasted Duck Breast, and it was incredibly tasty.  Fresh vegetables.  Mayan Chocolate Cheesecake for desert and it was very unique.  The service was excellent as well.  It was a very enjoyable experience and I left feeling satisfied.  I'll be returning for sure next time I'm in the area."}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

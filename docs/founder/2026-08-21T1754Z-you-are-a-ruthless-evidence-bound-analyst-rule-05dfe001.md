---
captured: 2026-08-21T17:54:00+00:00
session: c758d869-3edb-4e2c-81cd-6632ae6e66cd
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2844
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

Claim: The restaurant's data indicates that it has a 3.5-star rating based on customer reviews, with reviewers praising the quality of the food, particularly the yellow curry, which one reviewer described as "the shit."

Passages:
[s0034] {'name': 'Bangkok Palace', 'address': '2829 De La Vina St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Thai, Restaurants', 'hours': {'Monday': '11:0-21:0', 'Tuesday': '11:0-21:0', 'Wednesday': '11:0-21:0', 'Thursday': '11:0-21:0', 'Friday': '11:0-21:0', 'Saturday': '17:0-21:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': True, 'OutdoorSeating': False, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'touristy': False, 'hipster': False, 'divey': False, 'classy': False, 'trendy': False, 'upscale': False, 'casual': True}}, 'business_stars': 3.5, 'review_info': [{'review_stars': 3.0, 'review_date': '2014-02-04 02:20:15', 'review_text': "Their food Is great but I'm really disappointed to find out that they've stopped doing delivery."}, {'review_stars': 3.0, 'review_date': '2014-01-20 21:22:31', 'review_text': 'Really quick service and very friendly, sweet staff:) Coconut soup is delicious.... but the pad thai is really oily:( But the waiter was incredibly attentive and smiley. Everyone who came in seemed to know him and he emanated a lovely, positive energy.'}, {'review_stars': 5.0, 'review_date': '2013-12-24 03:22:29', 'review_text': 'Best Thai food in town. Delivery is fast and always delivered hot. Such friendly people too. Yellow curry is the shit. Tried nearly all thai in sb. Hands down the best!'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

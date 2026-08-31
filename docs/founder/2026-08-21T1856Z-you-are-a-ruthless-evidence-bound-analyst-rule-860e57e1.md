---
captured: 2026-08-21T18:56:02+00:00
session: c13c8eee-bd5d-42ab-bc3f-52e4bc8e0a2a
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3285
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

Claim: All three customers gave the restaurant a rating of five stars.

Passages:
[s0142] {'name': 'Aperitivo', 'address': '7 W Haley St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Desserts, Food, Bars, Wine Bars, Coffee & Tea, Nightlife, Tapas/Small Plates, Restaurants', 'hours': {'Monday': '0:0-0:0', 'Wednesday': '16:30-21:0', 'Thursday': '16:30-21:0', 'Friday': '16:30-21:0', 'Saturday': '16:30-21:0'}, 'attributes': {'BusinessParking': None, 'RestaurantsReservations': None, 'OutdoorSeating': True, 'WiFi': 'no', 'RestaurantsTakeOut': False, 'RestaurantsGoodForGroups': None, 'Music': None, 'Ambience': None}, 'business_stars': 5.0, 'review_info': [{'review_stars': 5.0, 'review_date': '2022-01-14 05:03:21', 'review_text': 'I am a foodie, I travel for work and have been fortunate enough to have amazing food all over the world. That being said this is one of the most underrated restaurants in Santa Barbara I can easily say this is one of the top three restaurants in Santa Barbara.  My recommendation would to be to order anything with the burrata on it! The 24 hrs burrata, the pere brushchette , and the stratacciatella brushchette were all amazing! The passion fruit margarita is also to die f\n\nThank you for upping the food game in Santa Barbara Aperitivo! \n\nSide note, my other two favorite restaurants in Santa Barbara are the Black Sheep and Bouchon'}, {'review_stars': 5.0, 'review_date': '2022-01-13 02:30:17', 'review_text': "No hesitation here with the 5 star review! Excellent food, stellar service,  and guaranteed high quality product every time.  When I want fresh and delicious pasta, Aperativo is my go-to.  I appreciate their dedication and consistency. Highly recommend for date night since its a cozy intimate venue with an open kitchen. I'm also a big fan of Tues pasta club for take out,  excellent wine pairings every time."}, {'review_stars': 5.0, 'review_date': '2022-01-07 01:01:24', 'review_text': 'I ordered the box of wine for pick up and was not disappointed. They were all wonderful wines! I highly recommend it AND the Pasta Club. The pasta selections are very flavorful and pair wonderfully with the wine. I plan to order everytime I am in town.'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T18:23:33+00:00
session: 3bd8d8c6-6669-47fb-85c2-531e9d294eb4
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3787
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

Claim: Another customer mentioned that the food was dry, tasteless, and expensive, expressing disappointment with the quality and cost.

Passages:
[s0078] {'name': 'Marbella', 'address': '1111 E Cabrillo Blvd', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Tapas/Small Plates, Restaurants, Breakfast & Brunch, Seafood, American (New)', 'hours': {'Monday': '17:0-22:0', 'Tuesday': '17:0-22:0', 'Wednesday': '17:0-22:0', 'Thursday': '17:0-22:0', 'Friday': '17:0-22:0', 'Saturday': '17:0-22:0', 'Sunday': '17:0-22:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': True, 'OutdoorSeating': True, 'WiFi': 'paid', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'touristy': False, 'hipster': False, 'romantic': False, 'divey': False, 'intimate': False, 'trendy': False, 'upscale': False, 'classy': False, 'casual': False}}, 'business_stars': 3.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2020-08-24 02:29:48', 'review_text': "We were tired and hungry.  The manager at Hyatt was kind of enough to serve us a great dinner.  I am fairly happy with the pasta, chicken salad especially the avocado toast.  Great flavor and it's not greasy either.  Everything is seasoned perfectly.  A little spice goes a long way."}, {'review_stars': 1.0, 'review_date': '2019-07-06 00:29:17', 'review_text': "Methinks not indeed. This place is so gross. The food has small, cold portions. The wait staff is a bunch of bus boys, who speak very poor English. It's as if they've fired their regular wait staff to save money, and then dragooned the dish washer into serving.\n Don't be penny wise and pound foolish, and this nonsense includes the tip.  One of the buffets was an $18 TERRIBLE hamburger and cold fries. Why? \nI had a grilled chicken sandwich that was apparently taken out of the ice box minutes before it found its way to my plate. It may have been left over from the previous day. Soooooo gross. The hotel is undergoing a renovation, according to the manger. START WITH THE RESTAURANT."}, {'review_stars': 1.0, 'review_date': '2019-04-13 23:50:55', 'review_text': 'My boyfriend and I wanted a late lunch/ snack. We decided to stay in the hotel to eat at this restaurant.  The vibe and food WASN\'T inviting. We just thought, "let\'s give this place a try."  SUPER DISAPPOINTED ON THE FOOD AND COST for this HOTEL!! Its pretty dry, tasteless, and expensive. (We ordered Nachos, Brussels sprouts, & Mahi Mahi fish taco). Did i mentioned that it was expensive too? GO ELSE WHERE FOR BETTER FOOD.Service was ok but we were there for food, Not the the service.'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

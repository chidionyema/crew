---
captured: 2026-08-21T18:37:48+00:00
session: 4d415a5a-4a5e-4401-9144-16d8c4bbad98
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3162
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

Claim: Ca'Dario Pizzeria Veloce is a pizza restaurant located in the Public Market in Santa Barbara, CA.

Passages:
[s0107] {'name': "Ca'Dario Pizzeria Veloce", 'address': '38 W Victoria St, Ste 104', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, Pizza', 'hours': {'Monday': '11:0-22:0', 'Tuesday': '11:0-22:0', 'Wednesday': '11:0-22:0', 'Thursday': '11:0-22:0', 'Friday': '11:0-22:0', 'Saturday': '11:0-22:0', 'Sunday': '11:0-22:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': None, 'WiFi': None, 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'touristy': False, 'hipster': False, 'romantic': False, 'divey': False, 'intimate': False, 'trendy': False, 'upscale': False, 'classy': False, 'casual': False}}, 'business_stars': 3.0, 'review_info': [{'review_stars': 1.0, 'review_date': '2021-12-01 04:54:03', 'review_text': 'Pizza was meh, service was even worse. Dont waste your money on overpriced wannabe "italian" pizza in the public market. There are plenty of places thatll greet you with a smile and serve you some delicious pizza'}, {'review_stars': 1.0, 'review_date': '2021-10-29 14:57:41', 'review_text': "ca'dario downtown is amazing. that's why i decided to get the pizza in public market. i THOUGHT it was going to be fresh but absolutely not. their pizzas are frozen that they put in the oven. very upset that i paid $15 for what i could have made store bought. you can instantly taste in the dough that it is not fresh. i ordered the bbq chicken pizza and the chicken was rubbery. not happy :("}, {'review_stars': 5.0, 'review_date': '2021-07-15 12:57:10', 'review_text': "Yep the egg and bacon pizza did not disappoint! The egg could have been a little more runny so the yolk could spread over the pizza. Not sure if the egg was just a garnish or to actually add\nFlavor but it fried over hard. I got the gluten free crust which was great! I'm interested to try other items!"}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T17:31:54+00:00
session: 23185dab-70b6-42bc-b0a0-a0bffdce2826
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3504
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

Claim: The business has 4.5 stars in total, with some customers leaving positive reviews about their experience.

Passages:
[s0001] {'name': 'Lilac Pâtisserie', 'address': '1017 State St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Specialty Food, Health Markets, Restaurants, Gluten-Free, Bakeries, Coffee & Tea, Desserts, Breakfast & Brunch, Food', 'hours': {'Monday': '0:0-0:0', 'Tuesday': '8:0-16:0', 'Wednesday': '8:0-14:0', 'Thursday': '8:0-14:0', 'Friday': '8:0-14:0', 'Saturday': '8:0-14:0', 'Sunday': '8:0-14:0'}, 'attributes': {'BusinessParking': None, 'RestaurantsReservations': False, 'OutdoorSeating': None, 'WiFi': 'no', 'RestaurantsTakeOut': None, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'touristy': False, 'hipster': False, 'romantic': False, 'divey': False, 'intimate': False, 'trendy': False, 'upscale': False, 'classy': True, 'casual': True}}, 'business_stars': 4.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2022-01-13 21:17:16', 'review_text': "If you want to find an entirely delicious gluten free restaurant, come to this place! Everything is absolutely delicious, they could add more seasoning to their breakfast potatoes, and avocado to their breakfast sandwiches, not going to lie. They're closed for remodeling, but I can't wait until they open back up!!"}, {'review_stars': 4.0, 'review_date': '2021-12-11 18:40:02', 'review_text': "* Nothing beats a beautiful and decadent warm cup of hot cocoa after a stressful week! I love that this cup is on the less sweet side, which pairs very well with their sweet pastries. Their latte art is beautifully done as well, which makes up for their $5.50 price point.\n\n* The lemon tart was textbook: had a beautiful shortbread crust with a lemon custard topped with a scorched meringue. It was flawless and I don't think I can point out any flaws. \n\n* The cake, however, had way too much cream and chocolate go the rest of the cake ratio which made it unsettling to eat and way too sweet. I think the flavor combination sounded good but unfortunately didn't deliver. \n\nWhat's unique is that I believe all the desserts are gluten free, which is incredible, and inclusive of our gluten free friends."}, {'review_stars': 5.0, 'review_date': '2021-12-08 04:43:21', 'review_text': "Fantastic decadent chocolate cake. Friendly staff. The cake didn't taste gluten free at all. Blueberry lemon tarte was fantastic."}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

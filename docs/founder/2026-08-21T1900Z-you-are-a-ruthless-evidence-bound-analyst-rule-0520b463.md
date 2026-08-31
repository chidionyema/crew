---
captured: 2026-08-21T19:00:27+00:00
session: 0aa8ceaa-4089-4a11-aee1-4f2eb3edf75e
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3804
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

Claim: This local gem is a popular choice for satisfying burger cravings and is worth a visit in Santa Barbara.

Passages:
[s0151] {'name': "Kyle's Kitchen", 'address': '791 Chapala St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Cafes, Restaurants, Sandwiches, Chicken Shop, Salad, American (New), Burgers, Breakfast & Brunch', 'hours': {'Monday': '11:0-21:0', 'Tuesday': '11:0-21:0', 'Wednesday': '11:0-21:0', 'Thursday': '10:30-20:0', 'Friday': '11:0-21:0', 'Saturday': '11:0-21:0', 'Sunday': '11:0-21:0'}, 'attributes': {'BusinessParking': {'garage': True, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'free', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'touristy': False, 'hipster': False, 'divey': False, 'classy': False, 'trendy': False, 'upscale': False, 'casual': True}}, 'business_stars': 4.0, 'review_info': [{'review_stars': 5.0, 'review_date': '2022-01-18 00:41:04', 'review_text': 'Had lunch here today and was pleasantly surprised. My husband mentioned this place to me before since he said he tried the Kyle Burger and liked it. Since we had to do some errands at Fedex (right beside it), we decided to have lunch here. I had the kale and caesar salad and Kyle Burger while my husband had tomato soup and Buffalo Chicken Sandwich. We were pleased with our orders and the serving was just right.\n\nIn their menu, you could create your perfect meal by selecting any 2 options for $13 (upgrades are available for an additional cost -just check the menu). They call this Pair It!\nThese are the options for Pair It!\n1. Burger or chicken sandwich\n2. Salad\n3. Bowl of soup\n4. Beverage\n\nThis place is clean and the interior is nice. We will definitely come back to this place especially if we have burger cravings!'}, {'review_stars': 5.0, 'review_date': '2022-01-14 20:57:48', 'review_text': 'The best burgers and salads ( my fave is the Thai peanut with chicken) and the staff is always great!'}, {'review_stars': 5.0, 'review_date': '2021-12-28 06:51:01', 'review_text': "Kyle's Kitchen is an unexpected gem in Santa Barbara. At first they look like some sort of chain restaurant like Eureka but no, they actually have really great quality fast food. \n\nWe came during a Sunday and their daily deal was chicken sandwiches and I must say, I was pleasantly surprised at how delicious it was. I guess I wasn't expecting to have received such a quality crispy chicken sandwich given the sort of sub-par marketing and location. Needless to say, I have definitely come back and I am excited to try more things from their menu."}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

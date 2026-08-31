---
captured: 2026-08-21T17:46:19+00:00
session: 1fd5f17d-9b7e-4461-b0e6-c4c54b255103
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3488
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

Claim: Overall, while some customers may have had negative experiences at Jack in the Box, others have enjoyed their visits.

Passages:
[s0023] {'name': 'Jack in the Box', 'address': '501 N Milpas St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, Fast Food, Mexican, Burgers, Tacos, Breakfast & Brunch', 'hours': {'Monday': '6:0-2:0', 'Tuesday': '6:0-2:0', 'Wednesday': '6:0-2:0', 'Thursday': '6:0-2:0', 'Friday': '0:0-0:0', 'Saturday': '0:0-0:0', 'Sunday': '6:0-2:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': True, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': False, 'WiFi': 'no', 'RestaurantsTakeOut': False, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'touristy': False, 'hipster': False, 'divey': False, 'classy': False, 'trendy': False, 'upscale': False, 'casual': False}}, 'business_stars': 1.5, 'review_info': [{'review_stars': 1.0, 'review_date': '2021-11-25 09:55:47', 'review_text': "This place sucks, every time you come here they have different people and they simply don't care \nIt takes forever to get your order \nSpecially on weekends \nPlease put people that you thrust and have confidence who ever the owner is !!!!!!!!!!"}, {'review_stars': 1.0, 'review_date': '2021-07-01 15:27:52', 'review_text': "Waiting for my order in the drive thru and I saw a red sanitation bucket under the ice cream dispenser. I assume they're cleaning it out, so okay, they're not gonna serve it. But what I saw next was the woman scoop out ice cream FROM the same red sanitation bucket. Into two cups, and prep them and serve them with whipped cream and a cherry on top for the guy behind me.\n\nI don't believe that red sanitation bucket is, um...SANITARY. That bucket isn't food grade safe, I assume! I've worked in a couple kitchens before and let me tell you I've never seen food, let alone ice cream, get cleaned out into the red sanitation bucket and then get SERVED. Normally, This bucket is filled with kitchen sanitation liquid, to be changed every four hours with a new towel. I'm very sure I'm never coming back to this place to see this unsanitary practice."}, {'review_stars': 5.0, 'review_date': '2020-12-21 02:58:32', 'review_text': "Hahahahaha wtf is up with all the reviews!? It's Jack in the box!! Get over it!! Yelp = Karen Culture"}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

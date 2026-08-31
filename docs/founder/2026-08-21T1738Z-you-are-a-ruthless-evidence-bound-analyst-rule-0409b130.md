---
captured: 2026-08-21T17:38:38+00:00
session: b680d85f-dee3-47e4-8d94-afab1637a12d
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3207
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

Claim: Based on the provided data, Pickles & Swiss has a rating of 4.5 stars.

Passages:
[s0013] {'name': 'Pickles & Swiss', 'address': '811 State St, unit E', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Delis, Gluten-Free, Fast Food, Salad, Sandwiches, Restaurants', 'hours': {'Monday': '0:0-0:0', 'Tuesday': '11:0-17:0', 'Wednesday': '11:0-17:0', 'Thursday': '11:0-17:0', 'Friday': '11:0-16:0', 'Saturday': '11:0-18:0', 'Sunday': '11:0-18:0'}, 'attributes': {'BusinessParking': {'garage': True, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'touristy': False, 'hipster': False, 'romantic': False, 'divey': False, 'intimate': False, 'trendy': False, 'upscale': False, 'classy': True, 'casual': True}}, 'business_stars': 4.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2022-01-18 03:35:34', 'review_text': "5/5 with the food and customer service. I've only had one time where my order was wrong but honestly didn't even mind because it was good regarles and their customer service is always so nice. I recommend their Chipotle Turkey Club it's always my go to. Having one of theirs sandwich always makes my day. :)"}, {'review_stars': 1.0, 'review_date': '2022-01-16 23:32:45', 'review_text': "It took more than an hour to get my half sandwich which they didn't tell me when I ordered it."}, {'review_stars': 2.0, 'review_date': '2022-01-14 00:47:39', 'review_text': "I've tried this place a couple times and have always left disappointed. The place is too small a crowded for the workers. The food prep stations are ALWAYS messy and gross and there's a lot of cross contaminating. Food takes forevor even when there's no one there. The workers are so unwelcoming and often distracted when taking your order. The food taste like nothing which is crazy cause so many reviews are hyping up the flavor but I literally can't taste much other than the sauce they drench their sandwiches with. South Coast Deli is the way to go."}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

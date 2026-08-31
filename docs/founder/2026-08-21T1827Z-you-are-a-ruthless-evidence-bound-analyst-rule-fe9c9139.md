---
captured: 2026-08-21T18:27:35+00:00
session: 2057d1f6-47e9-4355-b0e0-0072523fa500
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3967
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

Claim: The ambiance is casual and welcoming, with a divey and hipster vibe.

Passages:
[s0087] {'name': 'Breakwater Restaurant', 'address': '107 Harbor Way', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, American (Traditional), Seafood, Breakfast & Brunch', 'hours': {'Monday': '0:0-0:0', 'Tuesday': '8:0-16:45', 'Wednesday': '8:0-19:0', 'Thursday': '8:0-14:0', 'Friday': '8:0-14:0', 'Saturday': '8:0-19:0', 'Sunday': '8:0-19:0'}, 'attributes': {'BusinessParking': {'valet': False, 'garage': None, 'street': None, 'lot': None, 'validated': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'divey': False, 'hipster': False, 'casual': True, 'touristy': None, 'trendy': False, 'intimate': False, 'romantic': False, 'classy': False, 'upscale': False}}, 'business_stars': 3.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2022-01-12 17:43:24', 'review_text': 'This place was so great, we went two days in a row.  \n\nMy friend and I walked by after getting off the Tiny Tut water taxi from the Pier.  We had a mimosa and looked out at the great view.  We saw some wonderful-looking breakfast items being delivered around us (we had already eaten). My dad (89 years old) living in Northern California called while we were there and he remembers from 40+ years ago that they had great ice cream. He was right: we had the coffee one. Terrific!\n\nWe came back the next morning for breakfast and enjoyed a whole bottle of champagne (the cheapest way to do it).  Our food was excellent and huge servings.  The staff and manager are very friendly and very welcoming.'}, {'review_stars': 5.0, 'review_date': '2021-12-23 17:02:22', 'review_text': 'Hey Guys sometimes our best Experiences are Right under our Nose  The Breakwater Restaurant an Iconic Santa Barbara Eatery. My dear Friends Ed and Tanya Bailey Love the place, so when it was suggested I was Excited and that Excitement kept Building. Breakfast served until 3pm,Oh My!\nBasted Eggs  can be a challenge for some Restaurants but not the Breakwater! Basted Eggs  and Chicken Fried  Steak prepared to Perfection. Ed and Tanya both Enjoyed their Food as Well. \nAs we Celebrate the Christmas  Holiday season and Break Bread  with Family and Friends the Breakwater is a Great option or just about Anytime. Thanks To the Breakwater staff for the Great service and Oh Yes an Old Fashioned Ice Cream cone for dessert  \nMerry Christmas    and Happy New Year to my Yelp Family  in  2022'}, {'review_stars': 3.0, 'review_date': '2021-12-05 20:41:47', 'review_text': "I was excited to take my dad for lunch on the harbor. The line wasn't  long, and we got a table in about 5min. The staff was friendly. The menu  is very outdated. A little pricey (paying for the view?). And the food  was just OK."}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

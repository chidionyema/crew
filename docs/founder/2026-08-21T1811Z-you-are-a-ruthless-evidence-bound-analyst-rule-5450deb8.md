---
captured: 2026-08-21T18:11:34+00:00
session: aba8c630-f4c8-4594-ad60-b1d85f8ff019
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3195
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

Claim: The business offers outdoor seating and takeout services.

Passages:
[s0055] {'name': 'Paradise Store & Grill', 'address': '1 Paradise Rd', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'American (Traditional), Restaurants', 'hours': {'Monday': '9:0-18:0', 'Tuesday': '9:0-18:0', 'Wednesday': '9:0-18:0', 'Thursday': '9:0-18:0', 'Friday': '9:0-19:0', 'Saturday': '9:0-19:0', 'Sunday': '9:0-18:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': True, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'touristy': False, 'hipster': False, 'divey': False, 'classy': False, 'trendy': False, 'upscale': False, 'casual': False}}, 'business_stars': 4.0, 'review_info': [{'review_stars': 4.0, 'review_date': '2016-04-03 23:33:30', 'review_text': "Oh no!  They're closed for good!  Must have just happened.  A shame. This was a great place to stop after a hike in the Paradise Road area."}, {'review_stars': 5.0, 'review_date': '2016-03-30 19:02:09', 'review_text': "Neat, historic general store...and so much more!  Rustic little stop, seating on front deck, or out back nestled in the trees.  Both have live music usually!  Not a rock band, but one guy, one guitar, one voice.  So enjoyable for 20 minutes, or the entire afternoon!\n\nTwo words: Tritip Chili.  So good.  Even if all you do is stop for a couple of containers of the stuff (don't forget onions and cheese) and take them home.  You won't regret it.  Used to do that on the way home EVERY camping trip we made to Rancho Oso.  But don't be fooled, this place may have the best burger in SB County.  EVERYTHING on the menu is fantastic...and even a little better due to ambiance.\n\nDon't sell yourself short.  Stop here at the Paradise Store."}, {'review_stars': 2.0, 'review_date': '2015-12-01 21:08:21', 'review_text': 'Nice people. Did not try the food.the rating is for the 10$ they charged for a very small box of firewood.'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T17:33:56+00:00
session: 5bcf0699-3e4a-4c2c-a300-1fb22466ca37
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3581
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

Claim: The restaurant has a casual atmosphere and provides outdoor seating.

Passages:
[s0006] {'name': 'Rice Garden', 'address': '1180 University Ctr, Bldg 252', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Fast Food, Caterers, Chinese, Szechuan, Event Planning & Services, Restaurants', 'hours': {'Monday': '10:0-17:0', 'Tuesday': '10:0-17:0', 'Wednesday': '10:0-17:0', 'Thursday': '10:0-17:0', 'Friday': '10:0-17:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': True, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'paid', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'touristy': False, 'hipster': False, 'divey': False, 'classy': False, 'trendy': False, 'upscale': False, 'casual': False}}, 'business_stars': 3.5, 'review_info': [{'review_stars': 3.0, 'review_date': '2013-06-08 01:53:14', 'review_text': 'Its a shame, this place used to be so much better last year. They had a much wider variety last year. The curry chicken tasted almost like authentic chinese, and I enjoyed the Spicy Chicken every time. They switched around the menu, but usually they had 2 very good items everyday.\n\nNow, its pretty much the same generic items everyday. On top of that, they are almost always sold out, whether because its rush lunch hour, or its after 2 or 3 and they just give up making half the menu.\n\nI hear its getting replaced by Yoshinoya. I am glad because I love Yoshinoya.'}, {'review_stars': 1.0, 'review_date': '2013-03-07 21:26:31', 'review_text': 'I would say the food was good if I could ever have it. Every time I go to this place they are "out" of what I want, nothing on deck, just simply out. Some times when I go they tell me that things are going to be done at exactly 1pm (which may be over 30 mins away)...its especially frustrating when these should be (and probably are) the money makers for the business. Teriyaki chicken? ITS CHICKEN, why is this not in abundance?? Why does the business run out of it!??! Why is there a 50 cents extra charge for the simplest menu item??! I can\'t make sense of it, I won\'t be going back, it is simply absurd.'}, {'review_stars': 3.0, 'review_date': '2012-10-05 21:11:32', 'review_text': "Best place to eat anywhere near UCSB. It's cheap, it tastes awesome, and the service is fast and good. Everything tastes fresh, unlike Panda Express. Too bad it's gone now."}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

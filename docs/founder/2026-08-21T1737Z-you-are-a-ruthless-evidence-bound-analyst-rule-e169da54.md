---
captured: 2026-08-21T17:37:43+00:00
session: 2c07b517-fc67-4f5f-b1f6-bcb8e9e06f8f
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3120
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

Claim: Overall, Nikka Ramen is a must-visit destination for ramen lovers and fans of Japanese cuisine.

Passages:
[s0011] {'name': 'Nikka Ramen', 'address': '5701 Calle Real', 'city': 'Goleta', 'state': 'CA', 'categories': 'Restaurants, Japanese, Ramen', 'hours': {'Tuesday': '17:0-21:30', 'Wednesday': '17:0-21:30', 'Thursday': '17:0-21:30', 'Friday': '17:0-21:30', 'Saturday': '17:0-21:30', 'Sunday': '17:0-21:30'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': True, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'free', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'touristy': False, 'hipster': None, 'romantic': False, 'divey': False, 'intimate': False, 'trendy': True, 'upscale': False, 'classy': False, 'casual': True}}, 'business_stars': 4.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2022-01-19 06:15:16', 'review_text': "Amazing place, great food , great location. The atmosphere was fun, the music was great. I can tell it's a very popular spot. Servers are very attentive. I will definitely go back again."}, {'review_stars': 5.0, 'review_date': '2022-01-18 01:53:38', 'review_text': "Officially my favorite ramen spot. We don't live in the area but now make it a point to stop by and satisfy our Nikka craving whenever we're in Goleta.\n\nThe gyoza was a yummy appetizer but the spicy tuna was sooooo goood! I could eat 10 of those! The basic pork tonkatsu was just as delicious as I remember. Al dente noodles and broth cooked to perfection. The pork chashu is A1 quality. Every ingredient was meant to be on that plate from the tender pork chunks to the salad to the soft boiled egg.\n\nWe love Nikka. Period."}, {'review_stars': 5.0, 'review_date': '2022-01-07 01:34:51', 'review_text': 'Holly F@ck... mind blowing. Literally spent the last 20 minutes of my life having a mouth gasm. My knees are weak, And ima little sweaty. This ramen just had its way with me.... and I liked it'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

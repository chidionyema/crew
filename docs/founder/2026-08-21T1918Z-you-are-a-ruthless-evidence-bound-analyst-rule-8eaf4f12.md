---
captured: 2026-08-21T19:18:56+00:00
session: 68b1314c-fe5f-47cf-8a11-22a1a7592919
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2839
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

Claim: The customer also mentioned layoffs of long-term employees as a point of contention.

Passages:
[s0190] {'name': 'Haggen Food & Pharmacy', 'address': '163 S Turnpike Rd', 'city': 'Goleta', 'state': 'CA', 'categories': 'Food, Specialty Food, Grocery, Delis, Bakeries, Restaurants, Health Markets', 'hours': None, 'attributes': {'BusinessParking': None, 'RestaurantsReservations': False, 'OutdoorSeating': False, 'WiFi': 'no', 'RestaurantsTakeOut': False, 'RestaurantsGoodForGroups': None, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'classy': False, 'hipster': False, 'divey': False, 'touristy': False, 'trendy': False, 'upscale': False, 'casual': False}}, 'business_stars': 1.5, 'review_info': [{'review_stars': 1.0, 'review_date': '2015-09-29 21:56:52', 'review_text': 'We all know these guys are the worst, but STALE ICE CREAM, really?\nMy Thrifty brand Chocolate Malted Krunch ice cream had stale, gummy malt balls :('}, {'review_stars': 1.0, 'review_date': '2015-08-24 04:35:45', 'review_text': "@$!# you, Haggen!\n\nI was happy with my old vons who was just a block away.  Now I have to drive an exit away to the cheaper ralphs. Let's not forget that you laid off all the employees who have been there for years.\n\nBack to hell, demons! Back to hell!"}, {'review_stars': 1.0, 'review_date': '2015-08-04 17:42:35', 'review_text': "Worst grocery store in the world get outta Santa Barbara you SUUUUUUCK!!!!! Prices are too high for non organic food acting like it's organic n healthier just cause they don't package their produce so it's fresher even tho it's the same shit just trying to take our money, still going to Von's in other locations and by the way your stores are like ghost towns you ain't gonna survive hahahahah"}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T19:01:59+00:00
session: 137a1e1a-07b7-455e-8da6-c9c5da2fc623
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2735
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

Claim: One customer complained that the restaurant was closed and when it was open, the $1 menu items were actually priced at $1.59.

Passages:
[s0154] {'name': 'Taco Bell', 'address': '3771 State Street', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Fast Food, Restaurants, Tex-Mex, Mexican', 'hours': None, 'attributes': {'BusinessParking': None, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'free', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'classy': False, 'hipster': False, 'divey': False, 'touristy': False, 'trendy': False, 'upscale': False, 'casual': False}}, 'business_stars': 2.0, 'review_info': [{'review_stars': 1.0, 'review_date': '2015-12-16 22:03:54', 'review_text': 'CLOSED. Their $1 menu items were all $1.59. What was up with that, anyway?? The Milpas Taco Bell is still business as usual. And the $1 menu items are still $1.'}, {'review_stars': 1.0, 'review_date': '2015-10-16 06:31:41', 'review_text': 'Complete ripoff!!!! I bought a big box for the PlayStation promotion they have going on, I entered my code and I get a reply saying that the code has already been used. The only reason why I bought the box was for a chance to win. The employees must have used the codes, never coming to this taco bell again!'}, {'review_stars': 1.0, 'review_date': '2015-07-07 13:54:27', 'review_text': 'The restaurant is dirty. Outside the restaurant is also dirty. The floors of the patio outside is dirty. I will never invest my hard-earned money here due to sanitation reasons. My food will most likely be dirty & contaminated.'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

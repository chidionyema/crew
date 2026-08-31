---
captured: 2026-08-21T18:54:36+00:00
session: e96aab15-8082-4a01-b047-7767b928b6a0
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2803
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

Claim: The establishment is open every day, with varying operating hours.

Passages:
[s0139] {'name': 'Wine + Beer', 'address': '38 W Victoria St, Shop 113', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Wine Bars, Beer, Wine & Spirits, Wineries, Arts & Entertainment, Food, Nightlife, Bars, Beer Bar', 'hours': {'Monday': '11:0-21:0', 'Tuesday': '11:0-21:0', 'Wednesday': '11:0-18:0', 'Thursday': '11:0-22:0', 'Friday': '11:0-22:0', 'Saturday': '11:0-22:0', 'Sunday': '11:0-21:0'}, 'attributes': {'BusinessParking': {'garage': True, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': None, 'OutdoorSeating': None, 'WiFi': None, 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': None, 'Music': None, 'Ambience': None}, 'business_stars': 4.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2020-06-28 06:19:43', 'review_text': 'I just had the best 10 minutes of the past two weeks at Beer and Wine.\n\nBen, who helped me select wines from 3 continents was the most personable, polite and professional person I have met in a long time.\n\nHe really knows his stuff!'}, {'review_stars': 1.0, 'review_date': '2020-01-27 15:55:18', 'review_text': 'I would skip this place - limited selection, careless service and pricey.  Much better options to grab a beer or glass of wine all over Santa Barbara.  It is unfortunate because the Public Market is a great, fun place for lunch and dinner.'}, {'review_stars': 5.0, 'review_date': '2019-10-04 20:53:47', 'review_text': 'Great place to have a drink with a meal from the public market.  Nice selection of beers and wine on tap.  Had a couple free samples to help us decide.  Great local wines, and a not so local sour!'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

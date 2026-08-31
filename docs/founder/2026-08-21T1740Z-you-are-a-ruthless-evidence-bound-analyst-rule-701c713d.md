---
captured: 2026-08-21T17:40:19+00:00
session: b4835946-12ee-4745-91bd-123ba3cda7c9
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2825
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

Claim: The combination of good food, reasonable prices, and pleasant atmosphere make it a popular choice in Santa Barbara.

Passages:
[s0016] {'name': 'Courthouse Tavern', 'address': '129 E Anapamu St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, Bars, Nightlife, American (New), American (Traditional)', 'hours': None, 'attributes': {'BusinessParking': {'valet': False, 'garage': True, 'street': True, 'lot': False, 'validated': False}, 'RestaurantsReservations': None, 'OutdoorSeating': True, 'WiFi': None, 'RestaurantsTakeOut': None, 'RestaurantsGoodForGroups': None, 'Music': '{dj: None, live: False, jkebox: None, video: False, backgrond_msic: False, karaoke: None, no_msic: False}', 'Ambience': {'divey': False, 'hipster': None, 'casual': True, 'touristy': None, 'trendy': None, 'intimate': None, 'romantic': None, 'classy': None, 'upscale': None}}, 'business_stars': 4.0, 'review_info': [{'review_stars': 5.0, 'review_date': '2022-01-08 23:36:01', 'review_text': 'First time here and we will definitely be back. Sandwiches and cocktails were very, very good, and reasonably priced. Nice interior, great service.'}, {'review_stars': 5.0, 'review_date': '2021-12-21 03:27:03', 'review_text': 'I love this restaurant. Everything I have ordered has been delicious! The burgers are fabulous!! The restaurant is clean and the view of the courthouse is scenic. I hope more people go check it out.'}, {'review_stars': 4.0, 'review_date': '2021-12-05 18:47:09', 'review_text': 'Very nice outdoors & indoors space. The 4 of us (SB locals) had good burgers( fries were hot & crispy)!salad & a pasta dish. All was good food @  very reasonable price. Had nice red wine & margaritas. All good. Recommend giving this place a try.'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

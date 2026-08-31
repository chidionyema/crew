---
captured: 2026-08-21T18:46:42+00:00
session: 12bf7f47-2105-46ef-a6d2-bbab1a900306
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2775
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

Claim: Unfortunately, Cantwells Summerland Market appears to be closed according to one recent review, but previous reviews suggest that it was a popular destination for locals and visitors alike.

Passages:
[s0125] {'name': 'Cantwells Summerland Market', 'address': '2580 Lillie Ave', 'city': 'Summerland', 'state': 'CA', 'categories': 'Gas Stations, Delis, Automotive, Specialty Food, Restaurants, Convenience Stores, Fruits & Veggies, Food, Health Markets', 'hours': None, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': True, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'paid', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'classy': False, 'hipster': False, 'divey': False, 'touristy': False, 'trendy': False, 'upscale': False, 'casual': False}}, 'business_stars': 3.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2018-02-23 03:37:50', 'review_text': 'Was pricey, but convenient... the owner is the best, she actually helped me to get stuff I needed on the same day from else where...Sadly, it is already closed...'}, {'review_stars': 4.0, 'review_date': '2017-12-02 08:26:38', 'review_text': "Cantwell's is closing, all food probably gone. Too bad, they seemed to be busy. I liked coming here but they are gone."}, {'review_stars': 5.0, 'review_date': '2017-10-08 18:57:38', 'review_text': "The best food around, nice owners, and the employees that work there are amazing. I'm a local here in summerland and absolutely love going to this place from getting groceries to eating there amazing breakfast burritos!"}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

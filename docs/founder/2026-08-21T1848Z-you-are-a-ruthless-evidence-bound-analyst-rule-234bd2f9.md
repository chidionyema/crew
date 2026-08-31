---
captured: 2026-08-21T18:48:59+00:00
session: 0ff1a140-49b5-4f1e-bfed-7e3bbb9ad41f
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3096
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

Claim: On Saturdays, it opens from 12:00 to 21:00.

Passages:
[s0129] {'name': 'Yellow Belly', 'address': '2611 De La Vina St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'American (New), Pizza, Pubs, Nightlife, Bars, Restaurants, American (Traditional), Breakfast & Brunch, Beer Bar', 'hours': {'Monday': '0:0-0:0', 'Tuesday': '16:30-20:0', 'Wednesday': '16:30-20:0', 'Thursday': '16:30-20:0', 'Friday': '12:0-20:30', 'Saturday': '12:0-21:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': True, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': False, 'WiFi': 'free', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': False, 'Ambience': {'divey': False, 'hipster': None, 'casual': True, 'touristy': False, 'trendy': None, 'intimate': None, 'romantic': False, 'classy': False, 'upscale': False}}, 'business_stars': 4.0, 'review_info': [{'review_stars': 4.0, 'review_date': '2022-01-14 16:52:07', 'review_text': "Great neighborhood spot that never disappoints when we come to town. Always listen to recommendations from locals at the bar- they steered us right last night on the Mai Tai IPA and the Saison. We shared the seasonal apple, walnut and kale salad and the mand arugula pizza. Fantastic! I've previously had a fantastic burger there, too."}, {'review_stars': 5.0, 'review_date': '2022-01-07 02:41:32', 'review_text': 'Outstanding customer service! Great food, the fried chicken sandwich was so good! Relaxed atmosphere. This is a bar where you can relax and have a few good craft beers with tasty food. 10/10 would recommend and I will be coming back!'}, {'review_stars': 5.0, 'review_date': '2021-12-18 05:52:37', 'review_text': 'We got a couple delicious IPAs while we decided on food. The specials were great- Tri tip salad, curry chicken wings and flatiron steak- all perfectly grilled and prepared, with sauces on the side. Staff is knowledgeable and friendly. We always enjoy dinners at Yellow Belly.'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

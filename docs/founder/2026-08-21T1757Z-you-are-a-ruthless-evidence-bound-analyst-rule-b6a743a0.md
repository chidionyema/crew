---
captured: 2026-08-21T17:57:19+00:00
session: d09ef9aa-07f2-4019-ad9a-68576b4b217a
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3255
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

Claim: The restaurant has a casual and trendy atmosphere, with outdoor seating available.

Passages:
[s0040] {'name': 'Revolver', 'address': '1429 San Andres St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, Pizza', 'hours': {'Wednesday': '16:0-22:0', 'Thursday': '16:0-22:0', 'Friday': '16:0-22:0', 'Saturday': '16:0-22:0', 'Sunday': '16:0-22:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': None, 'OutdoorSeating': True, 'WiFi': 'free', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': None, 'Music': None, 'Ambience': {'divey': True, 'hipster': None, 'casual': None, 'touristy': None, 'trendy': True, 'intimate': None, 'romantic': None, 'classy': None, 'upscale': False}}, 'business_stars': 4.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2022-01-06 20:15:13', 'review_text': "Nothing derails my good intentions of starting a diet like a Revolver Pizza craving! It's absolutely the BEST!! Beautifully handmade crust and fresh toppings. Not fancy just delicious. And the salads are incredible. Best Caesar with real anchovy dressing. Market salad has yummy dill ranch, shaved vegetables on yummy lettuce. I don't love the atmosphere, so we always get it to go. It's super popular so get your order in early! But it's definitely our favorite pizza in SB."}, {'review_stars': 4.0, 'review_date': '2022-01-01 06:13:46', 'review_text': 'Great pizza but limited toppings odd hours and long wait time for food.\n\nThey really should open at 11am like any other normal pizza place.'}, {'review_stars': 5.0, 'review_date': '2021-12-20 02:58:37', 'review_text': "Hands down the best dang pizza in all of Santa Barbara. Not even close. Simple menu and from the crisp on the crust and bottom to the tang in the red sauce, SB you have a winner. It's artisan pizza meets NY on the west coast. Proves you don't need to be in the funk zone to have something great and feels like Brooklyn back 20\nYears ago in the fact that they are hip but hard working and making something great. The Caesar salad had a great dressing and fresh greens to boot."}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T19:24:44+00:00
session: 1ba27d3a-958d-4d40-a32d-78472065e140
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3400
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

Claim: The restaurant offers a range of Italian food options in a casual and welcoming atmosphere, making it a popular choice for locals and visitors alike.

Passages:
[s0199] {'name': 'Persona Pizzeria', 'address': '905 State St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Food, Italian, Pizza, Fast Food, Gelato, Chicken Wings, Sandwiches, Salad, Restaurants', 'hours': {'Monday': '11:30-20:0', 'Tuesday': '11:30-20:0', 'Wednesday': '11:30-20:0', 'Thursday': '11:30-20:0', 'Friday': '11:30-21:0', 'Saturday': '11:30-21:0', 'Sunday': '11:30-20:0'}, 'attributes': {'BusinessParking': {'garage': True, 'street': False, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': True, 'OutdoorSeating': True, 'WiFi': 'free', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'touristy': False, 'hipster': False, 'divey': False, 'classy': False, 'trendy': False, 'upscale': False, 'casual': True}}, 'business_stars': 4.0, 'review_info': [{'review_stars': 5.0, 'review_date': '2022-01-09 23:09:10', 'review_text': 'it was such a beautiful day today, that i decided to drive out to santa barbara and take my parents out in a little road trip. We did some shopping and happened to find this little hole in the wall pizza place. it was kind of hard to find bc their name has changed to cali-forno pizza lol. Andy was so kind, he accommodated us and make a delicious greek salad along with probably the best pizza we have ever had. this review is actually for jaime, our waiter. such a kind hearted amazing soul! he treated my parents and i like we were family. thank you so much, guys! we appreciate the kindness and the hospitality that you show to your customers, we felt so loved and cared for.'}, {'review_stars': 5.0, 'review_date': '2021-04-14 02:25:50', 'review_text': 'Randomly discovered this pizza place by walking on park at. Super yummy! Perfect casual spot. We had three small kids and ate outside. Staff was friendly. Restaurant was clean. Foos was good!'}, {'review_stars': 5.0, 'review_date': '2021-03-05 19:51:59', 'review_text': "Fast service, great flavor as well!! The staff is friendly! I like how the whole process works. Great lunch spot when you're on the go and want something fresh and fast."}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

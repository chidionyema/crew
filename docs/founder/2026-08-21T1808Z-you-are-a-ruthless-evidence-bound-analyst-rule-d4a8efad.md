---
captured: 2026-08-21T18:08:01+00:00
session: d97895aa-8e85-4e39-8514-e6950d418120
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2967
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

Claim: Another customer complained about the sandwich not being toasted on multiple occasions, even after speaking with the supervisor.

Passages:
[s0052] {'name': 'Subway', 'address': '1021 State St, Ste A', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Sandwiches, Restaurants, Fast Food', 'hours': {'Monday': '10:0-18:0', 'Tuesday': '10:0-18:0', 'Wednesday': '10:0-18:0', 'Thursday': '10:0-18:0', 'Friday': '10:0-18:0', 'Saturday': '11:0-18:0', 'Sunday': '11:0-18:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': True, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': False, 'WiFi': None, 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'classy': False, 'hipster': False, 'divey': False, 'touristy': False, 'trendy': False, 'upscale': False, 'casual': False}}, 'business_stars': 2.5, 'review_info': [{'review_stars': 1.0, 'review_date': '2020-10-29 04:55:07', 'review_text': 'I was halfway done w my sandwich and I felt something weird in my mouth. I spit it out and it was paper!! My sandwich had paper, I would go back to the store but they are closed. So disappointed...'}, {'review_stars': 1.0, 'review_date': '2020-06-17 20:47:54', 'review_text': "Ordered multiple times from this location and the sandwich didn't come toasted 3 times out of more than 10 orders. The only way to get a refund after talking to the supervisor was to go all the way back and return the subs. Horrible customer service don't recommend going here or ordering on the app from here."}, {'review_stars': 5.0, 'review_date': '2019-12-25 21:42:18', 'review_text': "Went there on Christmas Day the girl working was awesome great smile and very kind hearted wish I could have gave a tip on my card so I purchased her a steak sub I'll be back. Jacob"}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

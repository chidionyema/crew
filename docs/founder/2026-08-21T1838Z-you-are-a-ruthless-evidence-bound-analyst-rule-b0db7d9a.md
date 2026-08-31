---
captured: 2026-08-21T18:38:45+00:00
session: e0a4fb5d-1992-4fbf-b185-920714d46bff
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 4319
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

Claim: According to customer reviews, the restaurant has a casual ambiance, and the staff provides excellent customer service.

Passages:
[s0109] {'name': 'IHOP', 'address': '1114 Casitas Pass Rd', 'city': 'Carpinteria', 'state': 'CA', 'categories': 'Restaurants, Breakfast & Brunch, American (New), American (Traditional), Burgers', 'hours': {'Monday': '0:0-0:0', 'Tuesday': '6:0-20:0', 'Wednesday': '6:0-20:0', 'Thursday': '6:0-20:0', 'Friday': '8:0-20:0', 'Saturday': '6:0-20:0', 'Sunday': '6:0-20:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': True, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': False, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'touristy': False, 'hipster': False, 'romantic': False, 'divey': False, 'intimate': False, 'trendy': False, 'upscale': False, 'classy': False, 'casual': True}}, 'business_stars': 2.5, 'review_info': [{'review_stars': 1.0, 'review_date': '2022-01-02 19:49:44', 'review_text': 'When we entered, there were good tables open, still they tried to sit us in inside secluded table. \n\nWe are seniors ordered from seniors menu, he charged us full price. \n\nI ordered hot drink, he gave me ice-cold drink, then he was willing to change; but still......\n\nTotally dissatisfied.'}, {'review_stars': 3.0, 'review_date': '2021-08-25 23:24:25', 'review_text': 'It was my sons first day at kindergarten so I decided to take his mother to ihop to catch up and have some breakfast. I could tell the kitchen must have been like an episode of kitchen nightmares with Gordon Ramsay.\n\nI ordered the breakfast sampler, everything was cooked well but the eggs were basically a gelatinous consistency almost as if they were only cooked on one side and the bottom side of the eggs touching the plate were completely raw like they just flipped a raw egg onto my plate and called it a day so I just simply did not finish the meal after I lost my appetite from the raw food.\n\nShe ordered a chicken sandwich (yes I\'m aware that\'s a strange thing to order at 9:00 - 10:00 in the morning) and it came with a completely random "potato cake" they called it, sat on top of the chicken patty it was honestly the most random food item I have ever seen served before almost like something off of jack in the boxes late night munchie meals. On the bright side, we got a free "potato cake" :)\n\nThe front is great, amazing customer service and the manager came and walked around and greeted all of the customers that were eating and it was just a great positive atmosphere to be in you could tell they cared. My review is about the laziness of the kitchen on that day I had gone (monday) as it was not very busy at all so I really didn\'t see the point in rushing food to our table. I would have rather waited an extra 10 minutes than to have had my food served to me barely cooked without any love.'}, {'review_stars': 5.0, 'review_date': '2021-06-25 05:32:02', 'review_text': 'We had breakfast at the Carpinteria, Ca IHOP restaurant twice this week while on vacation. Both times, the food was served hot and the service was excellent! The manager is very attentive and friendly.'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

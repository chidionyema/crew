---
captured: 2026-08-21T18:44:58+00:00
session: deed1ef9-9e56-414a-b75e-eada0efa202c
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 4009
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

Claim: The restaurant serves burgers, sandwiches, and other fast food items.

Passages:
[s0121] {'name': "Carl's Jr", 'address': '4610 Carpinteria Ave', 'city': 'Carpinteria', 'state': 'CA', 'categories': 'Burgers, Restaurants, Fast Food', 'hours': {'Monday': '7:0-22:0', 'Tuesday': '7:0-22:0', 'Wednesday': '7:0-22:0', 'Thursday': '7:0-22:0', 'Friday': '7:0-22:0', 'Saturday': '7:0-22:0', 'Sunday': '7:0-22:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': True, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'classy': False, 'hipster': False, 'divey': False, 'touristy': False, 'trendy': False, 'upscale': False, 'casual': False}}, 'business_stars': 2.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2022-01-08 22:26:29', 'review_text': "I don't write many reviews on here, less so for a fast food restaurant but man oh man did this place impress me. Right when I walked in Ruben greeted me like we were old friends and was a beacon of service from the moment I stepped through the doors. I tried the hot honey chicken sandwich, it came out within 3 minutes and was delicious. Bacon was crispy, the chicken perfectly cooked, and the bun was not soggy at all. I had a great quick meal and was so impressed by Ruben that I had to come on here to give a review. Thank you so much for being so kind and helpful. If you're on a road trip and Ruben is working you'll be in for a delightful pit stop."}, {'review_stars': 5.0, 'review_date': '2021-11-28 18:43:37', 'review_text': "We had to exit to this city cause traffic was so bad omw home from Solvang.  People in Carpinteria are either super kind or they're flippant and don't like visitors  in their town. \nRUBEN was so kind and welcoming this morning as I entered to get a veggie breakfast burrito to soak in the 90 glasses of red wine. He has fabulous energy and took pride in his work and love for this city. I love people like him cause positive energy is contagious and started off my day beautifully! \nCarl's Jr is so lucky to have him on board. \n\nNo drive through fyi."}, {'review_stars': 2.0, 'review_date': '2021-10-08 01:22:50', 'review_text': "I used to eat breakfast there almost every day but in the last 2 weeks that I ate there I got really sick twice!! I believe it was the sausage because it was like black and dried out! Sausage should be brown not black! So I stopped eating there. I'll get a burger from time to time but usually only with coupons. The workers are very friendly and helpful, it's just the food that lacks. It's pretty expensive for burgers but even when they give you specials by the time you buy the fries and the soda you end up spending even more than a combo. I guess every place is expensive now though."}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

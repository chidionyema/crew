---
captured: 2026-08-21T18:41:03+00:00
session: 776b92f1-c1a4-476f-82b3-526722a1c7d3
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3059
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

Claim: They offer takeout and reservations, and have outdoor seating, WiFi, and parking available.

Passages:
[s0114] {'name': "Meat n' Potatoes", 'address': '4444 Hollister Ave', 'city': 'Goleta', 'state': 'CA', 'categories': 'American (Traditional), Restaurants', 'hours': None, 'attributes': {'BusinessParking': None, 'RestaurantsReservations': True, 'OutdoorSeating': True, 'WiFi': None, 'RestaurantsTakeOut': None, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'touristy': False, 'hipster': False, 'divey': False, 'classy': False, 'trendy': False, 'upscale': False, 'casual': True}}, 'business_stars': 4.0, 'review_info': [{'review_stars': 4.0, 'review_date': '2012-11-12 01:42:39', 'review_text': 'Came for the pizza and ended up ordering the fish tacos.  They were really good and agree with other reviews on the brussel sprouts.  Dessert list is sort of blah, but overall it was a good dining experience.'}, {'review_stars': 5.0, 'review_date': '2012-11-09 03:50:21', 'review_text': "Pizza is simple and wonderful!  I hear they use the old Deano's Pizza recipe."}, {'review_stars': 1.0, 'review_date': '2012-09-11 22:55:32', 'review_text': "Their menu selections were kind of strange.  I wan't sure what type of restaurant this was - - American fare or tapas?  Ordered the basic for dinner - - hamburger with fries.  Unfortunately, I couldn't finish the burger.  It was so salty (and I am a salt maniac).  I really tried to like it but it also didn't taste freshly made, ie. the burger patty had a strange texture, densely formed, and I wouldn't be surprised if it was pulled directly out of the freezer and put on the grill.  The waiter was nice, but it is too bad the food wasn't good.  The interior decor was a dark and dingy and felt like an extension of the biker bar next door.  The patio looked inviting, but it was too cold outside to try it.  Parking was difficult (getting in and out) once a spot was found."}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

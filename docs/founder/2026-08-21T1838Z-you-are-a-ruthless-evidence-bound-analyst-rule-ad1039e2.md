---
captured: 2026-08-21T18:38:16+00:00
session: 97f73460-6eb0-418f-8d0a-044fba9e6be3
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3974
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

Claim: The business hours are Monday from 9 AM to 7 PM and Saturday from 1 PM to 1:30 PM.

Passages:
[s0108] {'name': "C'est Cheese", 'address': '827 Santa Barbara St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Specialty Food, Cheese Shops, Cafes, Restaurants, Breakfast & Brunch, Wine Bars, Sandwiches, Food, Event Planning & Services, Caterers, Bars, Nightlife', 'hours': {'Monday': '0:0-0:0', 'Saturday': '1:0-1:30'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'classy': False, 'hipster': False, 'divey': False, 'touristy': False, 'trendy': False, 'upscale': False, 'casual': True}}, 'business_stars': 4.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2020-12-28 20:43:32', 'review_text': 'I loved this place. It is like a candy store for cheese and cured meats. We came here pre-covid and it was packed. \nWe waited our turn and when it was the staff was so nice asking us what we liked and icing us samples of what they had and offering suggestions. Turns out if you get a cheese board, you can have it delivered to the winery next door so that is exactly what we did. We got their standard board which for $25 had three cheese, some bits and some fig jam and added two more selections.  Everything was delicious and the board was presented beautifully. \n\nThe shop also has a bunch of cheese related items like knives as well as other kitchen items like hand towels, glasses and cutting boards. And of course they sell bottles of wine and spreads to go along with the cheese.'}, {'review_stars': 5.0, 'review_date': '2020-04-09 23:42:25', 'review_text': "Wonderful cheese and snack selection! I ordered a big delivery as part of my quarantine grocery situation, and it is sooo worth it. We got 7 different cheeses, olives, baguette, chicken pate, ham, dolma, arancini, and a bottle of white. Everything is delicious, especially the cheese of course. I asked my husband how the ham is, and his eyes literally rolled back in his head. C'est Cheese - you got that yummy yummy."}, {'review_stars': 5.0, 'review_date': '2020-03-24 00:12:29', 'review_text': 'Popped in the other day to get my cheese and charcuterie fix. I went with a classic French Brie and a little of the mole and caprese salamis (both have a nice little kick). I can never resist the fresh baguettes!  Staff are always very knowledgeable and will help you find something that matches your taste it to pair with a particular wine you plan to enjoy. I usually end up sampling a couple new cheeses and am always blown away by the variety. So grateful to have this local gem within walking distance to feed my cheese addictions.'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

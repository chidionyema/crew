---
captured: 2026-08-21T18:41:58+00:00
session: 77d291b1-a70c-4b53-a6b2-05be8fcf7ac1
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3860
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

Claim: The restaurant has a rating of 3.5 out of 5 stars on Google, with most reviews being negative.

Passages:
[s0116] {'name': "Mayo's Carniceria & Tacos", 'address': '2704 De La Vina St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Mexican, Restaurants', 'hours': {'Monday': '8:0-20:0', 'Tuesday': '8:0-20:0', 'Wednesday': '8:0-20:0', 'Thursday': '8:0-20:0', 'Friday': '8:0-20:0', 'Saturday': '8:0-20:0', 'Sunday': '8:0-20:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': False, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': False, 'Music': None, 'Ambience': {'touristy': False, 'hipster': False, 'romantic': False, 'divey': False, 'intimate': False, 'trendy': False, 'upscale': False, 'classy': True, 'casual': False}}, 'business_stars': 3.5, 'review_info': [{'review_stars': 1.0, 'review_date': '2021-01-24 06:15:13', 'review_text': 'DONT GO!! Disgusting! A few months ago i went in and bought some meat. When i got home it was green with some mold growing and smelled horrible!! I went back to return it and to get my money back and the owner got mad and told me that that\'s how its supposed to be! Like really C\'mon! Im not dumb i know when meat is bad ive been cooking all my life. Their meat display is so low quality and not at the right temperatures, so much cross contamination with red meats and chicken. Their "fresh" produce are always warm and never fresh. They always sell bad and rotten veggies. Another incident that happened, a few days ago i went to buy a soda. A soda cant go bad. YEAH RIGHT! I got the soda all the way from the back it was hot (whatever ill put it in the fridge when i get home) when i opened the soda there was no gas i tasted it and it was SO concentrated, all sugar i had to throw away! Just simply dont go here and don\'t consume there foods.'}, {'review_stars': 1.0, 'review_date': '2020-12-04 00:08:16', 'review_text': "The food we got was horrible.  I ordered a Torta and it was dry and tasteless.  I got takeout and it was missing the beans/rice cart blanche order.  My wife's combo of an enchilada and taco was missing its beans/rice.  No sauce in the enchilada-- terrible, terrible, terrible.  And add to this insult -- no napkins or plastic utensils.  I only hoe is that we don't get sick from the meal.  I didn't eat much of the meal -- so sad.  So for $23 I got no satisfaction."}, {'review_stars': 4.0, 'review_date': '2020-10-09 06:26:27', 'review_text': 'Their Torta Ahogada is amazing! Now this is Mexican food. The sauce they use is spicy spicy but that good heat you get mad at your mouth for not being able to handle it because you want to keep on eating.'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

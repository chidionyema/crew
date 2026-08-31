---
captured: 2026-08-21T18:21:36+00:00
session: f9c18cbf-69b3-47bd-b523-607757c219ec
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3730
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

Claim: Their hours of operation vary throughout the week, but they are open from 12:00 PM on Saturdays and Sundays.

Passages:
[s0066] {'name': 'Uptown Bar & Lounge', 'address': '3126 State St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Lounges, Karaoke, American (New), Mexican, Sports Bars, Tacos, Restaurants, Pizza, Bars, Nightlife, Food, Beer, Wine & Spirits', 'hours': {'Monday': '0:0-0:0', 'Tuesday': '15:0-23:0', 'Wednesday': '15:0-23:0', 'Thursday': '15:0-23:0', 'Friday': '15:0-1:0', 'Saturday': '12:0-1:0', 'Sunday': '12:0-23:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': True, 'valet': False}, 'RestaurantsReservations': True, 'OutdoorSeating': True, 'WiFi': 'free', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': True, 'Ambience': {'touristy': False, 'hipster': False, 'romantic': False, 'divey': False, 'intimate': False, 'trendy': False, 'upscale': False, 'classy': True, 'casual': True}}, 'business_stars': 4.0, 'review_info': [{'review_stars': 2.0, 'review_date': '2021-12-28 23:11:32', 'review_text': 'While polite, the ammonia smell was dismissed when asked and also surprise!  There\'s a 35 dollar holding amount on pen tabs ( mine was 6 dollars at the end) that holds for 2 to 3 days. Something you\'d think should be explained at the start of opening a tab. Especially if it\'s not busy. When called and asked about this mysterious 35 dollar charge it was met with a question of "the bartender didn\'t tell you about it? " Remembering my last visit to this place recalling there was no explication of 35 dollars being held. Further explication of why there is a 35 dollar hold was said "if someone can\'t pay their tab or leave before paying,  blah blah blah." I stopped caring. Was recommended to pay and close as I go or bring cash when drinking there. Unfortunately I will not be returning. Sorry you have less than great customers that cause you to HAVE to take 35 dollars out. Perhaps we evaluate. Good bye Uptown.'}, {'review_stars': 5.0, 'review_date': '2021-10-24 15:26:28', 'review_text': "I attended a friend's birthday party at the Uptown and was so impressed with the staff, food and surroundings.\n\nSeriously loved the whole experience. The staff couldn't have been more accommodating. Food was fresh & delicious, drinks were great.\n\nWill be returning soon for happy hour with friends.\nGreat local treasure :)"}, {'review_stars': 5.0, 'review_date': '2021-10-10 18:44:18', 'review_text': 'Hands down my favorite pizza in town. The tri tip pizza is so worthwhile. Drinks are great and always an incredibly fun atmosphere.'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T18:43:45+00:00
session: 229146e0-6781-4c0a-8b4e-46df1c97e210
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3112
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

Claim: Another customer also gave a positive review and enjoyed sitting down to relax with friends while having a drink.

Passages:
[s0119] {'name': 'Carpinteria and Linden Pub', 'address': '4954 Carpinteria Ave', 'city': 'Carpinteria', 'state': 'CA', 'categories': 'Pubs, Bars, Nightlife', 'hours': {'Monday': '15:0-0:0', 'Tuesday': '15:0-0:0', 'Wednesday': '15:0-0:0', 'Thursday': '15:0-0:0', 'Friday': '15:0-2:0', 'Saturday': '16:0-2:0', 'Sunday': '15:0-2:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': False, 'WiFi': 'free', 'RestaurantsTakeOut': None, 'RestaurantsGoodForGroups': True, 'Music': '{dj: None, live: False, jkebox: Tre, video: False, backgrond_msic: False, karaoke: None, no_msic: False}', 'Ambience': {'divey': True, 'hipster': None, 'casual': True, 'touristy': None, 'trendy': None, 'intimate': False, 'romantic': None, 'classy': None, 'upscale': False}}, 'business_stars': 3.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2020-03-20 05:09:18', 'review_text': "If you live in or visit Santa Barbara, seek out this secret gem in Carpinteria. Sweet little beach town spot to let your hair down. RELAX, HAVE A GOOD TIME, NO JUDGEMENTS... Just real people. \nThe owner Katie and Todd made us feel right at home. Super fun!\nGreat place to watch sports, play ping pong &shoot.\nLife sized Jenga, and if you're lucky a surprise piano man!"}, {'review_stars': 5.0, 'review_date': '2020-02-05 02:37:35', 'review_text': 'A wonderful experience,it feels awesome and like your at home,excellent service,my sister came down from Texas,sit down relax and have a beer or cocktail with some friends,,'}, {'review_stars': 1.0, 'review_date': '2019-07-30 03:43:49', 'review_text': 'This was a sketchy place.. it was hard to stay there more than 10 minutes.. A huge dog almost ate me on the way in. Everyone there had a great sense of humor, but the Yelp ranking failed me on this decision..'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

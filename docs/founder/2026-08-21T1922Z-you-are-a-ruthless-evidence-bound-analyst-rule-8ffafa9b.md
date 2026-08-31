---
captured: 2026-08-21T19:22:54+00:00
session: 6993a385-6e40-4ae5-929b-a58757f7942c
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2815
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

Claim: Overall, The Study Hall has a mixed reputation, with some negative experiences reported by customers.

Passages:
[s0197] {'name': 'The Study Hall', 'address': '6543 Pardall Rd', 'city': 'Isla Vista', 'state': 'CA', 'categories': 'Bars, Nightlife', 'hours': {'Monday': '19:0-0:0', 'Tuesday': '18:0-0:0', 'Wednesday': '18:0-0:0', 'Thursday': '18:0-0:0', 'Friday': '18:0-0:0', 'Saturday': '16:0-0:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': None, 'validated': None, 'lot': None, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': False, 'WiFi': 'free', 'RestaurantsTakeOut': None, 'RestaurantsGoodForGroups': True, 'Music': True, 'Ambience': {'touristy': None, 'hipster': None, 'romantic': None, 'divey': True, 'intimate': None, 'trendy': None, 'upscale': None, 'classy': None, 'casual': None}}, 'business_stars': 3.0, 'review_info': [{'review_stars': 1.0, 'review_date': '2021-04-18 20:43:05', 'review_text': 'The owner/manager was drunk on the job and kept trying to touch me so gross and was interrupting me and my friend in conversation. Also the drinks were horrible I will not be back'}, {'review_stars': 1.0, 'review_date': '2020-08-21 17:02:46', 'review_text': 'Why is this bar still open during the COVID-19 pandemic when there is a statewide order for bars to remain closed. There are always creepy men sitting outside in the new patio area on Pardall staring at girls and catcalling. This place shows the worst side of Isla Vista.'}, {'review_stars': 1.0, 'review_date': '2020-02-20 07:52:18', 'review_text': 'Horrible scary place. Multiple friends I know have been drugged here and we think it was the bartenders. Please stay away for your safety and tell friends to avoid here.'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

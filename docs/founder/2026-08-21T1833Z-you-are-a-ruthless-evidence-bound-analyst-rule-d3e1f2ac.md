---
captured: 2026-08-21T18:33:30+00:00
session: ef4b3ae1-4615-4ad8-b6ca-3f9c11a60a60
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3151
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

Claim: The Champagne Room is recommended for both dates and group gatherings.

Passages:
[s0098] {'name': 'Champagne Room', 'address': '7 W Haley St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Champagne Bars, Bars, Nightlife', 'hours': {'Tuesday': '17:0-0:0', 'Wednesday': '17:0-0:0', 'Thursday': '17:0-0:0', 'Friday': '17:0-0:0', 'Saturday': '17:0-0:0', 'Sunday': '15:0-22:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': True, 'OutdoorSeating': False, 'WiFi': 'no', 'RestaurantsTakeOut': None, 'RestaurantsGoodForGroups': True, 'Music': True, 'Ambience': {'touristy': False, 'hipster': False, 'romantic': True, 'divey': False, 'intimate': False, 'trendy': False, 'upscale': False, 'classy': True, 'casual': False}}, 'business_stars': 5.0, 'review_info': [{'review_stars': 5.0, 'review_date': '2017-07-22 02:27:44', 'review_text': 'Fantastic spot! Hidden gem and perfect for a night out. Great staff and great owners. Super friendly atmosphere and affordable menu. A must see!'}, {'review_stars': 5.0, 'review_date': '2017-07-21 18:44:20', 'review_text': "We were in Santa Barbara for one night only staying at the HIE. The Champagne Room was right next door and had great reviews so we checked it out. It's a pretty small place with cool intimate seating and a bar area. Lila was running the place when we went and was sooo great!! She was really funny and helpful. She suggested we split a bottle (can't remember the name), but it was soooo good! \n\nGreat place for the start of a night out!"}, {'review_stars': 5.0, 'review_date': '2017-06-11 00:22:00', 'review_text': "What a fantastic treat to find a dedicated hip champagne lounge in downtown Santa Barbara. They do offer mote than champagne - and their selection if champagne and sparkling wines are great. It's a great date place.  They have a lovely lounge atmosphere which is a throw back to a vintage french salon. Great for a group. A wonderful find and much needed addition to State Street."}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

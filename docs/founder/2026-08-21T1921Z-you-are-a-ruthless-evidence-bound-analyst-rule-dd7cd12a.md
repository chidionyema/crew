---
captured: 2026-08-21T19:21:01+00:00
session: 1aea0436-4572-4f2b-8d4e-27aea04d659b
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1770
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

Claim: Their hours of operation are Monday through Sunday from 8am to 8pm.

Passages:
[s0195] {'name': 'Beans BBQ and Catering', 'address': '', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Wedding Planning, Barbeque, Event Planning & Services, Restaurants, Caterers, Personal Chefs', 'hours': {'Monday': '0:0-0:0', 'Tuesday': '8:0-20:0', 'Wednesday': '8:0-20:0', 'Thursday': '8:0-20:0', 'Friday': '8:0-20:0', 'Saturday': '8:0-20:0', 'Sunday': '8:0-20:0'}, 'attributes': {'BusinessParking': None, 'RestaurantsReservations': False, 'OutdoorSeating': False, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': None, 'Music': None, 'Ambience': {'divey': False, 'hipster'

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

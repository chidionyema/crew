---
captured: 2026-08-21T18:37:36+00:00
session: f88cc885-ce25-4971-9954-1ce0ab2d75de
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1800
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

Claim: Ca'Dario Pizzeria Veloce is a pizza restaurant located in the Public Market in Santa Barbara, CA.

Passages:
[s0107] {'name': "Ca'Dario Pizzeria Veloce", 'address': '38 W Victoria St, Ste 104', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, Pizza', 'hours': {'Monday': '11:0-22:0', 'Tuesday': '11:0-22:0', 'Wednesday': '11:0-22:0', 'Thursday': '11:0-22:0', 'Friday': '11:0-22:0', 'Saturday': '11:0-22:0', 'Sunday': '11:0-22:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': None, 'WiFi': None, 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

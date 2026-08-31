---
captured: 2026-08-21T18:44:34+00:00
session: 1121efe3-ae71-4fd1-95f4-5b1394ae0cbe
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1772
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
[s0121] {'name': "Carl's Jr", 'address': '4610 Carpinteria Ave', 'city': 'Carpinteria', 'state': 'CA', 'categories': 'Burgers, Restaurants, Fast Food', 'hours': {'Monday': '7:0-22:0', 'Tuesday': '7:0-22:0', 'Wednesday': '7:0-22:0', 'Thursday': '7:0-22:0', 'Friday': '7:0-22:0', 'Saturday': '7:0-22:0', 'Sunday': '7:0-22:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': True, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'r

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

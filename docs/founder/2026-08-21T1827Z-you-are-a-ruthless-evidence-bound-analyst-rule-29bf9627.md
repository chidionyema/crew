---
captured: 2026-08-21T18:27:24+00:00
session: 83467156-e824-4f7f-8cb3-a840c867f8af
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1771
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

Claim: The ambiance is casual and welcoming, with a divey and hipster vibe.

Passages:
[s0087] {'name': 'Breakwater Restaurant', 'address': '107 Harbor Way', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, American (Traditional), Seafood, Breakfast & Brunch', 'hours': {'Monday': '0:0-0:0', 'Tuesday': '8:0-16:45', 'Wednesday': '8:0-19:0', 'Thursday': '8:0-14:0', 'Friday': '8:0-14:0', 'Saturday': '8:0-19:0', 'Sunday': '8:0-19:0'}, 'attributes': {'BusinessParking': {'valet': False, 'garage': None, 'street': None, 'lot': None, 'validated': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

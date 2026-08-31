---
captured: 2026-08-21T18:38:03+00:00
session: bfc17514-fcde-424e-a9ac-bc518d2e2fcf
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1785
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
[s0108] {'name': "C'est Cheese", 'address': '827 Santa Barbara St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Specialty Food, Cheese Shops, Cafes, Restaurants, Breakfast & Brunch, Wine Bars, Sandwiches, Food, Event Planning & Services, Caterers, Bars, Nightlife', 'hours': {'Monday': '0:0-0:0', 'Saturday': '1:0-1:30'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambien

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

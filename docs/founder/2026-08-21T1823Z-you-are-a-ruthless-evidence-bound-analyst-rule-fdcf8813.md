---
captured: 2026-08-21T18:23:22+00:00
session: fa316a8b-53b1-43f1-bd1c-70c3439dc9c6
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1831
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

Claim: Another customer mentioned that the food was dry, tasteless, and expensive, expressing disappointment with the quality and cost.

Passages:
[s0078] {'name': 'Marbella', 'address': '1111 E Cabrillo Blvd', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Tapas/Small Plates, Restaurants, Breakfast & Brunch, Seafood, American (New)', 'hours': {'Monday': '17:0-22:0', 'Tuesday': '17:0-22:0', 'Wednesday': '17:0-22:0', 'Thursday': '17:0-22:0', 'Friday': '17:0-22:0', 'Saturday': '17:0-22:0', 'Sunday': '17:0-22:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': False, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': True, 'OutdoorSeating': True, 'WiFi': 'paid', 'RestaurantsTakeOut': True, 'Restaura

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

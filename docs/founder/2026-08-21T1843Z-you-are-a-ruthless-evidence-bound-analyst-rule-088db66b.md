---
captured: 2026-08-21T18:43:34+00:00
session: d65113d9-bee7-450e-9925-c88c3013f4e8
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1816
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
[s0119] {'name': 'Carpinteria and Linden Pub', 'address': '4954 Carpinteria Ave', 'city': 'Carpinteria', 'state': 'CA', 'categories': 'Pubs, Bars, Nightlife', 'hours': {'Monday': '15:0-0:0', 'Tuesday': '15:0-0:0', 'Wednesday': '15:0-0:0', 'Thursday': '15:0-0:0', 'Friday': '15:0-2:0', 'Saturday': '16:0-2:0', 'Sunday': '15:0-2:0'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': False, 'WiFi': 'free', 'RestaurantsTakeOut': None, 'RestaurantsGoodForGroups': True, 'Music': '{dj: None,

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

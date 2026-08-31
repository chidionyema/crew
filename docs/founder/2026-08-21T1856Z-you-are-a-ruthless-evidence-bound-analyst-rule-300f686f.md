---
captured: 2026-08-21T18:56:45+00:00
session: 64c80d58-70b2-4f29-b25e-8567d68c9595
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3804
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

Claim: The business operates from Monday to Friday, from 9:00 AM to 5:30 PM.

Passages:
[s0144] {'name': 'University Club of Santa Barbara', 'address': '1332 Santa Barbara St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, Event Planning & Services, Party & Event Planning, Food, Venues & Event Spaces, Arts & Entertainment, Social Clubs, Specialty Food', 'hours': {'Monday': '9:0-17:30', 'Tuesday': '9:0-17:30', 'Wednesday': '9:0-17:30', 'Thursday': '9:0-17:30', 'Friday': '9:0-17:30'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': True, 'valet': False}, 'RestaurantsReservations': None, 'OutdoorSeating': None, 'WiFi': None, 'RestaurantsTakeOut': None, 'RestaurantsGoodForGroups': None, 'Music': None, 'Ambience': None}, 'business_stars': 5.0, 'review_info': [{'review_stars': 5.0, 'review_date': '2021-10-26 19:14:20', 'review_text': "We got married at the university club/ Riviera Mansion October 2021- and it truly couldn't have been a more perfect venue! The day felt completely magical, the staff was incredible, professional, and helpful, and the packages they offer make planning so simple. We worked closely with Christy, the venue/wedding coordinator, and she is absolutely amazing! Super responsive and helpful + clearly lists out options. For anyone looking for a venue in Santa Barbara, I'd 10/10 recommend this place!"}, {'review_stars': 5.0, 'review_date': '2019-09-26 18:28:37', 'review_text': 'Came here for lunch with my Aunt who is a member.  We sat on the gorgeous patio.   Excellent options on the menu - something for everyone.  The service is IMPECCABLE.  I got there early and was treated like a valued guest.  I was there on free glass of wine day - the wine was wonderful.  I ordered the French Dip sandwich. My cousin ordered the fresh ahi and my aunt had the soup.  Generous servings.  Again, our waiter and waitress made this such a wonderful afternoon.  Food is really good, but service here and ambiance is five star all day long.'}, {'review_stars': 5.0, 'review_date': '2019-08-08 19:31:13', 'review_text': 'The Riviera Mansion was the first wedding venue we looked at and the one we ended up falling for. We loved that it had the option of indoor/outdoor spaces and that we could have the entire venue to ourselves for the day. It was the perfect size to accommodate our 100 guests comfortably. The mansion and the grounds were a beautiful backdrop for all of our photos as well. Breanna was very responsive to all of our questions and was so great to work with. Chef Jamie was also nice enough to help us create a menu that met our needs and was present at our tasting to meet with us. Very pleased with our choice!!'}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

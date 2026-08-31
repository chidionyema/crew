---
captured: 2026-08-21T18:29:23+00:00
session: 135bf38d-cc95-4817-a8f8-b04ff338aaf8
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3312
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

Claim: Based on customer reviews, Big Joe's Tacos is well known for their delicious tacos and excellent service.

Passages:
[s0091] {'name': "Big Joe's Tacos", 'address': '3754 San Remo Dr', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Food Trucks, Event Planning & Services, Mexican, Street Vendors, Caterers, Restaurants, Food', 'hours': None, 'attributes': {'BusinessParking': None, 'RestaurantsReservations': None, 'OutdoorSeating': None, 'WiFi': None, 'RestaurantsTakeOut': None, 'RestaurantsGoodForGroups': None, 'Music': None, 'Ambience': None}, 'business_stars': 4.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2021-11-16 01:27:54', 'review_text': "Just had Joe cater our wedding in Santa Barbara. It was a semi destination wedding so I couldn't meet in person to taste the food and arrange the details. I booked based on yelp reviews alone and I was NOT disappointed. Joe worked with me via email to arrange everything and accepted payment via Venmo. He responded quickly to my questions and was very reasonably priced. They showed up on time, cooked the food on site, and set up their own canopies and tables. The food was served right on schedule and perfectly made. Joe was so nice when I met him at the venue and I literally am still getting compliments from guests on the tacos. The chips and guac they served at the cocktail hour was perfect! I am so happy with my choice and highly recommend them to anyone looking to have some delicious food from a low stress vendor at any special event! Big Joe's has some of the best tacos around!!"}, {'review_stars': 2.0, 'review_date': '2021-10-14 14:17:34', 'review_text': "We hired Big Joes for my son's wedding rehearsal dinner and they were difficult to communicate with with delayed responses . They forgot the churro bar , big disappointment! ! and the guacamole was watery and inedible !  When I contacted them to discuss the issues they never responded or apologized. Bad business !  I recommend Alvaro with La Colmena Catering !"}, {'review_stars': 5.0, 'review_date': '2021-05-19 01:00:32', 'review_text': "Big Joe was awesome, and delivered the taco bar set-up right to our campground. It was a big hit, and we'd definitely order again. Thanks!"}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

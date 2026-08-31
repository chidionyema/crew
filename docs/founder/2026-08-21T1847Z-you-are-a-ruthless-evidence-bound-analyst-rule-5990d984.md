---
captured: 2026-08-21T18:47:27+00:00
session: 319f369e-9038-4d86-884d-9932a76d9240
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3925
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

Claim: With a rating of 3.5 stars, the cafe offers a cozy atmosphere and delicious food.

Passages:
[s0127] {'name': 'Beachbreak Cafe', 'address': '324 State St', 'city': 'Santa Barbara', 'state': 'CA', 'categories': 'Restaurants, Breakfast & Brunch, American (Traditional), Cafes', 'hours': {'Monday': '7:0-14:30', 'Tuesday': '7:0-14:30', 'Wednesday': '7:0-14:30', 'Thursday': '7:0-14:30', 'Friday': '7:0-14:30', 'Saturday': '7:0-14:30', 'Sunday': '7:0-14:30'}, 'attributes': {'BusinessParking': {'garage': False, 'street': True, 'validated': False, 'lot': False, 'valet': False}, 'RestaurantsReservations': False, 'OutdoorSeating': True, 'WiFi': 'no', 'RestaurantsTakeOut': True, 'RestaurantsGoodForGroups': True, 'Music': None, 'Ambience': {'romantic': False, 'intimate': False, 'touristy': False, 'hipster': False, 'divey': False, 'classy': False, 'trendy': False, 'upscale': False, 'casual': True}}, 'business_stars': 3.5, 'review_info': [{'review_stars': 5.0, 'review_date': '2015-07-10 16:41:47', 'review_text': "So sad to see the Beachbreak cafe was gone. The Hawaiian french toast was awesome. After my shock I decided to try out the Dawn Patrol that is now in the Beachbreak location expecting to be disappointed my Johnny raincloud coming out. Hell if it wasn't fantastic. I had their hash with poach eggs a  scone and coffee. All were fantastic!!!\nI would highly recommend you come down to Dawn Patrol and try it out\nTo going to recommend to the Dawn Patrol restaurant that  they do  Hawaiian french toast :)"}, {'review_stars': 5.0, 'review_date': '2015-03-14 16:25:39', 'review_text': "Came to Santa Barbara last weekend for our anniversary trip, and Beachbreak cafe was our first stop! \n\nThe veggie benedict was AMAZING. I usually only get the traditional but figured I'd try something different and was so glad I did. The breakfast potatoes were the best I've had in a long time. Paired with a mimosa, it was the perfect brunch. \n\nThanks for hitting the spot!"}, {'review_stars': 5.0, 'review_date': '2015-02-21 04:31:52', 'review_text': "So happy yelp brought me to this lovely cafe! My husband and I were looking for a casual sit down traditional breakfast and this was everything we were looking for. Prices were what you'd expect for a typical breakfast spot. I ordered the scrambled eggs with toast, hash browns, and a pancake for my son. The food was great! My son wasn't hungry so I ate his pancake and although I am trying to eat healthy I couldn't help myself, it was one of the best pancakes I've had in a long time. There was only one girl working to seat people, take orders, and serve but you would have never known it because she did such a good job! She was so attentive and deserves some major props for taking care of a busy morning cafe all on her own! I will definitely be back next time I'm in the area."}]}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

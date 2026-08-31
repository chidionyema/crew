---
captured: 2026-08-21T18:58:55+00:00
session: 7087d3c4-cf1a-4401-aace-d8e850124aa9
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3180
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

Claim: Rory McIlroy and Lee Westwood share the lead at six under par after the first round of the DP World Tour Championship.

Passages:
[s0148] The Northern Irishman, twice a winner of the European Tour's season-finale, stumbled to a three-over-par 75 to lie joint 55th in a 60-man field. McIlroy, 27, has never finished worse than 11th in his seven appearances at Jumeirah Golf Estates in Dubai. Westwood, meanwhile, carded seven birdies and just one bogey in his 66. The 43-year-old Englishman found out earlier this week he would not be competing in the World Cup in Melbourne next week. Westwood's partner Danny Willett pulled out because of a back problem, and his place went to Chris Wood. Under tournament rules, Wood was able to select his own partner and opted for Andy Sullivan. "I'm disappointed not to be playing," said Westwood. "I can understand him picking a mate and he has picked a very good player. It is probably more to do with the rules than anything." The Tour Championship is the final event of the Race to Dubai, with four players still in with a chance of topping the European Tour Order of Merit. Henrik Stenson, holder of a course-record 25 under at the Earth Course, leads but Willett can leapfrog the Swede should he win the tournament. Willett would also top the list if he finishes second and neither Stenson nor Alex Noren win in Dubai. Noren, another Swede, needs to finish at least second and hope Stenson and Willett finish down the field. McIlroy has an outside chance which requires several permutations falling into place - including Stenson finishing no higher than 46th in the 60-man field. It took McIlroy 14 holes to register his first birdie of the day, and although he swiftly added another on the next, the four-time major winner double-bogeyed the 16th after needing two attempts - the second minus his right shoe and sock - to play from the edge of a water hazard. Westwood's former Ryder Cup partner Nicolas Colsaerts and France's Julien Quesne share second place on five under, with Sergio Garcia, Francesco Molinari and Joost Luiten a shot further back.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

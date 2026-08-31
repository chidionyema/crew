---
captured: 2026-08-21T17:50:06+00:00
session: 2ec1281b-90bd-4ba4-bd59-309f89de70b3
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2623
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

Claim: A second French tourist has died in two days while snorkelling on an Australian reef, in the second such incident in a week.

Passages:
[s0028] The 60-year-old man was scuba diving at Agincourt Reef in Far North Queensland when he was seen to be in trouble, tour operator Quicksilver said. The tourist, a certified diver, was helped to the surface but could not be revived. It comes after two French tourists died while snorkelling on the reef at Michaelmas Cay on Wednesday. They are both believed to have suffered cardiac arrests. Paramedics were alerted to the latest tragedy just after 12.30 local time (01:30 GMT) on Friday. "CPR was performed on a male patient in his sixties by a nurse on board a vessel and subsequently by a doctor," a Queensland Ambulance spokeswoman said. The Association of Marine Park Tourism Operators (AMPTO) said the alarm was raised when the diver was spotted without a regulator in his mouth 15m (49ft) below sea level on the ocean floor. "We're not sure as to what has happened at this stage," a Quicksilver spokeswoman said. The man was travelling with his wife. It was his second dive of the day from a boat called Silver Sonic. AMPTO executive director Col McKenzie said the boat was carrying oxygen and defibrillation equipment and had operated for 11 years without serious incident. "Accidents like this are a tragedy for the surviving family members, the crew and the passengers," he said. Agincourt Reef is about 100km (62 miles) north of the city of Cairns, and about 60km north of Michaelmas Cay.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

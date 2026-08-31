---
captured: 2026-08-21T18:26:16+00:00
session: 2cbfafef-7eeb-4064-9392-8ece564835fb
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1979
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

Claim: The true end of the Roman Empire is usually considered to be the fall of its eastern half, known as the Byzantine Empire, on May 29, 1453, when the Ottoman Empire, led by Sultan Mehmed II, captured the capital city, Constantinople .

Passages:
[s0073] BYZANTINE PERIOD : Eastern Roman Empire - Timeline Index The Conqueror Mehmed II (1432-1481), nicknamed the conqueror, was the sultan of the Ottoman Empire a short time in 1444 to 1446, and from 1451 to 1481. Mehmed II brought an end to the Byzantine Empire by capturing Constantinople in 1453 (during the well-known Sieg... The Fall of Constantinople was the capture of the capital of the Byzantine Empire which occurred after a siege laid by the Ottoman Empire, under the command of Sultan Mehmed II. The siege lasted from Thursday, 5 April 1453 until Tuesday, 29 May 1453... Suleiman I, The Magnificent Suleiman I, also called Süleyman I and

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

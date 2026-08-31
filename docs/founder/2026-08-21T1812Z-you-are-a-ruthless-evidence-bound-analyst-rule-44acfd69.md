---
captured: 2026-08-21T18:12:10+00:00
session: f48ce687-d68a-45cc-80a2-515f18a7f413
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1798
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

Claim: More maintained its top-song position for nine consecutive weeks.

Passages:
[s0056] [242] [243] Ariana Grande is the first artist whose first five number-one songs all debuted at the top spot. [189] She achieved this with the songs "Thank U, Next", "7 Rings", " Stuck With U ", " Rain On Me ", and " Positions " on the charts dated November 17, 2018, February 2, 2019, May 23, 2020, June 6, 2020, and November 6, 2020, respectively. In the list of August 17, 2019, Tool 's " Fear Inoculum " broke the record of longest song to enter the Hot 100, with 10 minutes and 21 seconds and peaking at number 93. Long as I Can See the Light "). [245] Groups En Vogue and Blood, Sweat & Tears tie for second, with three each.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

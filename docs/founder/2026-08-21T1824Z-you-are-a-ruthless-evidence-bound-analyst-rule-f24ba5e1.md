---
captured: 2026-08-21T18:24:14+00:00
session: b013d59e-1d80-434a-8bc6-a48d1e08d078
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1548
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

Claim: As of the 2020 Tokyo Olympic Games, China has accumulated a substantial number of gold medals.

Passages:
[s0080] Number of medals won by Chinese athletes at the Summer Olympic Games from 1984 to 2021, by type . Statista . Statista Inc.. Accessed: July 27, 2023. https://www.statista.com/statistics/1046201/china-summer-olympics-medal-number-type/ Olympian Database. "Number of Medals Won by Chinese Athletes at The Summer Olympic Games from 1984 to 2021, by Type."

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

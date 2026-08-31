---
captured: 2026-08-21T18:39:25+00:00
session: 58d3135f-e54e-465b-b2e4-9fb0fae3a3bf
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1781
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

Claim: Overall, the writer presents a calm and reassured perspective on the incident.

Passages:
[s0111] Just before writing this column, I reached into the depths of my wallet, and in between the pilot licenses, I slid out a postage stamp-size certificate issued by the Federal Aviation Administration. The certificate documents my successful completion of the DC Special Flight Rules Area, or SFRA, online course. The online course verifies that I am knowledgeable to fly a plane under visual flight rules into the most highly restricted U.S. airspace in the country. Although a "no-fly zone" over the White House has long existed, the SFRA airspace was developed to protect the Washington area further 

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

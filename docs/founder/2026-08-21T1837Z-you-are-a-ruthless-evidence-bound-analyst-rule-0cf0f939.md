---
captured: 2026-08-21T18:37:20+00:00
session: 3147c34a-e246-444b-9c6b-2c8aa8cc302e
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1831
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

Claim: The lack of written records from the period makes ironworking challenging to establish the exact timeline.

Passages:
[s0106] – November 19,1900 editorial New York Evening Journal 1901 1901, however, was the best year in Ironworker history, percentagewise at least. 1902 The first shop local of the International, Local 40 (Newark, N.J.), was chartered in 1902 and was designated as "Inside Architectural Bridge and Structural Iron Workers." With the 1902 Philadelphia success fresh in their minds, our small union, consisting of less than 30 locals, began to feel it was invincible. Similarly, the 1902 Convention agreed to help inside workers organize, but it took twenty-five years before the ability to launch an effective campaign was reached.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

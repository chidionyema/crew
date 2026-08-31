---
captured: 2026-08-21T18:55:39+00:00
session: 416bbb54-f578-4611-a949-a2579e479937
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1641
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

Claim: A pencil is 17 cm long.

Passages:
[s0141] Pencil, Types, By size, Typical: A standard, hexagonal, "#2 pencil" is cut to a hexagonal height of 1⁄4-inch (6 mm), but the outer diameter is slightly larger (about 9⁄32-inch (7 mm))

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

Your previous reply was not valid JSON (no valid JSON found in 364 chars. Start="I'm ready to analyze claims against passages using your strict evidence-based framework. However, I ", End='th verdict, confidence, rationale (≤2 sentences, one line), and citations — no prose or code fences.'). Return ONLY the corrected JSON value.

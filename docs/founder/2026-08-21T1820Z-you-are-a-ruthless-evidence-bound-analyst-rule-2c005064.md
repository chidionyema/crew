---
captured: 2026-08-21T18:20:46+00:00
session: c35ca2c2-1c71-4cf3-baa8-8d63e56b3d89
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1735
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

Claim: The laws of physics and chemistry are governed by specific sets of genes.

Passages:
[s0072] Posted By: Gert Korthof You ask 'Why it's so hard to formulate laws of biology?' and 'Why is it so much easier to talk about laws of physics?' An important factor must be that physical objects are dead, far less complex, all atoms of an isotope are identical, while biological 'objects' are literally unique individuals with a history. Considering these differences it makes no sense to demand universal, exceptionless laws in biology. I fully agree with your "I think there are general principles that we simply haven't properly explored or articulated yet".

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

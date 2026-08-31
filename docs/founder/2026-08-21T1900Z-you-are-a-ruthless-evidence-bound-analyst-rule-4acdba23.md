---
captured: 2026-08-21T19:00:41+00:00
session: 75d3dda7-1d95-4c26-a683-047459b10f18
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1889
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

Claim:  The 1821 loans were two loans that the provisional government of the **Hellenic Republic** contracted from **London** to fund the **war of independence** against the **Ottoman Empire**.

Passages:
[s0152] Several key economic and social points to understanding the historical context in which Greece attained independence in the 19th century



Constantine Tsoucalas, whilst exiled in Paris in 1969 during the Greek colonels’ dictatorship, wrote: « In almost a century and a half of modern Greek history, foreign intervention or foreign support has almost always been responsible – to a greater or lesser extent – for the birth and outcome of every crisis. Domestic social and political forces have never been able to develop or function autonomously. The Greek people have long been powerless to take the

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

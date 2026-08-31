---
captured: 2026-08-21T18:30:57+00:00
session: 6b4f45ac-3bcd-4bd8-a7e2-cba181198046
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1877
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

Claim: The situation has raised concerns of an unwinnable war and heightened tensions between the two countries, which have been at odds over Syria, Iraq, and other regional issues.

Passages:
[s0094] Relations between Iran and Saudi Arabia have always been thorny, but rarely has the state of affairs been as venomous as it is today. Tehran and Riyadh each point to the other as the main reason for much of the turmoil in the Middle East. In its most recent incarnation, the Iranian-Saudi conflict by proxy has reached Yemen in a spiral that both sides portray as climatic. For Riyadh and its regional allies, the Saudi military intervention in Yemen -- "Operation Decisive Storm" -- is the moment the Sunni Arab nation finally woke up to repel the expansion of Shia-Iranian influence. For Tehran and

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

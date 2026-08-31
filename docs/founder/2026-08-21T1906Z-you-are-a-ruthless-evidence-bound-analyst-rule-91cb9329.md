---
captured: 2026-08-21T19:06:16+00:00
session: 94884403-05a4-45e0-8a83-1eb56f815707
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1847
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

Claim: Robert Oppenheimer directed the project that developed the first atomic bomb at the same place where Richard Feynman worked on the Water Boiler.

Passages:
[s0162] Jewish culture, Science and technology. The Manhattan Project was a research and development project that produced the first atomic bombs during World War II and many Jewish scientists had a significant role in the project. The theoretical physicist Robert Oppenheimer, often considered the "father of the atomic bomb", was chosen to direct the Manhattan Project at Los Alamos National Laboratory in 1942. The physicist Leó Szilárd, that conceived the nuclear chain reaction; Edward Teller, "the father of the hydrogen bomb" and Stanislaw Ulam; Eugene Wigner contributed to theory of Atomic nucleus a

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

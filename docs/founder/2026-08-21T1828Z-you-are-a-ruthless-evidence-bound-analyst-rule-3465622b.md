---
captured: 2026-08-21T18:28:27+00:00
session: 2607424a-dcfa-46bb-8c7b-e3436cbc5eb8
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1780
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

Claim: A star's temperature is determined by the amount of mass and energy it has.

Passages:
[s0089] Learn more about Teams How to calculate the temperature of a star Ask Question Asked 7 years, 6 months ago Modified 7 years, 1 month ago Viewed 26k times 0 $\begingroup$ I need a way to calculate the effective temperature (surface temperature) of a star for a stellar model. I need something in the form Te=.... I have: Radius in m mass in kg the composition of particles (eg H 90%, He 8% etc) the combined stored thermal energy of the body in J Constants (any really but I'm using these for now): G=gravity constant=6.67408E-011 k=kbolzmann=1.3806485279E-023 s=sbolzmann=5,67036713E-008 PI=pi ~3.14...

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T18:09:35+00:00
session: 81421aba-a2d6-44fc-a601-6678345f0c76
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1858
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

Claim: The main difference between sigma bonds and pi bonds is that sigma bonds are stronger and more directional, while pi bonds are weaker and less directional.

Passages:
[s0054] [1] Pi bonds are formed by the sidewise positive (same phase) overlap of atomic orbitals along a direction perpendicular to the internuclear axis. During the formation of π bonds, the axes of the atomic orbitals are parallel to each other whereas the overlapping is perpendicular to the internuclear axis. This type of covalent bonding is illustrated below.[Image: Pi Bonds]Pi Bonds are generally weaker than sigma bonds, owing to the significantly lower degree of overlapping. Generally, double bonds consist of one sigma and one pi bond, whereas a typical triple bond is made up of two π bonds and 

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

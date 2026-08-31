---
captured: 2026-08-21T18:52:28+00:00
session: db05ccef-ee2f-459c-8ff9-566568490f59
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1928
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

Claim: One such method is the Dess-Martin Oxidation , an oxidation reaction that selectively oxidizes primary and secondary alcohols to aldehydes and ketones, respectively, using Dess-Martin periodinane (DMP) as the oxidizing agent.

Passages:
[s0135] Categories: C=O Bond Formation > Synthesis of aldehydes >Synthesis of aldehydesName ReactionsClaisen RearrangementCorey-Kim OxidationDess-Martin OxidationOppenauer OxidationSwern OxidationRecent LiteratureThe use of tert-butyl nitrite as the co-catalyst in a 2-azaadamantane-N-oxyl (AZADO)- and 9-azanoradamantane-N-oxyl (nor-AZADO)-catalyzed efficient aerobic oxidation of primary alcohols in MeCN instead of the previously reported AcOH provides the corresponding aldehydes selectively. The addition of saturated aqueous NaHCO 3 after the completion of the reaction suppresses the overoxidation of 

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

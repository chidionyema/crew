---
captured: 2026-08-21T18:45:10+00:00
session: f9c18d2d-3039-4680-b4d0-7a9ee75e86d0
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1909
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

Claim: Sharita described her sister as a "really, really good person" and hopes that her story will raise awareness about domestic violence prevention and the need for better political policies to protect victims.

Passages:
[s0122] Clarita Poole, 27: BF Charged With Murder Of Detroit Woman
A Detroit, Mich. woman was callously left to die in the street, but the authorities believe they detained the man responsible. In July 2020, a man casually made his way to a local store when he came across a gruesome scene. Clarita Poole was found lying in the road, wearing only a bra, and shot in the head. The man jumped into action, and instead of waiting for emergency responders to arrive, he rushed Clarita to a nearby fire station for help.
From there, Clarita Poole was taken to a hospital where doctors stated there was little brai

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T17:47:02+00:00
session: a572e3a4-d698-4afa-9251-f8ffe8d8da8f
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1822
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

Claim: Cut off the outer leaves of the plant with a small pair of garden shears, leaving the inner leaves to continue growing.

Passages:
[s0025] {'question': 'how to cut lettuce', 'passages': 'passage 1:2. Cut off the outer leaves of the plants with a small pair of garden shears to harvest just a few leaves. Remove the leaves at the base, leaving the inner leaves to grow on and continue producing. Trim back the entire plant when it reaches 3 to 6 inches high, or approximately every 10 days.\n\npassage 2:Inspect the lettuce plants for leaves that are ready to harvest. Most leaves are mature enough once they reach 1 to 3 inches long, but they should still be tender up to 6 inches long. Cut off the outer leaves of the plants with a small 

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

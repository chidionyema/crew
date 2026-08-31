---
captured: 2026-08-21T17:33:03+00:00
session: 3652041d-ac2d-4496-a1c5-a86fcff5b4f6
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1870
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

Claim: Firms advertise to create brand loyalty.

Passages:
[s0004] Basic purposes of advertisements: Awareness; Reminder to use; Changing belief about the brand; To assist salesmen in marketing products; Generating direct sales; Building the company’s image. Advertisements create awareness: One of the most widely accepted purpose of advertisements is to increase the recognition of a brand name or product, or to communicate information about the availability of the product to the public. This is an important objective from many point of view. First, when a new product enters the market, it does not easily gain the favor of the buyers unless they are well informed about it. That is, an awareness about the product must exist before a favorable attitude toward the brand can be developed.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

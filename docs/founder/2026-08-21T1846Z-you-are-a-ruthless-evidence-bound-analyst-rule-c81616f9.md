---
captured: 2026-08-21T18:46:09+00:00
session: 1924dfa4-b60d-4357-8caf-e850defdea19
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1760
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

Claim: Small steps on issues like drugs or environment are next.

Passages:
[s0124] WHITFIELD: All right. The U.S. flag raised above the American embassy in Havana for the first time in 54 years. The U.S. and Cuba marking their resumption of diplomatic relations. But what happens now between the two countries? Joining me from Houston, CNN presidential historian Douglas Brinkley, and in New York, Stephen Schlesinger, a fellow at the Century Foundation, whose father Arthur Schlesinger worked in and wrote extensively about the Kennedy White House. Good to see both of you.
DOUGLAS BRINKLEY, CNN PRESIDENTIAL HISTORIAN: Thank you.
STEPHEN SCHLESINGER, ADJUNCT FELLOW, CENTURY FOUNDA

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

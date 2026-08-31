---
captured: 2026-08-21T17:54:35+00:00
session: 7f8bb76f-9f28-41c0-824a-423b897b1fb6
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1850
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

Claim: Note: These steps provide general guidance, but it's important to refer to specific instructions for your pool and consult professionals if needed.

Passages:
[s0036] {'question': 'how to safely drain your pool', 'passages': "passage 1:If your's doesn't, use these tips to drain your pool: • Shut off the power to the pool's filtration system at the circuit breaker and turn off the. automatic water fill valve. • Find the sewer clean-out port to access the sanitary sewer line.\n\npassage 2:• Run a drainage hose from the sewer clean-out port to the pool, and connect it to a. submersible pump. Lower the pump into the deepest area of the pool, near the drain. As. you drain, monitor flow into the clean-out port to ensure water doesn't back up into your. home's sin

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

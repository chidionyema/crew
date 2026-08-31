---
captured: 2026-08-21T19:02:15+00:00
session: 605108fa-1600-4c94-a01e-76098a181cd0
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1842
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

Claim: The Supreme Court will hear oral arguments in a case this week that could determine whether gay couples nationwide have the right to marry.

Passages:
[s0143] Washington (CNN)Chief Justice John Roberts is back in the spotlight. Roberts -- who shocked conservatives nearly three years ago by providing a pivotal vote to uphold Obamacare -- once again faces a judicial crossroads in a historic case. The U.S. Supreme Court will hear oral arguments Tuesday in a case that could decide whether gay and lesbian couples nationwide have the constitutional right to marry. The question at the core of Obergefell v. Hodges is one of the most consequential debates of the early 21st century, and one that is already helping to shape the 2016 presidential race. Appeals 

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

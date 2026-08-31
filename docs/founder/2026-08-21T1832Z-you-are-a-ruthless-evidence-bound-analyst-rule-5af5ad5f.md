---
captured: 2026-08-21T18:32:38+00:00
session: 3620b99f-98db-437e-9bb2-b86837b7d3c0
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1824
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

Claim: For one, alcohol is a depressant, meaning it can have an effect on the central nervous system and can reduce inhibitions.

Passages:
[s0097] [1] While each individual will binge drink alcohol for different personal reasons, there are a couple overriding reasons for binge drinking. Here are a few of the most prominent reasons for binge drinking.


### The Expectations of the Effects of Alcohol on an Individual 


Human beings can sometimes be so simple. Like Pavlov’s dog, if an individual gets positive results from an action, then they will continue to perform that action. With regards to binge drinking, if someone drinks alcohol and it makes them feel good, they have fun and relieves them of social anxiety, then they will con

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

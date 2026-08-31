---
captured: 2026-08-21T19:07:56+00:00
session: cca29c09-8a47-439a-b0cd-1b80c20123f5
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1729
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

Claim: In the run-up to the general election on 8 June, we're bringing you a daily guide to the issues that matter to you, with a focus on the issues you care about.

Passages:
[s0166] The aim is to cut through the jargon and present election news in a different way. If you've got a question about the election or want to know what the parties will do for you, let us know. Follow our reporter Steffan Messenger on Facebook, where he'll be posting all our #iNeverKnew coverage and focusing on the issues you feel passionately about - your cash, your career, your future. And check out our guide to what the parties say they'll do for young people here.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

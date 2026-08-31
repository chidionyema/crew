---
captured: 2026-08-21T19:16:11+00:00
session: 5c355559-021d-454e-8ab3-e314f82c6fe3
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1825
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

Claim: The autopsy showed no signs of force being used against Gray, but he sustained a traumatic spinal injury while in custody.

Passages:
[s0184] Freddie Gray was arrested Baltimore police on the morning of April 12 without incident, according to police. Less than an hour after he was detained, officers transporting him called for a medic. He subsequently slipped into a coma, dying a week after his initial arrest. So what happened? The events surrounding Gray's encounter with police remain unclear. To shed light on what happened, police released a more detailed timeline of events on Monday, and officials speaking at a news conference elaborated on specifics of the events. "We want to clear up some of the confusions that may exist," Balt

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

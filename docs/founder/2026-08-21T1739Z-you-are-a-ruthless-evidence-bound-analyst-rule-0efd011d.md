---
captured: 2026-08-21T17:39:27+00:00
session: 2fae54f0-112f-4942-98dd-0c80ca5222f4
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1800
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

Claim: ESPN reporter Britt McHenry faced backlash for her behavior on camera after having her car towed.

Passages:
[s0015] Han and Chewie are back. An ESPN reporter went on a regrettable rant. And we all taxed our brains trying to deduce the date of Cheryl's damn birthday. Here are pop culture's most talked-about stories of the week. Producers of "Star Wars: The Force Awakens" unveiled a nearly two-minute trailer for the upcoming movie, arriving in December. When Harrison Ford shows up with Chewbacca at the end, you can almost hear the Internet's collective squeals. A logic problem from a Singapore math test somehow spread across the Web, leaving millions trying to figure out the hypothetical birthday of someone n

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

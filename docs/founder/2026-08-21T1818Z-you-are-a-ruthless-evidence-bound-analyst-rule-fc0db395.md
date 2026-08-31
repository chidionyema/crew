---
captured: 2026-08-21T18:18:42+00:00
session: fae6c4f1-7ac2-485c-9ab7-ada8ae804f28
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2032
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

Claim: Kenyans use social media to share the victims' stories, hopes and dreams. The hashtag # 147notjustanumber refers to the number of people killed at Garissa University College. Kenyan authorities have not released a list of the victims. The attack killed 142 students, three security officers and two university security personnel.

Passages:
[s0068] One hundred and forty-seven victims. Many more families affected. Even more broken hopes and dreams. As Kenyans mourned those killed last week in one of the deadliest terrorist attacks in the nation, citizens used social media to share the victims' stories, hopes and dreams. Using the hashtag #147notjustanumber -- a reference to the number of people, mostly students, killed at Garissa University College on Thursday -- Kenyans tweeted pictures of the victims in happier times. Kenyan authorities have not released a list of the victims. The posts provided heart-wrenching details on the victims, i

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

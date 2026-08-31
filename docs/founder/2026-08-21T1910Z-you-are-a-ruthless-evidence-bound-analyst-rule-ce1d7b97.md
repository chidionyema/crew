---
captured: 2026-08-21T19:10:07+00:00
session: 7cbc3464-18eb-4bc1-9880-7f95c3106ddf
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1835
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

Claim: The Nepali Pranksters' videos have become popular on social media, showcasing the team's humorous take on cultural norms and values.

Passages:
[s0170] A video shoot in Nepal for an Internet comedy series took a serious turn on Saturday as the earth began rumbling. The Nepali Pranksters were in the middle of shooting an episode for their hidden camera series when the magnitude-7.8 earthquake broke out. The team kept the camera rolling as they moved through the crowded streets, surveying destruction to homes and historic sites and capturing scenes of heroism and chaos. The Nepali Pranksters' videos show people's reactions to various "pranks" that challenge cultural norms. One video shows the pranksters walking up to strangers and taking their 

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

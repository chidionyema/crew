---
captured: 2026-08-21T18:31:53+00:00
session: c7f0eaa2-a41f-48e0-8b4d-44bbf788c476
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1793
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

Claim: Trump also tweeted attacks on Megyn Kelly, though voters dislike his comments about women.

Passages:
[s0092] JOHN KING, CNN HOST, “INSIDE POLITICS“: OK, it's an issue and it may be an issue in California, but for Jeb Bush to be stuck in the quick sand. I am convinced anchor baby could become the self- support of 2016. Once Mitt Romney went there in the campaign four years ago, it was over with Latino voters.
ASHLEY PARKER, “THE NEW YORK TIMES“: Right, I mean, it certainly was and here's the thing, Jeb Bush is a self-described policy wonk and a self-described nerd ball and so he wants to be talking about the policy and Trump has clearly gotten Jeb Bush and all the other Republicans off their game, and

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

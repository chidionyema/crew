---
captured: 2026-08-21T19:21:25+00:00
session: bbf0888f-94c0-4d5e-93a0-65c9b248ee10
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1910
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

Claim: Crystal Palace beat Manchester City 2 - 1 at Selhurst Park on Sunday. Co - chairman Steve Parish described the win as a' great moment' Parish posed for a picture with England boss Roy Hodgson and Bill Wyman.

Passages:
[s0196] Crystal Palace co-chairman Steve Parish described a 'great moment' as he basked in the glory of his club's 2-1 win over champions Manchester City. After the game, Parish posed for a picture at Selhurst Park with Palace manager Alan Pardew, England boss Roy Hodgson and Bill Wyman - one of the original members of The Rolling Stones and avid Palace fan. Parish posted the picture on Instagram, writing: 'Great moment for me , AP, the England manager, one of the original @RollingStones @bill_wyman.' . Writing in his FourFourTwo column broadcaster Geoff Shreeves, who was also in the Palace boardroom 

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

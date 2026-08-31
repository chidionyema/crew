---
captured: 2026-08-21T19:21:44+00:00
session: 63a2e6df-abbd-4d7f-a8b8-d7504ea08b56
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2836
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
[s0196] Crystal Palace co-chairman Steve Parish described a 'great moment' as he basked in the glory of his club's 2-1 win over champions Manchester City. After the game, Parish posed for a picture at Selhurst Park with Palace manager Alan Pardew, England boss Roy Hodgson and Bill Wyman - one of the original members of The Rolling Stones and avid Palace fan. Parish posted the picture on Instagram, writing: 'Great moment for me , AP, the England manager, one of the original @RollingStones @bill_wyman.' . Writing in his FourFourTwo column broadcaster Geoff Shreeves, who was also in the Palace boardroom after the game, said: '(Bill Wyman) has been an avid supporter for 68 years, having attended his first game aged 10. 'He can name virtually every player in that period, despite having spent 30 of those years in The Rolling Stones. 'Bill Wyman is not only a charming man but also somebody with a genuine passion for the game and its traditions. Wyman (back right) with fellow members of The Rolling Stones back in 1964. 'Given Bill’s rock-star status, Steve Parish overlooked his normally strict rule that you must wear a shirt and tie in the boardroom.' Hodgson, who was a youth team player for Palace in the 1960s and is from the area, will have been casting his eye over a host of English players. Pardew used seven Englishmen including matchwinner Jason Puncheon, while England No 1 Joe Hart and utility man James Milner both played for City. Jason Puncheon (right) celebrates his goal with fellow Englishman Wilfried Zaha.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

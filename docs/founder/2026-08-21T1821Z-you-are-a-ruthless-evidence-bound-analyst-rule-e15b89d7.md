---
captured: 2026-08-21T18:21:46+00:00
session: 90408d67-10a9-4751-9860-f3c21ba051c6
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1949
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

Claim: R. Kelly was seen in a Chicago nightclub last night, but protesters were outside his studio, chanting "Mute R. Kelly." Lady Gaga's omission of Terry Richardson's involvement in their collaboration highlights the problematic nature of the project.

Passages:
[s0074] KEILAR: Another big star is speaking out against singer, R. Kelly, amid explosive claims in which he's accused of being a sexual predator who abused multiple young women. Lady Gaga has apologized for working with the star and she's pulled all of her music that features R. Kelly from streaming platforms. Kelly and Gaga made a duet that was called, “Do What You Want with My Body.“ And they even performed it here on “Saturday Night Live“ together. But in a statement, Lady Gaga posted on Twitter, she explains this, in part, “What I am hearing about the allegations against R. Kelly is absolutely ho

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

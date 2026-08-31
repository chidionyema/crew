---
captured: 2026-08-21T18:22:00+00:00
session: 9cacca19-b7c2-4be6-bd63-0d3e396aac2f
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 5415
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
[s0074] KEILAR: Another big star is speaking out against singer, R. Kelly, amid explosive claims in which he's accused of being a sexual predator who abused multiple young women. Lady Gaga has apologized for working with the star and she's pulled all of her music that features R. Kelly from streaming platforms. Kelly and Gaga made a duet that was called, “Do What You Want with My Body.“ And they even performed it here on “Saturday Night Live“ together. But in a statement, Lady Gaga posted on Twitter, she explains this, in part, “What I am hearing about the allegations against R. Kelly is absolutely horrifying and indefensible. As a victim of sexual assault myself, I made both the song and video in a dark time in my life. I intend to remove this song off of iTunes and other streaming platforms and will not be working with him again.“ “Rolling Stone“ reports that at least two Dallas radio stations have banned his music from their air waves. Meanwhile, R. Kelly was spotted and videotaped last night inside a Chicago nightclub with a message for a crowd.
R. KELLY, SINGER: There's something that I must confess you all
KEILAR: While Kelly was in that club, there were several protesters rallying outside his Chicago studios chanting, “Mute R. Kelly.“ Joining me to discuss, we have Lola Ogunnaike, the anchor for “People TV.“ Lola, as you watch all of this, do you think this is the beginning of the end for R. Kelly?
LOLA OGUNNAIKE, ANCHOR, PEOPLE TV: Brianna, you and I were talking off-camera, I was here 17 years ago on CNN talking about a story that I'd written for the cover of “Vibe“ magazine. It was a 6,000-word expose. I do finally feel like justice will prevail like this time of around. It's taken a number of years, well over a decade but justice will finally prevail.
KEILAR: So this is something -- it's been on your radar for the better part of two decades. You have artists saying, I am not going to be associated with this guy. There were things that were known. What has changed?
OGUNNAIKE: I think the world at large has changed. The “Me Too“ movement has been very instrumental in helping people redefine the way they look at relationships between men and women, men and men, inappropriate relationships in general. I think people are willing to have a conversation that they weren't willing to have as early as a year ago. The “Me Too“ movement has been extremely instrumental in helping us have a very important conversation that had been ignored and swept under the rug for the better part of two decades.
OGUNNAIKE: I want to talk about Lady Gaga. Interestingly enough, Lady Gaga's apology went a long way, but she had a glaring omission in that apology. There was a video that was supposed to accompany this song and it was a video that was shot by famed fashion photographer, Terry Richardson. She had also been accused for more than a decade of being a sexual predator. He was accused of preying upon young girls. “Vogue“ banned him from shooting in his magazine. She worked with not one, but two sexual predators on this project. It was problematic then. She knew it. I find it interesting that now she's coming forward with her apology.
KEILAR: What did you think of R. Kelly on just how defiant he has been, that he shows up at this club and he is singing his heart out with some support there, obviously?
OGUNNAIKE: R. Kelly is doing what he's always done. R. Kelly in the past has always been able to get away with this behavior because he was always able to produce a hit and sing away his problems. He's at the tail end of his career. People had been muting R. Kelly for years. He's no longer at the height of his career and I do think people are now saying, I don't care what music he creates, I don't care if he's a musical genius, he has a serious problem with young women and it has to stop.
KEILAR: Lola, thank you so much. Lola Ogunnaike, we appreciate you being with us.
OGUNNAIKE: Thank you.
KEILAR: I'm Brianna Keilar, live in Washington. And tomorrow, 800,000 federal workers won't get paid. Many are protesting today.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

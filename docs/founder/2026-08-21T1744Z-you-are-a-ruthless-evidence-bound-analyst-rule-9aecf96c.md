---
captured: 2026-08-21T17:44:04+00:00
session: ddfa2f2d-b9ae-41a6-b044-c536dd3a2021
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 6689
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

Claim: It highlights the prevalence of dating violence among teens and the need for local support and awareness.

Passages:
[s0019] Speaker 0: Communication from Council member Richardson, Councilwoman Gonzalez, Councilman Price and Councilman Austin recommendation to request a resolution in support of National Teen Dating Violence Awareness and Prevention Month in February.
Speaker 1: Councilman Richardson.
Speaker 10: Thank you, Mr. Mayor. National Teen Dating, Dating Violence Awareness and Prevention Month is an effort to raise awareness about abuse in teen relationships and promote programs that prevent it during the month of February. Unfortunately, dating violence among teens is more common than most people know, according to a recent all national recent national survey. One in ten teens reported being hit or physically hurt, hurt by purpose or hurt on purpose by a boyfriend or girlfriend once in the last 12 months. In addition, one in four teenagers have been in a relationship where a partner is verbally abusive. By supporting the National Teen Dating Violence Awareness and Prevention Month, that's that's a mouthful. We as a city can bring awareness to the issue on a local level and demonstrate our commitment to fostering and supporting a healthier community for all. And we're going to hear during public comment from Candi Lewis, executive director of the Positive Results Corporation. Ms.. Lewis will share with us what her organization is doing to help address teen teen dating violence and how we can support their efforts. And with that, I'll move to move the item.
Speaker 1: It's a motion in a second, Councilwoman Gonzalez.
Speaker 2: Yes. Thank you, Councilmember Richardson, for bringing this forward. I think it's really important we make sure that we're talking about teen dating violence, both traditional and also via social media and other formats. It's really important. Our teens are certainly the future, and we want to make sure that, you know, that this council is very supportive of of what you're doing. And hopefully, if you are going through anything, you can seek support. But I look forward to hearing from the public and hearing a little bit more about about this issue. But let's stay on this. Thank you.
Speaker 1: Thank you. Any public comment on the item? Seeing nonmembers, please cast your votes. I didn't see over there.
Speaker 9: I.
Speaker 1: Let's let's let that lady make a few comments.
Speaker 4: Thank you, Mayor Garcia, Councilmember Richardson and the esteemed council members. My name is Candy Lewis, and I am the executive director of the Positive Results Corporation. We are a nonprofit, and our mission is to address teen dating violence and sexual assault in youth and communities of color. Teen dating violence is an epidemic. And the numbers that you've heard are just reported. The reported numbers are dismal, but the actual numbers are even worse right now. 90 every 90 seconds, a girl in the United States is assaulted. But that's only reported. That's a girl this over 12 years old. And so we're not really showing those correct numbers, according to our surveys that we have personally done in the last five years. We've had over 2200 people that we've surveyed. 37% were African-American. 43% were Latino, Latina, 9% white, 5% Asian, 33%. Pacific Islander, two Middle Eastern, 2%. Middle Eastern. 48% of youth and young adults have experienced sexual assault, dating and domestic violence by the sixth grade. 60.3% of youth and young adults report being hit, slapped, grabbed, pinch, spit, act, and over 60% didn't realize that they could be in a dating and domestic violence relationship. Teen dating violence looks like physical assault, verbal abuse, emotional mental, physical stalking and of course, cyber. And we thank you very much for bringing this to your to the city's attention. It is a national resolution. And because of your support, we'll be able to bring local work, a local commitment here into the city of Long Beach. There's a lot of work that's already being done, but it's not nearly enough because all of our children are impacted. Violence and abuse actually starts in the womb, and if we do not address it, we are going to have a worse problem. Right now, the numbers are 36% of every pregnant woman is physically assaulted. 36%. If we were to turn around and look at the audience and ask them, how many of you have experienced teen dating violence , domestic violence or sexual assault? I'm sure almost everyone would be because every one of us is impacted by it. If it's not in our family, it is in our neighbors, it's in our children. And so I thank you very much for bringing this to light. We do have additional information that we will be happy to share with you. I also have something for you all. I brought our brochure that talks about the work that we do. We not only address teen dating violence and sexual assault, but we also address bullying healthy relationships. Because if we do not talk about healthy relationships, we won't be talking about any relationships as well. And our organization has been partner with all state foundation to eliminate teen dating violence and sexual assault. And so I have a little something for everyone.
Speaker 1: Thank you, ma'am. Time to time is up. If you can just leave the stuff for for the clerk. That's for you. Thank you very.
Speaker 4: Much. Thank you very much.
Speaker 1: Any other public comment on this item? Okay. Seeing none members, please go ahead and cast your votes.
Speaker 0: Motion carries.
Speaker 1: Thank you. Next item, please.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

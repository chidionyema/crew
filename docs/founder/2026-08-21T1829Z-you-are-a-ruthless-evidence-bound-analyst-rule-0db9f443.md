---
captured: 2026-08-21T18:29:56+00:00
session: 54e6d7d7-2700-4ed4-8d61-dd04644af298
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 5367
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

Claim: He is known for his independent and libertarian views, and has urged his listeners to focus on economic issues rather than social ones.

Passages:
[s0084] ROBERT SIEGEL, HOST: Conservative talk radio host Neal Boortz announced this morning that he is retiring after more than 40 years on the air.
UNIDENTIFIED MAN: Flying high for decades, Boortz is reaching for the rip cord. But until he's on final approach, the oratorical aerobatics continue. It's the Boortz Happy Ending.
ROBERT SIEGEL, HOST: Boortz has been broadcasting since Richard Nixon was president. And he says he's giving up his nationally syndicated program on WSB Radio in Atlanta because it's too restrictive.
ROBERT SIEGEL, HOST: NPR's Kathy Lohr has the story.
KATHY LOHR, BYLINE: Neal Boortz, who calls himself The Talkmaster, says he got off the bus in Atlanta in 1967 and did whatever he could to make a living while he was trying to get a job on the radio. He was a jewelry buyer, an insurance salesman; he loaded trucks and wrote speeches for former Georgia Governor Lester Maddox.
NEAL BOORTZ: All this time, I'm just trying to get into radio - anything. I'll be a reporter. I'll be a cameraman for a TV station. Everybody told me, you don't have any experience. I mean, you don't know what you are doing. Get out of here.
KATHY LOHR, BYLINE: Then a local radio host committed suicide in 1969 and Boortz says he camped out at the station early the next morning to talk to the general manager.
NEAL BOORTZ: Well, OK, you can do it for a couple of weeks until we get a replacement in here for that show. So, they put me on that afternoon - 90 minutes. And two weeks later, they moved me to the morning show, and then that was it.
KATHY LOHR, BYLINE: Four decades later, Boortz says he's ready to call it quits.
NEAL BOORTZ: It's just been a total and absolute joy. Now, I'm going to miss everything associated with doing a talk radio show.
KATHY LOHR, BYLINE: About six million listeners a week tune into the Neal Boortz Show. He's a conservative yet independent voice. Boortz is a libertarian, and during the most recent Republican campaign for president has urged his listeners not to focus on social issues, including abortion and gay marriage. He is not a shock jock, but he attacks controversial issues head on. On a program last year, Boortz spoke with Herman Cain about disparaging comments being made about the former GOP presidential candidate.
NEAL BOORTZ: They called you a monkey, Herman. You're the monkey in the window.
HERMAN CAIN: Free at last, free at last. Thank God almighty, I'm free at last.
NEAL BOORTZ: OK. Now, let me ask you something.
HERMAN CAIN: Yes.
NEAL BOORTZ: Are you a runaway slave?
HERMAN CAIN: If you consider leaving the Democrat plantation, yes.
MICHAEL HARRISON: He is a force that has influence within politics and public policy, but he's also entertaining and funny.
KATHY LOHR, BYLINE: Michael Harrison is publisher of Talkers Magazine.
MICHAEL HARRISON: Although he may agree with Limbaugh and Hannity and some of the other big names in conservative talk radio, he is in no way a follower. He has always gone his own direction. He's very independent and quite unique.
KATHY LOHR, BYLINE: Perhaps not a complete surprise. Herman Cain, who has had a nightly talk show on the same radio station, will take over Boortz's morning slot on January 21st. That's inauguration day. Here's how Boortz put it.
NEAL BOORTZ: If it's Barack Obama, then I'm going to disappear into the mountains somewhere and come out after he has completely destroyed this country. If it is Mitt Romney, then we're all going to leave the air - well, we're going to start drinking, we'll start drinking as the show begins. And...
KATHY LOHR, BYLINE: He's calling his announcement the Boortz happy ending. Today, comedian Jeff Foxworthy was among those who called in to lament the end of an era.
JEFF FOXWORTHY: Man, are we going to miss you. It's just not going to be the same on the radio.
NEAL BOORTZ: Well, you're so kind and so kind to call.
KATHY LOHR, BYLINE: Boortz says after he retires, he plans to spend eight months on what he calls the Boortz bus traveling with his wife.
KATHY LOHR, BYLINE: Kathy Lohr, NPR News, Atlanta.
ROBERT SIEGEL, HOST: This is ALL THINGS CONSIDERED from NPR News.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

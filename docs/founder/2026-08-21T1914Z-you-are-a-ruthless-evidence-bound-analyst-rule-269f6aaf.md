---
captured: 2026-08-21T19:14:46+00:00
session: 5c2e087f-bd33-47e6-aaa0-c50e04db6713
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 5800
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

Claim: Celebrities, politicians, and even animals have taken selfies that have gone viral.

Passages:
[s0180] GORANI: A major shocker at the World Cup right now. Just minutes ago, Argentina lost to Croatia three nail. That would make it extremely difficult for Argentina to advance out of their group. On the pitch today, France beat Peru, one nail. Yay. Which moves them into the knockout stage of the World Cup. Russia and Uruguay, so far, are the only other teams to advance. Russia's success certainly is a surprise. They came into the cup as the lowest rated team in the tournament. They have something called a home advantage though, I think Fred Pleitgen has been following the Russian national team and he's in Moscow. Fred.
FREDERIK PLEITGEN, CNN SENIOR INTERNATIONAL CORRESPONDENT: Hala, we visited their training camp earlier today and what we saw there was a very confident team, obviously bolstered by those two win that they got and a team that believes that they could do great things at the World Cup. And so now does this nation. Here's what we saw.
PLEITGEN: It's not often that you see Russians this emotional. But the country's been in a football frenzy ever since the World Cup started. Thanks to Russia's Cinderella squad, a team most experts thought would fail miserably, but has outscored its opponents Eight to one so far. Defender Andrei Semyonov told me the team always believed in itself. Nobody believed in us, he says, now everyone does and they're starting to put medals on us. But we don't look at it. We studied our opponents really well and predicted everything. But few observers could have predicted their success. Russia is the lowest ranked team at the World Cup. Wouldn't have even qualified if they weren't the host nation. And many feared the mood at the World Cup would sour and the home team performed poorly. Now, the squad, led by striker Artem Dzyuba is on a roll. Team Russia has already proved all of its critics wrong, well, in all of its matches and already qualifying for the next round. And now both this nation and this team believe they can do great things at the FIFA 2018 World Cup. And with a successful squad, Russians are embracing their nation's role as hosts of the tournament. Striker Fyodor Kudryashov telling me, home field advantage has also helped elevate the team's performance. The fans are the 12th player on the field for us, he said. We feel their overwhelming support and our team goes forward. If there is a knock on the Russians, it's that they haven't played any of the really strong teams so far. But for now, Russia is enjoying the winning streak, hoping their World Cup fairy tale doesn't end any time soon.
PLEITGEN: And, Hala, of course the next game they have will be against the stronger team, it's against Uruguay. And after that, of course, we get to the knockout stages and it's really going to be there that the Russians are going to show whether they are for real or not, Hala.
GORANI: Yes, we will be watching. Thanks, Fred. For Shakespeare, it was the sonnet, for Rembrandt and Picasso, a masterpiece painted in oils. But in this day and age, there seems to be only one way to truly honor the special moments in our life.
UNIDENTIFIED FEMALE: Let me take a selfie. The Chainsmokers there capturing the very essence of social media's magnum opus, the selfie. A photographic custom being honored today on National Selfie Day. Selfie is a relatively new term. But did you know the first selfie was taken in 1839 by photographer Robert Cornelius in Philadelphia? Truly a visionary, so who we were to resist the tide of history? This is our HALA GORANI TONIGHT team in London. That's a selfie. One of these team has a super long arm. We reached out to our colleagues at CNN center in the U.S., but unfortunately, they were all having bad hair days. So instead, and keeping with another great internet tradition, here's a picture of a selfie taking cat, and his name is Manny. Manny takes these photos with a GoPro cam, and he's seen here with a close friend. New Zealand's prime minister has given birth, becoming only the second female world leader to do so while in office. Jacinda Ardern and her partner Clarke Gayford posted this snap with their newborn daughter earlier. Is it a selfie? Looks like it could be, actually. She will now take six weeks maternity leave and has handed over her responsibilities to the deputy prime minister, who is now serving as acting prime minister. She follows in the footsteps of the former Pakistani Prime Minister, Benazir Bhutto, who had a child while in office in 1990. Thanks for watching tonight, everyone. I'm Hala Gorani. Stay with CNN. “QUEST MEANS BUSINESS“ is up next. I'll see you tomorrow.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

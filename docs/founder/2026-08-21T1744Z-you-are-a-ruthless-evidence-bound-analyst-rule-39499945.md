---
captured: 2026-08-21T17:44:48+00:00
session: 004c63eb-0de7-4425-bf0c-e51db405033a
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3325
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

Claim: Cooper Smith, a 17-year-old from Texas, won $1 million at the 2023 Fortnite Champion Series Global Championship in Denmark, defeating top-tier players worldwide.

Passages:
[s0020] Epic Victory: How Cooper Smith a Texas Teenager Clinched $1M and Won Over 60k New Fans
ROUND ROCK, Texas — Local teen, Cooper Smith, alongside his gaming partner, emerged triumphant at the 2023 Fortnite Champion Series Global Championship held in Denmark, bagging a whopping $1 million grand prize. The three-day esports extravaganza, which ran from Oct. 13-15, showcased some of the world's best "Fortnite" players, battling it out in intense duos matchups.
The competition wasn't for the casual gamer; it's a prestigious event that requires players to earn their spot. Cooper explained, "Only those who placed in the top three in one of the three major tournaments this year could qualify for this Denmark championship." A feat Cooper had already achieved earlier in the year by securing second place in a major, earning him a hefty $95,000.
This global showdown attracted top-tier players from regions worldwide, including Europe, Middle East, Asia, and Oceana. And in this grand coliseum of virtual warfare, Cooper's skills not only earned him the monumental prize money but also a massive surge in online followers. Post-victory, his streaming platforms witnessed a spike of around 60,000 followers.
With his eyes set on a full-time esports career, Cooper decided to pivot from traditional public school to online classes, ensuring he dedicates his full attention to his newfound professional gaming and streaming ventures. "Balancing rigorous gaming training with regular school and sports simply wasn't feasible," Cooper elaborated.
Support has been a crucial element in Cooper's journey, with his parents playing a pivotal role. Reflecting on his father's influence, Cooper mentioned, "My dad introduced me to the gaming world. He even accompanied me to Denmark for the championship. Witnessing the win was a surreal experience for both of us."
For this Round Rock champion, the journey has only just begun. Cooper's ambitions are crystal clear: continue his reign in the gaming world, rake in victories, and do what he loves most for as long as he can.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

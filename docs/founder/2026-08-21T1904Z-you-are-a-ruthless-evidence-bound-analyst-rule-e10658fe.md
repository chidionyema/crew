---
captured: 2026-08-21T19:04:46+00:00
session: 9b2c4836-81a7-48d6-860e-5692b777b537
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 6246
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

Claim: In 2014, a 15-year-old boy survived a 5-1/2-hour flight from California to Hawaii in the wheel well of a Boeing 767.

Passages:
[s0159] MICHAELA PEREIRA, CNN ANCHOR: Welcome back to NEW DAY. Medical professionals remain shocked that a 15-year-old boy can survive a 5- 1/2 hour flight from California all the way to Hawaii in the wheel well of a Boeing 767. Although it is very rare, the teen would not be the first to live through this kind of journey. Back in 2000, a man survived a 7-1/2-hour flight from Tahiti to Los Angeles in the wheel well of a plane. Joining me now is the very physician who successfully treated that stowaway, Dr. Armand Dorian. Dr. Dorian, what a pleasure to have you here. Why don't you describe to us the condition of the stowaway survivor that presented to you in the E.R. back in 2000?
DR. ARMAND DORIAN, USC VERDUGO HILLS HOSPITAL: Back in 2000, the patient that rolled in by paramedics was not in the same state as this young boy this year. He was literally frozen, almost cartoonishly frozen. His arms were kind of jutted out. He was moaning. He was unconscious. He was not alert. We had to do multiple critical measures to keep him alive. His core body temperature was below 80 degrees. We had to intubate him, put chest tubes in. It was really touch and go.
PEREIRA: It was really a miracle that he survived in your estimation?
DORIAN: There's no question. I thought in my lifetime I would never even hear of another case like this, let alone hear of a case where the gentleman who was a stowaway walks away from the incident.
PEREIRA: Let's get to that. You already compared the difference between that. Quickly, before we move on, do you know if that man had lasting side effects? Oftentimes you don't know the results many years later. Do you know?
DORIAN: Actually he had no gross motor dysfunction, so something may actually be -- later on that may come up like depression, chronic headaches, but nothing obvious at the time when he was discharged from the hospital. Know that it was a month after he was admitted.
PEREIRA: Interesting. OK, to this 15-year-old, he essentially after an hour after the plane landed sort of came out of the wheel well mostly able to move on his own power. This is phenomenal. Talk to me about what you think happened that this young man would present in a very different condition than the man in 2000.
DORIAN: I mean, the planets all were aligned. This was a perfect storm of disaster that actually probably saved his life because when the airplane ascends, you lose oxygen, the air gets thin as we would say in layman's terms. You would pass out in about a minute after being up there. Also, the temperature drops. With the temperature dropping it actually starts slowing down your body's need for oxygen. It puts you in a frozen or some people termed it as a suspended state. Kind of like a cryogenic freezing that we've seen, you know, sci-fi or hear about in the future happening and because your demand decreases, you don't need as much oxygen. You can be suspended in time until your oxygen is replenished.
PEREIRA: We know your patient passed out and doesn't remember a thing of his flight. We don't what this young boy remembers. We know that he did tell police that he was unconscious for a time. What do you think it feels like for all of this to go on or do we know that because most people don't have a memory of it?
DORIAN: I'm pretty sure he's not going to have any memory or recollection of it. He's going to probably remember the adrenaline rush of trying to hide inside that wheel well, the beginning of that takeoff, and then about a minute max, 5 minutes after that takeoff he's unconscious. The next thing he remembers, he's waking up and he's landed already. Maybe he thinks he didn't take off. He passed out and is in a completely different place.
PEREIRA: How unusual is it, Dr. Dorian, for a person to survive subzero temperatures, lack of oxygen for 5-1/2 hours and also that he didn't fall out of the landing gear.
DORIAN: I kind of describe it as winning the lottery five times in a row. The fashion in which he did it, I would think it was a poor TV show production if they had a kid walk out of a wheel well like this. It's really mind-boggling.
PEREIRA: The story he was telling us, he was trying to get home to Somalia to see his mother. You can imagine the heartbreak. You can imagine the concern the family has. Hopefully he'll get medical attention to deal with any issues that come up after this. Dr. Dorian, what a pleasure to talk to you. Some miracles stories we are talking about. Thanks for joining us from Los Angeles -- Chris.
CUOMO: That just does not make sense. I don't know how that kid managed to not have any effects of such extreme conditions. Let's take a little break on NEW DAY to consider it. When we come back, an object of interest on the shoreline of Western Australia. Could it be debris from Flight 370?
BOLDUAN: The death toll continues to rise in the South Korean ferry disaster. Why did so many victims fail to get out alive? We'll take you inside a simulator to get a better understanding of the life-or- death emergency at sea.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

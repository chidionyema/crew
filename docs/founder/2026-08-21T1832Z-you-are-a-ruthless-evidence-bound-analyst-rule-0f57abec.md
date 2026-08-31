---
captured: 2026-08-21T18:32:52+00:00
session: 6c4a1c56-80ae-4b59-95f0-ba0f559f5a41
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3277
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

Claim: For one, alcohol is a depressant, meaning it can have an effect on the central nervous system and can reduce inhibitions.

Passages:
[s0097] [1] While each individual will binge drink alcohol for different personal reasons, there are a couple overriding reasons for binge drinking. Here are a few of the most prominent reasons for binge drinking.


### The Expectations of the Effects of Alcohol on an Individual 


Human beings can sometimes be so simple. Like Pavlov’s dog, if an individual gets positive results from an action, then they will continue to perform that action. With regards to binge drinking, if someone drinks alcohol and it makes them feel good, they have fun and relieves them of social anxiety, then they will continue to drink alcohol. That means that they will keep on grabbing drink after drink, “chasing the dragon” and trying to get the good feelings to continue to be present.

[2] At social gatherings, the effect of peer pressure is very real. If everyone is drinking alcohol, it is only natural to want to grab a drink as well. The euphoria that comes with being in a group of friends and peers can lead to a feeling of exuberance that is amplified by drinking alcohol. There also could be drinking games at the party as well. These factors create a breeding ground for binge drinking.

[3] * Peer pressure/acceptance issues: This is mostly evident in the case of high school and college crowds. ‘Fitting in’ has always been a bugbear since time immemorial, and if binge drinking can make you popular, then so be it- at least that’s what some kids think. Unfortunately, many students feel ‘socially obligated’ to binge drink if they are part of a clique or an environment where this habit is encouraged.

[4] * They want to socialize and feel more self-confident: This is particularly true of shy folks or introverts who find it a tad difficult to socialize unless they feel ‘free’ by- you guessed it- drinking. Alcohol does have this innate tendency to make you feel more uninhibited, and innumerable young adults have admitted to indulging in excessive drinking just to be ‘one’ among the crowd, feel sexy, and to get out there and mix around with others.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

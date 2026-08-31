---
captured: 2026-08-21T17:54:22+00:00
session: 712bdfc4-ed64-42fc-82ba-a37e1268594c
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3792
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

Claim: Noise can also disrupt our circadian rhythm, which is the internal clock that controls our sleep-wake cycle.

Passages:
[s0035] [1] How does noise disturb sleep? There are three primary effects:
1. Difficulty getting to sleep: Increasing the time it takes to fall asleep.
2. Trouble staying asleep: Waking you up during the night.
3. Altering the stages of sleep: You don't sleep as deeply, and you get proportionately less REM sleep.
Different people have different tolerances to noise when they're trying to sleep, but on average a sound exposure level above 55 dBA causes a sleeping person to awaken. However, even if a noise doesn't fully wake you up, it can cause other disturbances as you sleep. You have more restless body movements, your heart rate goes up, your blood pressure increases, your breathing changes. These physiological effects are seen with sound exposure levels as low as 40 dBA.

[2] Because loud or unusual noises often signaled danger in the lives of our ancestors, we have inherited from them an automatic "fight or flight" response to noise, which releases energizing stress hormones to prepare us to take emergency action. This response occurs in a primitive part of the brain (the amygdala), and triggers stress hormone secretions even when we're asleep. If this happens repeatedly, over time our stress hormone levels can become chronically elevated, a condition which is associated with a wide range of negative health effects.

[3] Carry disposable, foam earplugs: Pop them in, and you’ll at least muffle the noise around you so you can fall asleep1. Or, download a white noise app on your smartphone. When you want to snooze, put on your ear buds, turn on the app, and let the steady frequency of the white noise drown out the surrounding sounds.2 Alternatively, playing relaxing, classical music at a low volume can help.

[4] In general, it is easiest to sleep in a quiet place. Whether it is a vestige of surviving in the wilderness or for some other reason, we tend to respond to external stimuli while asleep. In other words, if we hear a noise, we will wake up. This is advantageous if a lion is trying to eat us while we sleep in a cave, but when the neighbor is blasting the radio too loud, it is less desirable.
When we hear a noise, we may not become fully conscious, but we certainly will come out of the deeper stages of sleep. If we are trying to sleep in a noisy environment, our ability to enjoy restful deep sleep will be compromised. It is, therefore, best to try to keep things as quiet as possible.
Some may benefit from using a white noise machine (or a fan), putting in earplugs, or keeping a radio or television on low volume to drown out street noises.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

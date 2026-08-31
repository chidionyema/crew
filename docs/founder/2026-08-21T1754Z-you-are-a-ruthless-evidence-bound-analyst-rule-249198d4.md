---
captured: 2026-08-21T17:54:11+00:00
session: 59e4976e-13e0-45dc-b041-58346dac562f
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1811
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
Different people have different tolerances to noise when they're trying to sleep, but on average a sound exposure level above 55 dBA causes a sleeping person to awaken. However, even if a noise doesn't fully wake you up, it can cause other disturbances as you sleep. You have more restless bod

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

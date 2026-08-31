---
captured: 2026-08-21T18:03:41+00:00
session: 1dc64bd8-37ed-4de5-8dad-6586797ee77c
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3266
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

Claim: The US military has made significant progress in developing self-steering bullets called "EXACTO" that can hit moving and evading targets with extreme accuracy.

Passages:
[s0046] You know the phrase "dodging a bullet"? Forget about it. Probably not going to happen anymore. The U.S. military said this week it has made great progress in its effort to develop a self-steering bullet. In February, the "smart bullets" -- .50-caliber projectiles equipped with optical sensors -- passed their most successful round of live-fire tests to date, according to the Defense Advanced Research Projects Agency, or DARPA. In the tests, an experienced marksman "repeatedly hit moving and evading targets," a DARPA statement said. "Additionally," the statement said, "a novice shooter using the system for the first time hit a moving target." In other words, now you don't even have to be a good shot to hit the mark. The system has been developed by DARPA's Extreme Accuracy Tasked Ordnance program, known as EXACTO. "True to DARPA's mission, EXACTO has demonstrated what was once thought impossible: the continuous guidance of a small-caliber bullet to target," said Jerome Dunn, DARPA program manager. "This live-fire demonstration from a standard rifle showed that EXACTO is able to hit moving and evading targets with extreme accuracy at sniper ranges unachievable with traditional rounds. Fitting EXACTO's guidance capabilities into a small .50-caliber size is a major breakthrough and opens the door to what could be possible in future guided projectiles across all calibers," Dunn said. Videos supplied by DARPA show the bullets making sharp turns in midair as they pursue their targets. It all conjures up images of a cartoon character frantically fleeing a bullet that follows him wherever he goes. Only, these bullets are traveling at hundreds of miles per hour. And even the Road Runner can't run that fast. DARPA says the smart bullets will also help shooters who are trying, for example, to hit targets in high winds. The goals of the EXACTO program are giving shooters accuracy at greater distances, engaging targets sooner and enhancing the safety of American  troops, DARPA said.


Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

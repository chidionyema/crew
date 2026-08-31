---
captured: 2026-08-21T18:27:57+00:00
session: 8fa45bc4-2542-4e8e-af00-16909f815494
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3199
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

Claim: Finally, seismologists may analyze the chemical composition of the ground to determine if human activities have altered the physical and chemical properties of the Earth's crust.

Passages:
[s0088] [1] There are a number of ways to do this. One is to measure the depth at which the earthquake occurred. Even with modern drilling technology, it is only possible to place a nuclear device a few kilometres below the ground; if an earthquake occurs at a depth of more than 10km, we can be certain it is not a nuclear explosion.
Studies of the numerous nuclear tests that took place during the Cold War show that explosions generate larger P waves than S waves when compared with earthquakes. Explosions also generate proportionally smaller Surface waves than P waves. Seismologists can therefore compare the size of the different types of wave to try to determine whether the waves came from an explosion or a natural earthquake.

[2] For cases like North Korea, which has carried out a sequence of nuclear tests since 2006, we can directly compare the shape of the waves recorded from each test. As the tests were all conducted at sites within a few kilometres of each other, the waves have a similar shape, differing only in magnitude.

[3] Seismological data can tell us whether there was an explosion, but not whether that explosion was caused by a nuclear warhead or conventional explosives. For final confirmation that an explosion was nuclear, we have to rely on radionuclide monitoring, or experiments at the test site itself.
Similarly, we cannot explicitly differentiate between a nuclear fission bomb and a thermonuclear hydrogen bomb, nor can we tell if a bomb is small enough to be mounted on a missile, as the North Korean government claims.
What we can get from the data is an idea of the size of the blast. This isn't simple, as the magnitude of the seismic waves and how they relate to the explosive power of the bomb depends a lot on where exactly the test took place, and how deep underground. But in the case of this latest test, we can directly compare the magnitude to previous North Korean tests.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

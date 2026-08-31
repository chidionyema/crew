---
captured: 2026-08-21T19:08:41+00:00
session: f6f28a47-cd20-4712-b883-1fc40a6b42f6
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3012
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

Claim: Samantha Chandrasekaran is the latest member of the International Space Station (ISS).

Passages:
[s0167] The European Space Agency astronaut arrived at the orbiting space lab on Monday, along with two crewmates from Russia and America. But what exactly will she be doing during her time in space? The ISS gives the chance to do scientific experiments that cannot be done on Earth, as the station offers an environment of microgravity. Here we run through a few examples of the experiments on Samantha's 'to do' list... Samantha will operate a gadget called an electromagnetic levitator, which can heat metals to 2,000Â°C and then cool them very quickly. This will be a chance to see what happens to different metals when they go from liquid to solid, without the effect of the Earth's gravity. It's hoped the results will reveal more about the physics of the metals and how they work. Samantha will be testing new machine technology and how well they work in space, such as this astronaut joystick. Using a joystick in space may feel very different in space compared to on Earth. So these experiments will see how being in space might affect how well an astronaut can control a space robot or space machinery. Another thing is that equipment may need to be attached to the astronaut so it doesn't float away. The testing will also see what impact this has. Samantha will be doing lots of experiments to see how being in space affects her body. For example, she will experience 16 sunrises and sunsets every day on the International Space Station and be tested to see how this affects her body clock. Another important subject is food and energy. Experiments to see how much food an astronaut would need for a long mission will be carried out. Samantha will record what she eats and her energy levels over a period of time. Other things that will be looked at include how space affects skin and why many astronauts get headaches.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

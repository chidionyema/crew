---
captured: 2026-08-21T17:32:39+00:00
session: 2050fab2-7671-41fd-a299-b57e6c5625a7
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2791
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

Claim: The cause of the blast is under investigation, but occurred at the spot where a county worker was operating a front loader.

Passages:
[s0003] A natural gas line explosion at a law enforcement shooting range in Fresno, California, injured 11 people, including some inmates who were on a work detail there. Others being treated include a county road worker and two sheriff's deputies, Fresno County Sheriff Margaret Mims said. The exact cause of Friday's blast is under investigation, Mims said, but it happened at the spot where a county worker was operating a front loader. The explosion sparked a fire that roared like a jet engine, Mims said. The operator of the front loader was injured but able to walk to an ambulance, the sheriff said. The most serious injuries were suffered by a group of inmates who were assigned to maintenance and cleaning work at the sheriff's firing range. There were 10 inmates near the blast site who were also injured, officials said. Three other inmates at the site were not hurt. Earlier, the sheriff's office included them in the injury count. After the blast, Mims said, two sheriff's deputies who were at the firing range ran toward the fire to move the injured. CNN affiliate KFSN posted a video of the scene that shows a tall ball of fire rising from near a highway. One inmate was airlifted to the hospital, the sheriff said. That inmate and the county worker were undergoing emergency surgery, she said. The others suffered mostly burns. The pair of deputies who provided aid also went for treatment for ringing ears and sunburn-like conditions, she said. Firefighters put out the blaze, revealing a crater at the blast site and a blackened front loader, Mims said.


Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

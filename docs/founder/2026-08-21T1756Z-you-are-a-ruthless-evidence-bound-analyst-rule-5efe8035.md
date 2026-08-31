---
captured: 2026-08-21T17:56:39+00:00
session: 37d1879c-29bd-44f7-9cd6-f9b9a356602d
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2990
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

Claim: Unscrew the two bolts that secure the torque converter access cover to the converter housing using a socket.

Passages:
[s0039] {'question': 'how to remove automatic gearbox out of ford ranger', 'passages': 'passage 1:    You can start by removing a few of the bolts holding the transmission fluid pan to the underside of the transmission, which will likely allow some of the fluid to drain out. While carefully holding the pan in place, remove the rest of the bolts, and remove the pan.   You can start by removing a few of the bolts holding the transmission fluid pan to the underside of the transmission, which will likely allow some of the fluid to drain out. While carefully holding the pan in place, remove the rest of the bolts, and remove the pan.\n\npassage 2:Unscrew the transmission oil pan bolts from the transmission using a wrench. Wait until all the fluid has drained from the pan, then remove the pan from the transmission. Unscrew the two bolts that secure the torque converter access cover to the converter housing using a socket.nscrew the bolts that secure the starter motor to the engine block, using a socket. Tie the starter motor to the vehicle’s frame using a plastic wire tie, so that the motor does not hang from the wiring harness. Unscrew the transmission cooler lines from the passenger side of the transmission, using a line wrench.\n\npassage 3:Making the world better, one answer at a time. Remove the Ford Ranger automatic transmission drain plug. The drain plug is in the bottom of the transmission. Allow the oil to drain out and replace the plug.Fill the transmission with new transmission fluid.   You can start by removing a few of the bolts holding the transmission fluid pan to the underside of the transmission, which will likely allow some of the fluid to drain out. While carefully holding the pan in place, remove the rest of the bolts, and remove the pan.\n\n'}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T17:50:43+00:00
session: bb02cd22-ba50-4702-9116-205ef14f2392
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3078
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

Claim: In addition to producing skeletal movement, muscles also play a crucial role in maintaining posture and body position, supporting soft tissues, guarding entrances and exits to the digestive and urinary tracts, and maintaining body temperature.

Passages:
[s0029] {'question': 'briefly explain how muscles produce movement', 'passages': 'passage 1:1 Skeletal muscles — These muscles contract to pull on tendons and move the bones of the skeleton. 2  In addition to producing skeletal movement, muscles also maintain posture and body position, support soft tissues, guard entrances and exits to the digestive and urinary tracts, and maintain body temperature. Skeletal muscles — These muscles contract to pull on tendons and move the bones of the skeleton. 2  In addition to producing skeletal movement, muscles also maintain posture and body position, support soft tissues, guard entrances and exits to the digestive and urinary tracts, and maintain body temperature.\n\npassage 2:Three types of muscles. The muscular system can be broken down into three types of muscles: skeletal, smooth and cardiac, according to the NIH. Skeletal muscles are the only voluntary muscle tissue in the human body and control every action that a person consciously performs.hree types of muscles. The muscular system can be broken down into three types of muscles: skeletal, smooth and cardiac, according to the NIH. Skeletal muscles are the only voluntary muscle tissue in the human body and control every action that a person consciously performs.\n\npassage 3:Muscular system is the system of Human Body that provides motor power for all movements of body parts. Muscular system is composed of special tissue called muscular tissue. Muscles have the ability to contract actvely to provide the force for movements of body parts.uscular system has the following important functions in human body; 1  MOVEMENTS OF BODY PARTS: Skeletal muscles are responsible for all voluntary movements of human body parts.\n\n'}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

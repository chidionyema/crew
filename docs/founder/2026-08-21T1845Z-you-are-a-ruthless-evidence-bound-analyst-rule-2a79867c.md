---
captured: 2026-08-21T18:45:58+00:00
session: 193fef94-bb7d-494a-acf6-36e24e096372
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3625
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

Claim: Us president barack obama has nominated a former deputy attorney general to be the next director of the fbi.

Passages:
[s0123] If confirmed by the Senate, James Comey will replace outgoing director Robert Mueller III, serving for 10 years.
At the White House, Mr Obama praised Mr Comey as a model of "fierce independence and deep integrity".
Mr Comey is known for successfully opposing a warrantless wiretapping programme backed by other Bush aides.
Mr Mueller took up his post shortly before the 9/11 attacks and is retiring as director on 4 September.
In remarks on Friday, Mr Obama said the outgoing director had displayed "a steady hand and strong leadership" during his time at the head of the FBI.
The US president said Mr Comey had "law enforcement in his blood".
"As a young prosecutor in the US attorney's office in Manhattan he helped bring down the Gambino crime family; as a federal prosecutor in Virginia he led an aggressive effort to combat gun violence that reduced homicide rates and saved lives," Mr Obama said.
He also joked that Mr Comey - who is 6ft, 8in tall (2.03m) -  was "a man who stands up very tall for justice and the rule of law".
The nominee said he could not describe his excitement to work again with the FBI.
"They are men and women who have devoted their lives to serving and protecting others and I simply can't wait to be their colleague," he said.
One of the most dramatic episodes of Mr Comey's tenure as deputy attorney general in the Bush administration came in 2004, when then-Attorney General John Ashcroft was ill in hospital.
Mr Bush's White House counsel Alberto Gonzales and Chief of Staff Andrew Card pressed him in his hospital bed to re-authorise a controversial programme allowing federal agents to eavesdrop on phone conversations without a warrant.
Mr Comey, who was acting as attorney general in Mr Ashcroft's stead, rushed to the hospital and intervened.
Changes were subsequently made to the programme and Mr Comey drew wide praise.
Mr Obama alluded to the incident on Friday, saying Mr Comey "was prepared to give up a job he loved rather than be part of something he felt was fundamentally wrong".
After leaving the Bush administration, Mr Comey was general counsel for Bridgewater Associates, a hedge fund in the US state of Connecticut. He now lectures at Columbia University law school in New York.
Before he became deputy attorney general, Mr Comey had a long tenure at the justice department, serving in many posts including as US attorney for the Southern District of New York.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

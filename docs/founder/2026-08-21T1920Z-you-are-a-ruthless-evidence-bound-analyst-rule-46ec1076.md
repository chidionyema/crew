---
captured: 2026-08-21T19:20:50+00:00
session: d14b38b2-f4ff-4c22-ab29-f38f03098625
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2487
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

Claim: The signs and symptoms of alcoholic hepatitis include changes in appetite, dry mouth, weight loss, nausea and vomiting, pain or swelling in the abdomen, yellowing of the skin or eyes (jaundice), fever, changes in mental state including confusion.

Passages:
[s0194] {'question': 'signs and symptoms of alcoholic hepatitis', 'passages': 'passage 1:If you have a mild case of the disease, you may not experience any symptoms. However as more damage occurs, you may begin to experience: 1  changes in appetite. 2  dry mouth. 3  weight loss. 4  nausea and vomiting. 5  pain or swelling in the abdomen. 6  yellowing of the skin or eyes (jaundice). 7  fever. 8  changes in your mental state, including confusion.\n\npassage 2:Signs and symptoms of severe alcoholic hepatitis include: 1  Retaining large amounts of fluid in your abdominal cavity (ascites). 2  Confusion and behavior changes due to brain damage from buildup of toxins (encephalopathy). 3  Kidney and liver failure.\n\npassage 3:You may not have symptoms in the early stages. Symptoms tend to be worse after a period of heavy drinking. Digestive symptoms include: 1  Pain and swelling in the abdomen. 2  Decreased appetite and weight loss. 3  Nausea and vomiting. 4  Fatigue. 5  Dry mouth and increased thirst. 6  Bleeding from enlarged veins in the walls of the lower part of the esophagus (tube that connects your throat to your stomach).\n\n'}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

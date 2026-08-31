---
captured: 2026-08-21T17:55:27+00:00
session: 1489328c-3b36-4da5-be75-562089a9201c
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2802
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

Claim: It is important to monitor the reheating process to ensure that the food reaches a safe temperature.

Passages:
[s0037] {'question': 'how do you reheat food for hot holding', 'passages': 'passage 1:Food safety facts. 1  Cooking and pooling of eggs. Contaminated eggs can carry Salmonella enteritidis and can cause the elderly, small children and those with immune-compromised systems to get sick when consuming raw or undercooked eggs. 2  Food safety in your home kitchen. Food safety in your home kitchen is just as important as food safety in restaurant kitchens. In fact, as much as 60% of foodborne illness may be from home kitchens. Labeling raw and undercooked foods.\n\npassage 2:Reheat foods using proper procedures. • Reheat the following foods to 165 °F for 15 seconds within 2 hours: ◊ Any food that has been cooked and cooled and will be reheated for hot holding, ◊ Leftovers reheated for hot holding, ◊ Products made from leftovers, such as soup or casseroles, and. ◊ Precooked, processed foods that have been previously cooled. • Reheat foods rapidly using the correct equipment. When reheating food, the total time the temperature. of the food is between 41 °F and 165 °F cannot exceed 2 hours. • Serve reheated food immediately or place in appropriate hot holding unit. Monitor reheating process. • Check food temperatures with a clean, sanitized, and calibrated thermometer.\n\npassage 3:Use a food thermometer to check the temperature after cooking. All food should be reheated to 165 degrees Fahrenheit. Step 3 Put roasted food in the oven Put roasts, casseroles, and pasta dishes with sauce in an oven-safe pan and cover loosely with aluminum foil. Bake at 325 degrees and heat to 165 degrees.\n\n'}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

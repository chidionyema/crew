---
captured: 2026-08-21T18:06:44+00:00
session: 84e500de-ff21-422c-80f9-95cb733faeae
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2705
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

Claim:   To sum up, the Canarian thermophilic forest is an interstitial region located at an altitude of 200 to 600 meters on the island of Tenerife that accommodates certain vegetation and likely different forms of animal life, adapting to moderate variations of rainfall and temperature.

Passages:
[s0051] Flora and fauna - Tenerife Canarian pine tree, which is particularly abundant in the south of the Island. Tenerife's vegetation can be divided into six ecosystems according to altitude and orientation, as follows: Canary island spurges and tabaibas: This type of greenery ranges from the coast up to altitudes of 700 m (2,300 ft) above sea level. These plants are xerophilic shrubs that have adapted to drought, strong winds and constant sunlight. There are various endemic species in this ecosystem. Thermophilic forests: This ecosystem is a transitional area ranging from 200 to 600 m (655 to 1970 ft) where the rainfall and temperatures are moderate,

Tenerife Flora and Fauna - species endemic to the island varied vegetation on Tenerife, with up to 140 species of plant being endemic to this island only. All these different factors contribute to the presence of many varied habitats in which widely differing types of plants and animals have thrived. There are six major zones of vegetation on the island, according to altitude and directional aspect. Lower Xerophytic Zone Sea level - 700m. A xerophyte is a plant adapted for growth under dry conditions. This area of Tenerife is ideal for them. Examples include spurges, cactus spurge and wax plants. Thermophile Forests 200 - 600 m. A "thermophile" is described

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

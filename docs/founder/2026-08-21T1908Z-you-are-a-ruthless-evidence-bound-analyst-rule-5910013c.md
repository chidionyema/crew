---
captured: 2026-08-21T19:08:55+00:00
session: 1ad227db-8a83-468c-8d0e-61301ea9631a
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1851
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

Claim: As of April 23, 2022, Advance operated 4,687 stores and 311 Worldpac branches in the United States, Canada, Puerto Rico and the U.S. Virgin Islands.

Passages:
[s0168] From Wikipedia, the free encyclopedia
|Type||Public|
|Industry||Auto Parts Retail|
|Founded||April 29, 1932|
|Founder||Arthur Taubman|
|Headquarters||Raleigh, North Carolina , U.S.|
Number of locations
|4,912 Advance Stores, 150 Worldpac branches and serves 1,250 independently owned Carquest branded stores (as of July 13, 2019)|
Area served
| United States |
Canada
Key people
| Jeffrey C. Smith |
Chair, Board of Directors
Tom Greco (CEO, President)
Jeff Shepherd (CFO)
|Products||Replacement automotive parts & accessories|
|Revenue||US$ 10.11 Billion ( 2020 ) [1]|
|US$ 749.9 Million ( 2020 ) [2

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

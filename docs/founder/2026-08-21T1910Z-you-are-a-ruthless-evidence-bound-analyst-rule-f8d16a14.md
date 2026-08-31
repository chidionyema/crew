---
captured: 2026-08-21T19:10:19+00:00
session: 98b8e570-1d94-4e22-8b92-4065368e54d0
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3439
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

Claim: The Nepali Pranksters' videos have become popular on social media, showcasing the team's humorous take on cultural norms and values.

Passages:
[s0170] A video shoot in Nepal for an Internet comedy series took a serious turn on Saturday as the earth began rumbling. The Nepali Pranksters were in the middle of shooting an episode for their hidden camera series when the magnitude-7.8 earthquake broke out. The team kept the camera rolling as they moved through the crowded streets, surveying destruction to homes and historic sites and capturing scenes of heroism and chaos. The Nepali Pranksters' videos show people's reactions to various "pranks" that challenge cultural norms. One video shows the pranksters walking up to strangers and taking their hands for a long, awkward, handshake; another shows them complimenting men and women on their clothes and appearance, with mixed results. For their next prank based on Nepal's ban on plastic bags, Ashish Prasai and Akash Sedai were in Jawalakhel, Sedai said in an email to CNN. The town, in Lalitpur District, is home to Nepal's famed Central Zoo. The camera was rolling when they felt the ground shaking around 11:55 a.m., Sedai said. People started screaming and crying and vehicles came to a standstill as a building collapsed in the background. But earthquakes are a fact of life in Nepal, and "we were still thinking it was a just a simple earthquake," Sedai said. They kept the camera rolling for 18 minutes as they traversed the streets full of crying and shouting people. They found homes destroyed, where people were pulling survivors out from piles of rubble. They stopped and talked to motorists, urging them to keep the streets clear for emergency vehicles, Sedai said. They continued filming as they made their way to to the historic Dharahara tower and Basantapur Durbar Square, a UNESCO world heritage site, where people crawled among the ruins. By then, they realized their country was in a "very bad condition," Sedai said. The Nepali Pranksters made it through the first day of the earthquake, as did their families, Sedai said. But with aftershocks and crumbling infrastructure still posing threats, safety is a temporary state of mind right now in Nepal. "We are scared. ... Earthquakes waves are occurring now," he said. "Hope we will be alive and the problem will get solved soon."


Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

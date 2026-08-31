---
captured: 2026-08-21T18:51:15+00:00
session: 44ea86e2-1262-4cf3-93b1-bac29803f2f3
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3680
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

Claim: This is usually the result of escalating infractions or indignities, often stemming from a batter being hit by a pitch, or an altercation between a baserunner and fielder, such as excessive contact during an attempted tag out.

Passages:
[s0132] [1] A bench-clearing brawl is a form of ritualistic fighting that occurs in sports, most notably baseball and ice hockey, in which every player on both teams leaves their dugouts, bullpens, or benches, and charges the playing area in order to fight one another or try to break up a fight. Penalties for leaving the bench can range from nothing to severe.

[2] In baseball, brawls are usually the result of escalating infractions or indignities,[2] often stemming from a batter being hit by a pitch, especially if the batter then charges the mound.[3] They may also be spurred by an altercation between a baserunner and fielder, such as excessive contact during an attempted tag out.[2]

[3] Unlike most other team sports, in which teams usually have an equivalent number of players on the field at any given time, in baseball the hitting team is at a numerical disadvantage, with a maximum of five players (the batter, up to three runners, and an on-deck batter) and two base coaches on the field at any time, compared to the fielding team's nine players. For this reason, leaving the dugout to join a fight is generally considered acceptable in that it results in numerical equivalence on the field, a fairer fight, and a generally neutral outcome, as in most cases, managers and/or umpires will intervene to restore order and resume the game.

[4] A major plus a game misconduct penalty shall be assessed to any player who leaves the players’ bench or the penalty bench during an altercation or for the purpose of starting an altercation. These penalties are in addition to any other penalties that may be assessed during the incident.
Substitutions made prior to the altercation shall not be penalized under this rule provided the players so substituting do not enter the altercation.
For purpose of this rule, an altercation is considered to be concluded when the referee enters the referee's crease or, in the absence of penalties, signals a face-off location.

[5] The first player to leave either bench or penalty box to join or start a fight is automatically suspended without pay for 10 games. The second player to do that is suspended for five games without pay. The players' teams are fined $10,000 for the first incident, and the coaches of the teams face possible suspension and a fine based on review of the incident by the commissioner.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

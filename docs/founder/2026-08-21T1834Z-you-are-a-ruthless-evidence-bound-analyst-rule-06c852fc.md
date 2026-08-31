---
captured: 2026-08-21T18:34:13+00:00
session: 64dcd5d3-4774-4dc8-b9fd-71f4ded3b693
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3229
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

Claim: England won the women's six nations for the first time with a comfortable victory over ireland in dublin.

Passages:
[s0099] Media playback is not supported on this device
Amy Wilson Hardy went over in the corner as England scored from their only chance in the first half.
Ireland could not breach England's solid defence and were made to pay as the world champions ran in four tries.
Forwards Laura Keates and Amy Cokayne extended the visitors' lead before backs Emily Scarratt and Lydia Thompson rounded off the win with fine tries.
With the under-20 men's side having won a Grand Slam earlier on Friday, England's men will look to complete a hat-trick by beating Ireland in Dublin on Saturday.
The women, who return to Ireland in the summer to defend their world title, have won their first Six Nations title since 2012.
Wing Wilson Hardy completed a fine England move in the 16th minute, but then Ireland dominated play.
Centre Sene Naoupu came within a metre of going over but was stopped by a superb tackle from flanker Marlie Packer, and home captain Paula Fitzpatrick was prevented from touching down by a posse of England players.
England regrouped after half-time and extended their lead when replacement prop Keates drove over the line from two metres out.
Ireland were reduced to 14 players two minutes before the hour when substitute Mairead Coyne made a deliberate knock-on.
Hooker Cokayne burst through to increase England's advantage but Ireland hooker Leah Lyons responded to give Ireland hope.
However, Scarratt finished off an excellent England move to put the result beyond doubt and then replacement winger Thompson showed her pace to score England's fifth try.
Ireland: Flood, Tyrrell, Murphy, Naoupu, Miller, Stapleton, Muldoon; Peat, Lyons, Egan, Spence, Reilly, Griffin, Molloy, Fitzpatrick (capt).
Replacements: O'Connor, Van Staden, O'Reilly, Cooney, Fryday, Healy, Caughey, Coyne.
England: Waterman, Wilson Hardy, Scarratt, Reed, Wilson, Scott, Mason; Clark, Cokayne, Lucas, Taylor, Millar-Mills, Matthews, Packer, Hunter.
Replacements: Fleetwood, Cornborough, Keates, Cleall, Noel-Smith, Blackburn, Burford, Thompson.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

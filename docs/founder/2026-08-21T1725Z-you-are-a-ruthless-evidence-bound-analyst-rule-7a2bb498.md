---
captured: 2026-08-21T17:25:22+00:00
session: d727b773-5784-4651-8036-b3792f6b3db7
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 4873
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

Claim: Red squirrels are still widespread in Scotland and Northern Ireland, but their numbers are decreasing and they are being pushed out of many areas.

Passages:
[s0007] Red squirrels were once found across most of the UK. However, non-native grey squirrels have pushed them out of many areas.
Jump to:
Red squirrels are widespread in Scotland (around 75 per cent of the UK population) – especially the Highlands, but also Southern Scotland and Fife – and in Northern Ireland.
The best places in southern England to see red squirrels are the Isle of Wight and Brownsea Island, in Poole Harbour.
Elsewhere in England and Wales, there are pockets on Anglesey and in northern England, such as Cumbria, Kielder Forest and a noted concentration of red squirrels around Formby.
We've been involved in red squirrel conservation for a number of years and plan to continue with this work.
We are involved in partnership work designed to prevent the decline of our remaining red squirrels strategically:
- We are a member of the Scottish Squirrel Group and have worked with various other partners in the creation of the Scottish Squirrel Strategy, designed to protect red squirrels in the main stronghold areas in the north and the relatively isolated red squirrel populations that remain in south Scotland.
- The RSPB is on the Project Advisory Board of the Red Squirrel Northern England project (RSNE), which focuses on protecting red squirrel populations in key strongholds and informs management work.
We are also providing a home for red squirrels on a number of our own reserves, some examples include:
- We ensure forest management in important red squirrel strongholds, such as Abernethy, is sympathetic to maintaining strong populations and monitor for grey squirrel presence on our reserves in South Scotland.
- In Northern England, the red squirrel is a key species at Haweswater reserve and at Geltsdale we are working with local red squirrel groups to monitor reds and support them in preserving populations.
- There is a good population of red squirrels at Brading Marshes on the Isle of Wight. We manage several semi natural ancient woodland copses, and since 2008 we have planted new woodland, which when mature will link and extend two of the copses specifically to benefit red squirrels.
Red Squirrels Northern England (RSNE) is a red squirrel conservation partnership working right across northern England.
The non-native grey squirrel has replaced the red squirrel in most of southern Britain.
Control measures to help red squirrels in these areas are futile. However, the RSPB does take action to protect red squirrels against the advance of grey squirrels in areas where the two species are likely to encounter one another, or in areas which grey squirrels may use as corridors to reach areas still inhabited by red squirrels.
This action does include limited culling, often done in partnership with other organisations. Grey squirrels are only culled on RSPB reserves when necessary to achieve nature conservation objectives, in an effective and humane way and in compliance with legal requirements.
We do not 'blame' the grey squirrel for these problems – it was people who brought the species over from America and introduced it into the wild. However, we do believe strategic action must be taken to protect our red squirrels.
The RSPB recognises the extreme threat posed to red squirrels by the advance of grey squirrels.
We were part of the partnership which developed the strategic approach to defending the reds' core distribution in Scotland. Where red squirrels occur on our reserves, such as the Isle of Wight and at Abernethy in Scotland – one of the UK's largest red squirrel strongholds – they are a high conservation priority and we manage habitats for their benefit.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T17:49:02+00:00
session: aacf95c5-679b-40cb-94bc-bfb836368647
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 6143
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

Claim: The document discusses a resolution to prioritize the spending of marijuana business license tax revenue for specific purposes, including public health, public safety, homelessness, and general services for regulation and enforcement.

Passages:
[s0018] Speaker 1: Motion carries.
Speaker 0: Thank you. Item number 13, please.
Speaker 1: Communication from City Attorney. Recommendation to adopt resolution expressing its intent to prioritize spending of marijuana business license tax revenue for specific purposes.
Speaker 0: Thank you, Councilman Price.
Speaker 5: Yes, I'd like any money that that is generated as a result of the tax to go to the items and areas specified by the city attorney in the resolution with a special focus on public health and safety. Thank you.
Speaker 0: Great. Thank you. And I'll just add my comments here. In August, we submitted this this resolution indicating our intent to use the business license, tax revenue for public safety, public health, homelessness, and general services for regulation and enforcement. And it's great to see that in the final resolution, all of these will be prioritized for spending if this tax passes. So I do want to thank city staff and the City Council for collaboration on this resolution to ensure that the revenue is spent in a way that fully benefits our city and our residents and recovers any costs associated with the regulation of the medical marijuana ordinance should it pass by the voters. So, Councilmember Pearce.
Speaker 4: Yes. I also want to thank staff for their report that they did previously and just want to reiterate that do want to see the funds go to cost recovery, prioritize that and then additionally making sure that we are addressing things like first responder times both with our police and our fire, that we are using these dollars to bring back our public safety. And then you know that. When we have that in the general fund, I would definitely support any additional funding after cost recovery and public safety. Again, going to issues of health equity and and areas like that that can be addressed through services. So thank you for your work on this.
Speaker 0: Thank you, Councilman Andrews.
Speaker 6: Thank you, Vice Mayor. You know, I'd like to thank Mr. Parkins for drafting this resolution. And I would hope that when we talk about public safety, we're not only talking about police and enforcement, but the critical fire service as well. Thank you.
Speaker 0: Thank you. Is there any public comment on this item?
Speaker 6: Mm hmm.
Speaker 1: Good evening, my Mayor Richardson and honorable city council members. My name is Margaret Dudley and I live in the ninth District. And I would just like to speak on the. The priority for the. The measure a spending funding. I believe you're going to need that for first responders. Police first. Hospitals, mental health care. Also paramedics. You're going to need it also for attorney lawyers because it's going to be a lot of lawsuits. So you need to prioritize that money that you're going to get from Missouri for that. Thank you very much.
Speaker 0: Thank you, Margaret. Next.
Speaker 7: Night seven works in Soho district is for two resident. Speaking on this agenda item for two different reasons. One, as I stated before, the current tax rates that are being considered under measure M-A are cost prohibitive for a business that is that is currently built for businesses that are going to be taxed under federal schedule to 80 , an effective rate of anywhere between 50 and 80%. So for the purpose of controlling the black market, the best way to meet and to ensure that that will happen is to give support to the businesses that are putting putting themselves in front of the breach and accepting the registration and working within written to the the created regulatory scheme. As such, it would be, you know, even a business like a business tax that anywhere from 8 to 12% is really cost prohibitive for, especially in the retail sector. Secondly, in the interest of protecting measure, it may and the ability in the city's ability to tax at this particular at at these levels, it's I think the city's being too cute by half by engaging in what is by all means a special tax. Any proposition to analysis that goes into the legislative intent of this measure, especially the ones that are being expressed at this turning time, especially for specific allocations towards public towards public safety and cost allocation, as we're talking about, really indicates something that is a special tax and that's fantastic. If the city wants to raise money for first responders, mental health, public health, I'll go along with them. But you also are going to be subject to it to the to it towards passing that particular measure at a two thirds rate, not a 50% plus one. Simple as that. Thank you. And have a good day.
Speaker 0: Thank you. Take it back behind the rail. Let's go ahead. And members, please cast your vote.
Speaker 1: Motion carries.
Speaker 0: Thank you. Let's have item number 14.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

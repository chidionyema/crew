---
captured: 2026-08-21T17:29:41+00:00
session: f35744f9-3095-4a9c-9165-8a4a5bd3c127
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 6333
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

Claim: Representatives held hearings in San Diego and Philadelphia to highlight their respective positions, with Republicans stressing the need for border security and Democrats advocating for the Senate's immigration bill.

Passages:
[s0011] LYNN NEARY, host: This is MORNING EDITION from NPR News. I'm Lynn Neary, in for Renee Montagne.
STEVE INSKEEP, host: And I'm Steve Inskeep. Good morning.
STEVE INSKEEP, host: All this year's debate and protest over immigration has left one giant question unanswered. The question is whether Congress will actually change immigration law - lawmakers are deeply divided. It is possible to imagine a compromise, as we'll here in a moment, but yesterday lawmakers put their differences on display. Senators turned up in Philadelphia to highlight the value of foreign workers, even those who came here illegally. Members of the House went to the opposite coast to make an opposing point. In San Diego, they stressed the need for tighter border security. Our coverage starts with NPR's Carrie Kahn.
CARRIE KAHN reporting: California Congressman Ed Royce picked a San Diego border patrol station to hold his Terrorism Subcommittee hearing in hopes of drumming up public support for the House immigration bill. Royce says by building more fences and hiring thousands of agents, the border will be safer.
Representative ED ROYCE (Republican, California): Immigration reform must be national security reform. Our country has made progress in fighting terrorism since 9/11, but in some areas we're losing ground, including the most fundamental task of securing our physical borders.
KAHN: Republicans highlighted the potential for terrorists coming into the U.S. from Mexico. Sheriff Rick Flores of Webb County, Texas, testified that he and his handful of deputies are outnumbered by drug dealers and smugglers. Congressman Ted Poe of Houston asked him about even greater threats.
Representative TED POE (Republican, Texas): Explain why, in your opinion, al-Qaida would set up operation in Mexico and come here.
Sheriff RICK FLORES (Webb County, Texas): Well, Mr. Poe, it's very easy for these people to go ahead and blend in in Mexico, learn the language, learn the culture, and camouflage themselves as Mexicans crossing the border.
Representative TED POE (Republican, Texas): Is it your opinion that that may happen, may even actually be going on?
Sheriff RICK FLORES (Webb County, Texas): It's probably already happened.
KAHN: House Democrats are quick to point to vulnerabilities at the Canadian border, which one Congressional study put at greater risk for terrorist incursions. And on several occasions, Democrats blamed six years of the Bush administration for failing to control the nation's borders. But Republicans pressed on. Newly elected Congressman Brian Bilbray, from San Diego, asked the local head of the border patrol why his agency can't do more to crack down on local gathering spots for illegal immigrants. Border Chief Darryl Griffen said his agents focus on the major hubs like bus stations and airports.
Chief Patrol Agent DARRYL GRIFFEN (San Diego Sector, U.S. Customs and Border Protection): That is our focus.
Representative BRIAN BILBRAY (Republican, California): Chief, in my neighborhood, the Home Depot is a major hub. It's a community center.
KAHN: The ranking Democrat on the subcommittee, Congressman Brad Sherman from Los Angeles, interrupted.
Representative BRAD SHERMAN (Democrat, California): Mr. chairman, if I could just comment. Our subcommittee focuses on terrorism, and I doubt there are many terrorists at Home Depot.
Representative ED ROYCE (Republican, California): We are going to now ask...
KAHN: Chairman blasted Republicans for putting on, what he said was, a dog and pony show stacked with sympathetic witnesses. But not all of them helped the cause. Los Angeles County Sheriff Lee Baca told lawmakers that a massive crackdown on illegal immigration might cost more than many Americans are willing to pay.
Sheriff LEE BACA (Los Angeles County Sheriffs Department, Los Angeles California): This is not an issue that can be easily dealt with with a simple solution. We don't have enough prisons in America, or enough local jails in America, to incarcerate employers and their workers combined. They're not there.
KAHN: While opponents of illegal immigration filled the hearing room and overflowed to a tent outside, immigrant supporters gathered down the street.
KAHN: Mariachi musicians sang of eluding the border patrol. And many spoke in support of the Senate's immigration bill, which would give millions of illegal migrants a chance at U.S. citizenship. Local labor leader, Jerry Butkiewicz, says it's time for real reform.
Mr. JERRY BUTKIEWICZ (Secretary/Treasurer, San Diego Labor Council): When people come to this country and they are willing to work hard, and they are willing to pay taxes, and they are willing to abide by our laws, they are willing to contribute to our economy, they have a right to real immigration reform. They have a right to citizenship.
KAHN: Activists on both sides of the debate say they will follow the House Republicans to Laredo, Texas, where the next hearing is scheduled to take place tomorrow.
KAHN: Carrie Kahn, NPR News, San Diego.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

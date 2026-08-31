---
captured: 2026-08-21T17:51:12+00:00
session: 19dae629-3d85-4546-8a2d-44cb523035f9
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 6114
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

Claim: A business case for the upgrade of the North Auckland Line and the Marsden Point Branch's construction was prepared by New Zealand Ministry of Transport and published May 2019.

Passages:
[s0030] TITLE: Northland rail upgrade to cost $1.3b, but Northport expansion needed to get value for money | Newshub More Weather ## Magic Talk Listen Now # Northland rail upgrade to cost $1.3b, but Northport expansion needed to get value for money John-Michael Swannix It estimates the total cost at $1.3b over 40 years. Credits: Newshub A new report reveals an upgrade of Northland's rail network will only be worthwhile if Northport's operations are expanded. The Ministry of Transport business case examined the cost of upgrading the rail line between Auckland and Whangārei, reopening the mothballed tracks north to Moerewa and west to Dargaville, and constructing a new spur east to Northport. It estimates the total cost at $1.3b over 40 years. Including $730m in the first four years during the construction phase and $3m for improvements and maintenance in the years after. However, the economics tread a fine line. In the best-case scenario, the report gives the investment a benefit-cost-ratio (BCR) of 1.19, meaning for every $1 spent there would be a $1.19 return. This would require a major expansion of Northport which would see it handling 400,000 containers, 100,000 from within Northland and 300,000 from Auckland. In the year to June 2019 Northport expects to handle 12,500 containers, up from 8000 last year. Without this expansion of Northport, the BCR falls to 0.32, meaning the Government would only get back 32 cents for every $1 spent. The majority of the economic benefits come from easing congestion on Northland and Auckland's roads, by reducing truck trips by 75,000 per year. A 2017 report found congestion costs Auckland between $900m and $1.9 billion a year. Just 1.4 percent of freight in Northland is currently moved by train due to the lack of rail to Northport and the tunnels and bridges, some of which can't fit modern containers or support heavier loads. If the investment was to go ahead, the amount of freight being transported by rail in Northland is expected to grow to 10 to 14 percent, around 2 million tonnes, which is above the national average of 7 percent of freight transported by rail. Other benefits include saving $20 million in road crashes involving trucks, saving $3.8 million in annual road maintenance and reducing carbon emissions by 10 thousand tonnes. The business case suggests that if Whangārei's growth figures were similar to that of Waikato or Tauranga, which have both benefited from strong road and rail connections, then it could see a further 2,000 to 10,000 jobs over a 12-year-period. However it does not include job creation in its BCRs, nor the impact such an investment would have on spurring business investment decisions in Northland. Associate Transport Minister Shane Jones says it's important to keep this in mind. "The reality is that if you're in the business of nation building, you cannot capture every perceived benefit over 50 to 100 years through one consultant's report." The business case also doesn't look at the costs to Auckland, in terms of jobs or added transportation costs, that would occur if the Ports of Auckland's operations were moved to Northport. Infrastructure NZ chief executive Stephen Selwood, speaking before seeing the report, told Newshub Nation that New Zealand's historic reliance on BCRs has led to the country's current infrastructure deficit. "Traditional benefit-cost-analysis measures direct benefits but not the wider social and economic benefits from investing in infrastructure, such as stimulating business growth or jobs or improving social connectivity. "If Richard Seddon [NZ Prime Minister from 1893-1906] had been given a BCR for building New Zealand's entire rail network it probably would have been around a 0.3. "In the 1990s, the Government often wouldn't invest in infrastructure projects unless they had a BCR of 3 or 4. This meant that regional roads went ahead of needed transport projects in Auckland because land prices there were too high, leading to a comparatively low BCR. "BCR analysis is an important component of an investment decision but in the end one has to make a judgment as to whether overall benefits - social, environmental, and economic - provide a return to the nation as a whole." Jones says his next steps are to consult with iwi and officials, secure the land along the rail corridor to Northport, and seek further information on potential freight demand. The business case will also factor into the research of the Upper North Island Supply Chain Working Group, which is due to release its recommendations in September. With Budget day around the corner, Jones also gave a hint of the Coalition Government's intentions. "Rail obviously is going to enjoy great attention coming up in the Budget, but I'll leave it to my leader [Winston Peters] to elaborate," Jones says. Newshub Nation.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

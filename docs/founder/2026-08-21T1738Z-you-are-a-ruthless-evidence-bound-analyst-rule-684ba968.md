---
captured: 2026-08-21T17:38:15+00:00
session: f727d44a-784e-434b-809b-c3d4c00f2d1b
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3765
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

Claim: The Yazidis have faced persecution for their religious beliefs, and ISIS' treatment of them has been particularly brutal, including rape and enslavement.

Passages:
[s0012] ISIS on Wednesday released more than 200 Yazidis, a minority group whose members were killed, captured and displaced when the Islamist terror organization overtook their towns in northern Iraq last summer, officials said. Most of those released were women and children; the rest were ill or elderly, said Rassol Omar, a commander in the Peshmerga force that defends  northern Iraq's semi-autonomous Kurdish region. Omar didn't say what led to the release, other than asserting that Arab tribal leaders helped to coordinate it. The freed Yazidis were received by Peshmerga, who sent them to the Kurdish regional capital, Irbil, said Nuri Osman, an official with Iraq's Kurdistan Regional Government. It wasn't immediately clear what motivated Wednesday's release, Osman said. Osman said 217 Yazidis were released. Omar, the Peshmerga commander, had a higher count: 228. ISIS previously released scores of other Yazidis -- largely children and the elderly -- since attacking the group's towns last year. The Sunni Islamist militant group steamrolled into Iraq's north last summer, forcing hundreds of thousands of minorities -- Yazidis among them -- from their homes. Yazidis are of Kurdish descent, and their religion is considered a pre-Islamic sect that draws from Christianity, Judaism and Zoroastrianism. One of the oldest religious communities in the world, the Yazidis have long suffered persecution, with many Muslims referring to them as devil worshipers. ISIS' cruelty to them has been extraordinary. ISIS' conquest of the town of Sinjar, in particular, provoked a major humanitarian crisis as some Yazidis fled into the mountains -- where many became trapped for a time without food and water -- and others fled by foot into neighboring Syria. ISIS slaughtered Yazidis by the hundreds, Yian Dakhil, the only lawmaker representing the Yazidis in Iraq's Parliament, told CNN last year. Reports emerged from some Yazidi survivors that ISIS raped and enslaved female Yazidi captives. An international coalition responded, first by airdropping supplies in the mountains. Rescues came next. And then, starting in August, the United States and other nations conducted airstrikes targeting ISIS in Iraq and Syria. The U.S. State Department estimates that 500,000 Yazidis live in northern Iraq, accounting for less than 1% of the country's population. CNN's Raja Razek reported from Beirut. CNN's Jason Hanna wrote from Atlanta. CNN's Hamdi Alkshali, Faith Karimi and Yousuf Basil contributed to this report.


Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T18:02:28+00:00
session: 3cb17e59-7e54-487d-92f7-76812c39e376
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3657
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

Claim: It is understood that North Korea is currently dealing with issues such as widespread poverty and ongoing disputes with South Korea and the US.

Passages:
[s0045] Moscow (CNN)Never mind. North Korean leader Kim Jong Un has backed out of next month's visit to Moscow for World War II anniversary celebrations, Kremlin spokesman Dmitry Peskov said Thursday. "We were informed of the decision via diplomatic channels," Peskov said. "The decision is connected with North Korean domestic affairs." The visit was highly anticipated because it would have marked Kim's first official foreign trip since inheriting the leadership of North Korea in late 2011. He was to have met with Russian President Vladimir Putin as part of the May visit to coincide with Victory Day, marking the 70th anniversary of the Soviet Union's victory over Nazi Germany in World War II. Kim also could have had the chance to rub elbows with the heads of about 30 other governments, including the leaders of China, Cuba, India, Germany, Vietnam and Venezuela. This number represents about half the world leaders that Russia has said it invited to the celebrations. Kim's trip had been anticipated since late December, when Russian state media reported that Moscow had extended an invitation. There was no further explanation, from Moscow or Pyongyang, as to why he wouldn't head west. Still, North Korea has a number of issues it's been wrestling with for years. They include widespread poverty, its longstanding spat with neighboring South Korea and the United States, as well as its international isolation largely due to its controversial nuclear program. And news about Kim's non-visit comes a day after South Korean intelligence agents told lawmakers that Kim is ruling with an iron fist, having ordered the execution of about 15 senior officials so far this year. CNN cannot independently confirm the executions detailed by Shin Kyung-min, a lawmaker with the New Politics Alliance for Democracy who attended the closed briefing.  And the nature of the intelligence supporting the allegations was not immediately clear. That said, North Korea is one of the most closed societies in the world. And there's little doubt that Kim is very much in charge. According to Shin, intelligence officials say the North Korean leader is ruling in an impromptu manner and does not countenance excuses or any views that vary with his own. CNN's Madison Park and Alla Eshchenko contributed to this report. CNN's Matthew Chance reported from Moscow, and CNN's Ed Payne and Greg Botelho wrote this story from Atlanta.


Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

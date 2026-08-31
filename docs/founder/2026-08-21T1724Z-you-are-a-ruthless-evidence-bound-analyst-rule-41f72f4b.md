---
captured: 2026-08-21T17:24:11+00:00
session: 48483560-c25b-4887-b32d-2ca57e19bdfc
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3238
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

Claim: Kenyans use social media to share the victims' stories, hopes and dreams. The hashtag # 147notjustanumber refers to the number of people killed at Garissa University College. Kenyan authorities have not released a list of the victims. The attack killed 142 students, three security officers and two university security personnel.

Passages:
[s0006] One hundred and forty-seven victims. Many more families affected. Even more broken hopes and dreams. As Kenyans mourned those killed last week in one of the deadliest terrorist attacks in the nation, citizens used social media to share the victims' stories, hopes and dreams. Using the hashtag #147notjustanumber -- a reference to the number of people, mostly students, killed at Garissa University College on Thursday -- Kenyans tweeted pictures of the victims in happier times. Kenyan authorities have not released a list of the victims. The posts provided heart-wrenching details on the victims, including one about an elderly man whose dreams died with his son. He had reportedly taken a loan to educate him at the university, where he was killed by Al-Shabaab terrorists. The attack in Kenya killed 142 students, three security officers and two university security personnel, and was the nation's deadliest since the bombing of the U.S. Embassy in 1998. Kenyan churches mourned the dead during Easter services Sunday as armed guards protected the congregations. In emotional services nationwide, churchgoers wept as they paid tribute to the victims of the massacre. The gunmen who attacked the university in the predawn hours separated Muslims from Christians and killed the latter. The extremist group has also killed Muslims in recent attacks. The Interior Ministry has identified one of the attackers killed by security forces as the son of a government official. The father of suspect Abdirahim Abdullahi is a chief in Mandera and had reported his son missing, officials said. The Islamist extremist group is based in Somalia, but it hasn't confined its terrorism to the nation that shares a border with Kenya. In 2013, militants attacked Nairobi's upscale Westgate Mall, killing nearly 70 people.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T18:45:23+00:00
session: 5f8cdd9f-3949-4e5c-8469-534cb3d2054f
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3751
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

Claim: Sharita described her sister as a "really, really good person" and hopes that her story will raise awareness about domestic violence prevention and the need for better political policies to protect victims.

Passages:
[s0122] Clarita Poole, 27: BF Charged With Murder Of Detroit Woman
A Detroit, Mich. woman was callously left to die in the street, but the authorities believe they detained the man responsible. In July 2020, a man casually made his way to a local store when he came across a gruesome scene. Clarita Poole was found lying in the road, wearing only a bra, and shot in the head. The man jumped into action, and instead of waiting for emergency responders to arrive, he rushed Clarita to a nearby fire station for help.
From there, Clarita Poole was taken to a hospital where doctors stated there was little brain activity. She later passed away.
Not long after the 27-year-old’s death, her sister, Sharita Poole, told reporters that she believed Charita’s boyfriend, Dorian Johnson, was involved in the murder. At the time, Sharita said that she could tell “from his social media” that “he is not a good person,” and an investigation would uncover past instances of alleged domestic violence involving the couple.
“We really didn’t recognize her at first,” Sharita recalled as she spoke about seeing Clarita at the hospital. “She had a gunshot wound in the back of her head. She wasn’t breathing on her own, she was completely on a machine.”
“It was a murder. She was purposely hurt. She was murdered.”
According to Sharita, her sister was being used for her money in her relationship, yet still, Clarita purchased a vehicle for Johnson. The pair were known to argue frequently argue and according to reports, Johnson even threatened to have Clarita gang-raped.
[Make Sure To Follow!]
“If he personally does not have that gun powder on his hands, he knows who did it and he’s the one who set it up to be done,” said Sharita. “It wasn’t much she would tell us because she knew we didn’t like him, we didn’t know her around him. We tried to warn her from the very second we heard about this guy.”
In March 2021, eight months after Clarita’s killing, Johnson was arrested and officially charged with first-degree homicide, firearms – possession by a felon, and two counts of felony firearm.
“She was a good person,” Sharita stated. “She was a really, really good person.”
Please share this story about Clarita Poole to help spread awareness about the importance of domestic violence prevention and to help shed light on political policies that do not protect victims in similar circumstances. She is our sister and her life mattered.
[Make Sure To Follow!]

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

---
captured: 2026-08-21T17:45:57+00:00
session: 267050fe-086e-43d2-be4c-704b459e53fd
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2243
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

Claim: Native-Americans and Alaska Natives have a higher tendency to experience feelings of nervousness and restlessness compared to non-Hispanic white people .

Passages:
[s0022] and Native-Americans — are more likely to experience the risk factors that can cause such mental health disorders. In one study, researchers found African-Americans had significantly higher rates of schizophrenia compared to whites. In contrast to their white counterparts, African-Americans were also more likely to report their depression as being extremely severe and disabling. Meanwhile, the same CDC report from 2016 found Native-Americans and Alaska Natives have a higher tendency to experience feelings of nervousness and restlessness when compared to non-Hispanic white people.Go to a tabular version of Mental Illness in U.S. Minority-Majority Groups.Social Determinants of Mental HealthA deep dive into the forces that drive disparities in minority care often points to barriers to medical access. Access can be limited by lack of insurance coverage — and more than half of uninsured U.S. residents are people of color. People with limited resources also experience logistical

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

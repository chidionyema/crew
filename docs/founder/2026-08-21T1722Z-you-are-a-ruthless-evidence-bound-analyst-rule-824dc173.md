---
captured: 2026-08-21T17:22:48+00:00
session: de4666b1-fd7b-4359-b0ac-b3fad3970568
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 1864
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

Claim: Mild allergic reactions can be managed by avoiding contact with the allergen, taking over-the-counter antihistamines, or using topical creams for skin symptoms .

Passages:
[s0000] skin prick tests and blood tests. Skin prick (scratch) tests can identify the allergens that cause your allergy symptoms. An allergist will use a thin needle to prick your skin with a tiny amount of different possible allergens. They then check to see if your skin reacts to the allergen. Blood (IgE) tests can also identify allergies. However, they’re not as sensitive as skin prick tests. Blood tests evaluate IgE antibodies that your immune system produces against a specific protein.

Management and Treatment How are allergies treated? Avoiding allergens is an important treatment approach. Howe

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

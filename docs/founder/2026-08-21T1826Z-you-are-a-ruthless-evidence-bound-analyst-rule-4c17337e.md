---
captured: 2026-08-21T18:26:49+00:00
session: 8a146173-f28c-4ee1-bd16-dbd8764a403e
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3475
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

Claim: They did this by writing a constitution that protects the freedom of individuals, guarantees their dignity, and ensures that all people are treated equally before the law.

Passages:
[s0085] [1] The German constitution, known as the Grundgesetz or Basic Law, protects the freedom of individuals, guarantees their dignity and ensures that all people are treated equally before the law - no matter what their race, origin, language or religion. It also subjects state power to strict controls through the separation of powers - to prevent a dictator from ever seizing power in Germany again.
With the Basic Law, Germany learned its lessons from the catastrophe of the Third Reich, the Nazi dictatorship under Adolf Hitler from 1933 to 1945. Tens of millions of people died in World War II, in which Germany was an aggressor. Six million Jews were murdered in the Holocaust.
After 1945, democracy returned to Germany, at least in the west of the country. There, the Basic Law was adopted in 1949. It was intended to serve as a transitional constitution, until Germany could be reunited.

[2] The Basic Law establishes a federal state with three levels of government. The federal and state governments share political power. The 16 states transfer central competencies to the federal government, but have a say in its legislation. In other areas, the states have legislative autonomy. The municipalities are the third, lowest level.
The constitution sets up barriers to radical, undemocratic tendencies. The Federal Republic has the power to ban unconstitutional parties - and used it to shut down the neo-Nazi Socialist Reich Party (SRP) in 1952 and the German Communist Party (KPD) four years later.

[3] Furthermore, not every party can get into parliament: Only those that overcome the constitutional 5-percent threshold in an election are allowed to take seats. This rule is intended to give the Bundestag stability.

[4] Another institution keeps an eye on power sharing, fundamental rights and democracy - the Federal Constitutional Court. Its main duty is the judicial review - examining laws for their constitutionality, and thus helping all citizens to enforce their rights and freedoms against the state.
The German court is a unique defender of the Basic Law, and it has been copied around the world. One example is Spain, where a similar court was also enshrined in the constitution.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

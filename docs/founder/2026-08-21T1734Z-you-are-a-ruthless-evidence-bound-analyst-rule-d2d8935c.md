---
captured: 2026-08-21T17:34:48+00:00
session: 6578e154-5d29-41f0-aabd-2d4a2e9be55e
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2544
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

Claim: A prominent ukrainian activist, olexander kalashnikov, has been found dead in his flat in the capital kiev.

Passages:
[s0007] Mr Kalashnikov had been involved in the "anti-Maidan" protests in support of deposed President Viktor Yanukovych.
It is not clear if he was murdered or committed suicide. Police say an investigation has been launched.
At least eight Yanukovych allies have died suddenly in the last three months.
Most of the deaths are said to have been suicides. However, officials say it was possible some were killed or forced to take their lives.
Commentators in Ukraine have accused supporters, as well as opponents, of the current pro-Western government of involvement in the deaths.
The BBC's David Stern in Kiev says no motive has emerged linking the deaths and no arrests have been made.
Mr Kalashnikov was a former deputy in parliament and a member of Mr Yanukovych's Party of Regions.
Accounts of his death differ, with some sources saying his body was found outside his flat in Kiev and others saying it was found within.
Mr Yanukovych fled Ukraine in February last year, after months of increasingly violent protests against him, centred on the Maidan, Kiev's main square.
He later reappeared in Russia. The government that succeeded him reversed his opposition to closer ties with the European Union - a major factor behind the protests.
It has since been plunged into a conflict with pro-Russian separatist rebels in the country's east.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

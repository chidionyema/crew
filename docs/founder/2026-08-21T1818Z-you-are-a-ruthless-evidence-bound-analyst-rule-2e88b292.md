---
captured: 2026-08-21T18:18:26+00:00
session: d07675b5-e0b4-42dc-8058-e423cdb198d0
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3165
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

Claim: Based on the provided passages, it appears that if your scholarship money exceeds the cost of attending school, your school will reduce the amount of financial aid you receive, including grants and loans, so that the total amount of aid does not exceed the school's cost of attendance.

Passages:
[s0067] {'question': 'what happens if my scholarship money exceed cost of school', 'passages': "passage 1:If your scholarship covers only your tuition and you are a degree-seeking student, you do not have to report any of your scholarship on your income taxes. However, if you are not a degree-seeking student, you must include the scholarship as taxable income.f your scholarship covers only your tuition and you are a degree-seeking student, you do not have to report any of your scholarship on your income taxes. However, if you are not a degree-seeking student, you must include the scholarship as taxable income.\n\npassage 2:This applies to your scholarship total, not each individual scholarship. For example, if you have a scholarship from the school of $15,000 and a private foundation scholarship of $10,000, your total scholarship aid would be $25,000.f your scholarship covers only your tuition and you are a degree-seeking student, you do not have to report any of your scholarship on your income taxes. However, if you are not a degree-seeking student, you must include the scholarship as taxable income.\n\npassage 3:Relevance. Rating Newest Oldest. Best Answer: Matt: Students are not permitted to profit from financial aid. If your total aid, including all loans, grants, and scholarships exceeds your school's actual Cost of Attendance, one or more forms of the aid will be 'cut back' so that an equilibrium is reached.Keep in mind, however, that Cost of Attendance is more than just your tuition, books and fees.f your total aid did, in fact, exceed your full Cost of Attendance, your school will hold back some of its own institutional grant funds (first), and then any outside funds-necessary to bring your total aid award level with your Cost of Attendance.\n\n"}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.

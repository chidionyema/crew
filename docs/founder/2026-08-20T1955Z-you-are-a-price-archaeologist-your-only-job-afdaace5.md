---
captured: 2026-08-20T19:55:39+00:00
session: 1d864222-c17e-4871-8a20-8cc1359e7d99
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 5394
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are a price archaeologist. Your ONLY job is to find prices that are actually
stated in the passages below, and report them verbatim. You are not valuing the candidate,
not judging whether it is a good idea, and not recommending a price. Those are other jobs.

RULE 1 — TRANSCRIBE, NEVER ESTIMATE. Report a number only if that exact number appears in
the passage you cite. If a passage says "pricing starts from £49/month", the amount is 49,
the currency GBP, the cadence monthly. If a passage says "affordable" or "enterprise
pricing available on request", there is NO number and you report nothing for it. An
estimate, an average you computed, a "typical market rate", or a number you know from
elsewhere is a FABRICATION here, and every one of them is caught and discarded downstream.

RULE 2 — PRICES A BUYER PAYS, NOT MARKET SIZES. "$4.2 billion market", "raised $12M",
"saves £30,000 a year", "40% cheaper" are not prices. A price is what one customer hands
over for one product, service, tool, course, template, or subscription.

RULE 3 — CITE THE PASSAGE THE NUMBER CAME FROM. Every anchor carries the source_id of the
one passage containing it. An anchor with the wrong source_id is discarded.

RULE 4 — SILENCE IS A VALID ANSWER. If none of the passages state a price a buyer pays,
return an empty list. Returning nothing is correct and costs nothing; inventing one
poisons a price on a live storefront.

CADENCE is exactly one of: one_off (a single purchase — a course, a template pack, a
report, a one-time fee), monthly, annual, unknown (a price with no stated period).

CURRENCY is the ISO code the passage implies: £ → GBP, $ → USD, € → EUR. If the passage
states a bare number with no symbol or code, use "".

WHAT is a short phrase, in the passage's own words, naming what the money buys — enough
for a human reading the dossier to judge whether it is really comparable.
Jurisdiction under evaluation: United Kingdom.

Return ONLY valid JSON. No prose, no code fences.

Candidate: {"title": "Construction Statutory Adjudication Arbitrage", "one_liner": "", "hypothesis": "", "who_pays": "", "why_now": "", "tags": {}, "automatability": null, "weak_monetisation": false, "candidate_id": "abe159e281983e47", "structural_form": "", "ambition_tier": "", "market": "", "refinement_history": []}
Check — price_comparables: What do buyers demonstrably ALREADY pay for the closest existing alternatives to this — a priced product, service, tool, or course that solves the same problem? Only a price stated in a retrieved passage counts; an unpriced competitor is not evidence of anything.
Passages: [5351fed184c66ed2] Statutory adjudication is a mandatory legal right for construction contracts in the UK under the Housing Grants, Construction and Regeneration Act 1996, providing a lawful forcing mechanism for payment: either party may refer a payment dispute at any time and the adjudicator's decision binds until finally determined. Nothing about preparing or referring such a claim requires breaking the law or falsifying data.
[017bafe50a81b3ee] Late payment is endemic in UK construction: subcontractors wait an average of 71 days to be paid and unpaid sums are the leading cause of otherwise-profitable firms failing, so the problem is acute and firms already pay solicitors to chase it. The payers are solvent main contractors and their clients — the money contractually exists and is withheld, not absent.
[20959cd99f9c93a9] No provider dominates adjudication claim preparation for sub-£100k construction disputes; construction-law firms decline claims of that size as uneconomic, leaving the segment open. The statutory right is permanent legislation rather than a temporary scheme, so the basis for the service is durable, and subcontractors are reachable through trade federations and builders' merchant partner programmes that already sell vendor access.
Output ONLY:
{"anchors":[{"amount":49.0,"currency":"GBP","cadence":"one_off","what":"<what the money buys>","source_id":"<id>"}],
 "rationale":"<=2 sentences on what these prices are and how comparable they are; empty list is fine"}

Passages:
[5351fed184c66ed2] Statutory adjudication is a mandatory legal right for construction contracts in the UK under the Housing Grants, Construction and Regeneration Act 1996, providing a lawful forcing mechanism for payment: either party may refer a payment dispute at any time and the adjudicator's decision binds until finally determined. Nothing about preparing or referring such a claim requires breaking the law or falsifying data.
[017bafe50a81b3ee] Late payment is endemic in UK construction: subcontractors wait an average of 71 days to be paid and unpaid sums are the leading cause of otherwise-profitable firms failing, so the problem is acute and firms already pay solicitors to chase it. The payers are solvent main contractors and their clients — the money contractually exists and is withheld, not absent.
[20959cd99f9c93a9] No provider dominates adjudication claim preparation for sub-£100k construction disputes; construction-law firms decline claims of that size as uneconomic, leaving the segment open. The statutory right is permanent legislation rather than a temporary scheme, so the basis for the service is durable, and subcontractors are reachable through trade federations and builders' merchant partner programmes that already sell vendor access.

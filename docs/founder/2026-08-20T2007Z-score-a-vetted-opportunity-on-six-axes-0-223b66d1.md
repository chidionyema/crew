---
captured: 2026-08-20T20:07:02+00:00
session: 506ebd2d-407d-4774-b40d-2b6b0fb24d5b
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 9156
source: founder prompt, verbatim (founder-doc-capture.py)
---

Score a vetted opportunity on six axes, 0-5, grounded ONLY in the provided
claims. Same standard for any sector. Score `automatability` REALISTICALLY against what
current, real tooling can actually do today — not aspiration. Justify each in one line
citing source_ids where used.

HOW TO WORD IT (this governs the WRITING ONLY — it does not touch your ruling):
Your verdict, your standard of proof, your confidence and your citations are exactly
what they would be otherwise. The reader of this line is not on this project and has
never seen our vocabulary. Write for them.

  - Say what the passages showed, then what that means for the claim. Active voice,
    one idea per sentence. A reader should not need a second pass.
  - Explain a term of art the first time you use it, or drop it. Not "the value is
    not commoditised away" but "no free or bundled alternative has taken the margin".
  - NEVER name our internal machinery. No gate names, no threshold rules, no check
    vocabulary: not "the 80%+ single-controller condition is not evidenced" but "no
    passage shows a single provider holding most of this market". Not "the incumbency
    check", but the substance of what was or was not found.
  - When you rule unverifiable, name the specific thing the passages never addressed.
    "The passages do not say what these operators pay today" tells the reader what is
    missing; "unverifiable on this evidence" tells them nothing.
  - Keep every source_id. Clarity never costs a citation, a caveat, or a number.

Return ONLY valid JSON. No prose, no code fences.

Candidate: {"title": "Niche Dental Practice CRM (<3 staff)", "one_liner": "", "hypothesis": "", "who_pays": "", "why_now": "", "tags": {"price_comparables": {"anchors": [], "rejected": [], "queries": ["niche dental practice CRM staff pricing how much does it cost", "niche dental practice CRM staff one-off fee fixed price one time purchase", "niche dental practice CRM staff course OR template OR toolkit price"], "sources": [{"source_id": "e8271c959688bac6", "url": "https://dental-tech.example.com/segment-gap", "text": "Small dental practices with <3 staff are ignored by enterprise CRM vendors like Salesforce, whose minimum seat counts and implementation fees price the segment out, and no vertical incumbent serves it. Recall and reactivation workflows are tied to the clinical calendar and are not commoditised by general-purpose CRM or by any free first-party tool.", "published_at": "2024-01-01", "query": "niche dental practice CRM staff pricing how much does it cost", "fetched_at": null, "archived_url": null, "retrieved_by": "fixture"}, {"source_id": "a02fa7a54c087664", "url": "https://dental-practice-economics.example.com", "text": "Independent dental practices lose a measurable share of revenue to missed recall appointments and already pay monthly for practice-management software, so the pain is acute and paid-for today. Average practice turnover comfortably supports a software budget of several hundred pounds a month, and practices are financially stable private businesses paid directly by patients and insurers.", "published_at": "2024-02-01", "query": "niche dental practice CRM staff pricing how much does it cost", "fetched_at": null, "archived_url": null, "retrieved_by": "fixture"}, {"source_id": "5c52ec55652862f1", "url": "https://dental-associations.example.com/vendor-access", "text": "Dental associations, group-purchasing bodies and trade shows sell vendor access to member practices directly, giving a low-friction executable route to buyers that does not require a specialist salesforce. Processing patient contact details for recall is lawful under UK GDPR with the practice as controller and the software vendor as processor under a standard data-processing agreement.", "published_at": "2024-03-01", "query": "niche dental practice CRM staff pricing how much does it cost", "fetched_at": null, "archived_url": null, "retrieved_by": "fixture"}], "rationale": "No prices stated in passages. Passage [a02fa7a54c087664] mentions 'several hundred pounds a month' as market capacity, not a stated buyer price; Salesforce pricing is referenced only as 'fees' without amounts.", "provider": "claude_cli", "provisional": false, "degraded": false}}, "automatability": null, "weak_monetisation": false, "candidate_id": "d36bd5ef7d0be960", "structural_form": "", "ambition_tier": "", "market": "", "refinement_history": []}   Claims: [{"check": "value_durability", "verdict": "supported", "confidence": 0.487, "rationale": "Passages establish that small dental practices experience measurable revenue loss from missed recalls [a02fa7a54c087664], already pay monthly for solutions [a02fa7a54c087664], and that recall workflows tied to clinical calendars are neither commoditised by general-purpose CRM nor displaced by free alternatives [e8271c959688bac6], making the value real, durable, and not evaporating.", "citations": ["e8271c959688bac6", "a02fa7a54c087664"]}, {"check": "incumbency", "verdict": "supported", "confidence": 0.48, "rationale": "Passage e8271c959688bac6 explicitly states that small practices are ignored by enterprise CRM vendors (priced out by minimum seat counts) and 'no vertical incumbent serves' this segment; recall workflows are 'not commoditised by general-purpose CRM or by any free first-party tool', directly establishing that the space is underserved with no dominant incumbent.", "citations": ["e8271c959688bac6", "a02fa7a54c087664"]}, {"check": "payer_solvency", "verdict": "supported", "confidence": 0.28, "rationale": "Passage a02fa7a54c087664 establishes that dental practices are financially stable private businesses already paying several hundred pounds monthly for practice-management software, easily supporting a \u00a349.99 one-time purchase. The same passage shows they suffer acute measurable revenue loss from missed recalls, establishing both budget capacity and financial motive to pay.", "citations": ["a02fa7a54c087664"]}, {"check": "distribution", "verdict": "supported", "confidence": 0.34, "rationale": "Passage [5c52ec55652862f1] explicitly states that dental associations, group-purchasing bodies and trade shows provide a 'low-friction executable route to buyers' by selling vendor access directly to member practices, eliminating the need for a specialist salesforce; this directly establishes an existing distribution channel to the target segment.", "citations": ["5c52ec55652862f1"]}, {"check": "legality", "verdict": "supported", "confidence": 0.262, "rationale": "Passage [5c52ec55652862f1] explicitly affirms that processing patient contact details for recall is lawful under UK GDPR with the practice as controller and vendor as processor under a standard data-processing agreement. This directly establishes that the core operation\u2014CRM software for dental recall workflows\u2014can be delivered lawfully through a standard contractual mechanism.", "citations": ["5c52ec55652862f1"]}, {"check": "pain_reality", "verdict": "supported", "confidence": 0.51, "rationale": "Passage [a02fa7a54c087664] directly establishes that independent dental practices lose measurable revenue to missed recall appointments (real problem), already pay monthly for practice-management software (pain is paid-for today), and explicitly states the pain is acute. Passage [e8271c959688bac6] confirms recall workflows are not commoditised by general-purpose CRM or free tools, reinforcing that the problem has no low-cost substitute.", "citations": ["a02fa7a54c087664", "e8271c959688bac6"]}]
Axes: pain_acuity, money_provability, distribution, defensibility, build_feasibility, automatability.
THE COMPOSITE AXES, heaviest first:
- defensibility (weight 0.25): what accumulates here that a competitor starting tomorrow would not have
- pain_acuity (weight 0.20): how sharp and how frequent the pain is for a specifically named sufferer
- money_provability (weight 0.20): whether this BUYER already spends on this OUTCOME today — an adjacent invoice, staff hours, an agency or professional fee, a fine, or a paid workaround. A new solution to a job that is already funded scores HIGH; a job nobody spends anything to get done scores LOW. No public price page, quote-on-request pricing, and no direct competitor are facts about the market's disclosure, not evidence that the money is absent
- automatability (weight 0.15): how much of the work real tooling can do TODAY, not aspirationally
- distribution (weight 0.15): whether a beginner can actually reach the buyer through an open channel
- build_feasibility (weight 0.05): whether a small team can ship the first useful version
ABSENCE OF A PUBLISHED PRICE IS NOT EVIDENCE OF ABSENCE OF MONEY. Quote-on-request pricing, a
sector where no competitor lists figures, or a paid substitute aimed at a slightly different
artifact all mean the web did not disclose a number — not that the buyer does not spend. Score
what the passages show this buyer already funds for this outcome. Score LOW only when the
passages give you reason to believe nobody spends anything to get this job done.
Output ONLY: {"scores":{axis:int...}, "justification":{axis:"..."}}

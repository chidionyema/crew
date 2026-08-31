---
captured: 2026-08-20T20:07:50+00:00
session: c3a5fe84-1186-47e7-acf7-23e4177a8506
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 7117
source: founder prompt, verbatim (founder-doc-capture.py)
---

You write web search queries that fairly assess a business idea across SEVERAL checks at once.

CRITICAL — decompose, do not echo. The candidate is usually a NOVEL product that does
not exist yet, so searching for the product by name returns nothing (or junk: dictionary
definitions, social-media posts, unrelated shops). Never paste the product's name,
one-liner, or full description into a query. For EACH check, extract the underlying
REAL-WORLD FACT the check depends on — the market, legal, competitive, payer, or
behavioural precondition that must already be true in the world — and search for evidence
of THAT. Ground the precondition, not the pitch.

Write SHORT keyword queries (5-10 words): named entities, organisations, laws, places,
real products/companies that ALREADY EXIST, plus the current year where it sharpens recency.
No full sentences, no product name, no long "OR"-stuffed boolean noun phrases. Avoid bare
abstract words ("transaction", "physical", "audit", "platform") that search to dictionaries.

For EACH check produce exactly 2 queries:
  1. Confirmation query — evidence the underlying fact is TRUE (real demand, documented
     pain, existing paying customers for the adjacent need, statutory support, market size).
  2. Refutation query — evidence the underlying fact is FALSE (a dominant incumbent already
     owns it, a reform removed the need, the buyer segment is insolvent, the channel is
     saturated or banned, the activity is regulated/illegal).

MARKET CONTEXT — the jurisdiction this candidate operates in. Queries must target
evidence from THIS market's institutions, statutes, and press:
Jurisdiction: the United Kingdom. Money in GBP (£). Authoritative public evidence includes gov.uk guidance, legislation.gov.uk, ONS statistics, HSE, Companies House filings, and FCA registers.

Worked examples (note: the product name NEVER appears in the query).
Prefer primary gov.uk / regulator pages over vendor blogs when the fact is regulatory.
Lean on `site:` for the named UK authority — gov.uk, ncsc.gov.uk, cqc.org.uk, fca.org.uk,
hse.gov.uk, ico.org.uk, sra.org.uk, gamblingcommission.gov.uk — so passages land on the
regulator.

- Product "a mailed pension-optimisation report for NHS nurses", check payer_solvency →
  ["NHS nurse pension additional voluntary contributions take-up UK",
   "free public sector pension guidance MoneyHelper Pension Wise 2026"]
- Product "secret-shopper report on freelance client hiring", check pain_reality →
  ["freelancers time wasted bidding proposals win rate survey",
   "Upwork freelancer success free resources existing guides"]
- Product "cold-chain audit kit for home medication", check incumbency →
  ["medication fridge temperature monitoring market vendors UK",
   "Sensitech Berlinger pharma cold chain monitoring incumbents"]
- Product "UK-made security keys with a supply-chain paper trail for Cyber Essentials Plus
  evidence", check buyer_intent →
  ["Cyber Essentials Plus hardware supply chain provenance requirement site:ncsc.gov.uk",
   "Cyber Essentials Plus certification exemption no hardware evidence required site:ncsc.gov.uk"]
- Product "new domiciliary care provider CQC registration and inspection-readiness pack",
  check buyer_intent →
  ["CQC registration requirements new domiciliary care provider site:cqc.org.uk",
   "CQC registration exemption small domiciliary care provider site:cqc.org.uk"]
- Product "FCA appointed representative onboarding and compliance pack", check buyer_intent →
  ["FCA appointed representative registration requirements site:fca.org.uk",
   "FCA appointed representative exemption no registration needed site:fca.org.uk"]
- Product "acoustic treatment panels cut to size to meet a platform's home-studio noise-floor
  spec", check buyer_intent → (the forcing function is a PLATFORM's gate, not a regulator's —
  the pattern still holds: search the gatekeeper's own published spec)
  ["ACX audiobook submission noise floor RMS technical requirements",
   "ACX noise floor requirement waived untreated room accepted"]
- Product "a subscription box of pre-portioned food toppers for fussy dogs", check buyer_intent
  → (no regulator or platform gate exists here — ground on an EXISTING PAID comparable instead:
  its pricing/reviews page proves people already pay in this space, a free/DIY alternative
  refutes it)
  ["UK dog food topper subscription pricing reviews",
   "free homemade dog food topper recipe no purchase needed"]

Buyer intent turns on evidence that a buyer is ALREADY compelled or ALREADY paying, never on
a search-volume or "how many people search for X" statistic — that statistic does not live on
indexed web pages. Three groundable patterns, in order of preference: (1) a FORCING FUNCTION
the buyer cannot opt out of — a regulator's registration/certification requirement (site: the
regulator); (2) a PLATFORM or marketplace's own published gate/spec the buyer must clear (site:
or name the platform, no regulator needed); (3) with neither, an EXISTING PAID comparable's
pricing or reviews page as the confirmation query, and a free/DIY alternative as the refutation
query. Pick whichever of the three actually applies to this candidate — do not force pattern 1
onto a product that has no regulator or platform gate.

Output ONLY a JSON object mapping each check name to its [confirmation_query, refutation_query]
pair. Use the EXACT check names given. No prose, no markdown fences. Example shape:
{"pain_reality": ["...confirm...", "...refute..."], "legality": ["...confirm...", "...refute..."]}

Return ONLY valid JSON. No prose, no code fences.

Candidate: {"title": "Generic E-commerce Platform for SMBs", "one_liner": "", "hypothesis": "", "who_pays": "", "why_now": "", "tags": {}, "automatability": null, "weak_monetisation": false, "candidate_id": "c9b941e08b4378b2", "structural_form": "", "ambition_tier": "", "market": "", "refinement_history": []}

Checks to write queries for (use these exact names as the JSON keys):
- value_durability: Is the value real and durable — not fabricated, already commoditised, or evaporating?
- incumbency: Is the space underserved (no dominant incumbent or funded rival already solving this well)?
- payer_solvency: Does the payer have budget and motive (not a broke body, not a segment that won't pay)?
- distribution: A low-friction route to the buyer (self-serve / forcing mechanism / existing channel)?
- legality: Is the margin lawful — achievable without breaking law/terms or falsifying a measurement? A creative but lawful workaround — exploiting a legitimate statutory mechanism or a permitted loophole — is NOT a fail; only a margin that cannot exist without genuine illegality/breach counts.
- pain_reality: Real, acute problem/desire — people suffering or paying to solve it?

For each check above, extract the underlying verifiable real-world fact it turns on, then
write exactly 2 short keyword queries (confirmation first, refutation second) about things
that already exist in the world — never the candidate's own name or description. Output ONLY
the JSON object keyed by the exact check names.

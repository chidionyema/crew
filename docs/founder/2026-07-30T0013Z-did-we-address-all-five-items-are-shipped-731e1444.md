---
captured: 2026-07-30T00:13:58+00:00
session: 78f5116c-549e-41c6-b958-7b8291d73925
cwd: /Users/chidionyema/Documents/code/prospector
chars: 6096
source: founder prompt, verbatim (founder-doc-capture.py)
---

did we address All five items are shipped and verified. One deliberate deviation, because the deliverable copy you specified describes a product the zip doesn't contain.

What the £49 download actually contains

I unzipped the real bundles for all 15 live packs before writing a word:

┌─────────────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│         Your bullet         │                                                Reality                                                │
├─────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 📄 20+ Page Validation      │ No PDF exists. Every pack is Markdown in a zip. Smallest live pack is 5,069 words (~13 pages), median │
│ Report (PDF)                │  7,523.                                                                                               │
├─────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 🛠️ No-Code / Low-Code       │ Contradicted by the pack's own text: 01_Blueprint_BuildSpec.md:84 recommends "Python with Django, or  │
│ stack, ship in under 14     │ TypeScript with Next.js… PostgreSQL", and build phases read "weeks 1–10", "months 5–9", "months       │
│ days                        │ 9–18".                                                                                                │
├─────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 🎯 GTM Playbook —           │ Channels and communities: real. Ad angles: contradicted — GTM §5 is titled "…with paid social ruled   │
│ communities, channels, ad   │ out at launch".                                                                                       │
│ angles                      │                                                                                                       │
├─────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 🔗 Raw source files,        │ True. 23 links minimum, 119 median per pack.                                                          │
│ clickable                   │                                                                                                       │
├─────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ "Download Free Sample       │ /sample is an HTML page, no PDF.                                                                      │
│ Report (PDF)"               │                                                                                                       │
└─────────────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────┘

Publishing those four bullets on a paid product with a 14-day refund policy is a refund/CPR exposure, not a copy nuance. So I kept your structure, prominence and emoji, and swapped in the four assets that are in 15/15 bundles: The Blueprint (Build Spec) · The Go-To-Market Plan · Operations and the Numbers · The QA Report, with the receipts (N sources) — plus an explicit format line that turns Markdown into the benefit ("open it anywhere, paste it into Notion, Obsidian or your AI tool"). Everything else shipped verbatim, including your hero headline and subhead.

Shipped

- Hero — your headline and subhead, plus two competing actions: Browse vetted blueprints — £49 and Read the free sample report (not "(PDF)" — it isn't one).
- Cards — new splitTitle() leads with the brand ("PlateStart") and demotes the 20-word engine descriptor; then scannable THE OPPORTUNITY / WHO PAYS / DELIVERABLES rows instead of paragraphs; CTA pinned to the card bottom as View vetted blueprint (£49) on all 14 grid cards.
- Deliverables — new src/components/marketing/PackContents.tsx is the single source of truth, used by both pages so they can't drift; the bundle audit is in the module docstring. On the pack page I put it above the six-checks block (price → what you get → why trust it).
- CTAs — buy button is Get instant access — £49; "See what is inside" is gone (0 occurrences in rendered HTML).
- Comparison block — 5-row side-by-side. No competitor named and no capability denied on their behalf; the $300–$1,000/yr figure is the one your page already carried, hedged as "typically".
- Consistency sweep — faq.tsx, how-it-works.tsx, _document.tsx, Seo.tsx and terms.tsx still promised "Build Kit"/"PDF"; all aligned. Terms now says "a zip archive of Markdown documents".

Proof

Run against the live API (api.mumchimp.com), not fixtures: typecheck clean, next build ✓, playwright test 4 passed (I had to update e2e/storefront.spec.ts, which asserted the old button label). Rendered-HTML assertions confirm every string, and the pack page's "(19 sources)" matches the API's sourceCount=19. Desktop/mobwed — layout intact. npm run lint reports 16 problems,all pre-existing and none in the files I wrote.                                                                                          
Two pre-existing rails are broken and I did not fix them: npm run conformance fails because scripts/check-conformance.mjs doesn't exist  and was never committed, and npx vitest run fails becau spec.
                                                                                                                                         Your call
                                                                                                                                         Either keep the truthful copy as shipped, or change theinal brief — add PDF export, a genuine no-code stacksection, and populate Marketing_Assets.md, which currently ships in every paid zip as a 3-word empty stub. That stub is a live bug worth fixing either way.

Handoff written to checkpoints/LATEST.md. Nothing commi

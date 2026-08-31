---
captured: 2026-08-01T09:11:30+00:00
session: e62a24f4-1f4f-4192-a76a-662fa5229b58
cwd: /Users/chidionyema/Documents/code/prospector
chars: 5428
source: founder prompt, verbatim (founder-doc-capture.py)
---

can you review suggestions annd address Here is the comprehensive design and UX feedback translated into a professional Agile Epic with actionable User Stories and Acceptance Criteria (AC).

Since you requested no CMS requirements for now, this is scoped entirely as frontend UI, UX, and state-management work.

Epic: World-Class Discovery & Guided Matchmaking

Epic Description: Transition the Mumchimp platform from a basic database filtering experience to a premium, guided matchmaking service. By upgrading terminology, refining the UI layout, and introducing a prescriptive "Matchmaker" wizard, we will build user trust and justify the Â£49 price point before the user even opens a dossier.

Target Persona: The UK-based prospective entrepreneur or gig-worker looking for a vetted, realistic business model to invest their time and money into.

User Story 1: Professional Filter Terminology

As a prospective buyer, I want to see industry-standard, professional terminology in the filter panel, So that I feel confident I am browsing a premium, stress-tested business intelligence platform rather than a casual blog.

Acceptance Criteria:

Update Filter 1: Rename "Skills you already have" to "Founder Skillset" (Options: Technical, Sales & BizDev, Operational, Creative, Domain Expertise).
Update Filter 2: Rename "Hours it needs from you" to "Time Commitment" (Options: Weekend Project [1-5 hrs], Side Hustle [5-15 hrs], Half-Time [15-30 hrs], Full-Time Enterprise [40+ hrs]).
Update Filter 3: Rename "Who the customer is" to "Target Market" (Options: B2B, B2C, B2G, Prosumer).
Update Filter 4: Rename "How much is automated" to "Tech Enablement" (Options: Fully Automated, Hybrid, Manual).
Update Filter 5: Rename "How it makes money" to "Revenue Model" (Options: One-off Fee, Monthly Retainer, SaaS Subscription, Commission, Arbitrage).
Update Filter 6: Rename "Sector it serves" to "Industry Vertical" (Use UK-specific terms: Property & Real Estate, FMCG, Trades & Construction, etc.).
User Story 2: Progressive Disclosure & "Pill" UI

As a mobile or desktop user, I want to interact with a clean, instantly responsive filter panel without feeling overwhelmed by choices, So that I can easily narrow down 47+ blueprints to the ones that fit my criteria.

Acceptance Criteria:

Progressive Disclosure: On page load, only the top 3 most critical filters (Time Commitment, Revenue Model, Founder Skillset) are expanded. The remaining filters are collapsed under a smooth accordion toggle (+ icon).
Visual Pills: For categories with 3 or fewer options (e.g., Target Market: B2B / B2C), replace standard HTML checkboxes with tap-friendly, stylised "pill" buttons.
Instant UI Updates: Filtering must happen client-side (e.g., via React state). The grid of 47 packs must instantly animate and filter the exact millisecond a pill/checkbox is toggled, with no page reload.
User Story 3: Intelligent Zero-State Handling

As a user who selects a highly specific combination of filters, I want to be guided toward alternative options if my exact search yields zero results, So that I do not hit a dead-end blank screen and leave the website.

Acceptance Criteria:

No Blank Screens: If a filter combination results in 0 blueprints, trigger the Zero-State UI.
Alternative Recommendations: Display a friendly message: "We don't have a blueprint that matches this exact combination yet. However, here are 3 blueprints that closely match your criteria if you are willing to change [Variable, e.g., 'Tech Enablement'].".
Fallback Display: Render the top 3 closest matching blueprint cards below the message to keep the user engaged.
User Story 4: The UK "Moat / Regulatory" Filter

As a UK-based entrepreneur, I want to filter businesses based on their barrier to entry, So that I can find resilient business models that leverage my specific knowledge of UK red tape (e.g., HMRC, DWP, DVSA).

Acceptance Criteria:

New Filter Category: Add a new filter titled "Moat Type" (or "Barrier to Entry").
Filter Options: Include checkboxes for: [Regulatory Knowledge], [Tech Complexity], and [Sales Hustle].
Tagging: Ensure blueprints like DLAChild or IHT Valuation Barometer are explicitly tagged with the Regulatory Knowledge moat on their respective UI cards.
User Story 5: "Find My Blueprint" Guided Matchmaker

As a user who doesn't know exactly what to look for, I want to answer a few simple questions about my goals, So that the platform does the heavy lifting and prescribes the exact business blueprint I should buy.

Acceptance Criteria:

Prominent Entry Point: Place a high-visibility button above the blueprint grid stating: "Not sure where to start? Take the 30-second matchmaker."
Wizard UI: When clicked, open a clean, 1-question-per-screen modal (similar to Typeform).
Step 1: Ask: "What is your realistic starting budget?" (Options: Under Â£500 / Â£500 - Â£2k / Â£2k+).
Step 2: Ask: "How are you approaching this?" (Options: I have a 9-to-5, need a side hustle / I want to build a full-time replacement / I just want passive income).
Step 3: Ask: "What is your unfair advantage?" (Options: I can sell to anyone / I can build software / I am highly organized / I know a specific industry inside out).
The Reveal: Display a loading spinner for 1-2 seconds for dramatic effect, then transition to a results view: "Based on your profile, we have stress-tested these blueprints for you." displaying 1 to 3 perfectly matched cards.

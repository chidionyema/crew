---
captured: 2026-08-15T22:50:39+00:00
session: 0c5421cf-3f28-415a-99ac-a6381ae54271
cwd: /Users/chidionyema/Documents/code/prospector
chars: 20025
source: founder prompt, verbatim (founder-doc-capture.py)
---

# Mumchimp — site-wide copy pass

Pages covered: home, /how-it-works, /about, /kill-log, /faq. (/sample is covered in the separate file.) Rule numbers refer to the house writing spec.

**Read Part Zero first.** It is not a copy problem, but it is the most serious thing on the site and it makes the copy work pointless if left alone.

---

# PART ZERO — THE NUMBERS DO NOT AGREE

Four different figures for the same facts are live across five pages right now.

| Claim | Home | /how-it-works | /about | /kill-log | Footer |
|---|---|---|---|---|---|
| Ideas researched | 1,444 | 1,444 | 1,313 implied | 1,168 | 1,444 |
| Ideas killed | 1,364 | 1,364 | 1,168 | 1,168 | 1,364 |
| Packs published | 59 | — | 145 | 145 | — |
| Rejection rate | — | 94.5% | — | 89% | — |

Further internal breaks:

- **/kill-log meta description** says 1,168 researched and 89% rejected. 89% of 1,168 is 1,040, not 1,168. The page headline says 1,168 were killed *to publish 145*, which makes the research total 1,313. Three numbers, none reconcilable.
- **/about** and **/kill-log** claim 145 packs on the shelf. The catalogue shows 59.
- **Home** says 1,444 researched and 1,364 killed, leaving 80 survivors, then lists 59 packs. The gap is never explained.
- **Home** says "48 UK packs · 11 US packs · 59 in total". Earlier catalogue states showed a third region group (US · FL). Either the group was dropped or the total is stale.
- **Home** says "Show the other 35 UK packs" against 48 UK packs and 4 shown.
- **Home** says "arrives as 5 files" then lists six files.
- **Home** says "Same 9 documents in every pack". **/sample** says "3 of 14 sections" and "Three sections of 14".
- **/how-it-works** headline says "Six checks, in order". The worked example directly above it shows nine.
- **/faq** says a pack is "four parts" delivered as "one zip of plain Markdown files". Home says nine documents delivered as HTML, PDF, CSV, TXT and JSON-LD.

**Why this outranks every prose fix:** the product's entire proposition is that nothing here is unsourced or invented. A reader who notices two different kill counts has been handed a reason to disbelieve the checks, and that reader is exactly the sceptical buyer the copy is written for.

**Action:** every number on the site comes from one source of truth at build time. No number is hard-coded in copy. Where a figure appears in prose, it is a template variable. Do this before any copy edit ships.

---

# PART ONE — HOME

## 1.1 Meta description

**Rule breaks:** R1, R2, R9 ("the engine")

**Before**
> Mumchimp sells sourced business opportunity packs. Each is an idea passed by the engine: build spec, GTM plan, operations and unit economics, and a QA report with every claim sourced. Instant download.

**After**
> Mumchimp sells researched business ideas. Each one survived checks designed to kill it. You get the build spec, the go-to-market plan, the numbers and a source behind every claim. Instant download.

"GTM" and "unit economics" are jargon for the buyer this site describes — a tradesperson or a solo operator, not a VC associate. "The engine" is unexplained on first contact.

## 1.2 Hero subheading

**Before**
> The buyer, the price, the margins and the plan, put through an AI built to kill the idea first.

**After** — no change. 20 words, concrete, active. This is the best sentence on the site.

## 1.3 Secondary CTA

**Rule break:** a button is not a sentence

**Before**
> Read a full pack free, no email needed.

**After**
> Read a full pack, free

Move "No email, no card" to the line beneath, where the same reassurance already appears elsewhere on the page.

## 1.4 "What survived" subhead

**Rule break:** R3 — two unrelated claims in one line

**Before**
> Same 9 documents in every pack. Bigger opportunity, higher price. Why prices differ

**After**
> Every pack has the same 9 documents. Price tracks the size of the opportunity — [why prices differ].

Also: confirm 9 is correct against /sample's 14. One of them is wrong.

## 1.5 The file manifest

**Rule break:** count mismatch

**Before**
> arrives as 5 files

**After**
> arrives as 6 files

Or cut one file from the list. Six are listed.

## 1.6 Manifest closing paragraph

**Rule breaks:** R1 (44 words), R2

**Before**
> 9 documents, 5,000+ words, as a web page you can read, a PDF you can print and a spreadsheet you can open. Yours to keep, edit, or paste anywhere. No login, no subscription.

**After**
> 9 documents, 5,000+ words. A web page to read, a PDF to print, a spreadsheet to open. Yours to keep, edit or paste anywhere. No login, no subscription.

## 1.7 The REFUTED block

**Rule breaks:** R1 (57 words), R2, R9 ("value proposition", "landscape", "commoditized"), US spelling

This is generated content and will recur across packs. Listed here because it is on the homepage, where it is the first prose a sceptical buyer reads closely.

**Before**
> The market for new-build snagging inspections is already highly commoditized and served by established, accredited firms that provide the exact services proposed (thermal imaging, fixed-fee reports, drone inspections). The core value proposition of a 'proprietary checklist' is invalidated, as competitors already align their inspections with industry-standard benchmarks like NHQB and NHBC guidelines. Furthermore, potential customers prioritize RPSA accreditation and insurance, creating high barriers to entry for a new solo operator attempting to compete on price alone in an already fixed-price, transparently-marketed landscape.

**After**
> Accredited firms already sell new-build snagging inspections, including thermal imaging, fixed-fee reports and drone surveys. They inspect against the same NHQB and NHBC benchmarks the idea claimed as its own checklist. Buyers ask for RPSA accreditation and insurance, which a new solo operator would not have. Competing on price alone, in a market that already publishes its prices, leaves nothing to win on.

Four sentences from three. "Commoditized", "prioritize" — the site is `en_GB`. Set the spelling in the generation prompt and add a Vale rule.

## 1.8 The pull quote

**Rule break:** two unrelated lines presented as one quote

**Before**
> "The homeowner can hire a structural engineer (e.g., £500-1000 per inspection) or rely on the warranty provider's own surveyor (often free but superficial).
> What people pay for this problem today."

**After** — separate them. The second line is a caption, not part of the quote. Also replace "e.g.," with "around", and set the range as £500–£1,000 with the en dash and the second currency symbol.

## 1.9 "Every idea walks into a room built to destroy it"

**After** — no change. Keep exactly as is.

---

# PART TWO — /HOW-IT-WORKS

## 2.1 Meta description

**Rule breaks:** R1, R2

**Before**
> How Mumchimp works: every pack is a sourced business opportunity, vetted against checks built to kill it and sourced to retrievable evidence before it can be listed.

**After**
> How Mumchimp works. Every idea faces checks designed to kill it, and nothing reaches the shelf unless the evidence against it failed to land.

## 2.2 Intro

**Rule break:** R1 (30 words), colon splice

**Before**
> Before anything reaches the store, it faces the checks: AI agents that each hunt for the reason it fails. Here is exactly how an idea earns its place.

**After**
> Before anything reaches the store it faces the checks. Each one is an AI agent hunting for the reason the idea fails. Here is how an idea earns its place.

## 2.3 The check-count contradiction

**Rule break:** factual

The worked example above shows **9 checks**. The heading below it reads:

> Six checks, in order. One hard fail and it stops.

Then the qualifier: "Some ideas face more checks; each pack page names its own." The qualifier arrives after the contradiction has already registered.

**After**
> Six checks every idea faces. Some face more.
>
> One hard fail and it stops. The example above faced nine, and each pack page names its own. Every kill is logged with its reason, so the filter is auditable rather than a black box.

## 2.4 The methodology paragraph

**Rule breaks:** R1 (58 words), R2, R4

**Before**
> The research is AI-led and automated: the checks below are run by AI agents, each instructed to rule only on passages it fetched from the open web, and the sources they used are published with the verdict so you can hold the reasoning against them yourself. A person reviews that record before the pack reaches the shelf.

**After**
> The research is automated. Each check is run by an AI agent that may rule only on passages it fetched from the open web. The sources are published alongside the verdict, so you can hold the reasoning against them yourself. A person reviews the record before the pack reaches the shelf.

## 2.5 Check names differ from /about

/how-it-works: Real pain · Lasting value · Room past the incumbents · A payer who can pay · A route to the buyer · No legal landmine

/about: Real demand · Lasting value · Room past the incumbents · Someone will pay · A route to the buyer · No legal landmine

Two of six differ. Pick one set and use it everywhere, including in pack pages and the kill-log filter labels. Recommended: **/how-it-works** wording — "Real pain" and "A payer who can pay" are more concrete than "Real demand" and "Someone will pay".

## 2.6 Truncated kill excerpts

Three of the six kill cards open mid-sentence:

> "7M+ jobs, 3300+ skills) that funnel freelancers into finding and bidding on work…"

> "5%, and the only other relevant note describes UK hospitality businesses as struggling…"

An orphan closing bracket and a bare percentage sign are visible on the page. The excerpt is being cut from the front rather than the back. Fix the truncation to start at a sentence boundary, and clamp from the end with an ellipsis.

## 2.7 "Then a second wave of agents attacks the survivor"

**After** — no change. Strongest section on the page.

## 2.8 "Then a person reviews it"

**Rule breaks:** R1 (47 words in the first sentence), R2

**Before**
> The finding, the checking and the sourcing are automated, and that is the point: it is how every idea gets the same treatment instead of the handful a person could read. But nothing reaches the shelf on its own.

**After**
> The finding, the checking and the sourcing are automated. That is the point: every idea gets the same treatment, instead of the handful a person could read. But nothing reaches the shelf on its own.

## 2.9 "The honest limits"

**After** — no change. Keep.

---

# PART THREE — /ABOUT

This page is the weakest on the site. It contradicts the others on numbers, and it leaks internal brand-guideline language into public copy.

## 3.1 Meta description

**Rule break:** factual

**Before**
> How Mumchimp works: an engine that tries to kill every business idea on cited evidence. 1168 killed, 145 survived.

**After**
> How Mumchimp works. An engine that tries to kill every business idea on cited evidence. [X] killed, [Y] on the shelf.

Template variables. Never hard-code.

## 3.2 Opening paragraph

**Rule breaks:** R1, R2, R7, awkward relative clause

**Before**
> Mumchimp is an engine that runs business ideas through a gauntlet of brutal checks. The ones that die on the first front where cited evidence is found against them are not listed. The ones that survive are the Mumchimp packs. Right now the kill count is 1,168 and the survivors are 145.

**After**
> Mumchimp runs business ideas through checks designed to kill them. An idea dies at the first check where the evidence goes against it, and a dead idea is never listed. The survivors become packs. [X] have been killed so far. [Y] are on the shelf.

## 3.3 "The voice is source-or-die"

**Rule break:** internal style guide published as customer-facing copy

**Before**
> The voice is source-or-die. Sourced, not sold. Refutational, not promotional. If a claim has no source, it is not in a pack. If an idea cannot survive the filter, it is not on the shelf.

**After**
> If a claim has no source, it is not in a pack. If an idea cannot survive the filter, it is not on the shelf.

The first three sentences are a brief written for a copywriter, not a statement to a reader. The two that remain say the same thing and say it as a promise rather than as a positioning note.

## 3.4 "Six fronts are common to every idea"

**Rule breaks:** R1 (43 words), R2

**Before**
> Six fronts are common to every idea. Some face more: a small side-business idea is also tested on whether buyers are actively searching, whether the trend is still current, and whether its claims can be checked.

**After**
> Six checks are common to every idea. Some face more. A small side-business idea is also tested on whether buyers are searching, whether the trend is current, and whether its own claims survive checking.

Note "fronts" here vs "checks" on /how-it-works. Standardise on **checks**.

## 3.5 "What a pack actually is"

**Rule breaks:** R1 (39 words), R2, contradicts /faq and home

**Before**
> A build spec, a go-to-market plan, an operations playbook and a QA report, with a citation behind every claim and a date stamped at publish. Yours outright: no login, no dashboard, no subscription, and plain text files you can open anywhere.

**After**
> Nine documents: the build spec, the go-to-market plan, the operations playbook, the numbers, and a QA report with a citation behind every claim. Each one is dated at publication. Yours outright — no login, no dashboard, no subscription.

"Plain text files you can open anywhere" contradicts the home page's file manifest. Cut it or align it.

## 3.6 "The same rigour that produced the catalogue produced it"

**Rule break:** circular, says nothing

**Cut.** The preceding sentence already offers the free sample.

## 3.7 "Who makes this"

The footer links to /about under the label "Who makes this". The page never says who makes it. Either add a short paragraph naming the operation, or relabel the footer link to "About".

For a site whose product is trust in a research process, a named human is worth more than any copy change on this page.

---

# PART FOUR — /KILL-LOG

The best-written page on the site. Three fixes.

## 4.1 Meta description

**Rule break:** arithmetic

**Before**
> We researched 1168 business ideas and rejected 89% of them. Here are the rejects, with the evidence that killed each one.

**After**
> We researched [X] business ideas and rejected [Y]%. Here are the rejects, with the evidence that killed each one.

Also format thousands with a comma. "1168" appears bare here and as "1,168" on the page.

## 4.2 Opening paragraph

**Rule breaks:** R1 (43 words), R2

**Before**
> Anyone can claim their research is rigorous. This is the receipt. Every idea below was generated, researched against live sources, and then shot, with the argument that killed it and, where a page was cited, a link so you can check it yourself.

**After**
> Anyone can claim their research is rigorous. This is the receipt. Every idea below was generated, researched against live sources, and then shot. Each carries the argument that killed it, and a link to the page where one was cited.

Keep "shot". It is the right word and it is the site's voice.

## 4.3 The closing note

**Rule breaks:** comma splice, R2

**Before**
> This is a sample of the log, not all 1,168 kills. Rejections whose only reason was a score below the bar are left out, they are true, and they tell you nothing. What you see here is every kill that came with an argument.

**After**
> This is a sample of the log, not all [X] kills. Rejections whose only reason was a score below the bar are left out. They are true, and they tell you nothing. What you see here is every kill that came with an argument.

## 4.4 Generated kill summaries

Same defects as every other generated block: 60-word sentences, semicolons, four-item lists, and orphan artefacts. Several entries contain raw internal IDs that have leaked into published prose:

> "Passages 9fa810377aee4d8f and 10481947a354f7f9 directly show…"

> "…already servicing deductions from the"

> "Multiple passages (,,,,) show that state bars actively prosecute…"

> "…satisfying the incumbency refutation threshold."

Four separate bugs: internal passage IDs rendered to the reader, sentences truncated mid-clause, empty citation parentheses, and internal scoring vocabulary ("refutation threshold", "hard gate", "candidate") surfacing in customer-facing text.

**Add to the writing-stage prompt:** never refer to a passage by ID, never use the words *candidate*, *hypothesis*, *threshold*, *hard gate*, or *passage* in output prose. Refer to the idea by name and to sources by publication.

**Add to the linter:** flag any 16-character hexadecimal string, any empty parenthesis group, and any body text ending without terminal punctuation.

---

# PART FIVE — /FAQ

Only the first answer is in the served HTML; the rest are behind an accordion. Fix what is visible, then apply the same treatment to the remaining answers.

## 5.1 "What am I actually buying?"

**Rule breaks:** R1 (54 words), R2, R4, contradicts home and /about

**Before**
> A pack: a grounded business opportunity dossier in four parts, a build spec, a go to market plan, an operations and financial model, and a QA report with a clickable source behind every claim. It arrives as one zip of plain Markdown files, 5,000+ words, yours to read and build from as soon as payment clears. Packs are priced individually and the price is shown on every pack page; whichever you pick it is one payment, with no subscription.

**After**
> A pack: nine documents on one business idea, 5,000+ words, with a clickable source behind every claim. It covers what to build, who buys it, what it costs to run, and what the checks found. It downloads as soon as payment clears. Prices are shown on each pack page. Whichever you pick, it is one payment and there is no subscription.

Three contradictions resolved: "four parts" becomes nine documents; "one zip of plain Markdown files" becomes the actual delivery format; the semicolon goes.

## 5.2 "grounded"

The word appears in the question "What makes a pack 'grounded'?" and in the footer disclaimer, but nowhere else on the site — the rest of the site says *sourced*. Standardise on **sourced** and rewrite the question as "What does 'sourced' actually mean here?"

## 5.3 Footer disclaimer differs between templates

Home and /sample:
> Mumchimp packs are sold for information only…

/faq, /about, /kill-log:
> Mumchimp packs are digital research products sold for information only…

Same disclaimer, two versions, two templates. Pick one and put it in a shared component. This is a legal notice — it should not vary by page.

## 5.4 Nav label differs between templates

Home, /sample, /how-it-works use **Categories · How it works · Kill log · FAQ**. /faq, /about, /kill-log add **Catalog** — US spelling, on an `en_GB` site, where the same link is labelled "Catalogue" in the footer.

Change to **Catalogue** and make the nav a shared component.

---

# PART SIX — NOT COVERED

These pages were not reachable in this pass. Same treatment needed:

- /ideas (categories)
- /pricing (linked from home as "Why prices differ")
- /terms, /privacy, /refund
- Individual pack pages — the largest surface by volume, and entirely generated

---

# PRIORITY ORDER

1. **Reconcile the numbers.** One source of truth, template variables, no hard-coded figures. Everything else is cosmetic until this is done.
2. **Fix the leaked internals** in kill-log summaries — passage IDs, empty parens, mid-clause truncation, scoring vocabulary.
3. **Shared components** for nav, footer and disclaimer. Three of these are currently forked.
4. **Standardise the vocabulary:** checks (not fronts), sourced (not grounded), Catalogue (not Catalog), en-GB spelling throughout.
5. **Then** the sentence-level rewrites above.
6. **Then** the generator, which is what stops all of this coming back with the next pack.

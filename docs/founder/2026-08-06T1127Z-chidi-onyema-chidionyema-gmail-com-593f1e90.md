---
captured: 2026-08-06T11:27:29+00:00
session: 178a5226-1096-423f-92b1-b50e1939b242
cwd: /Users/chidionyema/Documents/code/prospector
chars: 16532
source: founder prompt, verbatim (founder-doc-capture.py)
---

chidi onyema <chidionyema@gmail.com>
11:34 AM (52 minutes ago)
to chidi

I read every page’s rendered markup (home, /ideas + a category page, a pack page, /how-it-works, /kill-log, /sample, /faq, /about). One caveat up front: I can see structure, copy and DOM, not pixels — so this is IA, content-design and interaction critique, not a colour/type pass. Happy to do the visual layer if you drop screenshots.

1. The numbers contradict each other, on a site whose entire product is “we don’t invent numbers”

This is the highest-severity issue by a distance. A sceptical buyer — the exact persona you’re courting — will find these in 90 seconds:

Claim

Where

Conflicts with

“63 packs to choose from”

Home hero

“Showing 13 of 52” + “Show the other 39 packs” (= 52) on the same page

“1,168 killed · 145 survived”

Home, /about, /kill-log

Catalogue only exposes 63. Where are the other 82? The kill-log CTA literally says “Browse the 145 that survived” and lands on a 63-pack grid

“We researched 1168 business ideas and rejected 89%”

/kill-log meta description

/how-it-works says “Of 1,313 ideas researched, 145 survived”. 1,168 is the kill count, not the researched count

“The kill log has every one, with the sourced reason why”

Home

/kill-log bottom: “This is a sample of the log, not all 1,168 kills”

“29 sources · 6/6 checks”

Pack page header

Same page: “2 of them, open any of these now… The other 27 are cited inside the pack”

Actions:

Pick one canonical set of counters, compute them from one source of truth, and render them everywhere from that. researched = killed + survived should be an invariant, not three hand-written strings.
Reconcile 145 vs 63. If 82 survivors aren’t listed yet, say so explicitly (“145 survived; 63 are published, the rest are in production”) — that’s more on-brand than the silent gap.
Move “this is a sample of the log” to the top of /kill-log, and change the homepage line from “has every one” to “has every kill that came with an argument”. You’re currently overclaiming on the one page whose job is to prove you don’t overclaim.
2. Homepage / catalogue

Three competing totals on one screen (63 / 52 / 13-of-52). Fix per above.
The first card is duplicated. “Newest on the shelf” shows the recycling-boards pack, then “Newest survivors” immediately below opens with the same pack. Kill the hero card or exclude it from the grid.
Card anatomy is inconsistent. Some cards lead with a category label (“Housing and tenancy”), some with an initials monogram (“R RateRebase”, “HW”, “SF”), some with neither. It reads as a fallback firing when the category is missing. Pick one: category chip always, monogram never (or monogram only when there’s no thumbnail).
Two naming systems in one grid. “Write challenge letters when a council cuts care hours” sits next to “SwarmHold” and “GuyLine”. Brand names tell a browsing user nothing; descriptive titles are scannable. Standardise on BrandName — plain-English what it does, which is what your category pages already do. Right now the same pack has different names on / and on /ideas/vertical-software-ideas.
Truncation has no rule. Some descriptions clip at ~120 chars with “…”, others run 60+ words (“PitchCall Forensics”, “SailCert”). Uneven card heights and a ragged grid. Hard-cap to one line at a fixed character count and put the long version on the pack page.
The catalogue has a sort but no filters. You have rich facets — price, market (UK/US), B2B/B2C, automation level, skill fit, source count, category — and none of them are on the grid. This is the single biggest conversion improvement available. 63 items with only “Newest” is a scroll, not a shop.
The US section should be a filter, not a segregated carousel. “Written for US rules” as a 1 of 3 carousel with no visible controls buries 11 packs and creates the badge-ordering mess (“GCFor US rules”, “SFor US rules”). Make Market a filter chip on the main grid with a persistent US badge on the card.
The skills quiz is in the wrong place. “What skills do you bring? / Suits builders 25…” sits below the entire catalogue, after the user has already scrolled 63 cards. It’s a filter wearing a quiz costume. Move it above the grid as an optional narrowing step, or make it a first-visit interstitial — not a post-scroll afterthought.
Pricing rationale arrives too late. Cards show £29–£199 with no explanation; the “price follows the size of the opportunity” line is far below the fold. Put a one-tap “why prices differ” affordance next to the price on the card or at the top of the grid.
⌘K is shown unconditionally — wrong on mobile and on Windows. Detect platform, or just render a search field on touch devices.
3. Pack page (the money page)

Broken share links. x.com/intent/tweet?…&url= and linkedin.com/sharing/share-offsite/?url= both have an empty url param. Anyone sharing a pack shares nothing. Straight bug.
The description renders twice, verbatim, directly under the H1. Delete one.
You promise scores you don’t show. Copy says “the scores below show where this pack’s case is strong and where it is thin” — then lists six unscored bullets. Meanwhile /sample does show scored bars (Pain acuity 4/5, Defensibility 2/5). Port the sample’s scored bars onto every pack page. Showing a 2/5 is the most persuasive thing on your entire site and you’re only doing it on the free page.
The same 57% stat appears four times on one page (pull-quote, TOC preview, “A look inside”, receipts). Repetition reads as thin evidence, not depth. Show three different claims across the three slots.
“29 sources” but 2 are clickable. Reasonable paywall, badly framed. Reframe as “3 of 29 sources unlocked” with the remaining domains listed greyed but visible — showing the domain names without the claims proves breadth without giving away the research.
“Verified last month” on a £49 product invites “is this stale?”. Show the absolute date, and state a re-verification policy (“re-checked every 90 days”) — or your relative dates become a liability as the catalogue ages.
Three buy CTAs (top card, bottom card, sticky bar) is one too many. Drop the bottom static repeat, keep the sticky.
“Is this for you?” currently answers with two attribute chips and a paragraph about who pays. Make it answer the actual question: hours/week, skills needed, capital required, time to first revenue.
4. Kill log

Truncated mid-word, repeatedly. “…making the margin as described impossible without violati”, “…creating a gap where the candidate”, “…the candidate’s own hypothesis c”. Dozens of entries end mid-sentence with no ellipsis and no expand control. On your credibility page this reads as broken, not concise. Add a clean clamp + “read the full argument” disclosure.
Some kills have zero source links (“The Planning Objection API”, “WEP Watch”, “BackMile”). The page’s promise is “with the sourced reason why”. Either surface the sources or badge those entries honestly (“argument recorded, sources not published”).
60 dense entries, no pagination, no search, no sort. Add a search box and sort-by-gate/date. Also expose the killed-idea name as an anchor link so people can cite specific kills — that’s shareable proof and free SEO.
The filter chips (“All 60”) conflict with the headline’s 1,168. Label them “60 published kills” so the chip and the headline agree.
5. /ideas (categories)

The bubble/node viz has clipped labels: “Busin…23 packs”, “Busine…30 packs”, “Busi…14 packs”. Four categories start with “Business ideas…” and truncate to indistinguishable stubs. It’s decorative but actively unusable. Either shorten the display labels (“B2B”, “B2C”, “Evenings”, “Part-time”) or drop the viz on mobile and keep the list below, which already works well.
“63 researched packs across 16 categories” then counts summing to ~280 — because tags overlap. Say “packs can appear in several categories” once, near the counts.
Category descriptions are genuinely good (the vertical-software intro is the best copy on the site). Consider promoting that voice to the catalogue’s empty/filtered states.
6. FAQ, About, trust and legal

FAQ collapses everything but the first item. Twelve accordions plus four category filters is double navigation for a page whose content is short. Expand all by default; keep the filters.
“Was this helpful? Yes/No” on every answer adds noise and implies a feedback loop you probably aren’t acting on. Drop it or put one at the page bottom.
No human, no company, no address, anywhere. The footer link says “Who makes this” and /about names an engine, not a person. You’re selling a £149 digital product to UK consumers under a distance-selling regime that expects trader identity and a geographic address, and your whole positioning is “trust us, we don’t hide things”. Add a named founder, company number, registered address, and a line on VAT. This is simultaneously your biggest legal gap and your biggest trust unlock.
“Account” in the nav contradicts the FAQ, which promises “no login, no dashboard”. Either explain what the account is for (re-download access) or move it out of primary nav into the footer/order-confirmation flow.
Four names for one asset: “free sample” / “Read a full pack free” / “Report #00” / “the free report”. Pick one. I’d keep Report #00 as the name and “Read it free” as the CTA everywhere.
7. Cross-cutting

Logo alt text is duplicated — screen readers announce “Mumchimp Mumchimp” in header and footer. Set the image alt="" when adjacent text already says it.
UK/US spelling drifts: nav says “Catalog”, body says “catalogue”, og:locale is en_GB. Standardise on catalogue.
/sample reuses the homepage meta description verbatim — wrong for SEO and for the share preview, and its og:image is the generic og.png with a mismatched alt. Every page except pack pages shares one OG image; the pack pages already have dynamic ones, so extend that generator to /sample and /kill-log.
The newsletter block ships identical copy on home, /kill-log and /sample. Fine, but the form reads “Email me if a pack survives” as both label and button (“Email me” / “Tell me when one survives” differ across pages). One label, one button string, consistently.
If I could only fix six things this week

Reconcile every counter (63/52/145/1,168/1,313) from one source of truth.
Fix the “kill log has every one” vs “this is a sample” contradiction — move the caveat to the top.
Fix the empty url= on both share links.
Add filters (price, market, B2B/B2C, automation, skill) to the catalogue grid.
Put the scored bars from /sample onto every pack page — including the low scores.
Name a human, a company and an address.
The strategic read: your product is epistemic rigour, so every internal inconsistency costs disproportionately more than it would on a normal storefront. The site’s best assets — the kill log, the scored weak bars, the unresolved objection on the free sample — are exactly right and I’d lean harder into them. The gaps are almost all execution hygiene, not concept.


Still working from markup, not pixels — so the visual half below is direction and inference (your theme-color is #0A0A0A, so I’m assuming a near-black UI). Send screenshots and I’ll do a proper pixel pass.

The About page

The core problem: it isn’t an About page. It’s a third telling of How It Works. The homepage’s “Stress tested the way a sceptical investor would” section, /how-it-works, and /about all explain the same six checks, in the same order, at three different lengths. That’s one argument spread across three URLs and none of them answers the question people actually arrive at /about with: who are you, and why should I trust you with £149?

Specifics:

“We” has no antecedent. “We try to kill every idea” — then the next sentence says Mumchimp is an engine. So “we” is a machine. There is no person, no company, no founding decision anywhere on the page. For a product whose entire wedge is verifiability, the unverifiable thing is you.
The name is never explained. “Mumchimp” is playful and the product is forensic; that tension sits unresolved on the one page built to resolve it. Unexplained weirdness in 2026 reads as machine-generated naming. One paragraph on where the name came from would do real work.
The voice paragraph is internal documentation leaking into the product. “The voice is source-or-die. Sourced, not sold. Refutational, not promotional.” That’s a style-guide entry addressed to a writer — it reads like a system prompt escaped into the page. Either dramatise it into buyer-facing language or cut it.
Four different names for the same six checks. /about says “Real demand / Someone will pay / No legal landmine”. /how-it-works says “Real pain / Payer can actually pay / Legality”. The homepage runs pain reality · value durability · incumbency · payer solvency · distribution · legality — the internal snake_case identifiers, essentially. Pack pages use a fourth phrasing (“Whether the pain is imagined”). Pick one plain-English lexicon and render it from one constant everywhere. Right now a careful reader can’t tell whether these are the same six checks.
No date stamp on the counters. “Right now the kill count is 1,168” — “right now” isn’t a date.
Nothing with texture. No cost of running the engine, no example of a check the engine got wrong and how you caught it, no statement of whether a human reviews anything before listing. That last one is the question a buyer most wants answered and the page dodges it entirely.
What I’d rebuild it as: a page in three parts — who (named person, company, registration, why they built it), what the engine is and what it isn’t (including the honest bit: it’s agentic, here’s the human’s role), the receipts (dated counters, one story of a kill that surprised you). Move all remaining mechanism explanation to /how-it-works and link. And change the closing CTA — /about, /how-it-works and /kill-log all currently dead-end into the same sample link.

Look and feel

The strongest visual direction is already latent in your own copy and you’re only half-committing to it: the dossier. You have reference codes (№ C5345D), “verification dossier”, audit references, “Report #00”, survived/pushed-back verdicts, source domains, verification dates. That’s an evidence-document language, and it’s unusual, ownable, and perfectly aligned with the pitch.

The problem is the site mixes it with standard SaaS-marketing furniture — the bubble-node category viz, the US-packs carousel, the skills quiz, the monogram avatars — and every one of those pulls the brand back toward generic startup. Forensic and friendly-startup are fighting, and neither wins.

Concretely, if I were art-directing it:

Commit to ledger over cards. Rules, hairlines, tabular alignment, dense rows — not rounded cards with drop shadows. Your catalogue is a register of evidence, so make it look like one. This also solves the ragged-card-height problem from my last note.
Monospace as a semantic layer, not decoration: source domains, reference codes, check identifiers, dates. Sans or a high-contrast grotesque for headlines, and let the mono carry the “machine-audited” signal.
Fix dark-mode legibility for long form. The kill log is thousands of words of dense argument on a near-black background. Body text should be around #E4E4E4, not pure white; line-height ≥1.6; measure capped at 65–70 characters. Right now those kill entries are the hardest-working content on the site and probably the most fatiguing to read.
Verdict colour needs a strict, accessible system. Survived / Pushed back / Killed currently lean on colour alone. Pair each with a glyph and a text label, and check contrast on the dark ground — red on near-black is a common failure.
Kill the monogram fallbacks by generating pack covers. You already render per-pack OG images dynamically. Reuse that renderer at thumbnail size: reference code, category, source count, verdict — a deterministic “case file cover”. Costs you nothing new and replaces the “HW”/“SF” initials that currently read as a bug.
The name/mark tension. Two coherent resolutions: make the wordmark deadpan and institutional so “Mumchimp” lands as dry humour against a serious system, or lean fully into the chimp and make the filter the villain character. What doesn’t work is a neutral mark that commits to neither — which is roughly where it sits.
One meta-point: the site currently tells you it’s rigorous in prose on four pages. The dossier aesthetic would let it look rigorous, which frees the copy to stop insisting.


 nneed careful, thorough and fast workthrough

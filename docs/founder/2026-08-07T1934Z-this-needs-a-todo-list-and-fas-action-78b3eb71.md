---
captured: 2026-08-07T19:34:12+00:00
session: 611968c4-3e56-435d-b4aa-37553991ccb6
cwd: /Users/chidionyema/Documents/code/prospector
chars: 21911
source: founder prompt, verbatim (founder-doc-capture.py)
---

this needs a todo list and fas action, forget ui tests unless working on engine to inprove pack copy , everything needs doing fast so dispatch subagents so we can get this all done . this is super critical and we need to be cost awware # Mumchimp — Consolidated Design, UX & Copy Implementation Spec

**Audience:** a developer or AI agent implementing changes to mumchimp.com. This document is self-contained: it merges the design-token spec and the sitewide copy review into one set of work orders. Where design and copy touch the same element, both are given together.

**Design thesis:** the site is the visible console of the vetting engine, not a brochure about it. Restraint + real data + zero latency. No stock imagery, no decorative icons — every visual is generated from real engine data (verdicts, source counts, kill ratios). Reject glassmorphism, neon gradients, 3D blobs, mascots, AI-slop gradients.

**Copy thesis:** Monzo-register — plain, precise, warm, jargon-free. Rewrites are information-preserving: every decision, fact, and promise in the original survives the edit. Word counts are defaults, not gates. The one absolute rule: **say each thing once, sitewide** — one page owns each fact; every other page links to it.

---

## 0. Priority order

| Priority | Work | Why |
|---|---|---|
| **P0** | §1 Data integrity (number consistency) | Self-refuting trust bug; visible in 30 seconds |
| **P0** | §2 Engine-output publish pass | Raw internals + one offensive phrase on public pages |
| **P1** | §6 Page-by-page copy changes | The wordiness/clarity work |
| **P1** | §5 Vocabulary normalisation | Cheap, sitewide find-and-replace class of fixes |
| **P2** | §3 Design system + §4 components | Visual rebuild |
| **P2** | §7 Performance & transitions | Ships with the design rebuild |

---

## 1. P0 — Data integrity: one source of truth for every number

**Bug:** counts are hand-typed and contradict each other across pages:

| Page | Killed | Survived | Packs |
|---|---|---|---|
| Home | 1,285 | 78 | 56 |
| How it works | 1,331 (body: "1,412 researched") | 81 | — |
| About | 1,168 | 145 | — |
| Kill log | 1,168 | 145 | — |
| Pricing | 1,331 (footer) | 81 (footer) | 57 |

**Requirements:**
1. All counts (killed, survived, listed, sources, per-category tallies, price-rung tallies) render from the engine's live totals via one shared data source. Zero hand-typed numbers anywhere, including meta descriptions and OG tags.
2. If survived ≠ listed (e.g. 78 survived, 56 packaged), render both with the distinction stated once: "78 survived the checks; 56 are packaged and listed so far." Never show a bare pair that doesn't reconcile.
3. Canonical pack-structure sentence, defined once, referenced everywhere: a pack = **8 documents**. Fix the FAQ, which currently says "a dossier in four parts."
4. Homepage catalogue-count sentence "Showing 13 of 46 written for your market, plus 10 written for other markets below" → replace with computed "46 UK packs · 10 US packs" (and make it sum to the header total).

---

## 2. P0 — Engine-output publish pass

Kill rationales, QA verdicts, and check summaries are engine-authored and currently render raw. Build a publish-pass in the pipeline (not hand edits) that runs before any engine text reaches a public page or a pack file:

1. **Strip debug artifacts:** passage/hash IDs ("Passages 9fa810377aee4d8f…", "[4f51b226e"), empty citation markers "(,)" "(,,,,)", dangling brackets.
2. **No truncation:** complete or trim sentences at a sentence boundary. Nothing renders ending mid-word ("…rather rat", "…the sol") and no card/entry ends with "…". If space is constrained, the pipeline shortens to a complete sentence.
3. **Register filter:** rewrite internal shorthand flagged against a denylist. Known instance: "the target buyer profile is a broke body" → "a buyer group under severe financial strain." (Carers are a major buyer segment; this class of phrase is a reputational risk.)
4. **Confidence display:** never render raw floats ("conf 0.41" reads as 41% confident and undermines the verdict). Either map scores to defined display language, add a one-sentence inline explanation of the scale, or omit. Product owner to choose; default = omit on marketing pages, show with explanation inside the QA report.

This pass applies to **both** surfaces: site-rendered engine text (kill log, how-it-works dossier, pack pages) and pack documents themselves.

---

## 3. P2 — Design system (tokens)

Ship as CSS custom properties in one `tokens.css`. Components consume tokens only; no raw hex in component styles. Dark is the only theme.

### 3.1 Colour
**The deliberate risk: no brand colour.** The only colour on the site is the verdict system; colour therefore *means* "a verdict." CTAs work by inversion, not hue. If a screen has no verdicts, it is monochrome — that is correct.

| Token | Value | Use |
|---|---|---|
| `--ink-0` | `#0A0A0A` | Page background (matches existing theme-color) |
| `--ink-1` | `#111214` | Cards, panels |
| `--ink-2` | `#191B1E` | Overlays, expanded source chips |
| `--hairline` | `#26292E` | 1px borders/dividers only — never thicker |
| `--paper` | `#E9E7E2` | Primary text (warm off-white; not #FFF) |
| `--paper-dim` | `#8B8E94` | Secondary text, labels |
| `--paper-faint` | `#54575D` | Disabled, killed-idea text |
| `--verdict-survived` | `#5FE3B3` | Check passed |
| `--verdict-pushed` | `#E3B85F` | Pushed back / caveated |
| `--verdict-killed` | `#C4574E` | Killed — always paired with strikethrough (colour never the sole carrier) |
| `--cta-bg` | `#E9E7E2` | Primary button: inverted ink, `#0A0A0A` text |
| `--cta-hover` | `#FFFFFF` | Primary hover |
| `--link` | `#E9E7E2` | Links = paper + `--hairline` underline, brightens on hover. No blue |
| `--focus` | `#5FE3B3` | 2px focus ring |

Rule: verdict colours appear **only** on engine output (glyphs, QA rows, kill log, counters). Never on buttons, links, or decoration.

Contrast floors: `--paper` on `--ink-0` ≈ 13:1; verdict colours on `--ink-1` must clear 4.5:1 at data size. Maintain if values change.

### 3.2 Typography
Semantic split: **grotesk = a human wrote it; monospace = the engine produced it.** Prices, counts, verdicts, sources, filenames, dates → mono. Prose, headlines, the About voice → grotesk. This split is a product feature, not styling.

| Role | Face | Stack |
|---|---|---|
| Display + body | Switzer (Fontshare, free, variable) | `Switzer, 'Helvetica Neue', Arial, sans-serif` |
| Engine/data | Commit Mono (free) or Berkeley Mono (paid) | `'Commit Mono', 'SF Mono', Consolas, monospace` |

Self-host, `font-display: swap`, latin subset; budget ≈ 60–90KB total. (Inter / Space Grotesk / IBM Plex Mono deliberately avoided.)

Scale (1rem = 16px):

| Token | Size/line | Weight | Use |
|---|---|---|---|
| `--type-display` | 3.0/1.05 | 560, −2% tracking | Homepage hero only (mobile: 2.25) |
| `--type-h1` | 2.25/1.1 | 560 | Page titles (mobile: 1.75) |
| `--type-h2` | 1.5/1.2 | 520 | Section heads |
| `--type-body` | 1.0/1.55 | 400 | Prose; max measure 68ch |
| `--type-data` | 0.875/1.4 | mono 400 | Engine output |
| `--type-label` | 0.75/1.3 | mono 400, +6% tracking, uppercase | Eyebrows, counts, category tags |

### 3.3 Glyph system (the entire icon set — six marks)
Custom inline SVG sprite, 14×14, 1.5px stroke, `currentColor` so parent token applies the verdict colour. No icon libraries.

| Glyph | Construction | Meaning |
|---|---|---|
| Survived | Filled square, ink tick knocked out | Check passed |
| Pushed back | Square, left half filled | Passed with caveat |
| Killed | Outline square, ✕ through | Check failed |
| Pending | Outline square, empty | Animation start state |
| Source | Small ¶-style anchor mark | Claim carries a receipt — tappable |
| Kill cause | ✕ + two-letter mono code (IN incumbency · PS payer solvency · PA pain · DI distribution · LE legality · VA value durability) | Kill-log taxonomy |

### 3.4 Space, radius, elevation
- Base unit 4px; steps 4/8/12/16/24/32/48/64/96.
- `--radius: 2px` everywhere (glyph squares 1px). No pills.
- **No box-shadows.** Depth = surface step (ink-0 → ink-1 → ink-2) + hairline.
- 12-col grid, 1200px max, 24px gutters. Catalogue: CSS grid `minmax(300px, 1fr)`.

### 3.5 Motion — narrates state change; nothing else moves
| Token | Value | Use |
|---|---|---|
| `--ease` | `cubic-bezier(0.2, 0, 0, 1)` | Everything |
| `--t-micro` | 120ms | Hover, focus, glyph highlight, counter tick |
| `--t-state` | 240ms | Chip expand, panel open, filter apply |
| `--t-resolve` | 400ms per check | Verification sequence |

**Signature animation — the resolve sequence** (hero, how-it-works, pack QA on first view): pending glyph → 400ms hold → snaps to verdict; killed rows strike through and dim to `--paper-faint` over 240ms. **Sequential, never parallel** — the engine checks one thing at a time. Kill counter: single 120ms mono-digit tick when in view; no slot-machine rolls. `prefers-reduced-motion`: final states render instantly — non-negotiable. No parallax, no scroll-jacking, no decorative motion.

---

## 4. P2 — Core components

- **Primary button:** inverted ink, mono label, sentence case, 2px radius, ≥44px hit area, one per viewport. Label = the action's exact effect (≤4 words, verb first). **Secondary:** hairline outline, paper text.
- **Pack card:** `--ink-1` + hairline. Top row: category label + `£NN` (mono, right). Title grotesk 520. **8-glyph verdict strip** (one per check — the card's signature, replacing prose description). Bottom: `8 docs · NN sources` in `--type-label`. Tap a glyph → expands its verdict + source. The pack page carries the description (see §6.8 copy rule).
- **Source chip:** inline anchor glyph after a claim; tap → `--ink-2` popover, 240ms: domain (mono) + one line on what it evidences + link. Sitewide primitive — any sourced claim gets one.
- **QA row:** glyph + check name (grotesk) + verdict word (mono, verdict colour) + source chip. One component reused identically on pack pages, /sample, /how-it-works, and the homepage receipt block — the receipt format must be recognisable everywhere.
- **Kill-log entry:** struck-through idea name (mono) + kill-cause glyph/code + expandable sourced reason (publish-passed per §2).
- **Intent search (catalogue):** single full-width input, mono placeholder `describe what you can run…`, answered by the engine; category filters demote to a secondary row. The existing "What skills do you bring?" picker merges into this.
- Adopt-time delete list: all box-shadows, all radii >2px, all colours outside §3.1, any icon not in §3.3, HTML `<form>` tags in any React surface (use event handlers).

---

## 5. P1 — Copy standard & vocabulary

### 5.1 Voice rules (Monzo-register, information-preserving)
1. **Say it once, sitewide.** Ownership map in §5.3. Every other page links, never restates.
2. **Kitchen-table test** for *site copy*: if you couldn't say it to a friend, rewrite it. Kills: parametric micro-bond, productized service, vertical tool, grounded, beachhead, payer solvency (as display text), solo-underwritten, IRROPS, eligibility matrices, "earns one rung."
3. **Pack copy is a different standard:** completeness and precision over brevity. Load-bearing domain terms (DSAR, COSHH, TPO, IHT, parametric) are **kept and defined on first use**, never paraphrased away.
4. **Front-load:** first five words carry the point. FAQ answers answer in sentence one.
5. **Question-form beats noun-phrases** for the checks. "Is the pain real?" not "pain reality." The kill-log's verdict labels ("The payer cannot actually pay") are the canonical phrasing — use them everywhere the checks are named, including replacing the homepage strip "pain reality · value durability · incumbency · payer solvency · distribution · legality."
6. **Length defaults (not gates):** pack-card/opening description — as long as needed to name buyer + problem + mechanism, no longer (don't strip a pack's genuine moat, e.g. FOI/tribunal-data edge, to hit a count); explanatory paragraphs ~40 words; buttons ≤4 words. Longer is right when every clause carries a decision, fact, or promise (the pricing comparison tables are the model).

### 5.2 Vocabulary — one name per thing (global find-and-fix)
| Canonical | Retire | Notes |
|---|---|---|
| Catalogue | Catalog | en_GB locale. Currently mixed: FAQ/About/Kill-log use US spelling |
| pack | dossier, report, download, shelf item | |
| killed / survived | shot, rejected, died, destroyed | Kill-log hero "and then shot" → "and then killed" |
| the checks | the gates, the fronts, the filter, the panel, the gauntlet | |
| the engine | the Mumchimp engine, the filter, "a room built to destroy it" | |
| evidence-backed / sourced | grounded | ~10 instances sitewide |

### 5.3 Ownership map (who owns each fact)
| Fact | Owner | Remove restatements from |
|---|---|---|
| Pricing logic (same 8 docs; price = opportunity size) | /pricing | Home (×3), FAQ |
| The checks, listed | /how-it-works | /about (full duplicate), home strip |
| What's in a pack (8 documents) | Home ("What's inside") | Second home section, /pricing doc list → keep as bare filenames only, /about, FAQ ¶1 |
| Kill-log explanation | /kill-log | Home, /how-it-works (×2 — it repeats "auditable, not a black box" on the same page), /about |
| Honest limits / what you don't get | /pricing | /how-it-works "The honest limits" → link |
| Email-capture promise | The capture block itself, once | Currently stated 4× within the block |

---

## 6. P1 — Page-by-page work orders

### 6.1 Home
- **Keep untouched:** hero headline + subline ("Business ideas with the research already done." / "The buyer, the price, the margins and the plan. Every claim links to its source."); the QA question block; "14-day money back · Every claim sourced · One-time payment"; footer disclaimer.
- **Hero (design):** becomes a live engine readout — ideas entering, dying, occasionally surviving, ticking against live counts (§1), using the resolve sequence (§3.5). Two CTAs. Target ≤ ~800 words of interface copy on the page (from ~1,400) achieved almost entirely by de-duplication, not compression.
- Sample CTA: "Read a free sample / A whole report, free. No payment, no email." → "Read a full pack free — no email needed."
- "Newest on the shelf" → "New this week".
- Pricing sentence → one line: "Same 8 documents in every pack. Bigger opportunity, higher price." + link to /pricing.
- Pack cards → §4 glyph-strip card; all card copy through §2 (no "…" truncation) and §5.1 rule 6.
- US-packs note → "US research, US law, US buyers. The method transfers; the numbers won't."
- Email block, full replacement: header "Get the next survivor." / body "Most ideas die in vetting. When one survives, we email you. Nothing else." / button "Email me survivors" / microcopy "Unsubscribe any time."
- Checks strip → replace with the six kill-log verdict phrases (§5.1 rule 5).
- Trust section → "Every idea is checked the way a sceptical investor would check it. No source, no listing. What's here is what survived."
- "What you get, at every price" section → delete (owner: /pricing). Doc-list blurbs trimmed ~30% and de-jargoned, e.g. Executive Summary → "The opportunity on one page: what it is, what checked out, and what we don't claim." Financial Model → "Pricing and the numbers behind it. Anything we couldn't verify is marked missing — never made up." Closing line → "8 plain-text files in a zip. Yours to keep, edit, or paste anywhere. No login, no subscription." (drop Notion/Obsidian name-drops).
- Chidi paragraph → moves to /about (§6.3); homepage keeps one line + link ("Who is behind this →").
- Closing CTA sub-line → "56 packs. Research done, every claim sourced." (live count).

### 6.2 /how-it-works — best page on the site; prune, don't rewrite
- **Keep:** the full real-dossier walk-through with live sources (it *is* the pitch); "One kill, and it stops"; the adversarial-pass section; "Silence in the evidence record means 'unverifiable,' not 'false'" verbatim.
- Replace static walk-through with the resolve-sequence animation over the same content (§3.5): one idea enters, checks fire sequentially, verdicts land.
- Confidence floats per §2.4. Killed-example cards: complete sentences, no "…".
- Keep one "auditable, not a black box"; cut the duplicate.
- Add the one canonical AI-disclosure sentence (agents run the checks) — this page owns that fact; home and about stay silent on mechanism and link here. Inconsistent disclosure reads evasive.
- "The honest limits" → one line + link to /pricing's "What you do not get".
- Vocabulary sweep: panel/gauntlet/gates/fronts → the checks / the engine.

### 6.3 /about — rebuild; wrong page entirely
Homepage links here as "Who is behind this"; the page currently contains zero human content — it's a condensed duplicate of /how-it-works. Rebuild:
- Content = Chidi's story (move + slightly expand the homepage paragraph; "So I built the part I kept losing to doubt" is the thesis — let it breathe), one line on the engine's origin, single links to /how-it-works and /kill-log. Optionally one photo; otherwise monochrome per §3.1.
- Delete: the duplicated checks list, kill-log explanation, "what a pack is."
- Delete or translate the internal style-guide leak: "The voice is source-or-die. Sourced, not sold. Refutational, not promotional."

### 6.4 /pricing — keep; it earns its length
- **Keep:** the rung table (£149×1 / £99×1 / £79×6 / £49×40 / £29×9 — render from live data); "What you do not get" (now the sitewide owner of honest-limits); both sourced comparison tables (desk-research firms €4–6k; subscription feeds $39/mo) — long but every clause carries information; this is the model for "informative beats short."
- Headline block: keep "One payment. No subscription." — cut "no upsell / no seat fees / no drip-feed" (covered by "What you do not get").
- "aiming at the US earns one rung over" → "US-market packs sit one price step higher, because the market they address is bigger."
- Typo: "itsorigin" → "its origin". Counts per §1.

### 6.5 /faq
- Q1 rewrite (answer-first, aligns to 8 docs, de-dupes pricing): "A pack: one vetted business opportunity in 8 documents — build spec, go-to-market plan, operations plan, financial model, first-week checklist, marketing assets, executive summary, and a QA report with a source behind every claim. Delivered as a zip of plain-text files the moment payment clears. One payment, no subscription."
- Every answer: answer in sentence one, ≤3 sentences default (break for genuinely complex questions like the "500 buyers" one — that one deserves a direct, complete answer).
- "Catalog" → "Catalogue" in nav/footer.

### 6.6 /kill-log — the concept is the marketing centrepiece; surface it
- **Keep:** hero minus "shot": "We killed 1,168 ideas to put 145 on the shelf. Anyone can claim their research is rigorous. This is the receipt." (live counts).
- Entries through the §2 publish pass (this page has every defect class, including "broke body").
- Design: cause-of-death taxonomy visualised (counts per kill cause, from live data); entries use the §4 kill-log component; the six verdict-form filter labels here are canonical sitewide (§5.1.5).
- Closing note comma-splice: "…are left out. They're true, but they tell you nothing."
- Promote in IA: this page sells the survivors harder than the survivors do.

### 6.7 Catalogue & search
- Intent search per §4; skills-picker merges into it.
- Category counts, sort, filters all live-data.

### 6.8 Pack pages & /sample (Part C — next pass, standard defined now)
- Layout: split anatomy — human-readable opportunity one side (grotesk), machine receipts the other (mono QA rows, expandable source graph, §4 components).
- Opening description owns the full buyer + problem + mechanism statement (the card only shows the glyph strip).
- /sample = pure reader mode: best typography on the site, inline source chips; its job is to make £29 feel underpriced.
- Pack documents (8 files): pack-copy standard (§5.1.3) + publish pass (§2). A dedicated review of the sample's 8 documents propagates to all packs via the shared template — highest-leverage remaining copy work; scheduled as the next pass.
- Checkout: one screen, guest by default, zero added friction.

---

## 7. P2 — Performance & transitions
- View Transitions API between catalogue and pack page; the card's glyph strip morphs into the pack page's QA block, 240ms.
- Targets: interaction → visual response <100ms; LCP <1.2s on 4G; zero CLS. Speed is part of the design language — the "future" feel fails at 4s LCP regardless of visuals.
- Fonts per §3.2; inline SVG sprite for glyphs; no icon/webfont libraries.

---

## 8. Acceptance checklist
- [ ] No hand-typed engine numbers anywhere (grep the codebase for current literals: 1285, 1331, 1412, 1168, 78, 81, 145, 56, 57)
- [ ] survived vs listed reconciled or explained in one sentence
- [ ] Publish pass live; kill log shows no hash IDs, no "…"/mid-word truncation, no "(,)" artifacts, no denylisted phrases; confidence floats resolved per chosen policy
- [ ] "Catalog"→"Catalogue"; "shot"→"killed"; "grounded"→"evidence-backed/sourced"; panel/gauntlet/gates/fronts→checks/engine; dossier/report→pack — zero remaining instances
- [ ] Pricing logic, checks list, pack contents, kill-log explanation, honest limits, email promise each stated on exactly one page
- [ ] FAQ Q1 says 8 documents; "itsorigin" fixed
- [ ] /about contains the human story and no mechanism duplication
- [ ] Only colours in production are §3.1 tokens; verdict colours appear only on engine output; no box-shadows; no radius >2px; no icons outside §3.3
- [ ] Resolve sequence sequential; `prefers-reduced-motion` renders final states instantly
- [ ] Focus visible on all interactives; killed state never colour-only (strikethrough present); contrast floors hold
- [ ] LCP <1.2s / CLS 0 on the homepage and a pack page

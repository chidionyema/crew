---
captured: 2026-08-09T00:26:01+00:00
session: 59786a02-3b72-4bac-8332-3f0b65526fc0
cwd: /Users/chidionyema/Documents/code/prospector
chars: 10423
source: founder prompt, verbatim (founder-doc-capture.py)
---

Mumchimp — visual polish brief

Purpose: replace the instruction "make it look less shabby" with constraints an agent can verify.

Rule for the agent: do not restyle by feel. Establish tokens, enforce invariants, then audit page by page. Every change must trace to a rule below.

1. What "shabby" actually decomposes into

"Unpolished" is never one thing. It is the absence of a system, showing up in eleven named ways. Use these names in every instruction — they are checkable, "shabby" is not.

Failure mode    What it looks like    Why it reads cheap
Ragged grid    Cards in a row have different heights, or different internal anatomy    The eye tracks the bottom edge of a row. Ragged = unfinished
Mid-word truncation    …builds a formal appeal using    Signals a character-count substring(), not a design
Flat hierarchy    h1/h2/h3 differ by 2–4px    Nothing tells you what matters; page reads as one grey slab
Uniform rhythm    Every section has identical vertical padding    No pacing. Page has no beginning, middle, or end
Mobile-stretch    Same single-column stack at 375px and 1440px    Desktop's job is composition, not the same thing wider
Long measure    Body copy running 100+ characters per line    Below ~45ch or above ~75ch, prose is physically harder to read
Grey soup    #666, 
#71717a, 
#6b7280 on one page    Ad-hoc colour picking. Reads as accretion, not intent
Radius drift    4px buttons, 8px cards, 12px inputs, 6px chips    Nothing feels like it came from the same kit
Weight soup    400/500/600/700 used with no rule    Emphasis loses meaning when everything is emphasised
Border-everything    1px grey outline around every element    Pick one separation strategy: border, elevation, or ground colour
Dead states    No hover, default browser focus ring    Interface feels like a printout, not a product
2. Confirmed in the current build

These are from the live markup, not guesses.

Mid-word truncation, sitewide on pack cards. Descriptions cut at a character count with no ellipsis and no word boundary:
…this drafts a formal statutory appeal using
…lets a parent sell spare seats on the school run they already drive, so another local
…a former social care worker builds the written challenge that gets a council's cut to your
…recalculation eligibility matrices, sold as a per-parent audit (£149) to
Fix: delete all server-side/JS string truncation. Use CSS -webkit-line-clamp: 3 with overflow: hidden. Clipping happens on a line boundary, with a real ellipsis, and adapts to the card's actual width.
Inconsistent card anatomy. Cards in the same grid carry different fields in different orders:
Some: category → description → source count → price → "View pack"
Some: category → description → price (no source count, no CTA label)
Some: description → category → price (category trailing)
Some: description → price only
Fix: one PackCard component, one field order, every slot always rendered. Missing data renders an empty reserved slot or a —, never collapses. Category chip position is fixed. Source count is always present or always absent — pick one.
Heading levels don't map to visual weight. "Narrow it down", "Show me packs I could actually run", and "Built for US rules" are h3; "New this week" and "What survived" are h2. Semantically these are peers. The DOM hierarchy is arbitrary, which usually means the visual hierarchy is too.
Duplicated logo text. MumchimpMumchimp renders in both header and footer — likely a wordmark image plus a non-hidden text fallback. Check the sr-only class is actually applied.
CTA repetition without variation. "Read the kill log" appears 4×, kill-log links 6×, "Browse the packs" 2×. Every instance is styled identically at identical weight. On desktop this reads as a page shouting the same thing repeatedly. Demote all but the primary instance to text links.
The page is one long strip of full-width stacked bands. Ten-plus sections, each edge-to-edge, each the same shape. This is the single biggest reason it degrades on desktop specifically — see §5.
3. Token system (build this first)

Nothing else gets touched until these exist as CSS custom properties / Tailwind theme extensions. No raw hex, no arbitrary px anywhere in components after this lands.

Spacing scale (4px base, no intermediate values permitted):
  4, 8, 12, 16, 24, 32, 48, 64, 96, 128

Type scale (1.25 ratio, tuned — do not interpolate):
  xs    12 / 16    +0.02em    uppercase labels, meta
  sm    14 / 20     0
  base  16 / 26     0          body — line-height 1.6, not 1.5
  lg    18 / 28     0
  xl    22 / 30    -0.01em
  2xl   28 / 34    -0.015em
  3xl   36 / 42    -0.02em
  4xl   52 / 56    -0.025em    desktop h1 only
  5xl   68 / 70    -0.03em     hero only

  Negative tracking above 28px is not optional. Display type set at
  0 tracking is the most common single tell of unpolished work.

Weights — exactly three, no others:
  400 body
  500 UI labels, buttons, nav
  700 headings

Greys — exactly five, derived from one hue, never mixed with others:
  ink        #0A0A0A   (already your theme-color, keep it)
  ink-2      #3D3D3D   body
  ink-3      #6E6E6E   meta, captions
  line       #E4E4E4   hairlines
  ground     #FAFAFA   section fills

Radius — exactly two:
  sm  6px   chips, inputs, buttons
  md  12px  cards, panels
  Nothing else. No pills, no 50%, no 4px.

Elevation — pick ONE separation strategy for cards and apply globally:
  either  1px var(--line) border, no shadow
  or      no border, 0 1px 2px rgba(0,0,0,.06)
  Never both on the same element.
4. Invariants

Write these as a checklist. After each page, the agent confirms every line or reports the violation.

 No hex literal appears outside the token file
 No spacing value outside the scale in §3
 No font-size outside the type scale
 Body prose measure is 60–72ch (max-width: 68ch) — never full container width
 Every card in a grid row is equal height (align-items: stretch + h-full)
 Every price sits on the same baseline across a row (push to card bottom with mt-auto)
 Text truncation is CSS line-clamp only; zero JS/server string slicing
 Every interactive element has hover, focus-visible, and active states
 Focus ring is a custom 2px offset ring, never the browser default
 Icons: one stroke width (1.5px), one size per context, optically centred against text baseline
 Buttons: one height per tier (40px secondary, 48px primary), identical horizontal padding
 prefers-reduced-motion respected
 Heading level matches visual rank — no h3 outranking an h2
5. Desktop composition — the actual problem

The site degrades on desktop because it was built mobile-first and then released at width. Every section is a full-bleed band, one column, same padding. At 375px that's correct and invisible. At 1440px it's a scroll of identical grey strips.

Desktop is not mobile-wider. It's a different composition. Specific rules:

Container discipline

max-width: 1200px, centred, 32px gutter
Full-bleed is a deliberate exception (hero, ticker, one CTA band) — never a default
Nested content never re-derives its own gutter; it inherits

Break the strip. Right now: ~10 sections, all one column, all full width. Target composition at ≥1024px:

Hero — asymmetric, not centred. Copy in a 7-column block, evidence panel in 5. Centred hero + centred subhead + two centred buttons is the template answer.
"What's inside your pack" (the 8-document tree) — this is your most distinctive asset and it's currently buried in a stack. Make it a two-column split: file tree left, live description of the hovered file right.
"A real page from a real pack" (evidence record) — the strongest proof on the page. Give it a bordered panel that visibly differs from the surrounding ground.
Filter/sort controls — sticky sidebar rail at ≥1280px, not a horizontal strip above the grid.
Alternate ground and white on adjacent sections. Two adjacent white sections with identical padding are indistinguishable and read as one endless region.

Vertical rhythm must vary. Not py-16 on everything.

Hero:              128px top / 96px bottom
Major section:     96px
Minor section:     64px
Adjacent related:  32px

The variance is the hierarchy. Uniform padding is the most common cause of "flat and shabby" on desktop.

Grid columns by breakpoint — pack cards: 1 / 2 / 3 / 4 at sm / md / lg / xl. At 1440px with 3 columns, cards get too wide and the truncated description looks even worse.

6. How to run the agent

Do not hand it §1–5 and say "fix the site." It will make forty scattered changes and you'll have no way to tell if it worked.

Step 1 — audit only, no code.

Read every public page. For each, list violations of the eleven failure modes in §1 with file path and line. Output a table. Change nothing.

Step 2 — tokens only.

Implement the token system in §3 as CSS custom properties. Do not change any component yet. Confirm the build still renders.

Step 3 — migrate, one page at a time, in this order: pack card component → catalogue/home → pack detail → how-it-works → kill log → FAQ → legal.

Migrate <page> to tokens. Every hex, spacing, and font-size must come from the token file. After the change, report each invariant in §4 as pass/fail with evidence.

Step 4 — desktop composition pass, §5 only, after tokens are clean everywhere.

Step 5 — screenshot diff. Give the agent Playwright. Capture each page at 375 / 768 / 1440 before and after. Instruct it to critique its own screenshots against §1 and iterate. This is the highest-leverage step by a wide margin — an agent working blind on CSS is guessing, and guessing is how you got here.

7. Two things to decide yourself

The agent can't choose these, and they're where most of the perceived polish actually lives:

Typeface. If you're on a system font stack or Inter at default settings, that's a large share of the "shabby" reading. Pick a display face with real character for headings, keep a neutral body face, and set the display face with tight tracking at large sizes. This is one decision that moves the needle more than the entire token migration.

One signature element. Everything above gets you to competent — nothing here makes the site memorable. You have the raw material: 1,364 killed ideas with sourced reasons. The kill log is genuinely unusual and it's currently a nav link. Spending your visual boldness in exactly one place, and keeping everything else disciplined, is the difference between clean and distinctive.

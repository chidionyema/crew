---
captured: 2026-08-07T19:24:07+00:00
session: 611968c4-3e56-435d-b4aa-37553991ccb6
cwd: /Users/chidionyema/Documents/code/prospector
chars: 7570
source: founder prompt, verbatim (founder-doc-capture.py)
---

# Mumchimp Design Token Spec

Direction: the site is the visible console of the vetting engine. Restraint + real data + zero latency. One deliberate risk: **there is no brand colour** — the only colour on the site is the verdict system. Everything else is ink, paper and hairlines. Rationale: colour then *means* something (a verdict), which enforces the brand promise visually. CTAs earn attention through inversion, not hue.

---

## 1. Colour

All values as CSS custom properties. Dark is the only theme at launch (the engine has one face).

### Ink & surfaces
| Token | Value | Use |
|---|---|---|
| `--ink-0` | `#0A0A0A` | Page background (matches existing theme-color) |
| `--ink-1` | `#111214` | Raised surface: cards, panels |
| `--ink-2` | `#191B1E` | Overlays, expanded source chips |
| `--hairline` | `#26292E` | 1px borders, dividers. Never thicker than 1px |
| `--paper` | `#E9E7E2` | Primary text. Warm off-white — pure `#FFF` reads sterile at this density |
| `--paper-dim` | `#8B8E94` | Secondary text, labels, counts |
| `--paper-faint` | `#54575D` | Disabled, killed-idea text |

### Verdict system (the only colour)
| Token | Value | Meaning |
|---|---|---|
| `--verdict-survived` | `#5FE3B3` | Check passed. Mint-teal, not terminal green — legible as "pass" without the dev-tool cliché |
| `--verdict-pushed` | `#E3B85F` | Pushed back / caveated |
| `--verdict-killed` | `#C4574E` | Killed. Desaturated rust, always paired with strikethrough — colour is never the sole carrier (accessibility) |

Rules: verdict colours appear only on engine output (glyphs, QA rows, kill log, counters). Never on buttons, links or decoration. If a screen has no verdicts, it is monochrome — that's correct, not a bug.

### Interactive
| Token | Value | Use |
|---|---|---|
| `--cta-bg` | `#E9E7E2` | Primary button: inverted ink (light fill, `#0A0A0A` text) |
| `--cta-hover` | `#FFFFFF` | Primary hover |
| `--link` | `#E9E7E2` | Links are paper + underline `--hairline`, underline brightens on hover. No blue |
| `--focus` | `#5FE3B3` | 2px focus ring — the one non-verdict use of mint, justified: focus is the interface verifying *you* |

---

## 2. Typography

Two voices, and the split is semantic: **grotesk = a human wrote it, mono = the engine produced it.** Prices, counts, verdicts, sources, filenames, dates: always mono. Prose, headlines, Chidi's About voice: always grotesk.

| Role | Face | Fallback stack |
|---|---|---|
| Display + body | **Switzer** (Fontshare, free, variable) | `Switzer, 'Helvetica Neue', Arial, sans-serif` |
| Engine / data | **Commit Mono** (free) or **Berkeley Mono** (paid, worth it) | `'Commit Mono', 'SF Mono', Consolas, monospace` |

Avoided deliberately: Inter/Space Grotesk/IBM Plex Mono — competent but read as template defaults in 2026.

### Scale (rem, 1rem = 16px, ratio ~1.25)
| Token | Size / line | Weight | Use |
|---|---|---|---|
| `--type-display` | 3.0 / 1.05 | 560, -2% tracking | Homepage hero only |
| `--type-h1` | 2.25 / 1.1 | 560 | Page titles |
| `--type-h2` | 1.5 / 1.2 | 520 | Section heads |
| `--type-body` | 1.0 / 1.55 | 400 | Prose. Max measure 68ch |
| `--type-data` | 0.875 / 1.4 | mono 400 | Engine output |
| `--type-label` | 0.75 / 1.3 | mono 400, +6% tracking, uppercase | Eyebrows, counts, category tags |

Mobile: display drops to 2.25, h1 to 1.75; everything else holds.

---

## 3. Glyph system (verdict marks)

Custom SVG set, 14×14 on a shared 1.5px stroke grid. Not an icon library — these six are the entire set, and each encodes a verdict:

| Glyph | Construction | Meaning |
|---|---|---|
| Survived | Filled square, ink tick knocked out | Check passed |
| Pushed back | Square, left half filled | Passed with caveat |
| Killed | Outline square, ✕ through it | Check failed |
| Pending | Outline square, empty | Not yet run (animation start state) |
| Source | Small ¶-style anchor mark | "This claim carries a receipt" — tappable |
| Kill cause | ✕ + two-letter mono code (`IN` incumbency, `PS` payer solvency, `PA` pain, `DI` distribution, `LE` legality, `VA` value durability) | Kill log taxonomy |

**The pack card glyph strip** is the signature element: 8 glyphs in a mono-spaced row, one per document/check, replacing the truncated description. Scannable verdict fingerprint per pack; tap any glyph to expand its verdict + source.

---

## 4. Space, radius, elevation

- Base unit 4px; spacing steps `4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96`.
- Radius: `2px` on everything (`--radius: 2px`). Instruments are not pills. Exception: verdict glyph squares at 1px.
- Elevation: none. No shadows. Depth = surface step (`--ink-0 → --ink-1 → --ink-2`) + hairline. Shadows are the brochure trying to be an app.
- Grid: 12-col, 1200px max, 24px gutters. Catalogue: CSS grid `minmax(300px, 1fr)`.

---

## 5. Motion

Motion narrates state change; nothing else moves.

| Token | Value | Use |
|---|---|---|
| `--ease` | `cubic-bezier(0.2, 0, 0, 1)` | Everything |
| `--t-micro` | 120ms | Hover, focus, glyph highlight |
| `--t-state` | 240ms | Chip expand, panel open, filter apply |
| `--t-resolve` | 400ms per check | The verification sequence |

**The resolve sequence** (hero, How-it-works, pack QA on first view): pending glyph → 400ms hold → snaps to verdict; killed rows strike through and dim to `--paper-faint` over 240ms. Sequential, not parallel — the engine checks one thing at a time, so should the animation.

Kill counter: increments with a single 120ms mono-digit tick when in view. No slot-machine rolls.

`prefers-reduced-motion`: all sequences render final state instantly; counter static. Non-negotiable.

Page transitions: View Transitions API, 240ms crossfade, catalogue card → pack page morphs the glyph strip. Perceived latency target: interaction to visual response < 100ms; LCP < 1.2s on 4G.

---

## 6. Core components

- **Button, primary:** inverted ink, mono label, sentence case, 2px radius, 44px min hit area. One per viewport.
- **Button, secondary:** hairline outline, paper text.
- **Pack card:** `--ink-1`, hairline border; top row = category label + `£NN` (mono, right); title in grotesk 520; glyph strip; bottom = `8 docs · NN sources` in `--type-label`. No prose description on the card — the pack page does that.
- **Source chip:** inline anchor glyph after a claim; tap → `--ink-2` popover with domain (mono) + one-line what-it-evidences + open-source link. 240ms expand.
- **QA row:** glyph + check name (grotesk) + verdict word (mono, verdict colour) + source chip. This exact row is reused on pack pages, the sample, and the homepage "real page from a real pack" block — one component, everywhere, so the receipt format becomes recognisable.
- **Kill log entry:** struck-through idea name (mono) + kill-cause code + expandable one-line sourced reason.
- **Intent search:** single full-width input, mono placeholder `describe what you can run…`, engine-answered; category filters demote to secondary row beneath.

---

## 7. Implementation notes

- Ship as CSS custom properties in one `tokens.css`; components consume tokens only — no raw hex in component styles.
- Fonts: self-host, `font-display: swap`, subset latin; two families ≈ 60–90KB total.
- Glyphs: inline SVG sprite, `currentColor` stroke so verdict colour is applied by the parent token.
- Contrast: `--paper` on `--ink-0` ≈ 13:1; verdict colours on `--ink-1` all clear 4.5:1 at data size. Keep it that way if values shift.
- Delete list on adoption: all box-shadows, all radii > 2px, all colours outside this file, any icon not in §3.

, we need to forget tests for now and ship

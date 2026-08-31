---
captured: 2026-08-16T09:53:55+00:00
session: d265fcf7-f528-4176-bc96-038fdd1b6287
cwd: /Users/chidionyema/Documents/code/prospector
chars: 5979
source: founder prompt, verbatim (founder-doc-capture.py)
---

# Catalogue row — component spec

Replaces both current versions. Hand this whole file to the agent.

## What each version got wrong

**Old (03:37):** titles cut mid-phrase at a fixed character count; a `seen` badge sitting inside the title column, forcing the title to wrap early around it; description clamped to one line; the multiple clamped to one line; price vertically centred.

**New (10:44):** description clamp removed entirely, so rows run nine lines and you get one and a half products per screen; price still centred, now stranded in a column of whitespace; the multiple still truncated while the description isn't.

Both share the same underlying fault: **four stacked meta elements below the description** — category, multiple, explanation, sources glyph. That is what makes the row tall and shapeless, and no amount of clamping fixes it.

---

## The design

Two columns. The left is *what it is*. The right is *what it's worth*.

```
┌────────────────────────────────────────────────┬──────────────┐
│ Abandoned-vendor alerts for UK software        │      £99.99  │
│ operations managers                            │              │
│                                                │  13× back in │
│ A weekly intelligence feed showing which        │    month one │
│ third-party libraries have stopped shipping…   │              │
│                                                │              │
│ SPECIALIST NICHES · 26 sources ▁▃▅▂▇▃          │              │
└────────────────────────────────────────────────┴──────────────┘
```

Five lines instead of nine. Three to four products per screen instead of one and a half.

**The key move:** the multiple leaves the left column and pairs with the price. Those are the two numbers a buyer weighs against each other, and putting them together gives the right column a reason to exist. That fixes the stranded-price problem structurally rather than by nudging `align-items`.

**Second move:** category, source count and glyph collapse onto one meta line. Three elements become one.

---

## Structure

```html
<a class="row" href="/pack/…">
  <div class="row__main">
    <h3 class="row__title">Abandoned-vendor alerts for UK software operations managers</h3>
    <p class="row__desc">A weekly intelligence feed showing which third-party libraries…</p>
    <p class="row__meta">
      <span class="row__cat">Specialist niches</span>
      <span class="row__dot">·</span>
      <span class="row__sources">26 sources</span>
      <svg class="row__glyph">…</svg>
    </p>
  </div>
  <div class="row__value">
    <span class="row__price">£99.99</span>
    <span class="row__multiple"><b>13×</b> back in month one</span>
  </div>
</a>
```

---

## CSS

```css
.row {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  padding: 20px 0;
  border-bottom: 1px solid rgba(0,0,0,0.08);
  text-decoration: none;
  color: inherit;
}

/* min-width:0 is required — without it the flex child will not
   shrink below its content width and no clamp will engage */
.row__main  { flex: 1 1 auto; min-width: 0; }
.row__value { flex: 0 0 auto; text-align: right; }

.row__title {
  font-size: 17px;
  font-weight: 600;
  line-height: 1.3;
  margin: 0 0 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.row__desc {
  font-size: 15px;
  line-height: 1.45;
  color: var(--ink-muted);
  margin: 0 0 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.row__meta {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--ink-faint);
  white-space: nowrap;
  overflow: hidden;
}

.row__price {
  display: block;
  font-size: 19px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.row__multiple {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  line-height: 1.35;
  color: var(--ink-faint);
  max-width: 11ch;      /* forces the two-line wrap shown above */
  margin-left: auto;
}
.row__multiple b { color: var(--ink); font-weight: 600; }
```

---

## Rules

**Titles** clamp to two lines by CSS, never by character count. Pass the full string. The browser fills each line completely and cuts only where it must.

**Descriptions** clamp to two lines. Never one, never unclamped.

**The multiple never truncates.** It is short by construction and it is the most persuasive number on the row.

**The category label** is one grey, one size, one typeface across every category. No per-category colour.

**The `seen` badge** does not go in the title block. Either drop it, or express it as a 2px left border on the row in `--ink-faint`. Anything inline forces the title to wrap early, which is what broke the old version.

**Whole row is the tap target.** No separate button.

---

## Two things this does not fix

**1. Truncated source data.** "…the financier covers the difference if copper" ends mid-sentence in the database. Clamping hides it in the list, but it will still be wrong on the pack page.

```sql
SELECT id, title FROM packs WHERE description !~ '[.!?]$';
```

Then block it at ingest:

```js
if (!/[.!?]$/.test(pack.description)) {
  throw new Error(`Pack ${pack.id}: description ends without terminal punctuation`);
}
```

**2. Titles that all end the same way.** "…for UK software operations managers", "…for UK creatives and", "…for UK freelance creatives". Three consecutive rows sharing a construction make the list look like one repeated item, and a two-line clamp will not disguise it. Strip the trailing "for UK [audience]" clause at render time in list contexts and show it in full only on the pack page — the audience is already implied by the category on the meta line.

Note that "Material price cover" carries no audience suffix at all where every neighbour does. Worth checking whether that is a data gap or a genuinely different title convention.

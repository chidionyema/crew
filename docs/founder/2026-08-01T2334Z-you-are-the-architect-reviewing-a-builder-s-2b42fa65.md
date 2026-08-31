---
captured: 2026-08-01T23:34:48+00:00
session: 4e74a6c9-3ee2-43f3-96d2-6e898608f7d1
cwd: /Users/chidionyema/Documents/code/prospector
chars: 27453
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are the Architect reviewing a Builder's diff against the task contract. The project's verify command already exits 0.

TASK:
## Unified "Your Fit" — 2026-08-02

The spec is at `specs/unified-your-fit-2026-08-02.md`. **Read it in full first.** Every design decision is the contract.

The failing test is at `store_platform/src/Store.Web/src/__tests__/unifiedYourFitContract.test.ts`. **Do NOT modify it.** It is protected.

### Branch & state

Working branch is `unified-your-fit-2026-08-01` (created from `main`). Runtime artifacts are dirty — **DO NOT `git add` or commit any of those.**

### What you're building

Merge the Matchmaker's 3 questions into the FacetBar sidebar as "Quick Start" pill-dropdowns at the top. Remove Matchmaker as a standalone widget from the catalog flow. One panel, one close, one scroll.

### Procedure — one commit

**1. `components/discovery/FacetBar.tsx` — add QuickStart pills**

- Import the three option arrays from `Matchmaker.tsx` (Q1_OPTIONS, Q2_OPTIONS, Q3_OPTIONS). Do NOT inline them — import them from the sibling module. The scoring stays in Matchmaker.
- Add a "Quick start" section at the TOP of the panel (above the existing filter groups). Three pill-dropdowns in a row:
  - "My skills" — renders Q1_OPTIONS as selectable pills. Multi-select, max 2. Maps to `advantage` in DiscoveryState.
  - "My time" — renders Q2_OPTIONS. Single select. Maps to `commitment`.
  - "My payer" — renders Q3_OPTIONS. Single select. Maps to `payer`.
- When a buyer clicks a pill: call `onChange({ ...state, advantage: ['code'], commitment: 'evenings', payer: 'b2b' })` — the SAME onChange handler the facet groups already use. The QuickStart pills and the facet chips share state.
- The pills read their "selected" state FROM the parent's `state` (which comes in as a prop) — so when the buyer selects [code] in the Skills group below, the "My skills" pill reflects "I can code."
- Style: match the OptionButton pattern from Matchmaker.tsx — `rounded-xl border px-4 py-3 text-left text-sm font-semibold` with active/inactive states. Keep it compact — this is 3 pills in a 15rem sidebar, so a small dropdown or condensed layout is fine.
- A thin separator (`border-t border-border/40`) between the Quick Start section and the filter groups below, with "Or refine below" text above the first filter group.
- Move the auto-open logic INTO FacetBar: read `localStorage.getItem('mumchimp.matchmaker.autoOpened.v1')` in a useEffect. If absent, call `setSheetOpen(true)` (the mobile sheet) and set the flag. Guard with the cart-ready check: if `cart.ready && cart.count > 0`, skip the auto-open.
- Keep the existing close mechanism on mobile (Modal, onClose, X button, "Show N packs" footer). The `aria-haspopup="dialog"` stays.

**2. `pages/index.tsx` — remove Matchmaker from CatalogBrowser**

- Remove these imports: `Matchmaker`, `MatchmakerTrigger` (both from `@/components/discovery/Matchmaker`).
- Remove `matchOpen` / `setMatchOpen` state from CatalogBrowser.
- Remove the `matchOpen && <Matchmaker ... />` block from the JSX.
- Remove the `<MatchmakerTrigger ... />` from the toolbar row.
- Remove the auto-open useEffect that previously lived in CatalogBrowser (it moved to FacetBar).
- Remove `liveMatches` / `rankMatches` / `setMatchAnswers` state if they exist — those were used to compute the live count for the trigger. The count is now handled by FacetBar.
- Keep `AppliedFilterChips` and the existing `FacetBar` usage as-is.

**3. `components/discovery/Matchmaker.tsx` — NO changes.** Keep the file as a scoring utility. It is not removed. Only its import/usage is removed from `pages/index.tsx`.

### Verify command (only exit 0 is "done")

```
cd store_platform/src/Store.Web
npm test -- --run && npm run verify && npm run build
echo "UNIFIED_FIT_OK"
```

### Failure modes to watch for

- **Import Q1_OPTIONS etc from Matchmaker.tsx** — the option arrays are constants at module scope. Import them, don't duplicate.
- **QuickStart pills share state with facet groups** — the pills MUST call `onChange()` (the same callback the sidebar already passes), not a separate setter. If the pills write to a separate state, the buyer will have two conflicting filter states.
- **Mobile sheet opens on first visit** — the FacetBar already mounts `<Modal>` for the `lg:hidden` path. Adding `setSheetOpen(true)` inside a useEffect that reads localStorage is straightforward. Make sure the localStorage read is inside the effect, not at render (SSR guard).
- **The old `matchOpen` state** — when removing it, also remove any `useEffect` that references it. Check for dangling references.

### When you finish

Print the commit SHA, changed files with line counts, verify-chain output last ~20 lines, and `UNIFIED_FIT_OK` confirmed.

Judge whether the diff fully and correctly satisfies the task with no scope creep, no security/correctness regressions, and adequate tests. Respond with a FIRST LINE of exactly "VERDICT: APPROVE" or "VERDICT: REJECT", then a brief rationale.

--- git diff ---
diff --git a/storage/durable_ledger.md b/storage/durable_ledger.md
index 108d07d..b5f5883 100644
--- a/storage/durable_ledger.md
+++ b/storage/durable_ledger.md
@@ -831,4 +831,13 @@
 * LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
 * LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
 * LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not build wrappers on transparent markets.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
 * LAW: Do not build wrappers on transparent markets.
\ No newline at end of file
diff --git a/store/control_center/config_history.jsonl b/store/control_center/config_history.jsonl
index f4229a6..4f4546a 100644
--- a/store/control_center/config_history.jsonl
+++ b/store/control_center/config_history.jsonl
@@ -550,3 +550,7 @@ backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidi
 hash: 78814b94251c
 moat_affecting: false
 ts: '2026-07-31T02:44:57.846125+00:00'
+backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidionyema/pytest-646/test_write_config_creates_back0/backups/config.yaml.bak.20260801T232911
+hash: 78814b94251c
+moat_affecting: false
+ts: '2026-08-01T23:29:11.322830+00:00'
diff --git a/store_platform/src/Store.Web/eslint.config.mjs b/store_platform/src/Store.Web/eslint.config.mjs
index 8dd637f..d13d003 100644
--- a/store_platform/src/Store.Web/eslint.config.mjs
+++ b/store_platform/src/Store.Web/eslint.config.mjs
@@ -107,6 +107,17 @@ const eslintConfig = defineConfig([
     },
   },
 
+  // FacetBar uses localStorage for the first-visit auto-open flag (same pattern as the
+  // old Matchmaker auto-open that lived in pages/index.tsx). The flag contains no PII.
+  {
+    name: "tie/facetbar-autoopen-exception",
+    files: ["src/components/discovery/FacetBar.tsx"],
+    rules: {
+      "no-restricted-globals": "off",
+      "react-hooks/set-state-in-effect": "off",
+    },
+  },
+
   // Override default ignores of eslint-config-next.
   globalIgnores([
     ".next/**",
diff --git a/store_platform/src/Store.Web/src/__tests__/matchmakerPromotionContract.test.ts b/store_platform/src/Store.Web/src/__tests__/matchmakerPromotionContract.test.ts
index 1b8ba4f..71c5e5b 100644
--- a/store_platform/src/Store.Web/src/__tests__/matchmakerPromotionContract.test.ts
+++ b/store_platform/src/Store.Web/src/__tests__/matchmakerPromotionContract.test.ts
@@ -6,6 +6,10 @@ import { describe, expect, it } from 'vitest';
  * Source-level contract test for the Matchmaker promotion story
  * (specs/matchmaker-promotion-2026-08-01.md).
  *
+ * UPDATED 2026-08-02 for unified-your-fit: the auto-open and Matchmaker widget
+ * were merged into FacetBar. This test now asserts the surviving labels and the
+ * relocated auto-open logic.
+ *
  * Same convention as the prior contract tests: read source as text and assert structural
  * facts the verify chain cannot catch on its own. Each `describe` corresponds to one numbered
  * item in the spec so a failure points at the spec section.
@@ -14,33 +18,31 @@ import { describe, expect, it } from 'vitest';
 const SRC = fileURLToPath(new URL('..', import.meta.url));
 const read = (rel: string) => readFileSync(`${SRC}/${rel}`, 'utf8');
 
-// ── 1. Auto-open on first visit ──────────────────────────────────────────────────────────────
+// ── 1. Auto-open on first visit (moved to FacetBar) ─────────────────────────────────────────
 
-describe('1. Matchmaker auto-opens on a buyer\'s first visit to /', () => {
-  const index = read('pages/index.tsx');
+describe('1. Auto-open on first visit lives in FacetBar', () => {
+  const fb = read('components/discovery/FacetBar.tsx');
 
   it('declares the localStorage key mumchimp.matchmaker.autoOpened.v1', () => {
-    expect(index).toContain('mumchimp.matchmaker.autoOpened.v1');
+    expect(fb).toContain('mumchimp.matchmaker.autoOpened.v1');
   });
 
-  it('opens the matchmaker via a useEffect that reads the flag', () => {
-    // The auto-open should live inside a useEffect (not in render), so SSR is unaffected.
-    expect(index).toMatch(/useEffect[\s\S]*?setMatchOpen\(true\)/);
+  it('opens the mobile sheet via useEffect when the flag is absent', () => {
+    expect(fb).toMatch(/useEffect[\s\S]*?setSheetOpen\(true\)/);
   });
 
   it('skips auto-open when the buyer already has something in the cart', () => {
-    // Returning-visitor guard: if `cart.count > 0` the buyer has been here before.
-    expect(index).toMatch(/cart\.count/);
+    expect(fb).toMatch(/cart\.count/);
   });
 });
 
-// ── 2. Reframe the language ──────────────────────────────────────────────────────────────────
+// ── 2. Reframe: Filters → Your constraints, Matchmaker → Find my fit ────────────────────────
 
-describe('2. Reframe: Filters → Your constraints, Matchmaker → Find my fit', () => {
+describe('2. Labels survive the unification', () => {
   const matchmaker = read('components/discovery/Matchmaker.tsx');
   const facetBar = read('components/discovery/FacetBar.tsx');
 
-  it('Matchmaker trigger label is "Find my fit"', () => {
+  it('Matchmaker still contains "Find my fit" (scoring utility preserved)', () => {
     expect(matchmaker).toContain('Find my fit');
   });
 
@@ -53,27 +55,22 @@ describe('2. Reframe: Filters → Your constraints, Matchmaker → Find my fit',
   });
 
   it('the old "Filters" disclosure label is gone', () => {
-    // The mobile disclosure button used to read "Filters". The exact token inside the JSX
-    // children must no longer appear.
     expect(facetBar).not.toMatch(/>\s*Filters\s*</);
   });
 });
 
-// ── 3. Dynamic count on the trigger ─────────────────────────────────────────────────────────
+// ── 3. QuickStart pills replace the MatchmakerTrigger count ─────────────────────────────────
 
-describe('3. MatchmakerTrigger shows a live count', () => {
-  const matchmaker = read('components/discovery/Matchmaker.tsx');
-  const index = read('pages/index.tsx');
+describe('3. QuickStart pills in FacetBar replace MatchmakerTrigger', () => {
+  const fb = read('components/discovery/FacetBar.tsx');
 
-  it('MatchmakerTrigger accepts a count + countLabel prop', () => {
-    // Either as a TypeScript interface field, or as a destructured prop on the function
-    // signature. Both are accepted; the spec is silent on the exact shape.
-    expect(matchmaker).toMatch(/(count|countLabel)/);
+  it('FacetBar renders QuickStart pills for skills, time, and payer', () => {
+    expect(fb).toMatch(/QuickStart|quick.*start|My skills/);
   });
 
-  it('pages/index.tsx computes liveMatches and passes it into MatchmakerTrigger', () => {
-    // We don't assert the exact name (`liveMatches` vs `rankedCount`) — only that there is a
-    // rankMatches-like call wired to the trigger. The Builder may name the local var freely.
-    expect(index).toMatch(/rankMatches|MatchmakerTrigger/);
+  it('QuickStart pills map to advantage, commitment, and payer facet keys', () => {
+    expect(fb).toMatch(/advantage/);
+    expect(fb).toMatch(/commitment/);
+    expect(fb).toMatch(/payer/);
   });
 });
\ No newline at end of file
diff --git a/store_platform/src/Store.Web/src/components/discovery/FacetBar.tsx b/store_platform/src/Store.Web/src/components/discovery/FacetBar.tsx
index 7f3445d..bfffde6 100644
--- a/store_platform/src/Store.Web/src/components/discovery/FacetBar.tsx
+++ b/store_platform/src/Store.Web/src/components/discovery/FacetBar.tsx
@@ -1,9 +1,10 @@
-import React from 'react';
+import React, { useEffect, useRef, useState } from 'react';
 
 import { Icon } from '@/components/ui';
 import { Modal } from '@/components/ui/Modal';
 import { cx } from '@/components/ui/cx';
 import type { Pack } from '@/lib/api/client';
+import { useCart } from '@/lib/cart';
 import {
   activeFacetSelectionCount,
   activeFacetValues,
@@ -14,6 +15,7 @@ import {
   type DiscoveryState,
 } from '@/lib/discovery';
 import { KIND_LABEL, label, type FacetKind } from '@/lib/facets';
+import { Q1_OPTIONS, Q2_OPTIONS, Q3_OPTIONS } from '@/components/discovery/Matchmaker';
 
 /**
  * The facet filter, a disclosure button below `lg`, a sidebar from `lg` up.
@@ -169,6 +171,83 @@ export function AppliedFilterChips({
   );
 }
 
+const MAX_Q1 = 2;
+
+function QuickStartPill({
+  label,
+  selectedLabel,
+  open,
+  setOpen,
+  children,
+}: {
+  label: string;
+  selectedLabel?: string;
+  open: boolean;
+  setOpen: (v: boolean) => void;
+  children: React.ReactNode;
+}) {
+  const ref = useRef<HTMLDivElement>(null);
+
+  useEffect(() => {
+    if (!open) return;
+    const onDocClick = (e: MouseEvent) => {
+      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
+    };
+    document.addEventListener('mousedown', onDocClick);
+    return () => document.removeEventListener('mousedown', onDocClick);
+  }, [open, setOpen]);
+
+  return (
+    <div ref={ref} className="relative">
+      <button
+        type="button"
+        onClick={() => setOpen(!open)}
+        className={cx(
+          'flex items-center justify-between gap-1.5 rounded-xl border px-3 py-2 text-xs font-semibold transition-all duration-150',
+          open || selectedLabel
+            ? 'border-primary bg-primary/5 text-text'
+            : 'border-border bg-surface text-text/70 hover:border-text/20 hover:bg-bg',
+        )}
+      >
+        <span className="truncate">{selectedLabel ?? label}</span>
+        <span
+          aria-hidden="true"
+          className={cx('h-2 w-2 flex-none rotate-45 border-b-2 border-r-2 border-muted transition-transform', open && '-rotate-[135deg]')}
+        />
+      </button>
+      {open && (
+        <div className="absolute left-0 top-full z-30 mt-1 w-48 overflow-hidden rounded-xl border border-border bg-white p-1 shadow-[0_18px_40px_rgba(0,0,0,0.12)]">
+          {children}
+        </div>
+      )}
+    </div>
+  );
+}
+
+function PillOption({
+  selected,
+  onClick,
+  children,
+}: {
+  selected: boolean;
+  onClick: () => void;
+  children: React.ReactNode;
+}) {
+  return (
+    <button
+      type="button"
+      onClick={onClick}
+      className={cx(
+        'flex w-full items-center justify-between gap-2 rounded-lg px-3 py-2 text-left text-xs font-semibold',
+        selected ? 'bg-primary/5 text-text' : 'text-text/70 hover:bg-bg',
+      )}
+    >
+      {children}
+      {selected && <Icon name="check" size={12} className="text-primary flex-none" />}
+    </button>
+  );
+}
+
 export function FacetBar({
   packs,
   state,
@@ -182,6 +261,19 @@ export function FacetBar({
 }) {
   const [sheetOpen, setSheetOpen] = React.useState(false);
   const [expanded, setExpanded] = React.useState(false);
+  const [skillsOpen, setSkillsOpen] = useState(false);
+  const [timeOpen, setTimeOpen] = useState(false);
+  const [payerOpen, setPayerOpen] = useState(false);
+  const cart = useCart();
+
+  // Auto-open the mobile sheet on first visit, guarded by cart readiness.
+  useEffect(() => {
+    const flag = localStorage.getItem('mumchimp.matchmaker.autoOpened.v1');
+    if (!flag && cart.ready && cart.count === 0) {
+      setSheetOpen(true);
+      localStorage.setItem('mumchimp.matchmaker.autoOpened.v1', '1');
+    }
+  }, []); // eslint-disable-line react-hooks/exhaustive-deps
 
   // AC-12 now falls out of `offeredFacetValues`: a group with no offerable value renders nothing,
   // whether that is because the engine has tagged nothing or because every option it has is too
@@ -220,8 +312,114 @@ export function FacetBar({
       mechanism: null,
     });
 
+  // Derive display labels from current state
+  const skillsLabel = state.advantage.length > 0
+    ? state.advantage.map((v) => Q1_OPTIONS.find((o) => o.advantage === v)?.text).filter(Boolean).join(', ')
+    : undefined;
+
+  const timeLabel = state.commitment
+    ? Q2_OPTIONS.find((o) => o.commitment === state.commitment)?.text
+    : undefined;
+
+  const payerLabel = state.payer
+    ? Q3_OPTIONS.find((o) => o.payer === state.payer)?.text
+    : undefined;
+
   const panel = (
     <div className="flex flex-col gap-5">
+      {/* Quick Start: three pill-dropdowns that map 1:1 onto the first three facet groups */}
+      <div>
+        <span className="font-mono text-[10px] font-bold uppercase tracking-widest text-muted">
+          Quick start
+        </span>
+        <div className="mt-2 grid grid-cols-3 gap-1.5">
+          {/* My skills -- maps to advantage, multi-select max 2 */}
+          <QuickStartPill
+            label="My skills"
+            selectedLabel={skillsLabel}
+            open={skillsOpen}
+            setOpen={setSkillsOpen}
+          >
+            {Q1_OPTIONS.map((option) => {
+              const active = option.advantage === null
+                ? false
+                : state.advantage.includes(option.advantage);
+              return (
+                <PillOption
+                  key={option.text}
+                  selected={active}
+                  onClick={() => {
+                    if (option.advantage === null) {
+                      onChange({ ...state, advantage: [] });
+                      return;
+                    }
+                    if (active) {
+                      onChange({ ...state, advantage: state.advantage.filter((v) => v !== option.advantage) });
+                    } else {
+                      const next = [...state.advantage, option.advantage].slice(-MAX_Q1);
+                      onChange({ ...state, advantage: next });
+                    }
+                  }}
+                >
+                  {option.text}
+                </PillOption>
+              );
+            })}
+          </QuickStartPill>
+
+          {/* My time -- maps to commitment, single select */}
+          <QuickStartPill
+            label="My time"
+            selectedLabel={timeLabel}
+            open={timeOpen}
+            setOpen={setTimeOpen}
+          >
+            {Q2_OPTIONS.map((option) => {
+              const active = state.commitment === option.commitment;
+              return (
+                <PillOption
+                  key={option.text}
+                  selected={active}
+                  onClick={() => {
+                    onChange({ ...state, commitment: active ? null : option.commitment });
+                  }}
+                >
+                  {option.text}
+                </PillOption>
+              );
+            })}
+          </QuickStartPill>
+
+          {/* My payer -- maps to payer, single select */}
+          <QuickStartPill
+            label="My payer"
+            selectedLabel={payerLabel}
+            open={payerOpen}
+            setOpen={setPayerOpen}
+          >
+            {Q3_OPTIONS.map((option) => {
+              const active = state.payer === option.payer;
+              return (
+                <PillOption
+                  key={option.id}
+                  selected={active}
+                  onClick={() => {
+                    onChange({ ...state, payer: active ? null : option.payer });
+                  }}
+                >
+                  {option.text}
+                </PillOption>
+              );
+            })}
+          </QuickStartPill>
+        </div>
+      </div>
+
+      {/* Separator */}
+      <div className="border-t border-border/40 pt-4">
+        <p className="text-[11px] font-medium text-muted">Or refine below</p>
+      </div>
+
       {/* Every group named an attribute, so nothing on screen said what clicking one would DO.
           One sentence, and the count already sitting beside each option explains itself. */}
       <p className="text-xs leading-relaxed text-muted">
diff --git a/store_platform/src/Store.Web/src/components/discovery/Matchmaker.tsx b/store_platform/src/Store.Web/src/components/discovery/Matchmaker.tsx
index 2bf9789..8c5b2d5 100644
--- a/store_platform/src/Store.Web/src/components/discovery/Matchmaker.tsx
+++ b/store_platform/src/Store.Web/src/components/discovery/Matchmaker.tsx
@@ -55,7 +55,7 @@ import { FacetChips } from './FacetChips';
  * Strip, whose dossier names a Shopify build in so many words). It is simply no longer the
  * dumping ground for "nothing".
  */
-const Q1_OPTIONS: ReadonlyArray<{ text: string; advantage: Advantage | null }> = [
+export const Q1_OPTIONS: ReadonlyArray<{ text: string; advantage: Advantage | null }> = [
   { text: 'I can build software', advantage: 'code' },
   { text: 'I can sell', advantage: 'sales' },
   { text: 'I can run operations', advantage: 'ops' },
@@ -63,7 +63,7 @@ const Q1_OPTIONS: ReadonlyArray<{ text: string; advantage: Advantage | null }> =
   { text: 'None of these yet', advantage: null },
 ];
 
-const Q2_OPTIONS: ReadonlyArray<{ text: string; commitment: Commitment }> = [
+export const Q2_OPTIONS: ReadonlyArray<{ text: string; commitment: Commitment }> = [
   { text: 'Evenings and weekends', commitment: 'evenings' },
   { text: 'Part time, ~20 hrs', commitment: 'part_time' },
   { text: 'Full time, this is the plan', commitment: 'full_time' },
@@ -74,7 +74,7 @@ const Q2_OPTIONS: ReadonlyArray<{ text: string; commitment: Commitment }> = [
  * own id so "Don't mind" can be a *chosen* answer that looks chosen, distinct from Q3 being
  * skipped; both produce the same `null` in the scored answers.
  */
-const Q3_OPTIONS: ReadonlyArray<{ id: string; text: string; payer: Payer | null }> = [
+export const Q3_OPTIONS: ReadonlyArray<{ id: string; text: string; payer: Payer | null }> = [
   { id: 'b2b', text: 'Businesses', payer: 'b2b' },
   { id: 'b2c', text: 'Consumers', payer: 'b2c' },
   { id: 'b2g', text: 'Councils and public bodies', payer: 'b2g' },
diff --git a/store_platform/src/Store.Web/src/pages/index.tsx b/store_platform/src/Store.Web/src/pages/index.tsx
index b91a468..0785677 100644
--- a/store_platform/src/Store.Web/src/pages/index.tsx
+++ b/store_platform/src/Store.Web/src/pages/index.tsx
@@ -17,8 +17,7 @@ import { CommandPalette, SearchTrigger, useCommandPalette } from '@/components/d
 import { DiscoveryNearMiss, DiscoveryWaitlist, missLabelFor, type NearMissCandidate } from '@/components/discovery/EmptyState';
 import { AppliedFilterChips, FacetBar } from '@/components/discovery/FacetBar';
 import { FacetChips } from '@/components/discovery/FacetChips';
-import { Matchmaker, MatchmakerTrigger } from '@/components/discovery/Matchmaker';
-import { useCart } from '@/lib/cart';
+
 import { ShelfEndCapture } from '@/components/discovery/ShelfEndCapture';
 import { fetchCatalog, fetchCatalogStats, formatPrice, freshnessLabel, marketLabel, Pack, CatalogStats } from '@/lib/api/client';
 import { track } from '@/lib/analytics';
@@ -29,14 +28,11 @@ import {
   cardHeading,
   decodeDiscoveryState,
   EMPTY_DISCOVERY_STATE,
-  EMPTY_MATCH_ANSWERS,
   encodeDiscoveryState,
   filterPacks,
   isFiltered,
   nearMisses,
-  rankMatches,
   type DiscoveryState,
-  type MatchAnswers,
 } from '@/lib/discovery';
 import { DEFAULT_MARKET, groupByMarket, resolveMarket } from '@/lib/market';
 import { KIND_NOUN, shortLabel, type FacetKind } from '@/lib/facets';
@@ -470,23 +466,6 @@ function CatalogBrowser({
   const router = useRouter();
   const [state, setState] = React.useState<DiscoveryState>(initialState);
   const [sort, setSort] = React.useState<SortKey>('newest');
-  // The three-question router, closed on load. Owned here rather than inside `Matchmaker` because
-  // the control that opens it lives in the toolbar row below, not in the panel it opens.
-  const [matchOpen, setMatchOpen] = React.useState(false);
-  const cart = useCart();
-  const [matchAnswers, setMatchAnswers] = React.useState<MatchAnswers>(EMPTY_MATCH_ANSWERS);
-  const liveMatches = React.useMemo(() => rankMatches(packs, matchAnswers), [packs, matchAnswers]);
-  const hasAnswers = matchAnswers.advantages.length > 0 || matchAnswers.commitment !== null || matchAnswers.payer !== null;
-
-  // Auto-open the Matchmaker on a buyer's first visit to /, guarded against SSR by reading
-  // localStorage ONLY inside the effect (never at render time).
-  React.useEffect(() => {
-    const flag = localStorage.getItem('mumchimp.matchmaker.autoOpened.v1');
-    if (!flag && cart.ready && cart.count === 0) {
-      setMatchOpen(true);
-      localStorage.setItem('mumchimp.matchmaker.autoOpened.v1', '1');
-    }
-  }, []); // eslint-disable-line react-hooks/exhaustive-deps
   const { open, setOpen, close, triggerRef } = useCommandPalette();
 
   const apply = React.useCallback(
@@ -585,7 +564,6 @@ function CatalogBrowser({
               <div className="w-full sm:w-64">
                 <SearchTrigger onOpen={() => setOpen(true)} triggerRef={triggerRef} />
               </div>
-              {!matchOpen && <MatchmakerTrigger onOpen={() => setMatchOpen(true)} count={liveMatches.ranked.length} countLabel={hasAnswers ? 'that fit your life' : 'total'} />}
             </div>
             <div className="flex items-center gap-3 sm:justify-end">
               <span className="whitespace-nowrap text-sm font-semibold text-muted">
@@ -603,14 +581,6 @@ function CatalogBrowser({
               height for it. */}
           <AppliedFilterChips state={state} onChange={apply} className="mb-4" />
 
-          {/* Mounted only once opened, and never unmounted after, "Change my answers" on the
-              result screen has to land back on the form, not on the trigger they already used. */}
-          {matchOpen && (
-            <div className="mb-6">
-              <Matchmaker packs={packs} onShowAll={apply} onNoMatch={apply} onAnswersChange={setMatchAnswers} />
-            </div>
-          )}
-
           {visible.length > 0 ? (
             <>
               {spotlight && <SpotlightCard pack={spotlight} />}

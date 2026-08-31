---
captured: 2026-08-01T22:57:19+00:00
session: 2277c393-8aa9-4a73-86a1-ad1da74706fa
cwd: /Users/chidionyema/Documents/code/prospector
chars: 160845
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are the Architect reviewing a Builder's diff against the task contract. The project's verify command already exits 0.

TASK:
## Ultra-polish — 2026-08-01

The spec is at `specs/ultra-polish-2026-08-01.md`. **Read it in full first.** Every numbered item is the contract.

The failing test is at `store_platform/src/Store.Web/src/__tests__/ultraPolishContract.test.ts`. **Do NOT modify it.** It is protected.

### Branch & state

Working branch is `ultra-polish-2026-08-01` (already created from `main`). Runtime artifacts are dirty — **DO NOT `git add` or commit any of those.** Only `git add` the files you intend to change.

### Procedure — one commit

Four changes across three source files.

**1. Print styles — `styles/globals.css`**

Add a `@media print { }` block at the end of the file. Inside:
- `header, footer { display: none; }`
- `body { font-size: 12pt; color: black; }`
- Remove `max-width` constraints on the main content area: `[class*="max-w"] { max-width: none; }`
- Strip backgrounds and shadows: `* { background: white !important; box-shadow: none !important; }`

Keep it short — 6-8 lines total.

**2. Reading time — `pages/pack/[id].tsx`**

Check if the pack data has a `wordCount` field (imported from `@/lib/api/client`). If not, skip — no reading time. If yes:
- Compute `Math.ceil(pack.wordCount / 200)` and render near the title or price: `~{mins} min read`.
- Use `<span className="font-mono text-xs text-muted">` styling.

**3. Account skeleton — `pages/account/index.tsx`**

- Import `Skeleton` from `@/components/ui`.
- Replace `"Checking your session…"` (line ~77) with three Skeleton blocks:
```tsx
<div className="space-y-4">
  <Skeleton className="h-8 w-48" />
  <Skeleton className="h-4 w-full" />
  <Skeleton className="h-4 w-3/4" />
</div>
```

**4. Share buttons — `pages/pack/[id].tsx`**

Near the breadcrumbs or title, add three icon buttons in a `flex gap-2` row:
- **Copy link** — calls `navigator.clipboard.writeText(url)`, flips a local `useState` to `true` for 2s showing "Copied ✓", then resets.
- **X** — `<a href="https://x.com/intent/tweet?text=${encodeURIComponent(pack.title)}&url=${encodeURIComponent(url)}" target="_blank" rel="noopener noreferrer">` with the X icon.
- **LinkedIn** — `<a href="https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}" target="_blank" rel="noopener noreferrer">` with the LinkedIn icon.

All three use: `rounded-full border border-border bg-white p-2 text-muted hover:text-text hover:border-text/30`.

`url` = `window.location.origin + router.asPath`. Read inside `useSyncExternalStore` (matching the pattern at `pages/orders/success.tsx:46-49`) to keep SSR clean.

Do NOT create a new component file — inline in `pack/[id].tsx`.

### Verify command (only exit 0 is "done")

Run from `store_platform/src/Store.Web`:
```
npm test -- --run && npm run verify && npm run build
```
End with `echo "ULTRA_POLISH_OK"` on success.

### When you finish

Print the commit SHA, the changed files, the verify-chain output last ~20 lines, and `ULTRA_POLISH_OK` confirmed.

Judge whether the diff fully and correctly satisfies the task with no scope creep, no security/correctness regressions, and adequate tests. Respond with a FIRST LINE of exactly "VERDICT: APPROVE" or "VERDICT: REJECT", then a brief rationale.

--- git diff ---
diff --git a/storage/durable_ledger.md b/storage/durable_ledger.md
index 108d07d..855f950 100644
--- a/storage/durable_ledger.md
+++ b/storage/durable_ledger.md
@@ -831,4 +831,76 @@
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
+* LAW: Do not build wrappers on transparent markets.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not build wrappers on transparent markets.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not build wrappers on transparent markets.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not build wrappers on transparent markets.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not build wrappers on transparent markets.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not build wrappers on transparent markets.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
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
index f4229a6..4957bf9 100644
--- a/store/control_center/config_history.jsonl
+++ b/store/control_center/config_history.jsonl
@@ -550,3 +550,31 @@ backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidi
 hash: 78814b94251c
 moat_affecting: false
 ts: '2026-07-31T02:44:57.846125+00:00'
+backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidionyema/pytest-612/test_write_config_creates_back0/backups/config.yaml.bak.20260801T205359
+hash: 78814b94251c
+moat_affecting: false
+ts: '2026-08-01T20:53:59.430474+00:00'
+backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidionyema/pytest-613/test_write_config_creates_back0/backups/config.yaml.bak.20260801T215333
+hash: 78814b94251c
+moat_affecting: false
+ts: '2026-08-01T21:53:33.400530+00:00'
+backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidionyema/pytest-614/test_write_config_creates_back0/backups/config.yaml.bak.20260801T215711
+hash: 78814b94251c
+moat_affecting: false
+ts: '2026-08-01T21:57:11.940905+00:00'
+backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidionyema/pytest-617/test_write_config_creates_back0/backups/config.yaml.bak.20260801T222551
+hash: 78814b94251c
+moat_affecting: false
+ts: '2026-08-01T22:25:51.886766+00:00'
+backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidionyema/pytest-628/test_write_config_creates_back0/backups/config.yaml.bak.20260801T224453
+hash: 78814b94251c
+moat_affecting: false
+ts: '2026-08-01T22:44:53.523595+00:00'
+backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidionyema/pytest-634/test_write_config_creates_back0/backups/config.yaml.bak.20260801T225018
+hash: 78814b94251c
+moat_affecting: false
+ts: '2026-08-01T22:50:18.669116+00:00'
+backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidionyema/pytest-636/test_write_config_creates_back0/backups/config.yaml.bak.20260801T225249
+hash: 78814b94251c
+moat_affecting: false
+ts: '2026-08-01T22:52:49.582227+00:00'
diff --git a/store/provider_health.json b/store/provider_health.json
index 294fc00..e596b14 100644
--- a/store/provider_health.json
+++ b/store/provider_health.json
@@ -33,5 +33,10 @@
     "dead_until": 1781539872.553098,
     "marked_at": 1781536272.5535092,
     "dead_for_s": 3600.0
+  },
+  "cursor_cli": {
+    "dead_until": 1785619783.360401,
+    "marked_at": 1785616183.3605602,
+    "dead_for_s": 3600.0
   }
 }
\ No newline at end of file
diff --git a/store/provider_health_noncritical.json b/store/provider_health_noncritical.json
index 9e26dfe..be2b90c 100644
--- a/store/provider_health_noncritical.json
+++ b/store/provider_health_noncritical.json
@@ -1 +1,7 @@
-{}
\ No newline at end of file
+{
+  "cursor_cli": {
+    "dead_until": 1785619807.574739,
+    "marked_at": 1785616207.575287,
+    "dead_for_s": 3600.0
+  }
+}
\ No newline at end of file
diff --git a/store/scheduler/DIAGNOSTICS_LATEST.txt b/store/scheduler/DIAGNOSTICS_LATEST.txt
index 0323b90..8a2607f 100644
--- a/store/scheduler/DIAGNOSTICS_LATEST.txt
+++ b/store/scheduler/DIAGNOSTICS_LATEST.txt
@@ -1,23 +1,25 @@
 ════════════════════════════════════════════════════════════════════════
-BATCH DIAGNOSTICS  ·  2026-07-31T02:48:11.256935+00:00
+BATCH DIAGNOSTICS  ·  2026-08-01T20:36:54.570938+00:00
 ════════════════════════════════════════════════════════════════════════
 ── Funnel (top → bottom) ──
-  generated=5  dedup_dropped=0  rejection_fastpath=0  prescreen_in=5  prescreened_out=0  novelty_selected=5  vetted=5
-── Decisions ──  PASS 2 · KILL 3 · DEFER 0 · provisional 0 (of 5 vetted)
-  kill gates: min_composite=2, moat_ungrounded=1
-── Grounding ──  unverifiable 17.1%  ·  sources/check {1: 2, 2: 1, 3: 14, 4: 7, 5: 4, 6: 7}  ·  retrieval-empty checks 0
+  generated=15  dedup_dropped=0  rejection_fastpath=0  prescreen_in=15  prescreened_out=0  novelty_selected=15  vetted=15
+── Decisions ──  PASS 5 · KILL 9 · DEFER 1 · provisional 2 (of 15 vetted)
+  kill gates: moat_ungrounded=4, min_composite=4, pain_reality=1
+── Grounding ──  unverifiable 29.5%  ·  sources/check {0: 1, 1: 2, 2: 4, 3: 5, 4: 9, 5: 20, 6: 18, 7: 8, 8: 13, 9: 6, 10: 9}  ·  retrieval-empty checks 1
 ── Per-check verdicts (supported / refuted / unverifiable) ──
-  pain_reality       sup  3 | ref  0 | unv  1
-  value_durability   sup  2 | ref  0 | unv  0
-  incumbency         sup  0 | ref  0 | unv  2
-  payer_solvency     sup  2 | ref  1 | unv  1
-  distribution       sup  3 | ref  0 | unv  1
-  legality           sup  4 | ref  0 | unv  1
-── Confidence ──  supported med=0.585 (n=21)  ·  refuted med=0.581 (n=2)  ·  unverifiable med=0.732 (n=12)
-── Composite (need ≥2.5) ──  n=4 min=1.7 med=2.675 max=2.9 · within-0.5-of-bar=3
-── Brain ──  cursor_cli=35
+  pain_reality       sup  7 | ref  2 | unv  2
+  value_durability   sup  5 | ref  0 | unv  1
+  incumbency         sup  1 | ref  0 | unv  5
+  payer_solvency     sup  7 | ref  0 | unv  8
+  distribution       sup  9 | ref  0 | unv  5
+  legality           sup  6 | ref  1 | unv  7
+── Confidence ──  supported med=0.58 (n=60)  ·  refuted med=0.58 (n=3)  ·  unverifiable med=0.643 (n=32)
+── Composite (need ≥2.5) ──  n=9 min=1.55 med=2.65 max=3.5 · within-0.5-of-bar=8
+── Brain ──  claude_cli=85, minimax=9, ?=1
 ── Closest-to-pass kills ──
-  2.45  BandBreak — the gig worker's fixed-fee council tax reduction claim service
-  1.70  OverpayGuard — gets you back the student loan money you didn’t know you overpaid
-── PASSES ──  RateGuard – the tool that catches unfair gig ratings and gets them overturned; CureSafe Strip — the gel nail tech’s lamp-output test card that shows when curing power drops below safe levels
-── Cost ──  {'total': {'calls': 185, 'web_calls': 149, 'input': 171222, 'output': 100267, 'total': 271489, 'cached': 0, 'self_corrections': 1}, 'total_cost_usd': 0.1565, 'by_phase': {'main': {'calls': 27, 'web_calls': 0, 'input': 152819, 'output': 77353, 'total': 230172, 'cached': 0, 'self_corrections': 1}, 'vetting': {'calls': 158, 'web_calls': 149, 'input': 18403, 'output': 22914, 'total': 41317, 'cached': 0, 'self_corrections': 0}}, 'by_provider': {'deepseek': {'calls': 35, 'web_calls': 0, 'input': 171222, 'output': 100267, 'total': 271489, 'cached': 0, 'self_corrections': 0, 'cost_usd': 0.156524}, 'fallback(deepseek+cursor_cli+minimax)': {'calls': 1, 'web_calls': 0, 'input': 0, 'output': 0, 'total': 0, 'cached': 0, 'self_corrections': 1, 'cost_usd': 0.0}, 'cache': {'calls': 70, 'web_calls': 0, 'input': 0, 'output': 0, 'total': 0, 'cached': 0, 'self_corrections': 0, 'cost_usd': 0.0}, 'ddg': {'calls': 9, 'web_calls': 0, 'input': 0, 'output': 0, 'total': 0, 'cached': 0, 'self_corrections': 0, 'cost_usd': 0.0}, 'exa': {'calls': 70, 'web_calls': 0, 'input': 0, 'output': 0, 'total': 0, 'cached': 0, 'self_corrections': 0, 'cost_usd': 0.0}}}
\ No newline at end of file
+  2.75  LicenceLadder – the small business tool that keeps your local licenses current across every city you work in, so you never pay a late fee
+  2.65  CareForward — upfront cash for a share of your future caregiving wages
+  2.25  ImageAudit — find every stolen image and send a license demand, for one flat fee
+  1.55  RideCheck — a mobile pre-purchase car inspection built for rideshare drivers in California, so you never buy a car that gets rejected by Uber or Lyft
+── PASSES ──  RespiteFunds Texas — the primary carer's fixed-fee service that finds and applies for every respite care grant in your area, so you finally get a break; StorySprout – the custom printed social story book that helps your autistic child navigate a new situation, made from your own details; ClaimCare – helps California family caregivers get a long-term care insurance claim approved, with a guided evidence builder; CCPAppeal – the fixed-fee service that uses California's privacy law to get the data behind your deactivation and win your reinstatement; CiteFight Kit — the California contractor's step-by-step tool to slash a Cal/OSHA safety fine without a lawyer
+── Cost ──  {'total': {'calls': 705, 'web_calls': 380, 'input': 1501629, 'output': 912455, 'total': 8347397, 'cached': 2596410, 'self_corrections': 4}, 'total_cost_usd': 4.1967, 'by_phase': {'main': {'calls': 196, 'web_calls': 0, 'input': 1395252, 'output': 771177, 'total': 5253441, 'cached': 1176021, 'self_corrections': 3}, 'vetting': {'calls': 509, 'web_calls': 380, 'input': 106377, 'output': 141278, 'total': 3093956, 'cached': 1420389, 'self_corrections': 1}}, 'by_provider': {'ddg': {'calls': 927, 'web_calls': 0, 'input': 0, 'output': 0, 'total': 0, 'cached': 0, 'self_corrections': 0, 'cost_usd': 0.0}, 'deepseek': {'calls': 592, 'web_calls': 0, 'input': 4919133, 'output': 2080081, 'total': 6999214, 'cached': 0, 'self_corrections': 0, 'cost_usd': 3.616255}, 'cache': {'calls': 926, 'web_calls': 0, 'input': 0, 'output': 0, 'total': 0, 'cached': 0, 'self_corrections': 0, 'cost_usd': 0.0}, 'fallback(deepseek+cursor_cli+minimax)': {'calls': 5, 'web_calls': 0, 'input': 0, 'output': 0, 'total': 0, 'cached': 0, 'self_corrections': 5, 'cost_usd': 0.0}, 'fallback(cursor_cli+claude_cli)': {'calls': 2, 'web_calls': 0, 'input': 0, 'output': 0, 'total': 0, 'cached': 0, 'self_corrections': 2, 'cost_usd': 0.0}, 'unknown': {'calls': 379, 'web_calls': 0, 'input': 758, 'output': 721312, 'total': 13089632, 'cached': 5799732, 'self_corrections': 0, 'cost_usd': 0.0}, 'fallback(cursor_cli+claude_cli+minimax)': {'calls': 14, 'web_calls': 0, 'input': 0, 'output': 0, 'total': 0, 'cached': 0, 'self_corrections': 14, 'cost_usd': 0.0}, 'minimax': {'calls': 321, 'web_calls': 0, 'input': 1451245, 'output': 483601, 'total': 1934846, 'cached': 0, 'self_corrections': 0, 'cost_usd': 0.580454}}}
\ No newline at end of file
diff --git a/store/scheduler/batch_diagnostics.jsonl b/store/scheduler/batch_diagnostics.jsonl
index c5c2c0e..42b65e5 100644
--- a/store/scheduler/batch_diagnostics.jsonl
+++ b/store/scheduler/batch_diagnostics.jsonl
@@ -76,3 +76,4 @@
 {"ts": "2026-07-31T01:25:03.714483+00:00", "thresholds": {"confidence_floor": 0.0, "min_composite_to_pass": 2.5}, "by_market": {"uk": {"vetted": 5, "pass": 1, "kill": 4, "defer": 0, "checks": 30, "unverifiable_pct": 63.3, "retrieval_empty_checks": 0, "kill_gates": {"moat_ungrounded": 3, "min_composite": 1}}}, "funnel": {"generated": 5, "dedup_dropped": 0, "rejection_fastpath": 0, "prescreen_in": 5, "prescreened_out": 0, "novelty_selected": 5, "vetted": 5}, "decisions": {"pass": 1, "kill": 4, "defer": 0, "vetted": 5, "provisional": 0}, "kill_gates": {"moat_ungrounded": 3, "min_composite": 1}, "verdict_matrix": {"pain_reality": {"unverifiable": 4, "supported": 1}, "value_durability": {"supported": 3, "unverifiable": 2}, "incumbency": {"unverifiable": 5}, "payer_solvency": {"unverifiable": 3, "supported": 2}, "distribution": {"unverifiable": 2, "supported": 3}, "legality": {"unverifiable": 3, "supported": 2}}, "unverifiable_pct": 63.3, "sources_per_check": {"1": 2, "2": 3, "3": 3, "4": 4, "5": 6, "6": 12}, "retrieval_failed_checks": 0, "confidence": {"supported": {"n": 11, "min": 0.15, "med": 0.61, "max": 0.7, "mean": 0.501}, "refuted": {"n": 0}, "unverifiable": {"n": 19, "min": 0.38, "med": 0.7, "max": 0.76, "mean": 0.673}}, "providers": {"cursor_cli": 30}, "composite": {"n": 2, "min": 1.3, "med": 2.3, "max": 3.3, "mean": 2.3, "near_bar_within_0.5": 1}, "closest_kills": [[1.3, "TipGhost Round \u2014 The under-27 hospitality worker's tip-pool reconstruction pack"]], "passes": ["PitchBrief \u2014 The mobile street trader's multi-borough licence renewal engine"], "usage": {"total": {"calls": 148, "web_calls": 120, "input": 238752, "output": 87514, "total": 326266, "cached": 0, "self_corrections": 0}, "total_cost_usd": 0.1607, "by_phase": {"main": {"calls": 21, "web_calls": 0, "input": 226148, "output": 66287, "total": 292435, "cached": 0, "self_corrections": 0}, "vetting": {"calls": 127, "web_calls": 120, "input": 12604, "output": 21227, "total": 33831, "cached": 0, "self_corrections": 0}}, "by_provider": {"ddg": {"calls": 61, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 0, "cost_usd": 0.0}, "deepseek": {"calls": 28, "web_calls": 0, "input": 238752, "output": 87514, "total": 326266, "cached": 0, "self_corrections": 0, "cost_usd": 0.160728}, "cache": {"calls": 60, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 0, "cost_usd": 0.0}}}}
 {"ts": "2026-07-31T02:28:21.042606+00:00", "thresholds": {"confidence_floor": 0.0, "min_composite_to_pass": 2.5}, "by_market": {"uk": {"vetted": 5, "pass": 1, "kill": 4, "defer": 0, "checks": 35, "unverifiable_pct": 60.0, "retrieval_empty_checks": 0, "kill_gates": {"min_composite": 2, "moat_ungrounded": 2}}}, "funnel": {"generated": 5, "dedup_dropped": 0, "rejection_fastpath": 0, "prescreen_in": 5, "prescreened_out": 0, "novelty_selected": 5, "vetted": 5}, "decisions": {"pass": 1, "kill": 4, "defer": 0, "vetted": 5, "provisional": 0}, "kill_gates": {"min_composite": 2, "moat_ungrounded": 2}, "verdict_matrix": {"pain_reality": {"supported": 2, "unverifiable": 2}, "value_durability": {"unverifiable": 1, "supported": 1}, "incumbency": {"unverifiable": 2}, "payer_solvency": {"unverifiable": 4, "supported": 1}, "distribution": {"unverifiable": 3, "supported": 2}, "legality": {"unverifiable": 3, "supported": 2}}, "unverifiable_pct": 42.9, "sources_per_check": {"2": 4, "3": 7, "4": 4, "5": 7, "6": 13}, "retrieval_failed_checks": 0, "confidence": {"supported": {"n": 14, "min": 0.37, "med": 0.571, "max": 0.722, "mean": 0.547}, "refuted": {"n": 0}, "unverifiable": {"n": 21, "min": 0.35, "med": 0.7, "max": 0.73, "mean": 0.67}}, "providers": {"cursor_cli": 35}, "composite": {"n": 3, "min": 0.55, "med": 2.7, "max": 2.7, "mean": 1.983, "near_bar_within_0.5": 2}, "closest_kills": [[2.7, "ShiftCast \u2014 the delivery rider\u2019s real\u2011time earnings\u2011forecast tool for switching between apps"], [0.55, "PunctureFix \u2014 mobile bicycle roadside repair that gets delivery riders back on the road in 30 minutes"]], "passes": ["NailDesk COSHH \u2013 The self-employed nail tech's ready-to-print COSHH pack"], "usage": {"total": {"calls": 173, "web_calls": 140, "input": 163551, "output": 112052, "total": 275603, "cached": 0, "self_corrections": 0}, "total_cost_usd": 0.1674, "by_phase": {"main": {"calls": 25, "web_calls": 0, "input": 145997, "output": 90088, "total": 236085, "cached": 0, "self_corrections": 0}, "vetting": {"calls": 148, "web_calls": 140, "input": 17554, "output": 21964, "total": 39518, "cached": 0, "self_corrections": 0}}, "by_provider": {"deepseek": {"calls": 33, "web_calls": 0, "input": 163551, "output": 112052, "total": 275603, "cached": 0, "self_corrections": 0, "cost_usd": 0.167416}, "cache": {"calls": 70, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 0, "cost_usd": 0.0}, "ddg": {"calls": 70, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 0, "cost_usd": 0.0}}}}
 {"ts": "2026-07-31T02:48:11.256935+00:00", "thresholds": {"confidence_floor": 0.0, "min_composite_to_pass": 2.5}, "by_market": {"uk": {"vetted": 5, "pass": 2, "kill": 3, "defer": 0, "checks": 35, "unverifiable_pct": 34.3, "retrieval_empty_checks": 0, "kill_gates": {"min_composite": 2, "moat_ungrounded": 1}}}, "funnel": {"generated": 5, "dedup_dropped": 0, "rejection_fastpath": 0, "prescreen_in": 5, "prescreened_out": 0, "novelty_selected": 5, "vetted": 5}, "decisions": {"pass": 2, "kill": 3, "defer": 0, "vetted": 5, "provisional": 0}, "kill_gates": {"min_composite": 2, "moat_ungrounded": 1}, "verdict_matrix": {"pain_reality": {"supported": 3, "unverifiable": 1}, "value_durability": {"supported": 2}, "incumbency": {"unverifiable": 2}, "payer_solvency": {"supported": 2, "unverifiable": 1, "refuted": 1}, "distribution": {"supported": 3, "unverifiable": 1}, "legality": {"supported": 4, "unverifiable": 1}}, "unverifiable_pct": 17.1, "sources_per_check": {"1": 2, "2": 1, "3": 14, "4": 7, "5": 4, "6": 7}, "retrieval_failed_checks": 0, "confidence": {"supported": {"n": 21, "min": 0.16, "med": 0.585, "max": 0.712, "mean": 0.532}, "refuted": {"n": 2, "min": 0.58, "med": 0.581, "max": 0.583, "mean": 0.581}, "unverifiable": {"n": 12, "min": 0.58, "med": 0.732, "max": 0.76, "mean": 0.711}}, "providers": {"cursor_cli": 35}, "composite": {"n": 4, "min": 1.7, "med": 2.675, "max": 2.9, "mean": 2.487, "near_bar_within_0.5": 3}, "closest_kills": [[2.45, "BandBreak \u2014 the gig worker's fixed-fee council tax reduction claim service"], [1.7, "OverpayGuard \u2014 gets you back the student loan money you didn\u2019t know you overpaid"]], "passes": ["RateGuard \u2013 the tool that catches unfair gig ratings and gets them overturned", "CureSafe Strip \u2014 the gel nail tech\u2019s lamp-output test card that shows when curing power drops below safe levels"], "usage": {"total": {"calls": 185, "web_calls": 149, "input": 171222, "output": 100267, "total": 271489, "cached": 0, "self_corrections": 1}, "total_cost_usd": 0.1565, "by_phase": {"main": {"calls": 27, "web_calls": 0, "input": 152819, "output": 77353, "total": 230172, "cached": 0, "self_corrections": 1}, "vetting": {"calls": 158, "web_calls": 149, "input": 18403, "output": 22914, "total": 41317, "cached": 0, "self_corrections": 0}}, "by_provider": {"deepseek": {"calls": 35, "web_calls": 0, "input": 171222, "output": 100267, "total": 271489, "cached": 0, "self_corrections": 0, "cost_usd": 0.156524}, "fallback(deepseek+cursor_cli+minimax)": {"calls": 1, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 1, "cost_usd": 0.0}, "cache": {"calls": 70, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 0, "cost_usd": 0.0}, "ddg": {"calls": 9, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 0, "cost_usd": 0.0}, "exa": {"calls": 70, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 0, "cost_usd": 0.0}}}}
+{"ts": "2026-08-01T20:36:54.570938+00:00", "thresholds": {"confidence_floor": 0.0, "min_composite_to_pass": 2.5}, "by_market": {"us": {"vetted": 15, "pass": 5, "kill": 9, "defer": 1, "checks": 95, "unverifiable_pct": 33.7, "retrieval_empty_checks": 1, "kill_gates": {"moat_ungrounded": 4, "min_composite": 4, "pain_reality": 1}}}, "funnel": {"generated": 15, "dedup_dropped": 0, "rejection_fastpath": 0, "prescreen_in": 15, "prescreened_out": 0, "novelty_selected": 15, "vetted": 15}, "decisions": {"pass": 5, "kill": 9, "defer": 1, "vetted": 15, "provisional": 2}, "kill_gates": {"moat_ungrounded": 4, "min_composite": 4, "pain_reality": 1}, "verdict_matrix": {"pain_reality": {"refuted": 2, "supported": 7, "unverifiable": 2}, "value_durability": {"supported": 5, "unverifiable": 1}, "incumbency": {"unverifiable": 5, "supported": 1}, "payer_solvency": {"unverifiable": 8, "supported": 7}, "distribution": {"unverifiable": 5, "supported": 9}, "legality": {"unverifiable": 7, "supported": 6, "refuted": 1}}, "unverifiable_pct": 29.5, "sources_per_check": {"0": 1, "1": 2, "2": 4, "3": 5, "4": 9, "5": 20, "6": 18, "7": 8, "8": 13, "9": 6, "10": 9}, "retrieval_failed_checks": 1, "confidence": {"supported": {"n": 60, "min": 0.13, "med": 0.58, "max": 0.76, "mean": 0.545}, "refuted": {"n": 3, "min": 0.244, "med": 0.58, "max": 0.64, "mean": 0.488}, "unverifiable": {"n": 32, "min": 0.0, "med": 0.643, "max": 0.733, "mean": 0.597}}, "providers": {"claude_cli": 85, "minimax": 9, "?": 1}, "composite": {"n": 9, "min": 1.55, "med": 2.65, "max": 3.5, "mean": 2.639, "near_bar_within_0.5": 8}, "closest_kills": [[2.75, "LicenceLadder \u2013 the small business tool that keeps your local licenses current across every city you work in, so you never pay a late fee"], [2.65, "CareForward \u2014 upfront cash for a share of your future caregiving wages"], [2.25, "ImageAudit \u2014 find every stolen image and send a license demand, for one flat fee"], [1.55, "RideCheck \u2014 a mobile pre-purchase car inspection built for rideshare drivers in California, so you never buy a car that gets rejected by Uber or Lyft"]], "passes": ["RespiteFunds Texas \u2014 the primary carer's fixed-fee service that finds and applies for every respite care grant in your area, so you finally get a break", "StorySprout \u2013 the custom printed social story book that helps your autistic child navigate a new situation, made from your own details", "ClaimCare \u2013 helps California family caregivers get a long-term care insurance claim approved, with a guided evidence builder", "CCPAppeal \u2013 the fixed-fee service that uses California's privacy law to get the data behind your deactivation and win your reinstatement", "CiteFight Kit \u2014 the California contractor's step-by-step tool to slash a Cal/OSHA safety fine without a lawyer"], "usage": {"total": {"calls": 705, "web_calls": 380, "input": 1501629, "output": 912455, "total": 8347397, "cached": 2596410, "self_corrections": 4}, "total_cost_usd": 4.1967, "by_phase": {"main": {"calls": 196, "web_calls": 0, "input": 1395252, "output": 771177, "total": 5253441, "cached": 1176021, "self_corrections": 3}, "vetting": {"calls": 509, "web_calls": 380, "input": 106377, "output": 141278, "total": 3093956, "cached": 1420389, "self_corrections": 1}}, "by_provider": {"ddg": {"calls": 927, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 0, "cost_usd": 0.0}, "deepseek": {"calls": 592, "web_calls": 0, "input": 4919133, "output": 2080081, "total": 6999214, "cached": 0, "self_corrections": 0, "cost_usd": 3.616255}, "cache": {"calls": 926, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 0, "cost_usd": 0.0}, "fallback(deepseek+cursor_cli+minimax)": {"calls": 5, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 5, "cost_usd": 0.0}, "fallback(cursor_cli+claude_cli)": {"calls": 2, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 2, "cost_usd": 0.0}, "unknown": {"calls": 379, "web_calls": 0, "input": 758, "output": 721312, "total": 13089632, "cached": 5799732, "self_corrections": 0, "cost_usd": 0.0}, "fallback(cursor_cli+claude_cli+minimax)": {"calls": 14, "web_calls": 0, "input": 0, "output": 0, "total": 0, "cached": 0, "self_corrections": 14, "cost_usd": 0.0}, "minimax": {"calls": 321, "web_calls": 0, "input": 1451245, "output": 483601, "total": 1934846, "cached": 0, "self_corrections": 0, "cost_usd": 0.580454}}}}
diff --git a/store_platform/src/Store.Web/src/data/kill-log-totals.json b/store_platform/src/Store.Web/src/data/kill-log-totals.json
index 52f799e..d2c747a 100644
--- a/store_platform/src/Store.Web/src/data/kill-log-totals.json
+++ b/store_platform/src/Store.Web/src/data/kill-log-totals.json
@@ -1,20 +1,20 @@
 {
-  "killed": 960,
-  "passed": 103,
+  "killed": 1080,
+  "passed": 129,
   "shown": 60,
   "byGate": {
-    "min_composite": 511,
+    "min_composite": 551,
     "adversarial_decisive": 154,
-    "incumbency": 146,
-    "value_durability": 47,
-    "moat_ungrounded": 43,
-    "payer_solvency": 22,
-    "legality": 9,
+    "incumbency": 150,
+    "moat_ungrounded": 92,
+    "value_durability": 54,
+    "payer_solvency": 25,
+    "source_or_die": 16,
+    "legality": 12,
+    "pain_reality": 7,
     "route_to_market": 6,
-    "source_or_die": 5,
-    "pain_reality": 5,
     "currency": 5,
-    "distribution": 4,
+    "distribution": 5,
     "buyer_intent": 3
   }
 }
diff --git a/store_platform/src/Store.Web/src/data/kill-log.json b/store_platform/src/Store.Web/src/data/kill-log.json
index 91320b6..552491f 100644
--- a/store_platform/src/Store.Web/src/data/kill-log.json
+++ b/store_platform/src/Store.Web/src/data/kill-log.json
@@ -1,28 +1,161 @@
 {
-  "generatedAt": "2026-07-31T16:32:13+00:00",
+  "generatedAt": "2026-08-01T22:57:08+00:00",
   "totals": {
-    "killed": 960,
-    "passed": 103,
+    "killed": 1080,
+    "passed": 129,
     "shown": 60,
     "byGate": {
-      "min_composite": 511,
+      "min_composite": 551,
       "adversarial_decisive": 154,
-      "incumbency": 146,
-      "value_durability": 47,
-      "moat_ungrounded": 43,
-      "payer_solvency": 22,
-      "legality": 9,
+      "incumbency": 150,
+      "moat_ungrounded": 92,
+      "value_durability": 54,
+      "payer_solvency": 25,
+      "source_or_die": 16,
+      "legality": 12,
+      "pain_reality": 7,
       "route_to_market": 6,
-      "source_or_die": 5,
-      "pain_reality": 5,
       "currency": 5,
-      "distribution": 4,
+      "distribution": 5,
       "buyer_intent": 3
     }
   },
   "entries": [
     {
-      "title": "AssessAid — the carer's statutory assessment evidence dossier builder",
+      "title": "WEP Watch, your Texas-sized forecast of the Windfall Elimination bite before you claim",
+      "oneLiner": "A personalized data brief that shows how much the SSA will cut your Social Security under the Windfall Elimination Provision and the real odds of overturning it.",
+      "gate": "value_durability",
+      "gateLabel": "The value would not last",
+      "reason": "Passages state WEP was repealed on January 5, 2025 under the Social Security Fairness Act, with SSA recalculating benefits afterward. The product’s core value, forecasting ongoing WEP cuts and appeal paths, therefore no longer rests on a live reduction rule.",
+      "citations": [],
+      "date": "2026-08-01"
+    },
+    {
+      "title": "PropTax Appeal Kit, your DIY property tax appeal report for California homeowners",
+      "oneLiner": "A step-by-step tool that pulls recent home sales to build an evidence-backed case for a lower property tax assessment, saving thousands without a lawyer.",
+      "gate": "value_durability",
+      "gateLabel": "The value would not last",
+      "reason": "Passages already offer free California appeal templates and comparable-property worksheets, free DIY guides that teach pulling comps and building an appeal-ready analysis, and a free AI appraisal plus a complete DIY appeal kit with letter, comps, and filing guide. That means the paid one-off report package is already available at no cost, so there is no lasting paid margin left for this offering.",
+      "citations": [],
+      "date": "2026-08-01"
+    },
+    {
+      "title": "BackMile, The gig worker's missed-deduction reclaim service. For a fixed fee, we dig through your last 3 years of platform earnings, file amended returns, and get you back what the IRS owes.",
+      "oneLiner": "We find every missed business deduction in your past 3 years of Uber, DoorDash, or Instacart work and file amended returns to get your money back.",
+      "gate": "incumbency",
+      "gateLabel": "Incumbents already own the space",
+      "reason": "TurboTax is repeatedly cited as a dominant incumbent that already offers exactly the overlapping capability: free support for independent contractors with hundreds of built-in deductions, tutorials for amending returns on Form 1040-X, and TurboTax Experts available 24/7 to identify missed deductions and file amended returns. That footprint, a market-leading tax-prep brand with dedicated contractor tooling and expert-assisted amendment services, is a clear market leader with dominant share in the space BackMile targets, satisfying the incumbency refutation threshold.",
+      "citations": [],
+      "date": "2026-08-01"
+    },
+    {
+      "title": "BandShift, the primary carer's fixed-fee council tax band appeal broker",
+      "oneLiner": "Appeals your home’s council tax band using real Valuation Office Agency decision data, so you pay only if you save.",
+      "gate": "payer_solvency",
+      "gateLabel": "The payer cannot actually pay",
+      "reason": "Passages on unpaid carers, the named payer, show sharply elevated poverty and financial hardship, including deep poverty for about one in ten carers and poverty rates far above non-carers. That portrays this payer group as often unable to fund discretionary spend, so the claim that they can and will pay does not hold on this evidence.",
+      "citations": [],
+      "date": "2026-08-01"
+    },
+    {
+      "title": "ClassSync, the student gig worker’s schedule blocker that silences delivery pings during class and turns you on for the good windows",
+      "oneLiner": "For students juggling gig apps and classes, ClassSync syncs your syllabus to your delivery platforms so you never miss a tip-out window because of a lecture.",
+      "gate": "pain_reality",
+      "gateLabel": "The pain was not real",
+      "reason": "The passages say DoorDash drivers can freely turn down any order, that declining boosted 'Flash Offers' while offline carries no penalty, and that ending a dash early incurs no direct penalty, so simply ignoring the phone during a lecture is a free workaround, and none of the passages describe drivers losing money or status because of scheduled commitments. Nothing here mentions students, class schedules, or anyone paying to automate availability, so the acute, paid-for pain the product assumes is not shown and the penalty it claims to pr",
+      "citations": [
+        {
+          "url": "https://www.ridesharingdriver.com/doordash-pause-dash-acceptance/",
+          "domain": "ridesharingdriver.com"
+        },
+        {
+          "url": "https://help.doordash.com/en-us/dashers/article/flash-offers",
+          "domain": "help.doordash.com"
+        },
+        {
+          "url": "https://climbtheladder.com/can-you-end-a-dash-early-without-penalty/",
+          "domain": "climbtheladder.com"
+        }
+      ],
+      "date": "2026-08-01"
+    },
+    {
+      "title": "AlertBadge, the clip‑on badge that hears a situation turning hostile and keeps a safe record, for NHS and council staff who deal with the public",
+      "oneLiner": "A wearable device that listens for aggression in real time and secures audio evidence without you pressing a button.",
+      "gate": "legality",
+      "gateLabel": "There is a legal landmine",
+      "reason": "Passages state that covert recordings by staff are not permitted and that covert or secret recording may be treated as gross misconduct. The badge’s paid value for NHS and similar public-facing staff is a discreet device that starts capturing audio without the wearer taking an overt step, which is exactly the covert recording those rules forbid.",
+      "citations": [],
+      "date": "2026-08-01"
+    },
+    {
+      "title": "GrabSure, same-day grab rail installation for older people, so you don't wait months for the council to make your home safe after a fall",
+      "oneLiner": "Same-day grab rail installation for older people, so you don't have to wait months for the council to make your home safe after a fall or hospital stay.",
+      "gate": "payer_solvency",
+      "gateLabel": "The payer cannot actually pay",
+      "reason": "One passage states that minor home adaptations costing under £1,000, which a roughly £200 grab rail fit would be, are usually paid for free by the local council, so the individual has little motive to pay out of pocket, with further material on grants available to cover adaptation costs. The passages on pensioner finances also show many older people are stretched: one in seven has fallen behind on bills or rent, some using payday loans or skipping meals, and a quarter of renting pensioners are behind on energy bills [8",
+      "citations": [
+        {
+          "url": "https://www.homecare.co.uk/advice/how-do-i-pay-for-home-adaptations",
+          "domain": "homecare.co.uk"
+        },
+        {
+          "url": "https://www.independentage.org/get-advice/housing/home-adaptations",
+          "domain": "independentage.org"
+        },
+        {
+          "url": "https://www.gbnews.com/money/retirement-state-pension-poverty-low-income",
+          "domain": "gbnews.com"
+        },
+        {
+          "url": "https://www.lbc.co.uk/article/thousands-elderly-brits-afford-basic-essentials-5HjdCwJ_2/",
+          "domain": "lbc.co.uk"
+        }
+      ],
+      "date": "2026-08-01"
+    },
+    {
+      "title": "FieldYield Max, the farm software that sizes up every SFI option for your fields and picks the best-paying mix",
+      "oneLiner": "Software that analyses your farm’s land parcels against every Sustainable Farming Incentive option and generates the highest-paying submission plan.",
+      "gate": "value_durability",
+      "gateLabel": "The value would not last",
+      "reason": "The passage from explicitly states that 'we will stop accepting new applications for SFI from today' because the sustainable farming budget has been 'successfully allocated' with record numbers of farm businesses already enrolled. This removes the primary entry point for the candidate's value proposition, helping farmers submit new optimised SFI applications, since the scheme is closed to new applicants. While mentions an SFI26 application window and shows 15-25% profit uplift, the structural closure of new SFI applications directly underm",
+      "citations": [
+        {
+          "url": "https://defrafarming.blog.gov.uk/2025/03/11/an-update-on-the-sustainable-farming-incentive/",
+          "domain": "defrafarming.blog.gov.uk"
+        },
+        {
+          "url": "https://www.gov.uk/government/collections/sustainable-farming-incentive-guidance-for-applicants-and-agreement-holders",
+          "domain": "gov.uk"
+        },
+        {
+          "url": "https://ahdb.org.uk/stacking-options-for-SFI-2026-arable",
+          "domain": "ahdb.org.uk"
+        }
+      ],
+      "date": "2026-08-01"
+    },
+    {
+      "title": "IHSS HourClaim, the primary carer's tool that builds your In-Home Supportive Services appeal packet, using the state's own rules to get the hours you're owed",
+      "oneLiner": "A web app that steps a California primary carer through a functional assessment of their loved one, then generates a ready‑to‑file IHSS fair hearing appeal packed with data‑backed arguments.",
+      "gate": "legality",
+      "gateLabel": "There is a legal landmine",
+      "reason": "The passages state that in California only licensed attorneys may practice law or give legal advice, and that doing so without a license is a crime; the tool's core offering, individually tailored legal arguments and a ready-to-file appeal packet for a specific person's hearing, is legal advice delivered by a non-attorney business, which these passages say is prohibited. The passages do not carve out any exception for software or self-help products, so on this evidence the product's value cannot be delivered lawfully by an unlicensed provider.",
+      "citations": [],
+      "date": "2026-08-01"
+    },
+    {
+      "title": "CareFee Lens, the self-funder’s window into what your council really pays for care",
+      "oneLiner": "See your local authority’s secret care home rates and use them to negotiate your own fees down to the council’s price.",
+      "gate": "value_durability",
+      "gateLabel": "The value would not last",
+      "reason": "Free league tables already publish local-authority care rates gathered by FOI across all 173 English and Welsh councils, including residential homes, and current fee-rate maps continue that coverage. That free public dataset removes the paid tool’s claimed durable edge in aggregating and selling council rates obtained the same way.",
+      "citations": [],
+      "date": "2026-07-31"
+    },
+    {
+      "title": "AssessAid, the carer's statutory assessment evidence dossier builder",
       "oneLiner": "A web app that asks a carer a series of questions and produces a personalised, legally grounded evidence pack to maximise the outcome of their Carer's Assessment under the Care Act 2014.",
       "gate": "route_to_market",
       "gateLabel": "There is no route to reach buyers",
@@ -31,7 +164,34 @@
       "date": "2026-07-31"
     },
     {
-      "title": "DecibelKit – the home noise evidence pack that makes the council act",
+      "title": "The Creative Pulse Index, a monthly briefing on where the freelance creative market is headed, built from a panel of 500 of your peers",
+      "oneLiner": "A subscription briefing that gives freelance creatives a forward‑looking index of confidence, demand and rate trends so they can plan their pipeline before the feast or famine hits.",
+      "gate": "incumbency",
+      "gateLabel": "Incumbents already own the space",
+      "reason": "IPSE, the UK's main self-employment trade body, already runs the Freelancer Confidence Index in association with Upwork, a forward-looking panel measure of freelancer business confidence that has been published quarterly since at least 2017 (sources e0638762, 8ab4672, ea9248c9). IPSE explicitly claims to be 'the UK's authoritative source on self-employment,' and the index is paired with Upwork, a well-funded platform, together a well-funded rival already serving this exact segment. Creative UK also publishes comprehensive research on the creative freelance economy (sources f10714b5, 40611c8,",
+      "citations": [],
+      "date": "2026-07-31"
+    },
+    {
+      "title": "TrendStitch, The freelance designer's monthly data brief forecasting which tools and specialties will pay in three months",
+      "oneLiner": "A paid monthly report that mines job ads, freelance platform activity and agency brief summaries to predict short-term demand for specific design skills, so you can re-skill before the market tips.",
+      "gate": "legality",
+      "gateLabel": "There is a legal landmine",
+      "reason": "The candidate relies on scraping UK job postings, and the most prominent source of UK professional job listings is LinkedIn, whose Terms of Service explicitly ban bots and scraping. A separate passage confirms that platforms hosting public personal data have obligations under UK data protection law to prevent unlawful scraping. Because the forecast model cannot operate without scraping LinkedIn job listings at scale, the service is contractually blocked from existing as described.",
+      "citations": [
+        {
+          "url": "https://connectsafely.ai/articles/is-linkedin-automation-safe-tos-scraping-guide-2026",
+          "domain": "connectsafely.ai"
+        },
+        {
+          "url": "https://ico.org.uk/media2/migrated/4026232/joint-statement-data-scraping-202308.pdf",
+          "domain": "ico.org.uk"
+        }
+      ],
+      "date": "2026-07-31"
+    },
+    {
+      "title": "DecibelKit, the home noise evidence pack that makes the council act",
       "oneLiner": "A meter, logbook and data‑backed guide that turns a neighbour noise problem into a formal complaint councils can’t ignore.",
       "gate": "value_durability",
       "gateLabel": "The value would not last",
@@ -40,7 +200,122 @@
       "date": "2026-07-31"
     },
     {
-      "title": "HeatLeak Ledger – a thermal camera home survey that gives you a report of heat leaks and the paperwork to claim government insulation grants",
+      "title": "PensionShortfall Map, the retiree’s personalised State Pension underpayment discovery brief",
+      "oneLiner": "Shows if you’re owed thousands in missing State Pension, with a ready-to-use claim pack, built from DWP’s own correction patterns.",
+      "gate": "distribution",
+      "gateLabel": "There is no route to reach buyers",
+      "reason": "The candidate relies on a self-serve web questionnaire for retirees, yet the passages show severe digital exclusion among the exact target demographic: roughly 2 million people aged 75+ in the UK do not use or rarely use the internet, and 4.7 million over-65s lack basic digital skills. This evidence directly undermines the viability of a self-serve web route to reach over-80s and digitally excluded retirees who form the core audience.",
+      "citations": [],
+      "date": "2026-07-31"
+    },
+    {
+      "title": "LicenseSafe, the pub landlord's licence review risk score and evidence pack",
+      "oneLiner": "A tool that turns your answers into a data‑backed risk score and persuasive evidence for a licensing committee hearing.",
+      "gate": "payer_solvency",
+      "gateLabel": "The payer cannot actually pay",
+      "reason": "The passages confirm the motive is real: licensing committees do hear representations and pubs face genuine hearings with existential consequences (a63083afdc0e3442, 6644305bc3145a43). However, the payer segment is in severe financial distress, hospitality is closing at a rate of four businesses per day, with 366 permanent pub losses across England and Wales in 2025 alone, and major chains collapsing (f58c3d3d4952cdd7, c175e15413ab06a0, 19d154fcef9513ac). Pubs already drawing noise complaints and review notices are likely among the more marginal operators, and the candidate's own hypothesis c",
+      "citations": [],
+      "date": "2026-07-31"
+    },
+    {
+      "title": "TribunalView, the small business owner’s employment tribunal risk assessor",
+      "oneLiner": "A tool that analyses your employee dispute and predicts the likely employment tribunal outcome and compensation cost.",
+      "gate": "value_durability",
+      "gateLabel": "The value would not last",
+      "reason": "Passage describes a free tribunal risk calculator that already asks structured questions, produces a low/medium/high risk rating, and gives an estimated financial exposure figure, essentially the same product as the candidate, but free. A free, already-deployed tool capturing this exact value removes the margin available to a paid entrant, meaning the value has been commoditised. Additionally, passages,, and confirm that the underlying outcome-prediction data corpus is publicly available (CLC-UKET), undermining any pr",
+      "citations": [
+        {
+          "url": "https://www.daisyhr.co.uk/free-hr-tools/tribunal-risk-calculator",
+          "domain": "daisyhr.co.uk"
+        },
+        {
+          "url": "https://blogs.law.ox.ac.uk/oblb/blog-post/2025/01/benchmarking-case-outcome-prediction-uk-employment-tribunal-clc-uket-dataset",
+          "domain": "blogs.law.ox.ac.uk"
+        },
+        {
+          "url": "https://arxiv.org/html/2409.08098v2",
+          "domain": "arxiv.org"
+        },
+        {
+          "url": "https://www.law.cam.ac.uk/publications/322512",
+          "domain": "law.cam.ac.uk"
+        }
+      ],
+      "date": "2026-07-31"
+    },
+    {
+      "title": "DataWipe, wipe your personal data from UK data brokers, fixed fee",
+      "oneLiner": "A done-for-you service that sends opt-out requests to hundreds of UK data brokers, so your personal data no longer gets sold.",
+      "gate": "incumbency",
+      "gateLabel": "Incumbents already own the space",
+      "reason": "Passages show Incogni and DeleteMe already submit opt-out and removal requests for UK users under UK GDPR, covering large numbers of data brokers, with Incogni rated Editors’ Choice over DeleteMe. That means paid providers already serve this exact need, so the market is not an open gap with no serious existing solution.",
+      "citations": [],
+      "date": "2026-07-31"
+    },
+    {
+      "title": "MotabilitySell, The carer’s fixed-fee Motability vehicle sale broker",
+      "oneLiner": "We sell your end-of-lease Motability car for a flat fee, handling buyer vetting, paperwork and the scheme’s strict resale rules so you keep the profit without the hassle.",
+      "gate": "pain_reality",
+      "gateLabel": "The pain was not real",
+      "reason": "Official Motability guidance states you cannot buy the Scheme vehicle at lease end, and a further passage notes that since December 2023 Motability no longer offers the hoped-for end-of-lease purchase. Without that purchase, the claimed acute problem of carers needing paid help to resell a bought Motability car does not exist now.",
+      "citations": [],
+      "date": "2026-07-31"
+    },
+    {
+      "title": "MouldBreak, the home mould survey that makes your landlord or council fix the damp",
+      "oneLiner": "A trained surveyor visits your home, takes air samples and thermal images, and gives you a report that quotes the exact legal duties your landlord or council is breaking, so they cannot ignore you.",
+      "gate": "incumbency",
+      "gateLabel": "Incumbents already own the space",
+      "reason": "Passage describes an existing service already producing Awaab's Law-compliant survey reports that are 'trusted by councils' and priced from £250+VAT, the same price band as the candidate's £199, £299 offering. Passage shows professional damp/mould survey reporting software for UK surveyors is an established category. Additionally, passages,, and show well-funded, established law firms (e.g. NJS Law with 4.8 Trustpilot) already offering tenants a no-win-no-fee route to enforce the same Awaab's Law deadl",
+      "citations": [
+        {
+          "url": "https://www.thedampandmouldman.co.uk/social-housing-mould",
+          "domain": "thedampandmouldman.co.uk"
+        },
+        {
+          "url": "https://www.dampsurvey-pro.co.uk/awaabs-law-damp-and-mould",
+          "domain": "dampsurvey-pro.co.uk"
+        },
+        {
+          "url": "https://awaabs-law.com/",
+          "domain": "awaabs-law.com"
+        },
+        {
+          "url": "https://housingrepairsolutions.co.uk/no-win-no-fee-solicitors/",
+          "domain": "housingrepairsolutions.co.uk"
+        }
+      ],
+      "date": "2026-07-31"
+    },
+    {
+      "title": "RentRewind, get back rent from unlicensed HMO landlords, fixed fee",
+      "oneLiner": "A fixed-fee service that checks if your shared house needs a licence and builds your rent repayment application.",
+      "gate": "value_durability",
+      "gateLabel": "The value would not last",
+      "reason": "The core value RentRewind offers, a licensing-status check plus a ready-to-file Rent Repayment Order pack, is already covered by free alternatives. A free licence checker covering 350+ schemes and additional free checkers (8746cfb5e4e47b22, c92b78f8310a39b9) commoditise the licensing verification step, while the government RRO1 form itself is freely downloadable from the First-tier Tribunal. With both the data lookup and the application template available at no cost, the remaining margin for a £99 productised dossier is substantially eroded.",
+      "citations": [
+        {
+          "url": "https://www.kammadata.com/kamma-licensing/property-licence-checker/",
+          "domain": "kammadata.com"
+        },
+        {
+          "url": "https://tenant-rights.uk/england/rro-success-rates-winning-rent-repayment-orders-in-england",
+          "domain": "tenant-rights.uk"
+        }
+      ],
+      "date": "2026-07-31"
+    },
+    {
+      "title": "PotholePay Kit, the car owner's instant pothole damage claim pack",
+      "oneLiner": "A smartphone‑based toolkit that captures impact evidence and compiles a compensation claim for your local council, backed by a proprietary payout database.",
+      "gate": "value_durability",
+      "gateLabel": "The value would not last",
+      "reason": "Free UK guides already teach rights, evidence gathering, and claim wording, including MoneySavingExpert tips and template letters, and an official checklist of what to tell the highway body. A further passage states pothole damage claims are meant to be straightforward and cost-free and that claimants do not need a claims management company, so a paid claim-pack’s edge is already given away for free.",
+      "citations": [],
+      "date": "2026-07-31"
+    },
+    {
+      "title": "HeatLeak Ledger, a thermal camera home survey that gives you a report of heat leaks and the paperwork to claim government insulation grants",
       "oneLiner": "A portable thermal imaging service for NHS and council staff who want independent proof of their home’s heat loss before applying for the ECO4 or Great British Insulation Scheme.",
       "gate": "value_durability",
       "gateLabel": "The value would not last",
@@ -49,11 +324,11 @@
       "date": "2026-07-30"
     },
     {
-      "title": "SaltCourt Rounds — The Council Leisure Manager's Portable Pool-Hall & Sports-Floor Slip-Coefficient Reinstatement Round",
-      "oneLiner": "A one-person mobile bench that turns up out-of-hours at school and council-run sports halls, wet-changing rooms and poolside walkways, mechanically re-tests the floor's slip resistance to the BS 7976 pendulum method, and — in the same visit — performs a measured abrasive/chemical reinstatement pass that lifts the reading back above the wet-barefoot threshold, leaving a signed before/after pendulum ledger the duty-holder can put in front of an insurer or a claimant's solicitor.",
+      "title": "SaltCourt Rounds, The Council Leisure Manager's Portable Pool-Hall & Sports-Floor Slip-Coefficient Reinstatement Round",
+      "oneLiner": "A one-person mobile bench that turns up out-of-hours at school and council-run sports halls, wet-changing rooms and poolside walkways, mechanically re-tests the floor's slip resistance to the BS 7976 pendulum method, and, in the same visit, performs a measured abrasive/chemical reinstatement pass that lifts the reading back above the wet-barefoot threshold, leaving a signed before/after pendulum ledger the duty-holder can put in front of an insurer or a claimant's solicitor.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show the UK leisure-centre slip-testing space is already served by multiple established nationwide providers — National Testing, UKAS ISO 17025 accredited pendulum testers, and Slip Safety marketing HSE-endorsed pendulum testing directly at leisure centres [183c310eaea760d6, 4a8acf678977b52a] — alongside nationwide anti-slip treatment contractors. Critically, describes a provider already bundling anti-slip treatment AND pendulum slip testing in one offering, which is the candidate's supposed structural gap",
+      "reason": "The passages show the UK leisure-centre slip-testing space is already served by multiple established nationwide providers, National Testing, UKAS ISO 17025 accredited pendulum testers, and Slip Safety marketing HSE-endorsed pendulum testing directly at leisure centres [183c310eaea760d6, 4a8acf678977b52a], alongside nationwide anti-slip treatment contractors. Critically, describes a provider already bundling anti-slip treatment AND pendulum slip testing in one offering, which is the candidate's supposed structural gap",
       "citations": [
         {
           "url": "https://www.nationaltesting.co.uk/",
@@ -75,11 +350,11 @@
       "date": "2026-07-30"
     },
     {
-      "title": "SplitCare Rebate — The Primary Carer's Council-Tax Second-Adult & Care-Occupancy Reclassification Broker",
+      "title": "SplitCare Rebate, The Primary Carer's Council-Tax Second-Adult & Care-Occupancy Reclassification Broker",
       "oneLiner": "A fixed-fee transaction broker that reconstructs a caring household's occupancy history and executes the specific council-tax reclassification claims (second-adult rebate, carer disregard, annexe/dependent-relative exemption, banding-effect adaptations) with the billing authority, charging per successful reclassification plus a slice of the backdated refund.",
       "gate": "payer_solvency",
       "gateLabel": "The payer cannot actually pay",
-      "reason": "The named payer segment — unpaid carers in caring households — is described as frequently in poverty or financial hardship, facing extra care costs and higher household bills, and increasingly unable to afford day-to-day living costs to the point of skipping meals, which contradicts the ability to pay a £145 upfront per-claim fee. Related passages frame this cohort as one needing help because it cannot afford bills including council tax, reinforcing constrained cash rather than available budget.",
+      "reason": "The named payer segment, unpaid carers in caring households, is described as frequently in poverty or financial hardship, facing extra care costs and higher household bills, and increasingly unable to afford day-to-day living costs to the point of skipping meals, which contradicts the ability to pay a £145 upfront per-claim fee. Related passages frame this cohort as one needing help because it cannot afford bills including council tax, reinforcing constrained cash rather than available budget.",
       "citations": [
         {
           "url": "https://www.carersuk.org/policy-and-research/our-areas-of-policy-work/money-and-finance/",
@@ -97,20 +372,20 @@
       "date": "2026-07-30"
     },
     {
-      "title": "ReferencePass — The Multi-App Gig Worker's Tenancy Referencing Pass-Dossier Desk",
-      "oneLiner": "A fixed-fee productized service that reconstructs a gig worker's fragmented multi-platform income into the exact evidence format each automated tenancy-referencing agency's underwriting rules will accept — before the application is submitted, so the reference passes first time.",
+      "title": "ReferencePass, The Multi-App Gig Worker's Tenancy Referencing Pass-Dossier Desk",
+      "oneLiner": "A fixed-fee productized service that reconstructs a gig worker's fragmented multi-platform income into the exact evidence format each automated tenancy-referencing agency's underwriting rules will accept, before the application is submitted, so the reference passes first time.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "Housing Hand is described as 'the UK's largest and most trusted professional rent guarantor service', having supported over 100,000 students and young working professionals and standing as guarantor for those unable to provide one — a dominant incumbent that directly resolves the exact failure the candidate monetises (applicant fails referencing and lacks a guarantor). Tenant-side help also already exists (Fraser Bond's expert guidance for those who failed referencing), so the space is not shown to be open.",
+      "reason": "Housing Hand is described as 'the UK's largest and most trusted professional rent guarantor service', having supported over 100,000 students and young working professionals and standing as guarantor for those unable to provide one, a dominant incumbent that directly resolves the exact failure the candidate monetises (applicant fails referencing and lacks a guarantor). Tenant-side help also already exists (Fraser Bond's expert guidance for those who failed referencing), so the space is not shown to be open.",
       "citations": [],
       "date": "2026-07-30"
     },
     {
-      "title": "S117Broker — The Primary Carer's Mental Health Act s.117 Aftercare Activation & Means-Test-Defence Desk",
-      "oneLiner": "A fixed-fee, per-case transaction broker for primary carers of adults detained (or previously detained) under the Mental Health Act 1983 who reactivates a free, non-means-tested Section 117 aftercare package from the local authority and Integrated Care Board — and recovers three years of illegally means-tested charges when the LA cites Care Act assessments — at £795 per case activated or 20% of charges reversed, whichever is greater.",
+      "title": "S117Broker, The Primary Carer's Mental Health Act s.117 Aftercare Activation & Means-Test-Defence Desk",
+      "oneLiner": "A fixed-fee, per-case transaction broker for primary carers of adults detained (or previously detained) under the Mental Health Act 1983 who reactivates a free, non-means-tested Section 117 aftercare package from the local authority and Integrated Care Board, and recovers three years of illegally means-tested charges when the LA cites Care Act assessments, at £795 per case activated or 20% of charges reversed, whichever is greater.",
       "gate": "payer_solvency",
       "gateLabel": "The payer cannot actually pay",
-      "reason": "Passages directly indicate primary carers are disproportionately from low-income households, receive only £81.90/week carer's allowance, and qualify for free legal aid specifically targeting low-income and disabled individuals — structurally undermining ability to pay £795+ upfront.",
+      "reason": "Passages directly indicate primary carers are disproportionately from low-income households, receive only £81.90/week carer's allowance, and qualify for free legal aid specifically targeting low-income and disabled individuals, structurally undermining ability to pay £795+ upfront.",
       "citations": [
         {
           "url": "https://carers.org/campaigning-for-change/new-research-finds-unpaid-care-has-huge-impact-on-mental-health-and-affects-low-income-households",
@@ -128,8 +403,8 @@
       "date": "2026-07-30"
     },
     {
-      "title": "AllotmentClock — The Independent Tree Surgeon & Arborist's Per-Tree Preservation Order & Conservation-Area Notice Clock",
-      "oneLiner": "A vertical tool that tells a sole-trader arborist, before quoting, exactly which of the trees at a given address are legally gated (TPO / conservation-area / felling-licence) and prints the correct notice with the correct clock — so the quote is priced with the 6-week statutory wait, not blown up by it.",
+      "title": "AllotmentClock, The Independent Tree Surgeon & Arborist's Per-Tree Preservation Order & Conservation-Area Notice Clock",
+      "oneLiner": "A vertical tool that tells a sole-trader arborist, before quoting, exactly which of the trees at a given address are legally gated (TPO / conservation-area / felling-licence) and prints the correct notice with the correct clock, so the quote is priced with the 6-week statutory wait, not blown up by it.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
       "reason": "A UK-wide interactive TPO map already lets anyone check by postcode whether trees are protected before starting work, and Arb Quotes already occupies the tree-work quoting workflow this tool would sit inside, so both halves of the wedge are served by existing national-scale products rather than an open space.",
@@ -146,20 +421,20 @@
       "date": "2026-07-30"
     },
     {
-      "title": "KerbRound — The Primary Carer's Multi-Borough PCN Cancellation & Carer-Permit Stack Broker",
-      "oneLiner": "A no-cancel-no-fee transaction broker that kills the parking, bus-lane and moving-traffic penalties a family carer racks up on their daily care round, then re-plans the round onto a stack of discretionary carer/health-worker permits and low-enforcement kerb space — priced per PCN cancelled and per permit granted.",
+      "title": "KerbRound, The Primary Carer's Multi-Borough PCN Cancellation & Carer-Permit Stack Broker",
+      "oneLiner": "A no-cancel-no-fee transaction broker that kills the parking, bus-lane and moving-traffic penalties a family carer racks up on their daily care round, then re-plans the round onto a stack of discretionary carer/health-worker permits and low-enforcement kerb space, priced per PCN cancelled and per permit granted.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show the PCN-appeal transaction is already occupied at scale by a free incumbent — DoNotPay, which has successfully challenged 160,000 parking tickets (~$4m) in London and New York and is marketed as making appeals effortless — and by an existing no-win-no-fee parking-ticket appeal operator using the identical pricing model KerbRound proposes. That is a free dominant-volume service plus a direct commercial rival on the same segment, not an open space.",
+      "reason": "The passages show the PCN-appeal transaction is already occupied at scale by a free incumbent, DoNotPay, which has successfully challenged 160,000 parking tickets (~$4m) in London and New York and is marketed as making appeals effortless, and by an existing no-win-no-fee parking-ticket appeal operator using the identical pricing model KerbRound proposes. That is a free dominant-volume service plus a direct commercial rival on the same segment, not an open space.",
       "citations": [],
       "date": "2026-07-30"
     },
     {
-      "title": "BedFall Bench — The Independent Care-Home Owner's Per-Bedroom Furniture Entrapment & Gap-Measurement Bench",
-      "oneLiner": "A camera-and-caliper vertical tool that lets a single-site care-home owner measure, log and re-prove every bed rail, hoist and window-restrictor dimensional gap in their building against the MHRA/CQC entrapment zones — producing a per-bedroom dimensional ledger that becomes the home's own defence asset when an incident or inspection lands.",
+      "title": "BedFall Bench, The Independent Care-Home Owner's Per-Bedroom Furniture Entrapment & Gap-Measurement Bench",
+      "oneLiner": "A camera-and-caliper vertical tool that lets a single-site care-home owner measure, log and re-prove every bed rail, hoist and window-restrictor dimensional gap in their building against the MHRA/CQC entrapment zones, producing a per-bedroom dimensional ledger that becomes the home's own defence asset when an incident or inspection lands.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "Passage describes an existing service offering exactly the candidate's core function — helping care homes check bed rail measurements, equipment compatibility and inspection records for compliance — and shows a monthly bed-rail audit template already referenced to CQC Regulation 12, so the dimensional-check need is already being served rather than open. The passages do not establish dominant market share, so this is a competitor-occupied space rather than a proven monopoly.",
+      "reason": "Passage describes an existing service offering exactly the candidate's core function, helping care homes check bed rail measurements, equipment compatibility and inspection records for compliance, and shows a monthly bed-rail audit template already referenced to CQC Regulation 12, so the dimensional-check need is already being served rather than open. The passages do not establish dominant market share, so this is a competitor-occupied space rather than a proven monopoly.",
       "citations": [
         {
           "url": "https://welcometoable.co.uk/resources/bed-rail-compliance/",
@@ -173,20 +448,20 @@
       "date": "2026-07-30"
     },
     {
-      "title": "MeterSplit Rounds — The Under-27 HMO Renter's Sub-Metered Utility Overcharge Reconstruction & Refund Round",
+      "title": "MeterSplit Rounds, The Under-27 HMO Renter's Sub-Metered Utility Overcharge Reconstruction & Refund Round",
       "oneLiner": "A fixed-fee productized service that reconstructs, from a landlord's own resale-of-energy billing records, how much a shared-house tenant was overcharged above the Maximum Resale Price, and runs the recovery to conclusion.",
       "gate": "distribution",
       "gateLabel": "There is no route to reach buyers",
-      "reason": "Two of the three named routes are contradicted by the passages: the renter-forum rules explicitly prohibit linking to, advertising, soliciting business for, or recommending any paid service [f8e297e7687cccc9, 991148b7ab004882], and the student-housing bodies described are landlord-facing — Unipol runs Landlord Clinics in Leeds, Bradford and Nottingham to support landlords, and the university-union event celebrates landlords alongside union representatives [c2040b39a36990e8, 67b967e3660aeb17] — an implausible host for a service that pursues those same landlords for refunds. No passage evidences",
+      "reason": "Two of the three named routes are contradicted by the passages: the renter-forum rules explicitly prohibit linking to, advertising, soliciting business for, or recommending any paid service [f8e297e7687cccc9, 991148b7ab004882], and the student-housing bodies described are landlord-facing, Unipol runs Landlord Clinics in Leeds, Bradford and Nottingham to support landlords, and the university-union event celebrates landlords alongside union representatives [c2040b39a36990e8, 67b967e3660aeb17], an implausible host for a service that pursues those same landlords for refunds. No passage evidences",
       "citations": [],
       "date": "2026-07-30"
     },
     {
-      "title": "CustodyClock — The Primary Carer's Court-Ordered Contact Breach Reconstruction & Enforcement Filing Broker",
+      "title": "CustodyClock, The Primary Carer's Court-Ordered Contact Breach Reconstruction & Enforcement Filing Broker",
       "oneLiner": "A fixed-fee transaction broker that reconstructs a year of missed, curtailed or sabotaged child-contact handovers into a court-ready C79 enforcement application for separated primary carers, charging £220 per filed application plus £90 per subsequent breach schedule update.",
       "gate": "payer_solvency",
       "gateLabel": "The payer cannot actually pay",
-      "reason": "The passages describing this payer segment state single-parent families are nearly twice as likely to be in poverty (67%), and that single parents on low income are directed to charity grants and free one-to-one legal support — evidence of a structurally cash-constrained payer, not one with budget. The unbundled-legal-services passages establish a paid limited-scope model is recognised in England & Wales family courts but say nothing about this segment's ability to fund it, so they do not offset the sol",
+      "reason": "The passages describing this payer segment state single-parent families are nearly twice as likely to be in poverty (67%), and that single parents on low income are directed to charity grants and free one-to-one legal support, evidence of a structurally cash-constrained payer, not one with budget. The unbundled-legal-services passages establish a paid limited-scope model is recognised in England & Wales family courts but say nothing about this segment's ability to fund it, so they do not offset the sol",
       "citations": [
         {
           "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5932102/",
@@ -208,11 +483,11 @@
       "date": "2026-07-29"
     },
     {
-      "title": "SharpsCount Rounds — The NHS Ward Sister's Overnight Instrument-Tray Photo-Census & Loan-Kit Shortfall Round",
+      "title": "SharpsCount Rounds, The NHS Ward Sister's Overnight Instrument-Tray Photo-Census & Loan-Kit Shortfall Round",
       "oneLiner": "A physical night-round service that photo-censuses reusable surgical/procedure trays and loan kits across a hospital's wards and theatres before the 07:00 list, producing a signed shortfall sheet that ward sisters use to stop a cancelled list being blamed on their department.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show funded incumbents already selling exactly this capability: Censis offers AI-driven surgical instrument management for sterile processing departments, enterprise deployments of such tracking systems are widespread enough to have documented 18–36 month ROI benchmarks and an established global market with active competition [9beb16cc5523e83d, 198fd17e9abbb6a0], and one system explicitly tracks dispatch and receipt of orthopaedic implant loan kits — the candidate's core chain-of-custody need.",
+      "reason": "The passages show funded incumbents already selling exactly this capability: Censis offers AI-driven surgical instrument management for sterile processing departments, enterprise deployments of such tracking systems are widespread enough to have documented 18, 36 month ROI benchmarks and an established global market with active competition [9beb16cc5523e83d, 198fd17e9abbb6a0], and one system explicitly tracks dispatch and receipt of orthopaedic implant loan kits, the candidate's core chain-of-custody need.",
       "citations": [
         {
           "url": "https://www.foresightiq.co/competitive-landscape/censis-technologies",
@@ -226,11 +501,11 @@
       "date": "2026-07-29"
     },
     {
-      "title": "BorderCare Split — The Cross-Border Primary Carer's Dual-State Care-Cost Attribution & Recovery Broker",
-      "oneLiner": "A fixed-fee transaction broker that reconstructs which of two jurisdictions is legally liable for a dependent's care, treatment or benefit costs — then recovers the wrongly-paid share from the losing authority on behalf of the carer who fronted the money.",
+      "title": "BorderCare Split, The Cross-Border Primary Carer's Dual-State Care-Cost Attribution & Recovery Broker",
+      "oneLiner": "A fixed-fee transaction broker that reconstructs which of two jurisdictions is legally liable for a dependent's care, treatment or benefit costs, then recovers the wrongly-paid share from the losing authority on behalf of the carer who fronted the money.",
       "gate": "payer_solvency",
       "gateLabel": "The payer cannot actually pay",
-      "reason": "The passages state that 1.2 million unpaid carers in the UK live in poverty, per the Carers UK/WPI Economics report on the scale of carer poverty, which cuts against the named payer — unpaid primary carers — having the budget to front £2k–£40k and pay £180+£450 fees; the remaining passages describe rising self-funder care costs and unfair care-home charges without evidencing carers' capacity or willingness to pay a broker.",
+      "reason": "The passages state that 1.2 million unpaid carers in the UK live in poverty, per the Carers UK/WPI Economics report on the scale of carer poverty, which cuts against the named payer, unpaid primary carers, having the budget to front £2k, £40k and pay £180+£450 fees; the remaining passages describe rising self-funder care costs and unfair care-home charges without evidencing carers' capacity or willingness to pay a broker.",
       "citations": [
         {
           "url": "https://www.carersuk.org/reports/poverty-and-financial-hardship-of-unpaid-carers-in-the-uk/",
@@ -252,8 +527,8 @@
       "date": "2026-07-29"
     },
     {
-      "title": "PourWindow — The Independent Ready-Mix & Screed Batching Plant Owner's Per-Load Slump-Loss & Rejection Forecast Bench",
-      "oneLiner": "A vertical bench tool for owner-operators of single-plant ready-mix concrete batching operations that predicts, before the drum leaves the yard, whether a given mix design will arrive on-site outside its slump/temperature acceptance window — and issues a signed pre-departure load certificate that shifts the rejection argument onto the receiving site.",
+      "title": "PourWindow, The Independent Ready-Mix & Screed Batching Plant Owner's Per-Load Slump-Loss & Rejection Forecast Bench",
+      "oneLiner": "A vertical bench tool for owner-operators of single-plant ready-mix concrete batching operations that predicts, before the drum leaves the yard, whether a given mix design will arrive on-site outside its slump/temperature acceptance window, and issues a signed pre-departure load certificate that shifts the rejection argument onto the receiving site.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
       "reason": "The passages describe an established, commercially deployed incumbent solving exactly this need: GCP's patented VERIFI® in-transit system measures and manages slump, temperature and water additions from plant to job site and is deployed fleet-wide by operators like the Neilsen Group, with Load Assurance giving dispatch minute-by-minute slump/air/temperature visibility. A crowded dispatch-software field (Command Alkon, Sysdyne, Zylocon, Dispatch360) further indicates the space is served rather than open",
@@ -278,11 +553,11 @@
       "date": "2026-07-29"
     },
     {
-      "title": "StandDown Bond — The Owner-Driver HGV Operator's DVSA Roadside Prohibition Income Micro-Bond",
-      "oneLiner": "A fixed-premium income bond that pays an owner-driver HGV/PSV operator a daily cash sum for every day their vehicle is off the road under a DVSA roadside 'S-marked' prohibition, funded and priced from the operator's own pre-enrolment inspection record — with payout rising as DVSA enforcement intensity rises.",
+      "title": "StandDown Bond, The Owner-Driver HGV Operator's DVSA Roadside Prohibition Income Micro-Bond",
+      "oneLiner": "A fixed-premium income bond that pays an owner-driver HGV/PSV operator a daily cash sum for every day their vehicle is off the road under a DVSA roadside 'S-marked' prohibition, funded and priced from the operator's own pre-enrolment inspection record, with payout rising as DVSA enforcement intensity rises.",
       "gate": "payer_solvency",
       "gateLabel": "The payer cannot actually pay",
-      "reason": "The passages describe UK hauliers operating under 'the tightest conditions in years: thin margins, rising non-fuel costs' with a live run of freight-sector failures in summer 2026 — T.M.S Service Provider Limited and S&B Haulage Ltd both entering liquidation within a week — which cuts against small operators having discretionary budget for a new premium; the one countervailing datapoint, easing headline insolvencies and falling diesel, is economy-wide rather than specific to owner-driver hauliers, and no passage shows this segment buying",
+      "reason": "The passages describe UK hauliers operating under 'the tightest conditions in years: thin margins, rising non-fuel costs' with a live run of freight-sector failures in summer 2026, T.M.S Service Provider Limited and S&B Haulage Ltd both entering liquidation within a week, which cuts against small operators having discretionary budget for a new premium; the one countervailing datapoint, easing headline insolvencies and falling diesel, is economy-wide rather than specific to owner-driver hauliers, and no passage shows this segment buying",
       "citations": [
         {
           "url": "https://hauliermagic.co.uk/blogs/uk-road-haulage-industry-crisis-2025-hidden-threats-nobody-talking-about/",
@@ -300,17 +575,17 @@
       "date": "2026-07-29"
     },
     {
-      "title": "UnclaimedSeat — The Primary Carer's Nursery & Childminder Funded-Hours Mid-Term Vacancy Claim Broker",
+      "title": "UnclaimedSeat, The Primary Carer's Nursery & Childminder Funded-Hours Mid-Term Vacancy Claim Broker",
       "oneLiner": "A fixed-fee broker who finds and secures unadvertised mid-term funded-hours childcare places for carers whose arrangement has just collapsed, charging £145 per confirmed placement plus a claim-back of the outgoing provider's unspent funded-hours entitlement.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "Passage 529082a4c171336b shows the Family Information Service already performs exactly the brokered service for parents struggling to find childcare — 'we will conduct on your behalf a detailed search of childcare available that best suits your needs' — i.e. a free, council-run brokerage, not the mere directory the candidate assumes; 7dd945f209695f02 confirms local FIS operations handling places and funded childcare options. A free statutory incumbent delivering the core search-and-place function in every council occupies the need the £145 fee is charged for.",
+      "reason": "Passage 529082a4c171336b shows the Family Information Service already performs exactly the brokered service for parents struggling to find childcare, 'we will conduct on your behalf a detailed search of childcare available that best suits your needs', i.e. a free, council-run brokerage, not the mere directory the candidate assumes; 7dd945f209695f02 confirms local FIS operations handling places and funded childcare options. A free statutory incumbent delivering the core search-and-place function in every council occupies the need the £145 fee is charged for.",
       "citations": [],
       "date": "2026-07-29"
     },
     {
-      "title": "SubletTrace — The Under-27 Renter's Rent-Repayment-Order Evidence & Filing Pack",
-      "oneLiner": "A fixed-fee productized service that reconstructs the 12-month evidence chain a Gen Z renter needs to win a Rent Repayment Order against an unlicensed or banned landlord — and hands them a tribunal-ready bundle plus the exact filing route, priced at £145 with an uplift on award.",
+      "title": "SubletTrace, The Under-27 Renter's Rent-Repayment-Order Evidence & Filing Pack",
+      "oneLiner": "A fixed-fee productized service that reconstructs the 12-month evidence chain a Gen Z renter needs to win a Rent Repayment Order against an unlicensed or banned landlord, and hands them a tribunal-ready bundle plus the exact filing route, priced at £145 with an uplift on award.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
       "reason": "The passages show established rivals already serving this exact need: Flat Justice CIC provides RRO applications against unlicensed and rogue landlords with a free DIY guide, advice and no-win-no-fee representation, a specialist adviser covers RROs across ten London boroughs on a free-assessment, no-win-no-fee basis, and Justice for Tenants assists thousands of tenants every year and is referred to by dozens of organisations [0226494a1b92a04c, 07896cb4d133507b]. A free/contingency full-representation service assisting thousands annually occupies the tenant",
@@ -327,11 +602,11 @@
       "date": "2026-07-29"
     },
     {
-      "title": "TerpSheet — The Independent UK Distiller's Botanical Batch-to-Cut Yield & Flavour-Drift Bench Tool",
+      "title": "TerpSheet, The Independent UK Distiller's Botanical Batch-to-Cut Yield & Flavour-Drift Bench Tool",
       "oneLiner": "A vertical bench tool for the ~700 owner-operated UK gin/rum distilleries that records every still run's botanical lot, maceration curve and cut points against sensory outcome, so the one person who owns the palate can reproduce a winning batch and defend it when their botanical supplier silently changes origin.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show multiple established distillery/brewery production-management platforms already serving this exact segment — Breww for craft breweries, Ollie's batch tracking of ingredients and costs, MasterDistiller covering 'all aspects of the production and maturation process', a distillery ERP covering distillation, blending and quality control, and a management product explicitly for whisky, rum and gin makers. The passages do not, however, show any of these capturing supplier lot codes or post-re",
+      "reason": "The passages show multiple established distillery/brewery production-management platforms already serving this exact segment, Breww for craft breweries, Ollie's batch tracking of ingredients and costs, MasterDistiller covering 'all aspects of the production and maturation process', a distillery ERP covering distillation, blending and quality control, and a management product explicitly for whisky, rum and gin makers. The passages do not, however, show any of these capturing supplier lot codes or post-re",
       "citations": [
         {
           "url": "https://breww.com/",
@@ -353,20 +628,20 @@
       "date": "2026-07-29"
     },
     {
-      "title": "The Late-Onset Atlas — The Retiree's Per-Trial Clinical-Study Eligibility & Reimbursed-Travel Decision Brief",
-      "oneLiner": "A data intelligence product that reconstructs, from public trial registries and site-level protocol documents, which UK/EU clinical trials a 60-75-year-old with a specific comorbidity stack would actually be admitted to — and which of those sites pay travel, accommodation and companion costs — sold as a personalised per-condition decision brief.",
+      "title": "The Late-Onset Atlas, The Retiree's Per-Trial Clinical-Study Eligibility & Reimbursed-Travel Decision Brief",
+      "oneLiner": "A data intelligence product that reconstructs, from public trial registries and site-level protocol documents, which UK/EU clinical trials a 60-75-year-old with a specific comorbidity stack would actually be admitted to, and which of those sites pay travel, accommodation and companion costs, sold as a personalised per-condition decision brief.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "Join Dementia Research is an NIHR-managed national service, in partnership with Alzheimer's Society, Alzheimer's Research UK and Alzheimer Scotland, that already matches UK patients to trials at scale (over 10,000 people enrolled per its NIHR National Director), and Deep 6 AI's Precision Research Ecosystem is deployed enterprise-wide across health systems to match patients against complex trial inclusion criteria — now integrated with Tempus. These are funded, dominant-position players occupying the patient-to-trial matching need in exactly this segment (UK dementia/retiree cohort), so the spa",
+      "reason": "Join Dementia Research is an NIHR-managed national service, in partnership with Alzheimer's Society, Alzheimer's Research UK and Alzheimer Scotland, that already matches UK patients to trials at scale (over 10,000 people enrolled per its NIHR National Director), and Deep 6 AI's Precision Research Ecosystem is deployed enterprise-wide across health systems to match patients against complex trial inclusion criteria, now integrated with Tempus. These are funded, dominant-position players occupying the patient-to-trial matching need in exactly this segment (UK dementia/retiree cohort), so the spa",
       "citations": [],
       "date": "2026-07-29"
     },
     {
-      "title": "PitStop Ledger — The Gig Driver's Per-Vehicle Warranty & Recall Claim Reconstruction Service",
+      "title": "PitStop Ledger, The Gig Driver's Per-Vehicle Warranty & Recall Claim Reconstruction Service",
       "oneLiner": "A fixed-fee productized service that reconstructs a high-mileage gig driver's fragmented service history into a manufacturer-grade warranty/goodwill claim pack, recovering repair costs the dealer has already refused.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show existing commercial operators already serving this exact need — Motor Claims Helpline offers professional resolution of vehicle disputes explicitly including warranty claims, and claims consultancies run no-win-no-fee vehicle claim services with zero upfront cost [e1ea2d30b5b50f01, d184033068e77779], undercutting a £180-£340 fixed fee. The Motor Ombudsman additionally operates a free ADR channel embedded into businesses' own complaints processes and is already absorbing a rising volume of service and repair complaints [eaebe2a03a52cfc4, 577baafcaff7fa6f, 99",
+      "reason": "The passages show existing commercial operators already serving this exact need, Motor Claims Helpline offers professional resolution of vehicle disputes explicitly including warranty claims, and claims consultancies run no-win-no-fee vehicle claim services with zero upfront cost [e1ea2d30b5b50f01, d184033068e77779], undercutting a £180-£340 fixed fee. The Motor Ombudsman additionally operates a free ADR channel embedded into businesses' own complaints processes and is already absorbing a rising volume of service and repair complaints [eaebe2a03a52cfc4, 577baafcaff7fa6f, 99",
       "citations": [
         {
           "url": "https://www.motorclaimshelpline.co.uk/",
@@ -376,11 +651,11 @@
       "date": "2026-07-29"
     },
     {
-      "title": "NightWaiver — The Under-27 Rideshare Driver's Private Hire Licence Medical & Endorsement Objection Round",
+      "title": "NightWaiver, The Under-27 Rideshare Driver's Private Hire Licence Medical & Endorsement Objection Round",
       "oneLiner": "A fixed-fee productized service that builds and files the evidence-led objection pack when a council licensing officer refuses, suspends or refers a young private-hire driver's badge over a medical group-2 assessment or DVLA endorsement, drawing on a compounding per-council dataset of which committee arguments actually reversed which refusal reason.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show established specialist solicitor firms already positioned on exactly this need — taxi/PHV licence appeals marketed as protecting the driver's livelihood — and a self-described UK market leader in motoring law running fixed-fee representation at 4,000–5,000 cases a year with 5–15 court hearings daily. That is dominant, well-resourced incumbency over the licence-and-endorsement defence segment rather than a mere competitor, so the space is not open.",
+      "reason": "The passages show established specialist solicitor firms already positioned on exactly this need, taxi/PHV licence appeals marketed as protecting the driver's livelihood, and a self-described UK market leader in motoring law running fixed-fee representation at 4,000, 5,000 cases a year with 5, 15 court hearings daily. That is dominant, well-resourced incumbency over the licence-and-endorsement defence segment rather than a mere competitor, so the space is not open.",
       "citations": [
         {
           "url": "https://www.ellisjones.co.uk/business/regulatory-solicitors/licensing-disputes/taxi-and-private-hire-vehicle-licence-appeals/",
@@ -402,11 +677,11 @@
       "date": "2026-07-29"
     },
     {
-      "title": "CutList Arbiter — The Independent Joinery & Kitchen-Fitting Shop's Sheet-Goods Yield & Off-Spec Board Reject Bench",
+      "title": "CutList Arbiter, The Independent Joinery & Kitchen-Fitting Shop's Sheet-Goods Yield & Off-Spec Board Reject Bench",
       "oneLiner": "A vertical desktop tool that, before a single cut is made, nests a shop's job on the actual boards it received, measures each delivered pack's real thickness/moisture/bow against BS EN 14322 tolerance, and prints both the optimised cut list and a merchant-facing off-spec reject claim.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show established panel-saw optimisation software already serving this exact workflow — OptiCut nesting for panel/beam saws with grain and stock management, and automatic panel-saw cutting optimisation with material costing tied to the major machine vendors BIESSE, SCM and HOMAG explicitly serving small companies, with SCM distributing its optimisation software to users. The core cut-list/nesting function the candidate sells is thus occupied by well-established vendors, though no passage addresses the measured-deviation/rejec",
+      "reason": "The passages show established panel-saw optimisation software already serving this exact workflow, OptiCut nesting for panel/beam saws with grain and stock management, and automatic panel-saw cutting optimisation with material costing tied to the major machine vendors BIESSE, SCM and HOMAG explicitly serving small companies, with SCM distributing its optimisation software to users. The core cut-list/nesting function the candidate sells is thus occupied by well-established vendors, though no passage addresses the measured-deviation/rejec",
       "citations": [
         {
           "url": "https://wooddesigner.org/wood-cnc-machines/",
@@ -424,20 +699,20 @@
       "date": "2026-07-29"
     },
     {
-      "title": "SolderFloor — The Squeezed-Middle Parent's Board-Level Repair Bench for Dead School Chromebooks and Tablets",
-      "oneLiner": "A component-level toolkit-and-training operation that sells the exact jig, donor-board map and failure-code playbook that lets a parent or a school IT lead resurrect the specific dead Chromebook/iPad models UK schools issue to pupils — sold as a physical kit plus a per-model bench manual, not a repair service.",
+      "title": "SolderFloor, The Squeezed-Middle Parent's Board-Level Repair Bench for Dead School Chromebooks and Tablets",
+      "oneLiner": "A component-level toolkit-and-training operation that sells the exact jig, donor-board map and failure-code playbook that lets a parent or a school IT lead resurrect the specific dead Chromebook/iPad models UK schools issue to pupils, sold as a physical kit plus a per-model bench manual, not a repair service.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show iFixit already occupies exactly this slot for the same devices — 'iFixit makes Chromebook repair easy:... unmatched DIY fix kits, and free in-depth, accurate repair manuals', backed by tested parts, precision tools, schematics and a large fixer community [c2457179eee87ddc, 3703f1c35d36405b, 580f95a74dabad17] — i.e. a dominant DIY repair-kit-plus-manual incumbent giving the manual half away free. The board-level training half is likewise already sold by existing micro-soldering course providers covering IC repair and no-charge fault diagnosis [edf4d5674e2a7b75, b1700b6b685d11",
+      "reason": "The passages show iFixit already occupies exactly this slot for the same devices, 'iFixit makes Chromebook repair easy:... unmatched DIY fix kits, and free in-depth, accurate repair manuals', backed by tested parts, precision tools, schematics and a large fixer community [c2457179eee87ddc, 3703f1c35d36405b, 580f95a74dabad17], i.e. a dominant DIY repair-kit-plus-manual incumbent giving the manual half away free. The board-level training half is likewise already sold by existing micro-soldering course providers covering IC repair and no-charge fault diagnosis [edf4d5674e2a7b75, b1700b6b685d11",
       "citations": [],
       "date": "2026-07-29"
     },
     {
-      "title": "SaltPrint Rounds — The School Site Manager's Termly Playground-Surfacing Impact-Attenuation Drop Test & Depth Ledger",
-      "oneLiner": "A mobile physical-testing round that drop-tests every impact-absorbing playground surface in a school or nursery to BS EN 1177, records the measured Critical Fall Height against the installed equipment's actual free-height-of-fall, and leaves a photographic, GPS-and-depth-stamped ledger the site manager can put in front of the insurer, the RPA claims handler, and the head teacher — with each subsequent visit compounding into a per-square-metre degradation curve nobody else holds.",
+      "title": "SaltPrint Rounds, The School Site Manager's Termly Playground-Surfacing Impact-Attenuation Drop Test & Depth Ledger",
+      "oneLiner": "A mobile physical-testing round that drop-tests every impact-absorbing playground surface in a school or nursery to BS EN 1177, records the measured Critical Fall Height against the installed equipment's actual free-height-of-fall, and leaves a photographic, GPS-and-depth-stamped ledger the site manager can put in front of the insurer, the RPA claims handler, and the head teacher, with each subsequent visit compounding into a per-square-metre degradation curve nobody else holds.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show the candidate's exact core service is already commercially marketed by multiple existing providers — computerised headform HIC/GMAX drop testing to establish Critical Fall Height as part of playground inspection offerings, TRIAX impact testing rigs, and an HIC impact testing machine sold on a recurring seasonal schedule ('if you haven't already scheduled your testing... early-season testing... coming out of winter'), alongside established UK inspection firms serving schools, councils and parish councils [e49d52757a0e72b",
+      "reason": "The passages show the candidate's exact core service is already commercially marketed by multiple existing providers, computerised headform HIC/GMAX drop testing to establish Critical Fall Height as part of playground inspection offerings, TRIAX impact testing rigs, and an HIC impact testing machine sold on a recurring seasonal schedule ('if you haven't already scheduled your testing... early-season testing... coming out of winter'), alongside established UK inspection firms serving schools, councils and parish councils [e49d52757a0e72b",
       "citations": [
         {
           "url": "https://trassig.com/products/hic-drop-test",
@@ -455,11 +730,11 @@
       "date": "2026-07-29"
     },
     {
-      "title": "TheatreLift — The Hospital Theatre Nurse's Bariatric Ceiling-Hoist Load-Proof & LOLER-Recert Round",
-      "oneLiner": "A mobile physical-ops round that arrives on-site with calibrated dynamometer test-weight rigs and load-proofs the ceiling hoists, gantry tracks and shower chairs in independent hospices, private clinics and specialist care homes — issuing a per-anchor LOLER thorough-examination certificate and building a proprietary per-track deflection-history dataset nobody else holds.",
+      "title": "TheatreLift, The Hospital Theatre Nurse's Bariatric Ceiling-Hoist Load-Proof & LOLER-Recert Round",
+      "oneLiner": "A mobile physical-ops round that arrives on-site with calibrated dynamometer test-weight rigs and load-proofs the ceiling hoists, gantry tracks and shower chairs in independent hospices, private clinics and specialist care homes, issuing a per-anchor LOLER thorough-examination certificate and building a proprietary per-track deflection-history dataset nobody else holds.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show established, well-resourced LOLER thorough-examination providers already serving this exact need — Zurich Engineering, a UKAS-accredited inspection body with 'professionally qualified, fully certified engineer surveyors' conducting on-site thorough examinations of lifting equipment [c9207e9b4239a40e, 800e142a1f98d4cf, ec58da1dbb515e8a] — and third-party providers already combining LOLER inspection with servicing for care operators, plus procured patient-lifting inspection contracts in healthcare. These are independent competent-person ins",
+      "reason": "The passages show established, well-resourced LOLER thorough-examination providers already serving this exact need, Zurich Engineering, a UKAS-accredited inspection body with 'professionally qualified, fully certified engineer surveyors' conducting on-site thorough examinations of lifting equipment [c9207e9b4239a40e, 800e142a1f98d4cf, ec58da1dbb515e8a], and third-party providers already combining LOLER inspection with servicing for care operators, plus procured patient-lifting inspection contracts in healthcare. These are independent competent-person ins",
       "citations": [
         {
           "url": "https://medaco.co.uk/who-carry-loler-inspection-annual-service-patient-lifting-equipment/?srsltid=AfmBOor8QQFXZ_ng5WlkyXB3LeMzvWycND1L3jGinkbJT6ooxRo-Wc0S",
@@ -473,11 +748,11 @@
       "date": "2026-07-29"
     },
     {
-      "title": "SaltFront Rounds — The Council Highways Officer's Coastal Street-Furniture Galvanic Depletion Round",
+      "title": "SaltFront Rounds, The Council Highways Officer's Coastal Street-Furniture Galvanic Depletion Round",
       "oneLiner": "A solo mobile round that measures residual zinc coating thickness and galvanic corrosion depth on coastal council street furniture (railings, lamp columns, bin housings, bus shelter frames) using an ultrasonic/eddy-current bench, selling per-asset remaining-life certificates that let a highways officer defer or trigger replacement with defensible evidence.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "Passage shows a local authority (Leicestershire County Council) already procuring exactly this need through a Structural Testing of Street Lighting Columns Framework Agreement, with an incumbent NDT supplier (Roch NDT Services, £87,500) awarded — i.e. councils have an established, contracted route for column structural testing rather than an open space. The remaining passages concern lighting-control hardware, laptops, and US defence contracts and bear on nothing here.",
+      "reason": "Passage shows a local authority (Leicestershire County Council) already procuring exactly this need through a Structural Testing of Street Lighting Columns Framework Agreement, with an incumbent NDT supplier (Roch NDT Services, £87,500) awarded, i.e. councils have an established, contracted route for column structural testing rather than an open space. The remaining passages concern lighting-control hardware, laptops, and US defence contracts and bear on nothing here.",
       "citations": [
         {
           "url": "https://gvtcx.com/procurement/cf/ocds-b5fd17-5dc88c14-88b1-488a-bc39-71bb660da6ef/structural-testing-lighting-columns",
@@ -487,11 +762,11 @@
       "date": "2026-07-29"
     },
     {
-      "title": "ThawPoint — The Independent Ice-Cream Van & Mobile Freezer Operator's Per-Route Product-Integrity & Insurance-Defence Bench",
-      "oneLiner": "A vertical tool that turns a cheap logger in the freezer into a per-load, per-stop soft-serve mix and hard-scoop integrity record — telling the owner-operator which stops are quietly cooking their stock, and producing the temperature-chain exhibit that wins a spoilage or food-complaint dispute.",
+      "title": "ThawPoint, The Independent Ice-Cream Van & Mobile Freezer Operator's Per-Route Product-Integrity & Insurance-Defence Bench",
+      "oneLiner": "A vertical tool that turns a cheap logger in the freezer into a per-load, per-stop soft-serve mix and hard-scoop integrity record, telling the owner-operator which stops are quietly cooking their stock, and producing the temperature-chain exhibit that wins a spoilage or food-complaint dispute.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show an established commercial field already serving this exact need: UK-stock battery fridge probes buyable online today, wireless Bluetooth fridge monitors with mobile apps aimed at reducing food waste, full temperature-monitoring software platforms, and cold-chain vendors (Berlinger/Sensitech, tempmate®) selling IoT loggers with cloud, 'verified visibility and audit-ready records' — i.e. the logging-plus-audit-record function is already productised. The passages do not show any single",
+      "reason": "The passages show an established commercial field already serving this exact need: UK-stock battery fridge probes buyable online today, wireless Bluetooth fridge monitors with mobile apps aimed at reducing food waste, full temperature-monitoring software platforms, and cold-chain vendors (Berlinger/Sensitech, tempmate®) selling IoT loggers with cloud, 'verified visibility and audit-ready records', i.e. the logging-plus-audit-record function is already productised. The passages do not show any single",
       "citations": [
         {
           "url": "https://indiott.com/fridge-temperature-monitoring/",
@@ -513,11 +788,11 @@
       "date": "2026-07-29"
     },
     {
-      "title": "BridgeTheGrant — The Primary Carer's Disabled Facilities Grant Cashflow Bridge & Contractor Settlement Desk",
-      "oneLiner": "A transaction broker that fronts the builder's stage payments on an already-approved Disabled Facilities Grant, then collects the council's post-completion reimbursement directly — carer never touches a penny, broker takes a fixed 9% of grant value.",
+      "title": "BridgeTheGrant, The Primary Carer's Disabled Facilities Grant Cashflow Bridge & Contractor Settlement Desk",
+      "oneLiner": "A transaction broker that fronts the builder's stage payments on an already-approved Disabled Facilities Grant, then collects the council's post-completion reimbursement directly, carer never touches a penny, broker takes a fixed 9% of grant value.",
       "gate": "payer_solvency",
       "gateLabel": "The payer cannot actually pay",
-      "reason": "The passages establish that unpaid carers — the named payer segment — are disproportionately impoverished (1.2m in poverty, 400,000 in deep poverty, poverty rate 50% higher, with caring itself reducing income) [84a4670aa1d88132, 0a5f5e41f78afcaa, 7ccbad63cdcccaac], which is precisely the 'broke body' condition; the DFG budget growth to £761m shows council money exists but does not show the carer can pay, and the candidate itself concedes the carer pays nothing out of pocket.",
+      "reason": "The passages establish that unpaid carers, the named payer segment, are disproportionately impoverished (1.2m in poverty, 400,000 in deep poverty, poverty rate 50% higher, with caring itself reducing income) [84a4670aa1d88132, 0a5f5e41f78afcaa, 7ccbad63cdcccaac], which is precisely the 'broke body' condition; the DFG budget growth to £761m shows council money exists but does not show the carer can pay, and the candidate itself concedes the carer pays nothing out of pocket.",
       "citations": [
         {
           "url": "https://stairliftguru.co.uk/stairlift-grants/uk-disabled-facilities-grant-funding-statistics/",
@@ -527,11 +802,11 @@
       "date": "2026-07-28"
     },
     {
-      "title": "AshCert Rounds — The Public-Sector Wood-Burner Owner's Post-Installation Chimney Compliance & Insurance-Evidence Round",
+      "title": "AshCert Rounds, The Public-Sector Wood-Burner Owner's Post-Installation Chimney Compliance & Insurance-Evidence Round",
       "oneLiner": "A booked physical inspection round that sweeps, camera-surveys and smoke-tests wood-burning stoves in older housing stock for public-sector households, producing a dated instrument-backed defect record that a retrospective HETAS certificate or Building Regulations completion cannot supply.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show multiple existing UK chimney firms already bundling exactly the proposed physical wedge — sweeping plus CCTV flue survey with condition diagnosis and remedial advice, aligned to HETAS-recommended post-installation visual examination — and dedicated CCTV survey specialists serving domestic clients. The in-room instrument inspection the candidate treats as an unserved gap is an established, competitively offered service rather than an open space.",
+      "reason": "The passages show multiple existing UK chimney firms already bundling exactly the proposed physical wedge, sweeping plus CCTV flue survey with condition diagnosis and remedial advice, aligned to HETAS-recommended post-installation visual examination, and dedicated CCTV survey specialists serving domestic clients. The in-room instrument inspection the candidate treats as an unserved gap is an established, competitively offered service rather than an open space.",
       "citations": [
         {
           "url": "https://inspectorflueso.co.uk/chimney-services/cctv-chimney-inspections/",
@@ -553,11 +828,11 @@
       "date": "2026-07-28"
     },
     {
-      "title": "BracketLock — The Independent Bike Shop Owner's E-Bike Motor-Recall & Battery-Serial Fitment Bench Engine",
-      "oneLiner": "A bench-side vertical tool for owner-operator UK bicycle shops that resolves, per bike on the workstand, whether that exact e-bike's motor/battery serial falls inside an active OPSS/manufacturer recall or a UN38.3 shipping restriction — and prints the refuse-or-repair decision sheet the shop needs to avoid taking liability for someone else's battery.",
+      "title": "BracketLock, The Independent Bike Shop Owner's E-Bike Motor-Recall & Battery-Serial Fitment Bench Engine",
+      "oneLiner": "A bench-side vertical tool for owner-operator UK bicycle shops that resolves, per bike on the workstand, whether that exact e-bike's motor/battery serial falls inside an active OPSS/manufacturer recall or a UN38.3 shipping restriction, and prints the refuse-or-repair decision sheet the shop needs to avoid taking liability for someone else's battery.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show an existing, free, publicly searchable recall/alert database that already lists e-bike battery recalls down to serial-number ranges (e.g. \"Serial numbers between 190790036E and 190790137E only\") with email subscription for new entries, i.e. the serial-level recall-lookup need is already served by an authoritative incumbent. The motor-side need is likewise covered by the dominant OEM's dealer channel — certified service networks with diagnostics and firmware updates, and dealer-only software gated to authorised shops [df63",
+      "reason": "The passages show an existing, free, publicly searchable recall/alert database that already lists e-bike battery recalls down to serial-number ranges (e.g. \"Serial numbers between 190790036E and 190790137E only\") with email subscription for new entries, i.e. the serial-level recall-lookup need is already served by an authoritative incumbent. The motor-side need is likewise covered by the dominant OEM's dealer channel, certified service networks with diagnostics and firmware updates, and dealer-only software gated to authorised shops [df63",
       "citations": [
         {
           "url": "https://www.gov.uk/guidance/product-recalls-and-alerts",
@@ -575,11 +850,11 @@
       "date": "2026-07-28"
     },
     {
-      "title": "KilnLog — The Independent Pottery Studio's Per-Firing Kiln Element & Cone-Drift Ledger",
+      "title": "KilnLog, The Independent Pottery Studio's Per-Firing Kiln Element & Cone-Drift Ledger",
       "oneLiner": "A vertical tool for one-person UK/EU ceramics studios that logs every kiln firing against measured cone-drift and element resistance, predicting the exact firing at which a batch will underfire so the studio reschedules production rather than losing a £2,000 commission load.",
       "gate": "payer_solvency",
       "gateLabel": "The payer cannot actually pay",
-      "reason": "The passages show the payer segment is structurally low-income: UK visual artists have a median income of £12,500/year, 79% cannot afford their livelihoods from art earnings and 96.4% earn below the median wage, and a whole studio can be started for £2,000–£5,000 with firings costing only £3–£50 — so a £19/mo per-kiln subscription plus £45 briefs sits against budgets with no evidenced slack. Nothing in the passages shows this payer willing or able to buy software.",
+      "reason": "The passages show the payer segment is structurally low-income: UK visual artists have a median income of £12,500/year, 79% cannot afford their livelihoods from art earnings and 96.4% earn below the median wage, and a whole studio can be started for £2,000, £5,000 with firings costing only £3, £50, so a £19/mo per-kiln subscription plus £45 briefs sits against budgets with no evidenced slack. Nothing in the passages shows this payer willing or able to buy software.",
       "citations": [
         {
           "url": "https://creativesunite.eu/article/majority-of-uk-artists-earn-less-than-minimum-wage",
@@ -601,11 +876,11 @@
       "date": "2026-07-28"
     },
     {
-      "title": "TrigPointHold — The Sole-Trader Land Surveyor's Instrument-Recall Income Micro-Bond",
+      "title": "TrigPointHold, The Sole-Trader Land Surveyor's Instrument-Recall Income Micro-Bond",
       "oneLiner": "A fixed-premium micro-bond that pays a self-employed land/setting-out surveyor a daily income sum for every day their total station or GNSS rover is quarantined by a manufacturer calibration recall or a failed UKAS-traceable baseline check, funded from a pooled subscription ledger the operator underwrites off proprietary drift data.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show an established, funded incumbent category directly serving this payer: self-employed income protection policies that pay a monthly or weekly sum when the sole trader cannot work, alongside business interruption cover for loss of operating income and brokers already distributing such cover to sole-trader tradies. However, none of the passages addresses a calibration/recall trigger — they cover illness, injury, or physical damage — so the incumbency is over the adjace",
+      "reason": "The passages show an established, funded incumbent category directly serving this payer: self-employed income protection policies that pay a monthly or weekly sum when the sole trader cannot work, alongside business interruption cover for loss of operating income and brokers already distributing such cover to sole-trader tradies. However, none of the passages addresses a calibration/recall trigger, they cover illness, injury, or physical damage, so the incumbency is over the adjace",
       "citations": [
         {
           "url": "https://www.drewberryinsurance.co.uk/income-protection-insurance/self-employed-income-protection",
@@ -627,11 +902,11 @@
       "date": "2026-07-28"
     },
     {
-      "title": "BadDebtBack — The Gig-Economy Landlord-Deposit & Rent-Credit Forensic Recovery Round for Under-27 Renters",
-      "oneLiner": "A fixed-fee productized service that reconstructs a Gen Z gig worker's full renting history across every landlord, agent and flat-share they have lived in since age 18, and recovers every unprotected-deposit penalty, unreturned deposit, and mis-recorded rent arrears marker still suppressing their credit file — priced per tenancy recovered, not per hour.",
+      "title": "BadDebtBack, The Gig-Economy Landlord-Deposit & Rent-Credit Forensic Recovery Round for Under-27 Renters",
+      "oneLiner": "A fixed-fee productized service that reconstructs a Gen Z gig worker's full renting history across every landlord, agent and flat-share they have lived in since age 18, and recovers every unprotected-deposit penalty, unreturned deposit, and mis-recorded rent arrears marker still suppressing their credit file, priced per tenancy recovered, not per hour.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "Passage shows an existing commercial channel already serving this exact wedge — a panel of deposit solicitors running no-win-no-fee claims for deposits not protected within 30 days or with missing prescribed information — i.e. the s.214 penalty claim the candidate is built on, offered at zero upfront cost versus the candidate's £39/tenancy fee; the surrounding passages [90072c00f8499751, 5184dc9bfd67f338] show the mature UK no-win-no-fee claims industry that supplies such panels. The passages do not show a single dominant leader, so this is a rival-capture finding rather tha",
+      "reason": "Passage shows an existing commercial channel already serving this exact wedge, a panel of deposit solicitors running no-win-no-fee claims for deposits not protected within 30 days or with missing prescribed information, i.e. the s.214 penalty claim the candidate is built on, offered at zero upfront cost versus the candidate's £39/tenancy fee; the surrounding passages [90072c00f8499751, 5184dc9bfd67f338] show the mature UK no-win-no-fee claims industry that supplies such panels. The passages do not show a single dominant leader, so this is a rival-capture finding rather tha",
       "citations": [
         {
           "url": "https://www.claimexperts.co.uk/tenancy-deposit-claims/",
@@ -641,11 +916,11 @@
       "date": "2026-07-28"
     },
     {
-      "title": "SchoolTransportBridge — The Primary Carer's Home-to-School Transport Refusal Reversal & Independent-Panel Broker",
-      "oneLiner": "A fixed-fee transaction broker who takes a refused (or downgraded) statutory home-to-school transport application for a disabled or SEND child all the way through the two-stage council appeal to Stage 2 independent panel, and — where the panel is lost or delayed — simultaneously brokers the interim Personal Transport Budget / mileage settlement so the carer stops driving unpaid on day one.",
+      "title": "SchoolTransportBridge, The Primary Carer's Home-to-School Transport Refusal Reversal & Independent-Panel Broker",
+      "oneLiner": "A fixed-fee transaction broker who takes a refused (or downgraded) statutory home-to-school transport application for a disabled or SEND child all the way through the two-stage council appeal to Stage 2 independent panel, and, where the panel is lost or delayed, simultaneously brokers the interim Personal Transport Budget / mileage settlement so the carer stops driving unpaid on day one.",
       "gate": "payer_solvency",
       "gateLabel": "The payer cannot actually pay",
-      "reason": "The passages describe the payer segment (unpaid carers) as structurally poor: carers on Carer's Allowance alone have a 33% poverty rate versus 18% for non-carers, with ~90,000 in poverty [15d2c57b0eeb99c3, c9c8b7b5e09dfb94]. The only passage touching the transport settlement itself says personal transport budgets/mileage payments exist but vary by council — it does not show the carer can or will pay a £180 upfront fee.",
+      "reason": "The passages describe the payer segment (unpaid carers) as structurally poor: carers on Carer's Allowance alone have a 33% poverty rate versus 18% for non-carers, with ~90,000 in poverty [15d2c57b0eeb99c3, c9c8b7b5e09dfb94]. The only passage touching the transport settlement itself says personal transport budgets/mileage payments exist but vary by council, it does not show the carer can or will pay a £180 upfront fee.",
       "citations": [
         {
           "url": "https://load2learn.org.uk/getting-children-to-school-when-standard-transport-does-not-fit/",
@@ -655,11 +930,11 @@
       "date": "2026-07-28"
     },
     {
-      "title": "SlipRisk Bond — The Sole-Trader Resin-Bound Driveway Installer's Post-Cure Slip-Test Failure Income Micro-Bond",
+      "title": "SlipRisk Bond, The Sole-Trader Resin-Bound Driveway Installer's Post-Cure Slip-Test Failure Income Micro-Bond",
       "oneLiner": "A subscription micro-bond that pays a named resin-bound surfacing installer a fixed daily income while a customer-commissioned pendulum slip test (BS 7976 / UKSRG) has failed and the driveway is disputed, in exchange for exclusive rights to the installer's per-batch cure telemetry.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
-      "reason": "The passages show an established UK tradesman-insurance market already selling the adjacent products to this exact payer — sole-trader income protection for when a tradesperson can't earn (de2144c0a07e8f21, b72e61d1b7222bd7) and Tradesman Saver contract works cover including £10,000–£50,000 for financial loss — on a pick-and-mix basis at £75–£1,200 a year (0cab99bedbc6b890, b0bea8e3effda339). Incumbent insurers already occupy the sole-trader income-and-financial-loss cover slot cheaply, so the space is not shown to be open; the passages do not describe any product tied to a",
+      "reason": "The passages show an established UK tradesman-insurance market already selling the adjacent products to this exact payer, sole-trader income protection for when a tradesperson can't earn (de2144c0a07e8f21, b72e61d1b7222bd7) and Tradesman Saver contract works cover including £10,000, £50,000 for financial loss, on a pick-and-mix basis at £75, £1,200 a year (0cab99bedbc6b890, b0bea8e3effda339). Incumbent insurers already occupy the sole-trader income-and-financial-loss cover slot cheaply, so the space is not shown to be open; the passages do not describe any product tied to a",
       "citations": [
         {
           "url": "https://www.tradesmansaver.co.uk/contract-works-insurance/",
@@ -669,8 +944,8 @@
       "date": "2026-07-28"
     },
     {
-      "title": "CycleMark — The NHS Hospital Bike-Shed Forensic Mark-Up Round",
-      "oneLiner": "A mobile operator who works NHS hospital bike sheds at the 6am/6pm shift-change window, forensically marking staff bicycles with a UV-traceable code onto a multi-Trust recovery database cross-linked to local police BikeRegister — sold as a £25 one-off mark-up plus £15/year per-bike subscription.",
+      "title": "CycleMark, The NHS Hospital Bike-Shed Forensic Mark-Up Round",
+      "oneLiner": "A mobile operator who works NHS hospital bike sheds at the 6am/6pm shift-change window, forensically marking staff bicycles with a UV-traceable code onto a multi-Trust recovery database cross-linked to local police BikeRegister, sold as a £25 one-off mark-up plus £15/year per-bike subscription.",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
       "reason": "Passages establish BikeRegister as a clear dominant incumbent: used by ALL UK police forces, its marking kits achieve an 83% theft-reduction rate, it reunites hundreds of cyclists annually, and police regularly run marking events (, ). This dominant share in the bike security marking space meets the standard for refuting incumbency. The passages do not, however, directly address whether any incumbent specifically serves the NHS hospital bike-shed shift-change channel, so some uncertainty remains.",
@@ -687,8 +962,8 @@
       "date": "2026-07-22"
     },
     {
-      "title": "The Quiet Ledger — The UK Freelance Creative's Financial-Benchmark Weekly",
-      "oneLiner": "A paid weekly Substack (£11/month) publishing anonymized aggregated financial-health benchmarks for UK freelance creatives — billable utilization, project margins, expense ratios, IR35-borderline patterns, pension-contribution sweet spots, year-end tax windows — drawn from a proprietary monthly subscriber survey that compounds into an intelligence layer no incumbent can replicate.",
+      "title": "The Quiet Ledger, The UK Freelance Creative's Financial-Benchmark Weekly",
+      "oneLiner": "A paid weekly Substack (£11/month) publishing anonymized aggregated financial-health benchmarks for UK freelance creatives, billable utilization, project margins, expense ratios, IR35-borderline patterns, pension-contribution sweet spots, year-end tax windows, drawn from a proprietary monthly subscriber survey that compounds into an intelligence layer no incumbent can replicate.",
       "gate": "value_durability",
       "gateLabel": "The value would not last",
       "reason": "The passages show free first-party AI tools (ChatGPT, Gemini, Claude prompts; ChatGPT Pro's personalized financial insights) already delivering expert financial guidance for freelancers, and that AI financial advice is becoming 'cheap and universally accessible.' This commoditizes the broader financial-intelligence value category the candidate sells, removing most margin for a paid newsletter even if peer-benchmark specifics aren't directly addressed.",
@@ -696,301 +971,22 @@
       "date": "2026-07-22"
     },
     {
-      "title": "VulnerabilityTap — The Primary Carer's Multi-Utility Social-Tariff, PSR & Crisis-Grant Activation Broker",
-      "oneLiner": "A fixed-fee transaction broker who, in one bundled transaction per household, audits eligibility for — and then completes the forms, switches and grant applications across — energy (PSR, social tariff, Warm Home Discount), water (WaterSure, CWTtariff), telecoms (BT Home Essentials, Virgin Oomph, social broadband, free SIM schemes), and council-tax reductions on behalf of the carer and the cared-for person simultaneously, charging £195 dual-household or £120 single.",
+      "title": "VulnerabilityTap, The Primary Carer's Multi-Utility Social-Tariff, PSR & Crisis-Grant Activation Broker",
+      "oneLiner": "A fixed-fee transaction broker who, in one bundled transaction per household, audits eligibility for, and then completes the forms, switches and grant applications across, energy (PSR, social tariff, Warm Home Discount), water (WaterSure, CWTtariff), telecoms (BT Home Essentials, Virgin Oomph, social broadband, free SIM schemes), and council-tax reductions on behalf of the carer and the cared-for person simultaneously, charging £195 dual-household or £120 single.",
       "gate": "payer_solvency",
       "gateLabel": "The payer cannot actually pay",
-      "reason": "The passages consistently characterize unpaid carers as a population in financial distress: Carers UK published a dedicated report titled 'Carer poverty and financial hardship in the UK' and held a parliamentary event on carer poverty; the Carer Poverty Coalition was formed specifically because 'financial support available to them' is 'limited'; and the cost-of-living crisis is highlighted as impacting them. This evidence undermines the claim that the target payer segment has discretionary budget for a £120–£195 fee, as the candidate concedes the payer draws from a 'constrained household budge",
+      "reason": "The passages consistently characterize unpaid carers as a population in financial distress: Carers UK published a dedicated report titled 'Carer poverty and financial hardship in the UK' and held a parliamentary event on carer poverty; the Carer Poverty Coalition was formed specifically because 'financial support available to them' is 'limited'; and the cost-of-living crisis is highlighted as impacting them. This evidence undermines the claim that the target payer segment has discretionary budget for a £120, £195 fee, as the candidate concedes the payer draws from a 'constrained household budge",
       "citations": [],
       "date": "2026-07-22"
     },
     {
-      "title": "SoleClaim — The Gen Z Sole-Trader's Money-Claims-Online Filing & Pre-Action Decision Pack",
-      "oneLiner": "A productised service that, from a Gen Z sole-trader's spreadsheet of an unpaid invoice (typically £400–£5,000 from a previous client), drafts a per-defendant-type pre-action letter plus a Money-Claims-Online (MCOL) County-Court filing pack ready for the sole-trader to lodge without a solicitor — charged at a flat £95 (pre-action only) or £185 (full MCOL filing pack, court-fee pass-through inclusive).",
+      "title": "SoleClaim, The Gen Z Sole-Trader's Money-Claims-Online Filing & Pre-Action Decision Pack",
+      "oneLiner": "A productised service that, from a Gen Z sole-trader's spreadsheet of an unpaid invoice (typically £400, £5,000 from a previous client), drafts a per-defendant-type pre-action letter plus a Money-Claims-Online (MCOL) County-Court filing pack ready for the sole-trader to lodge without a solicitor, charged at a flat £95 (pre-action only) or £185 (full MCOL filing pack, court-fee pass-through inclusive).",
       "gate": "incumbency",
       "gateLabel": "Incumbents already own the space",
       "reason": "Passages show Rocket Lawyer is a well-funded rival with 100K+ monthly users offering 'legal letters' and 'affordable legal documents' directly overlapping with the candidate's core pre-action letter and document-pack value proposition, meeting the 'well-funded rival' threshold for incumbency refutation.",
       "citations": [],
       "date": "2026-07-22"
-    },
-    {
-      "title": "WishlistAtlas — The Solo Indie Game Dev's End-to-End Steam Discovery & Conversion Atlas",
-      "oneLiner": "A paid weekly Substack that benchmarks anonymised Steam wishlist-to-sale conversion rates by genre, art style, demo presence, trailer strategy, launch discount and post-launch DLC cycle, sourced from a contributor panel of solo/small-team indie devs sharing their real per-game numbers.",
-      "gate": "incumbency",
-      "gateLabel": "Incumbents already own the space",
-      "reason": "GameDiscoverCo is a well-funded, dominant incumbent with tens of thousands of subscribers and a Pro tier already providing wishlist-to-sale conversion analysis (passages 03c0ad374df61464, abfb13669955df2e), supplemented by established tools like GameDevTools.net and SteamyData offering wishlist benchmarks; this goes beyond a mere competitor and represents a clear market leader already capturing a large share of the Steam discovery benchmarking need.",
-      "citations": [],
-      "date": "2026-07-22"
-    },
-    {
-      "title": "GasSafe Hold-Bond — The Sole-Trader Domestic Gas Engineer's Statutory-Trigger Income Micro-Bond",
-      "oneLiner": "A parametric daily income bridge that pays a sole-trader domestic gas engineer 75% of their verified day-rate (capped at 30 days per event, max 2 events per policy year) on ANY of four measured triggers: (1) Gas Safe Register Prohibition Notice or formal registration suspension, (2) ACS certificate re-assessment failure in the prior 90 days, (3) customer complaint escalated to Gas Safe with a formal investigation opened, or (4) mid-policy withdrawal of the engineer's Public Liability cover by their insurer.",
-      "gate": "legality",
-      "gateLabel": "There is a legal landmine",
-      "reason": "The candidate is functionally a contract of insurance (collecting recurring premiums and paying out on contingent statutory events). The passages establish that insurance activities require FCA authorisation [5d42ad9f5b94a83a, 16d24b5c34aed04b] and that the 'contract of insurance' is defined broadly enough to include arrangements 'that might not be considered a contract of insurance at common law'. Without FCA authorisation as insurer or intermediary, operating this parametric bond in the UK would breach the regulatory perimeter, so the margin cannot exist lawfully.",
-      "citations": [
-        {
-          "url": "https://handbook.fca.org.uk/handbook/perg2",
-          "domain": "handbook.fca.org.uk"
-        }
-      ],
-      "date": "2026-07-22"
-    },
-    {
-      "title": "NewtStop Bond — The Groundwork Contractor's Protected-Species Statutory Stop-Work Daily Income Micro-Bond",
-      "oneLiner": "A fixed-fee per-project micro-bond sold to UK groundworks and small civils contractors that pays a daily income bridge (capped at 60 days) if a great crested newt, bat roost, badger sett, hazel dormouse, water vole or white-clawed crayfish discovery halts works pending a Natural England or NRW mitigation licence — priced via a compounding dataset that crosses parish-level protected-species density with named ecologist turnaround times per local authority.",
-      "gate": "payer_solvency",
-      "gateLabel": "The payer cannot actually pay",
-      "reason": "The passages show construction accounts for 16% of all insolvencies in England and Wales (e2dd0d33831b751f, 6942c22fe5a22e52, 45b6d09e36e5aa05) and that even established groundworks subcontractors cannot obtain credit accounts from plant hire firms, indicating the payer segment is structurally financially fragile and likely unable or unwilling to commit discretionary budget to a £350–£900 micro-bond premium.",
-      "citations": [
-        {
-          "url": "https://archdesk.com/blog/problems-with-construction-subcontractor-procurement-uk",
-          "domain": "archdesk.com"
-        }
-      ],
-      "date": "2026-07-22"
-    },
-    {
-      "title": "FastTrackDESK — The Primary Carer's NHS Continuing Healthcare Fast-Track Application & Refusal-Reversal Broker",
-      "oneLiner": "Fixed-fee transaction broker who screens an elderly relative's eligibility, drafts the clinician-signed Fast-Track Pathway Tool with a condition-specific evidence pack, lodges it with the Integrated Care Board within 24-48 hours, and writes the per-ICB refusal-reversal letter — built on a proprietary dataset of per-ICB approval rates and rejection-reasons that swings outcomes.",
-      "gate": "incumbency",
-      "gateLabel": "Incumbents already own the space",
-      "reason": "Beacon is explicitly described as a well-funded organisation offering 'paid-for casework representation' for families navigating CHC, and another provider advertises 'Expert representation' with 'Over 50,000 helped' — these constitute well-funded rivals already serving the paid CHC advocacy/representation market the candidate targets.",
-      "citations": [
-        {
-          "url": "https://uk.linkedin.com/company/beacon-chc",
-          "domain": "uk.linkedin.com"
-        },
-        {
-          "url": "https://beaconchc.co.uk/",
-          "domain": "beaconchc.co.uk"
-        }
-      ],
-      "date": "2026-07-11"
-    },
-    {
-      "title": "GrievanceForge — The Gen Z Gig Worker's Platform Grievance Pack Engine",
-      "oneLiner": "A fixed-fee advisory pack engine for Gen Z gig and platform workers (Deliveroo, Stuart, Evri, Amazon Flex, Just Eat couriers, Uber Eats) hit by sudden pay-cuts, algorithmic deactivation, withheld tips, or contract re-classification — delivering per-platform grievance-letter templates, back-pay arithmetic, ACAS conciliation packs, and employment tribunal filing briefs for £89 per dispute pack.",
-      "gate": "value_durability",
-      "gateLabel": "The value would not last",
-      "reason": "The candidate's claimed defensible core is a proprietary dataset of platform grievance outcomes 'scraped from public Employment Tribunal decisions.' But passage describes a free, daily-updated structured index of exactly those public tribunal decisions, cross-cut by employer and outcome — directly commoditising the proprietary data moat. Combined with free ACAS templates and advice (, ), the first-party free tools remove the margin the pack relies on.",
-      "citations": [
-        {
-          "url": "https://tribunalwatch.co.uk/",
-          "domain": "tribunalwatch.co.uk"
-        },
-        {
-          "url": "https://www.acas.org.uk/advice",
-          "domain": "acas.org.uk"
-        },
-        {
-          "url": "https://www.acas.org.uk/",
-          "domain": "acas.org.uk"
-        }
-      ],
-      "date": "2026-07-10"
-    },
-    {
-      "title": "FarrierCycle — The Sole-Trader Farrier's Per-Horse Service Cycle, Yard Access & Owner-Communication Brief",
-      "oneLiner": "A vertical scheduling tool for UK sole-trader farriers that tracks every horse's trim/shoe cycle, sends automated owner SMS reminders, stores per-yard logistics (parking, gate codes, stable layout, handling notes) and produces FRFC-aligned CPD logs plus insurance-defensible yard risk assessments.",
-      "gate": "incumbency",
-      "gateLabel": "Incumbents already own the space",
-      "reason": "The passages document at least four dedicated farrier-specific apps (ee1caa8f5404ec39, 7a6af7e1ff668c5e, 6a78cb9df87c154c, 11d99c73cca6bc3e) plus the Stables platform, all offering scheduling, invoicing, reminders, horse-level service records, and contacts — the core features the candidate claims as its wedge. Multiple specialized, UK-available competitors targeting this exact segment constitutes a served market, not an underserved one.",
-      "citations": [
-        {
-          "url": "https://stables.co/blog/best-farrier-management-software",
-          "domain": "stables.co"
-        }
-      ],
-      "date": "2026-07-10"
-    },
-    {
-      "title": "CycleCrash — The Gig Cyclist's First-72-Hours Adversarial Evidence Pack",
-      "oneLiner": "A fixed-fee adversarial evidence pack for Gen Z Deliveroo, Uber Eats or Just Eat cyclists who have been hit by a car on shift — capturing scene data before the platform's own incident protocol or the at-fault driver's loss-adjuster can revise the narrative, built on a proprietary dataset of per-borough police RTC referral rates and per-platform incident-response variance.",
-      "gate": "incumbency",
-      "gateLabel": "Incumbents already own the space",
-      "reason": "Multiple passages describe well-funded specialist law firms (Fletchers Solicitors, Cycle's specialist solicitors, and others) operating dedicated delivery-rider accident claims teams targeting exactly this audience—Deliveroo/Uber Eats cyclists in non-fault RTCs—on a No Win No Fee basis, which would subsume evidence preservation as part of their service. This constitutes funded rivals already capturing this exact segment, not an open space.",
-      "citations": [],
-      "date": "2026-07-09"
-    },
-    {
-      "title": "SolePitch — The Public-Sector Worker's Workplace Shoe & Leather Repair Pop-Up",
-      "oneLiner": "A solo mobile cobbler who sets up a monthly 'done-while-you-work' shoe, boot, belt and bag repair pitch at NHS trust, local-government and school staff car parks, undercutting high-street chains by 30-40% because there's no shop rent, no counter staff and the shift-worker never has to leave the ward or classroom.",
-      "gate": "value_durability",
-      "gateLabel": "The value would not last",
-      "reason": "Multiple passages indicate shoe repair demand is structurally declining: UK cobblers falling 3.8% yearly, fast fashion reducing repairable shoe quality and demand, millennials bypassing cobblers for cheaper replacements, and industry predicted to continue declining. Only one passage hints at a sustainability counter-trend, but it describes awareness rather than confirmed behavior change. The net evidence suggests the underlying value of shoe repair is evaporating rather than durable.",
-      "citations": [
-        {
-          "url": "https://journalism-school.cardiff.ac.uk/thecardiffian/2025/12/03/when-times-are-bad-cobblers-will-always-do-well-how-one-cardiff-cobbler-is-finding-success-during-the-cost-of-living-crisis/",
-          "domain": "journalism-school.cardiff.ac.uk"
-        },
-        {
-          "url": "https://decentfoot.com/why-is-the-shoe-maker-business-dead-2/",
-          "domain": "decentfoot.com"
-        },
-        {
-          "url": "https://www.blabber.buzz/flipbook/1053090-the-diminishing-art-of-shoe-repair--how-fast-fashion-is-outpacing-cobblery",
-          "domain": "blabber.buzz"
-        },
-        {
-          "url": "https://www.reskinned.clothing/the-re-edit-blog/12-sustainable-shoe-disposal-options",
-          "domain": "reskinned.clothing"
-        }
-      ],
-      "date": "2026-07-09"
-    },
-    {
-      "title": "NI-GapSweep — The Gen Z Casual Worker's NI-Record Gap Audit & Voluntary Contribution Decision Pack",
-      "oneLiner": "A £45 fixed-fee productised audit pack for Gen Z casual workers that reconstructs their HMRC National Insurance record from their State Pension Forecast PDF, ranks missing qualifying years by 2028-state-pension-forecast impact, and ships with pre-filled CF83 Class 3 voluntary-contribution forms for the optimal six-year backfill window — without the user ever needing to read a 90-page HMRC guidance note.",
-      "gate": "pain_reality",
-      "gateLabel": "The pain was not real",
-      "reason": "The passages confirm Gen Z is aware of state pension concerns but explicitly document a 'troubling gap between knowledge and action', with nearly half believing the state pension won't exist by retirement. This combination — acute anxiety paired with demonstrated inaction — undermines the pain_reality claim that Gen Z casual workers will pay £45 NOW to audit NI gaps, as the target persona is shown to be aware but not converting awareness into action.",
-      "citations": [
-        {
-          "url": "https://www.professionalpensions.com/opinion/4518679/pensions-age-uncertainty-gen",
-          "domain": "professionalpensions.com"
-        },
-        {
-          "url": "https://www.professionalpensions.com/opinion/4518679/pensions-age-uncertainty-gen",
-          "domain": "professionalpensions.com"
-        }
-      ],
-      "date": "2026-07-08"
-    },
-    {
-      "title": "CareDeposit Rescue — The Bereaved Carer's Care-Home Deposit Clawback Broker",
-      "oneLiner": "A no-win-no-fee transaction broker that audits a UK care home's deductions from a deceased resident's deposit, challenges every contractually illegitimate line item, and remits 75% of the net refund to the bereaved primary carer.",
-      "gate": "legality",
-      "gateLabel": "There is a legal landmine",
-      "reason": "The candidate's 75% contingency fee arrangement is functionally a Damages-Based Agreement, and the passages establish that DBAs are capped at 25% for personal injury and 50% for commercial actions in England and Wales [58d8d132159e5072, f92b7dab877b90df], meaning a 75% fee exceeds the statutory cap and is therefore unlawful.",
-      "citations": [],
-      "date": "2026-07-08"
-    },
-    {
-      "title": "The Adoption Match Atlas",
-      "oneLiner": "A personalised matching intelligence brief for approved UK adopters, built on a FOI-derived, quarterly-compounding dataset of per-agency wait times, placement-preference profiles and family-finding social-worker turnover across England's Regional Adoption Agencies and Voluntary Adoption Agencies.",
-      "gate": "payer_solvency",
-      "gateLabel": "The payer cannot actually pay",
-      "reason": "The candidate rests payer solvency on adopters having 'already invested £10–30k in legal/social-work fees,' but passages [1c90867e] and [5b4d8f5b] state domestic UK adoption is free with out-of-pocket costs of only 'a few hundred pounds in total' (the £12–25k figure in [4f75b49a] is explicitly for international adoption). Passage [095ead1e] further shows this exact demographic is served by free advice lines, undercutting both the sunk-cost framing and likely willingness to pay a new £175–£295 fee.",
-      "citations": [],
-      "date": "2026-07-08"
-    },
-    {
-      "title": "WindBond — The Scaffolder's HSG253 High-Wind Stop-Work Daily Income Micro-Bond",
-      "oneLiner": "A parametric micro-bond sold per scaffold contract that pays the scaffolder a verified day-rate whenever Met Office station data confirms sustained wind above the HSG253 stop-work threshold during the contracted hire period.",
-      "gate": "legality",
-      "gateLabel": "There is a legal landmine",
-      "reason": "The passages establish that 'effecting contracts of insurance' is a regulated activity, parametric policies are within the scope of insurance contract law review, and 'insurance risk transformation' is being introduced as a new regulated activity under FSMA. The candidate's product—premium paid in exchange for an automated payout triggered by a defined weather event—is structurally insurance regardless of its 'micro-bond' framing, and under this regulatory framework would require FCA authorization to be sold lawfully to UK scaffolders.",
-      "citations": [],
-      "date": "2026-07-08"
-    },
-    {
-      "title": "AdaptClear Desk — The Carer's Post-Care Major Home-Adaptation Removal & Resale Broker",
-      "oneLiner": "When the person a primary carer has been caring for at home dies or moves into a care home, the home is left with a stairlift, a level-access shower, a ceiling hoist and a wet-room floor — adaptations that block re-sale of the property, cost £300–£1,500 each to remove, and that an estate agent has just told the carer will knock £4–£9k off the asking price. AdaptClear aggregates the small, fragmented UK trade of specialist adaptation-removal contractors, brokers the booking within 48 hours, and also brokers resale of cleaned-and-tested units to second-user installers — converting an invoice into a £150–£400 net rebate in the carer's pocket.",
-      "gate": "incumbency",
-      "gateLabel": "Incumbents already own the space",
-      "reason": "The candidate's hypothesis that no intermediary brokers the private-household supply side for adaptation removal-plus-resale is directly contradicted by the passages, which describe at least two stairlift removal services offering exactly this bundled model (removal + cash-back purchase of used stairlifts), including nationwide coverage.",
-      "citations": [],
-      "date": "2026-07-07"
-    },
-    {
-      "title": "MindReady — The Ofsted-Ready Childminder's Per-Inspection Evidence Dossier",
-      "oneLiner": "A per-inspection evidence dossier, compiled from each childminder's existing logs and a proprietary FOI-derived atlas of which evidence types Ofsted inspectors actually cite when awarding 'Good' or 'Outstanding' grades.",
-      "gate": "pain_reality",
-      "gateLabel": "The pain was not real",
-      "reason": "Passage 03bfb0dbb1ab7135 states 98% of childcare providers had been judged good or outstanding, directly contradicting the candidate's claim that 'the majority prepare generic evidence folders [and] fail to Good.' With only ~2% failing inspection, the acute pre-inspection pain and willingness-to-pay is far narrower than the hypothesis asserts.",
-      "citations": [],
-      "date": "2026-07-05"
-    },
-    {
-      "title": "CareCostCompass — The Squeezed-Middle Eldercare Forward Planner",
-      "oneLiner": "A web app that turns a family's specific parental finances — savings, property, gifting history, local authority — into a 5–20 year projection of council-funded vs self-funded social-care costs, flagging deprivation-of-asset triggers and the inheritance-tax endgame.",
-      "gate": "value_durability",
-      "gateLabel": "The value would not last",
-      "reason": "Passage describes a free UK long-term care calculator already covering England/Scotland/Wales/NI, the £86k cap, home-protection logic, and Power of Attorney / wills / SOLLA — a free first-party tool that commoditises the bulk of the basic care-planning value proposition CareCostCompass proposes to charge £80–£250 for. No passage confirms that the forward 5–20 year LA-specific projection is uniquely available or not already subsumed by this free offering.",
-      "citations": [
-        {
-          "url": "https://wealthr.co.uk/tools/long-term-care-uk/",
-          "domain": "wealthr.co.uk"
-        }
-      ],
-      "date": "2026-07-05"
-    },
-    {
-      "title": "The Hard Brief",
-      "oneLiner": "A paid weekly newsletter for creative freelancers that publishes forensic teardowns of real difficult-client scenarios, with sample language, contract clauses, and tactical playbooks for handling scope creep, late payments, and rate pushback.",
-      "gate": "value_durability",
-      "gateLabel": "The value would not last",
-      "reason": "The passages show the core tactical value the newsletter would sell — complete escalation frameworks with email templates, late-fee strategies, scope-creep prevention strategies with real examples and free tools, and contract clauses — already exists as free, comprehensive content. Combined with advancing AI contract generators and management tools, the underlying tactical content is substantially commoditised, eroding the margin a paid curation layer could capture.",
-      "citations": [],
-      "date": "2026-07-03"
-    },
-    {
-      "title": "RemoRidge — The Squeezed-Middle Remortgage Cliff-Edge Decision Pack",
-      "oneLiner": "A £39 one-off downloadable decision pack for UK homeowners whose 2020–2022 cheap-fix mortgage is unwinding: combines your current ERC exposure, lender stress-test affordability floor, salary-sacrifice-to-overpay micro-simulator, broker-interview script and a maintained live database of back-channel re-fix products — so the £500 whole-of-market broker fee feels optional.",
-      "gate": "incumbency",
-      "gateLabel": "Incumbents already own the space",
-      "reason": "Passage explicitly describes Tembo as 'Voted the UK's Best Mortgage Broker 5 years running' with 100+ lenders and 20,000+ schemes — a clear market leader in the remortgage space, which per the incumbency precedent constitutes a dominant incumbent. Passage further shows free remortgage comparison and personalised advice services, indicating the comparison-shopping layer is not underserved.",
-      "citations": [
-        {
-          "url": "https://www.tembomoney.com/remortgage-lp?msclkid=ca75a2076f5f1371552fc840ce082866&utm_source=bing&utm_medium=cpc&utm_campaign=PPC_Remortgage_Generics&utm_term=remortgage&utm_content=Remortgage_Generics_Core_Phrase",
-          "domain": "tembomoney.com"
-        },
-        {
-          "url": "https://getmymortgage.co.uk/pre/5/remortgage-calculator?utm_source=bing&utm_medium=cpc&utm_campaign=686996689&utm_adgroup=1312819174762880&utm_keyword=remortgage%20deals&matchtype=p&utm_network=o&utm_device=c&utm_term=Moneyfacts%20MSE%20Which%20remortgage%20guide%20free%20incumbent&utm_creative=82051430126009&utm_content=&exp=&v=&role=&msg=&loc_int=&loc_phy=41471&msclkid=ab2dd7ec4822142c1849bdabe9750d32",
-          "domain": "getmymortgage.co.uk"
-        }
-      ],
-      "date": "2026-07-03"
-    },
-    {
-      "title": "CHC Retrospect — The NHS Continuing Healthcare Retroactive Claim Broker",
-      "oneLiner": "A no-win-no-fee transaction broker for UK primary_carers — prepares and prosecutes retrospective NHS Continuing Healthcare (CHC) claims against the ICB for care-home fees the family should not have paid, taking 18–22% of the statutory cash recovered.",
-      "gate": "incumbency",
-      "gateLabel": "Incumbents already own the space",
-      "reason": "Beacon CHC has already helped over 50,000 families and explicitly provides 'Expert representation' and 'Full appeal management and complaints service' for CHC claims (not merely advice), directly occupying the adversarial-representation role the candidate claims is open; Martin Searle and other firms also serve retrospective CHC reclamations, making this a contested space with a clear incumbent leader.",
-      "citations": [],
-      "date": "2026-07-02"
-    },
-    {
-      "title": "BatteryDossier — The Gig Driver's EV Resale Health Certificate",
-      "oneLiner": "A done-for-you battery-health certification service that lets high-mileage rideshare/delivery drivers sell their used EV at a verified premium instead of a fear-discount.",
-      "gate": "incumbency",
-      "gateLabel": "Incumbents already own the space",
-      "reason": "Recurrent already sells battery-health resale certificates that boost used-EV prices ~7% and is integrated into Experian's AutoCheck vehicle history reports [872c130da09bcb97, 3e83a6c7e10a74f0], a well-funded rival already solving the exact certified-resale-premium need, so the space is not underserved.",
-      "citations": [
-        {
-          "url": "https://businessmodelcanvastemplate.com/products/recurrent-business-model-canvas",
-          "domain": "businessmodelcanvastemplate.com"
-        }
-      ],
-      "date": "2026-07-02"
-    },
-    {
-      "title": "RoastLock — The Micro-Roaster's Roast-Curve IP Vault",
-      "oneLiner": "A vertical tool that captures every roast's thermocouple curve and ties it to the exact green-bean lot, turning a micro-roaster's tacit skill into a re-orderable, drift-controlled proprietary profile library.",
-      "gate": "incumbency",
-      "gateLabel": "Incumbents already own the space",
-      "reason": "Cropster is a dominant incumbent trusted in over 100 countries that already does exactly what the candidate claims is uncaptured — linking cupping/quality data to every roast batch and managing green lots; the space is crowded with named rivals rather than underserved.",
-      "citations": [
-        {
-          "url": "https://www.cropster.com/",
-          "domain": "cropster.com"
-        },
-        {
-          "url": "https://eng.firescope.cropster.com/cropster",
-          "domain": "eng.firescope.cropster.com"
-        },
-        {
-          "url": "https://www.cropster.com/products/roast/features/",
-          "domain": "cropster.com"
-        },
-        {
-          "url": "https://coffeetec.com/blogs/news/roast-profiling-software-helps-you-achieve-a-consistent-coffee-roast?srsltid=AfmBOop1xcc7Ch0fmDwbil9SQuFS_30YJzdUr5dQuMJNO_MCl6TCr4dC",
-          "domain": "coffeetec.com"
-        }
-      ],
-      "date": "2026-07-02"
     }
   ]
 }
diff --git a/tools/make_kill_log.py b/tools/make_kill_log.py
index aeced95..bfd2f96 100644
--- a/tools/make_kill_log.py
+++ b/tools/make_kill_log.py
@@ -93,6 +93,27 @@ ACCUSATORY = re.compile(
 CITATION_REF = re.compile(r"[\(\[]([0-9a-f]{16})[\)\]]")
 
 
+def nodash(s: str | None) -> str:
+    """Strip em-dashes and en-dashes — the universal AI writing tell.
+
+    Replaces them with `, ` (the most natural English substitution) and collapses
+    any leftover whitespace. Compound words like "out-of-hours" and "slip-resistance"
+    are preserved because the regex only matches dashes surrounded by whitespace.
+
+    Mirrors the same pattern in tools/make_sample_report.py so the published voice
+    is consistent across the kill-log and the free sample report. The post-processor
+    runs at publish time, here, so the underlying dossiers and the engine's verdicts
+    are untouched — no moat change, only cosmetic normalisation.
+    """
+    if not s:
+        return ""
+    s = s.replace("\u2014", ", ").replace("\u2013", ", ")
+    s = re.sub(r"\s+-\s+", ", ", s)
+    s = re.sub(r"\s+", " ", s).strip()
+    # Tidy up the spaces the dash substitution leaves behind: "Brand , X" → "Brand, X".
+    return re.sub(r"\s+([.,;])", r"\1", s)
+
+
 def _sources_by_id(dossier: dict) -> dict[str, str]:
     """Every retrieved source in the dossier, keyed by the hash its prose cites."""
     index: dict[str, str] = {}
@@ -109,14 +130,15 @@ def _clean_reason(reason: str) -> str:
 
     Two prefix formats are in the corpus — the older `Gate 'incumbency' fired — ...` and the
     newer `It failed on: Do incumbents already own this? (`incumbency`) — ...`. Both restate
-    the gate, which the page renders separately, so both go.
+    the gate, which the page renders separately, so both go. `nodash()` is applied last to
+    sweep the em/en-dashes the LLM verdict uses for parenthetical clauses.
     """
     text = re.sub(r"^Gate '[^']+' fired\s*[—–-]\s*", "", reason).strip()
     text = re.sub(r"^It failed on:.*?\(`[^`]+`\)\s*[—–-]\s*", "", text).strip()
     text = re.sub(r"^refuted \(conf [\d.]+\):\s*", "", text).strip()
     text = CITATION_REF.sub("", text)
     text = re.sub(r"\s{2,}", " ", text).strip()
-    return re.sub(r"\s+([.,;])", r"\1", text)
+    return nodash(re.sub(r"\s+([.,;])", r"\1", text))
 
 
 def build(limit: int) -> dict:
@@ -151,8 +173,8 @@ def build(limit: int) -> dict:
 
         candidate = dossier.get("candidate") or {}
         entries.append({
-            "title": str(candidate.get("title") or "").strip(),
-            "oneLiner": str(candidate.get("one_liner") or "").strip(),
+            "title": nodash(candidate.get("title")),
+            "oneLiner": nodash(candidate.get("one_liner")),
             "gate": gate,
             "gateLabel": GATE_LABELS.get(gate, "It failed a check"),
             "reason": _clean_reason(reason),

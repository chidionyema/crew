---
captured: 2026-08-01T22:46:49+00:00
session: dfd30925-927b-4488-8a7f-417d180331d3
cwd: /Users/chidionyema/Documents/code/prospector
chars: 32068
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are the Architect reviewing a Builder's diff against the task contract. The project's verify command already exits 0.

TASK:
## Matchmaker promotion — 2026-08-01

The spec is at `specs/matchmaker-promotion-2026-08-01.md`. **Read it in full first.** Every numbered item, every file, every acceptance clause is the contract. Do not paraphrase.

The failing test is at `store_platform/src/Store.Web/src/__tests__/matchmakerPromotionContract.test.ts`. **Do NOT modify it.** It is protected; restoring byte-for-byte at verify time.

### Branch & state

Working branch is `matchmaker-promotion-2026-08-01` (already created from `main`). Runtime artifacts are dirty — **DO NOT `git add` or commit any of those.** Only `git add` the files you intend to change.

### Procedure — one commit

Three changes across three files (plus the new test + spec).

**Change 1: Auto-open the Matchmaker on first visit to `/`**

In `pages/index.tsx`'s `CatalogBrowser`:

- Add a `useEffect` that fires once on mount. Inside it, read `localStorage.getItem('mumchimp.matchmaker.autoOpened.v1')`. If absent AND the buyer has no cart items, call `setMatchOpen(true)` and write the flag back.
- The check `cart.count > 0` (or `cart.ready && cart.count > 0`) is the returning-visitor guard. Returning buyers see the shelf immediately.
- Guard against SSR: read `localStorage` ONLY inside the `useEffect`, never at render. The HTML must not depend on browser state (same regression that the existing `useSyncExternalStore` at `pages/orders/success.tsx:46` works around).
- Do NOT re-open on subsequent visits. The flag is set on first auto-open. The buyer can still open manually via the toolbar trigger.

**Change 2: Reframe the language (copy only, no mechanics)**

| File | Find | Replace |
|------|------|---------|
| `components/discovery/FacetBar.tsx:213` (mobile disclosure JSX) | `Filters` (inside the button children) | `Your constraints` |
| `components/discovery/FacetBar.tsx:233` (Modal title prop) | `Narrow the shelf` | `Tell us what fits your life` |
| `components/discovery/Matchmaker.tsx` `MatchmakerTrigger` label | current "Matchmaker" or whatever the trigger renders | `Find my fit` |

The interior copy of the Matchmaker stays verbatim — only external labels change.

**Change 3: Dynamic count on the MatchmakerTrigger**

In `pages/index.tsx`'s `CatalogBrowser`:

- Compute `liveMatches` via `rankMatches(packs, answers)` whenever `packs` or the answers state change. Lift the call up so the trigger can read it without the panel being open.
- Pass `count={liveMatches.length}` and `countLabel="that fit your life"` (or `countLabel="total"` when no answers are set) into `<MatchmakerTrigger onOpen={...} count={...} countLabel={...} />`.

In `components/discovery/Matchmaker.tsx`:

- Extend `MatchmakerTrigger`'s props to accept `count?: number` and `countLabel?: string`.
- Render `Find my fit — {count} {label}` when `count` is provided; render `Find my fit` alone when it isn't. The button stays a button — no separate focus target.

`MatchmakerTrigger` is presentational. No internal data fetching.

### Verify command (only exit 0 is "done")

Run from `store_platform/src/Store.Web`:

```
npm test -- --run && npm run verify && npm run build
```

End with `echo "MATCHMAKER_OK"` on success.

### Failure modes to watch for

- **localStorage at SSR** — read inside `useEffect` ONLY. `typeof window === 'undefined'` is not the right guard; just never touch localStorage at render time.
- **Hydration mismatch** — auto-opening the panel must not produce different HTML between server and client. The panel is `matchOpen ? <Matchmaker ... /> : null`, and `matchOpen` starts as `false` (the useState default). The effect runs after mount and updates state, which is the supported React pattern.
- **`cart.count` SSR** — the cart context reads from localStorage too. Read it inside the effect, or use `cart.ready` to guard.
- **MatchmakerTrigger aria-label** — keep the existing `aria-label` if there is one; just add the count rendering as visible text inside the button. Don't break the existing aria contract.
- **Tailwind 4 classes** — any new utility that doesn't compile (e.g. `gap-x-N` with a non-standard value) should fall back to a class that compiles. Run `npm run build` and check the output.

### When you finish

Print:
- The commit SHA with one-line summary.
- The full file list you changed, with line counts.
- The verify-chain output, last ~20 lines.
- A one-line confirmation that `echo "MATCHMAKER_OK"` printed.

Do NOT self-report success — the verify exit code is the only signal that counts.

Judge whether the diff fully and correctly satisfies the task with no scope creep, no security/correctness regressions, and adequate tests. Respond with a FIRST LINE of exactly "VERDICT: APPROVE" or "VERDICT: REJECT", then a brief rationale.

--- git diff ---
diff --git a/storage/durable_ledger.md b/storage/durable_ledger.md
index 108d07d..0e3ad5b 100644
--- a/storage/durable_ledger.md
+++ b/storage/durable_ledger.md
@@ -831,4 +831,58 @@
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
 * LAW: Do not build wrappers on transparent markets.
\ No newline at end of file
diff --git a/store/control_center/config_history.jsonl b/store/control_center/config_history.jsonl
index f4229a6..2edb227 100644
--- a/store/control_center/config_history.jsonl
+++ b/store/control_center/config_history.jsonl
@@ -550,3 +550,23 @@ backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidi
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

---
captured: 2026-08-06T21:23:08+00:00
session: 04edd4c2-05bb-4f4c-a710-35d198e64ca2
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2798
source: founder prompt, verbatim (founder-doc-capture.py)
---

not jist tech r or startup operator. And the hardcoded sector list in discover.py:18-21 contains no technology/software/AI entry at all. The catalogue has 78 distinct niches (beekeepers, funeral directors…) but they're all one meta-shape: individual-vs-bureaucracy claims/compliance recovery. Fix is upstream and small: add tech sectors + a tech-operator we neeed to broaded nore, , we need to address properoly 
Quality floor is a real commercial liability: one live pack ships a green ✅ PASS banner while its own claims_verifiable check is refuted ("the sources contradict this") and its own adversarial pass names an accredited £300 incumbent doing exactly the same thing — buried at line 98 of the QA report. Another pack's financial model mixes £ and $ on its own headline revenue line for a US-market buyer. The ceiling is genuinely good (business-plan-grade, ~20 citations, honest assumption labelling), so this is a floor problem, not a capability problem.

Format: buyers get 8 markdown files + 1 static HTML render. Meanwhile the pipeline already computes and then discards exactly what the market research said commands higher prices: a numeric six-axis score breakdown, Python-exact financial-model figures, and cited price-comparables anchors (fetched, used internally for pricing, never shown to the buyer). Shipping financials.json / comparables.json in the bundle is mostly plumbing in bridge.py.
, the fornat also, we need ore options not just narkdown, i neant less reliance on large language nodel 
"Less reliance on the coding agent" is closer than expected: a working API-key ClaudeOperator already exists and is already trusted in MOAT_PRIMARY (operator.py:161-183, :889). Funding the API operator is pure config wiring — set ANTHROPIC_API_KEY, add claude to the operator chain. Generation, prescreen, score, and artifact stages are already routed to cheaper non-critical chains; only verdict + adversarial structurally need moat-grade trust. query_gen and price_comparables currently ride the moat but don't rule — downgrade candidates worth an A/B.,
The pipeline & k=100 audit is in. The headline findings:

k=100 is a config change, not a rewrite — the binding constraints are three mechanical bottlenecks:
1. claude_concurrency: 4 (config.yaml:150) — a machine-wide ceiling on concurrent CLI subprocesses shared by every parallelism layer. Raising it needs load-testing (there's a proven prior collision at concurrency=2 fixed by per-slot stable cwd), not just editing the number.
2. vet_workers: 3 — only 3 candidates are ever mid-vet at once; must rise in lockstep with #1.
3. The per-candidate verdict loop is sequential by design (kill-fast short-circuit) — survivors pay 8+ sequential round-trips each.
 we need solutiona, yoi RE NOST capable agent and you can resech

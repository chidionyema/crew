---
captured: 2026-08-08T00:26:34+00:00
session: 069c917e-0749-4238-856c-5885c780ae4b
cwd: /Users/chidionyema/Documents/code/prospector
chars: 9641
source: founder prompt, verbatim (founder-doc-capture.py)
---

The POPDD gate is running on the commit (~9 min). Here is the close-out.

All four items addressed

1. The numeric-citation live rate — the measurement was measuring us.

The shipped shadow read 38.0% of asserted figures as untraceable; q4c read 10.1% on the same corpus. Both were wrong, in the same direction.

[A] store/numeric_citation_shadow/shadow-2026-08.jsonl  rows=132
[B] ALL 132 rows              : 35/92 = 38.0%   <- double-counts re-vetted checks
[C] 104 distinct (cand,check) : 21/62 = 33.9%   <- lumped, right denominator
[D] the 62 figures, WITH the self-reference split
      self_ref      15/62 = 24.2%
      UNTRACEABLE    6/62 =  9.7%   Wilson95 [4.5, 19.5]
    q4c on 1,611 dossiers, same statistic: 10.1%  -> inside the interval

The load-bearing part isn't the denominator, it's the second error: verify._check_question started stating the actual price rung to payer_solvency on 2026-08-06 so the check would stop inventing one. The model now repeats the rung we handed it, and a checker with no self-reference bucket scored that obedience as a fabricated claim. An enforcement threshold calibrated on the lumped number would have tightened every time we told the model more truth. numeric_citation.py now carries q4c's buckets. untraceable_rate keeps its old lumped meaning for rows written before today, and summarise_shadow_log counts those rows separately instead of assuming they held zero self-references — that assumption is what made the two numbers look like they disagreed. Still shadow_mode: true; enforcement stays your call, but the number it would be made on is now the right number.

2. Vocabulary drift — §30.3's claim is retracted. The drift is real (29 structural_form values in the index against 8 configured, 421 rows), but the consequence the doc attributed to it is false: generate.py:272-274 does supply the configured domain, and coverage_sampler.enabled is False anyway. The legacy values arrive with fresh timestamps because the drain vets candidates minted under older configs, not because generation is producing them. The latent trap (sampling_domains falling back to cov.observed if a caller forgets domains=) is now fenced, and coverage.off_domain_values() ships in every receipt — a measurement instead of prose.

3. _keywords mangled tails — real, but dead code. The k=4 call site is _entity_queries (verify.py:267), gated at verify.py:564-565 on hybrid_entity_checks, which is [] at config.yaml:113. Unreachable. The shipped path is k=6 at verify.py:224, where 31.2% of query bases lead with a product-wrapper word instead of a domain term. I did not act on that — E1 is just-measured evidence that blind query surgery can be wrong-signed. Filed as a candidate experiment.

4. E3's quiet fence is now per call. E1's run bo2mosjog had store/scheduler/PAUSE created at 00:25Z and gone by 00:35Z with the run in flight and the daemon live. Nothing in this repo unlinks it, so it can't be prevented — but every measured call now stamps its own reading, and _quiet_report names the call wd marks the run unquotable. Recorded, never aborted.

Also found: E15 and E17 are not a matched pair. Sament fingerprints (d97829ed7ea0bae0 at 20:16:23Z vs81d96e5387f7467a at 20:35:10Z). Any agreement figure across them compares two samples, not two methods. The fingerprinted repeat
is still owed.

Do we use the experiments in the pipeline?

Re-read from disk, not from memory:

┌──────────────────────┬──────────────────────────────────────────────────────────┬────────────────┐
│      Experiment      │                Config                │           Reaches the pipeline at           │     State      │
├──────────────────────┼──────────────────────────────────────────────────────────┼────────────────┤
│ E11 confidence floor │ confidence_floor: 0.4                │ kill_filter.py:50                           │ ACTING         │
│                      │ (config.yaml:223)                                        │                │
├──────────────────────┼──────────────────────────────────────┼─────────────────────────────────────────────┼────────────────┤
│ Q4 admissibility     │ policy: P1_check_aware (:2,512 — demotes inadmissible    │ ACTING         │
│                      │                                      │ rulings to UNVERIFIABLE                     │                │
├──────────────────────┼──────────────────────────────────────────────────────────┼────────────────┤
│ E3 concurrency knee  │ claude_concurrency: 4 (:154)         │ operator.py:1081 → claude_cli.py:48         │ ACTING         │
├──────────────────────┼──────────────────────────────────────────────────────────┼────────────────┤
│ Generation           │ generation.structural_forms          │ generate.py:167                             │ ACTING         │
│ vocabulary           │                                                          │                │
├──────────────────────┼──────────────────────────────────────┼─────────────────────────────────────────────┼────────────────┤
│ numeric_citation     │ enabled: true, shadow_mode — logs, cannot rule           │ SHADOW         │
│                      │ (:1075-1076)                         │                                             │                │
├──────────────────────┼──────────────────────────────────────────────────────────┼────────────────┤
│ E6 prescreen         │ shadow_mode: true (:1036)            │ prescreen.py:23,169                         │ SHADOW (E6     │
│ prefilter            │                                                          │ killed)        │
├──────────────────────┼──────────────────────────────────────┼─────────────────────────────────────────────┼────────────────┤
│ E1 hybrid entity     │ hybrid_entity_checks: [] ( — empty gate                  │ INERT (E1      │
│ queries              │                                      │                                             │ killed)        │
├──────────────────────┼──────────────────────────────────────────────────────────┼────────────────┤
│ E16 rerank           │ no key exists                        │ —                                           │ INERT (ceiling │
│                      │                                                          │  probe)        │
├──────────────────────┼──────────────────────────────────────┼─────────────────────────────────────────────┼────────────────┤
│ V2 coverage sampler  │ enabled: false (:1087)    72                             │ INERT          │
└──────────────────────┴──────────────────────────────────────┴────────────────────────────
Four levers act on every run. Two log behind an explicit fence. Three are inert because thea ceiling probe — which is the programme working: ahipping is the cheapest result available.
                                                                                           Verification
                                                                                           tests/unit — 1513 passed, 2 skipped in 67.76s     (
                                                                                           All 18 new tests mutation-proved: six mutations, eaace, each killing exactly the tests that pin it, tree restored green. The non-vacuity tests (test_the_split_is_not_vacuous_without_the_haystack, test_a_world_claim_is_never_absorbed_into_self_refes_nothing_rather_than_flagging_everything) fail on abuild that classifies everything, so the positive tests can't pass trivially.

The one failure from the earlier run — test_claim_lock.py::test_exactly_one_of_eight_threads_wins_when_stealing_an_expired_lock —
passed 3/3 alone and passed in this full run; it's rn, and nothing I touched is near it.

§31 is written to docs/COMMERCIAL_READINESS_PROGRAMrrying all of the above including the retraction andthe experiment-wiring table.

I'll confirm when the POPDD gate finishes and the commit lands.

✻ Worked for 24m 44s

⏺ Background command "Commit the three fixes, tests and §31" completed (exit code 0)

Exit 0 there is tail's status, not the commit's — verifying the commit actually landed:

  Ran 1 shell command

Commit was blocked, not landed — the notification's exit 0 was tail's. A real lint failure in my own test:

⏺ Update(tests/unit/test_e3_quiet_fence.py)
Removed 1 line


def test_no_calls_at_all_is_not_held():
    e3 = _load_e3()
    assert _load_e3()._quiet_report([])["held"] is False



  Ran 2 shell commands

The commit was blocked, not landed — worth stating plainly since I'd told you it was pending.                                   
ruff failed the POPDD gate on my own test: tests/unit/test_e3_quiet_fence.py:92: F841 Local variable 'e3' is assigned to but nevused — I bound e3 = _load_e3() and then called _loaine. Fixed, lint now clean on all seven paths,test_e3_quiet_fence.py still 6/6. Re-running the gate.                                                                          
Two notes on the mechanics, since both bit here:                                                                                
- The task notification's exit code 0 was tail's, not git commit's — the known trap. git log -1 showed HEAD still at 44fef95,   which is how the block surfaced.
- I should have linted my own paths before spending the first ~9-minute gate cycle. That's on me; doing it as a preflight now.  
Everything else in the close-out stands unchanged — the suite result (1513 passed, 2 skipped), the six mutation proofs, and §31 are all on disk and unaffected by the lint fix. I'lly moves.

✻ Brewed for 40s · 1 shell still ok so whats the status? are we ready to ship and close the prograe? what is outstanding

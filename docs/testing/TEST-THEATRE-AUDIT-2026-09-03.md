# Test theatre audit — idp `tests/`, 2026-09-03

Ordered by the founder 2026-09-03: "whats useful and whats just theatre" (verbatim capture
in `docs/founder/2026-09-03T1040Z-tests-are-theatre-need-test-architect.md`; ruling
`docs/rulings/R76-test-architect-owns-test-strategy.md`). Every number below comes from the
script at the bottom, run fresh at 2026-09-03T10:4xZ against idp main + the
`docs/provider-key-console-intake` branch (identical test tree).

## Headline

```
test files: 482   test functions: 2143
incident-reflex files (test_incident_*): 434 (1848 tests)
files pinning prose read from repo files: 374 (1939 prose asserts)
files executing behavior: 239
files grading parsed structure only: 51
```

While this suite stood green enough to merge daily, the estate carried 8 Flux
Kustomizations unable to reconcile, a standing FREEZE, and open P0s. The suite did not
predict or prevent any of those. That is the founder's point, measured.

## What is useful

- **Tests that execute the thing** (239 files touch `subprocess.run`): the merge-script
  tests that run `bin/idp-vault-put`'s block with real inputs, generator idempotency
  (two runs, byte-identical), gate fixtures in AGENTS.md that must refuse the bad case
  and pass the good one in one run. These fail when behavior breaks. Keep.
- **Contract tests on parsed data** (51 files parse YAML/JSON and grade shape): the two
  router configs kept in step, fallback chains resolving, env references having a seed
  pair. These fail when configuration breaks. Keep, minus their prose asserts.

## What is theatre

- **1,939 asserts that an English sentence exists in a repo file** (374 files). They fail
  when a comment is reworded and pass while the platform burns. Cost today, measured on
  one change: freeing one router lane required editing two of these tests; the edit then
  tripped `ruff format`, adding a third round trip. Zero defects can be caught by them.
- **One file per fire** (434 `test_incident_*` files, 90% of the suite). Many grade a real
  property, but the property is buried under a story: 42 tests in one break-glass file,
  83 prose asserts in it. The worst offenders:

```
test_incident_crew539_break_glass_admits_the_runner_for_one_job.py  tests=42  prose_asserts=83
test_incident_crew554_drills_run_on_the_estates_clock.py            tests=8   prose_asserts=35
test_incident_crew483_diagnose_telemetry.py                         tests=13  prose_asserts=23
test_incident_crew412_founder_page_answers_from_github_not_memory.py tests=6  prose_asserts=20
test_incident_crew516_node_surge.py                                 tests=18  prose_asserts=19
```

(full ranking: re-run the script; it prints all 374.)

## The plan (executes only on the founder's word)

1. **Stop the bleeding now (already in R76):** no new test may assert prose; no new
   file-per-fire; a mistake becomes the smallest test on the property that broke.
2. **Prune pass, one scripted sweep (one-pass rule):** delete every assert whose only
   subject is a sentence read from a repo file; collapse incident files that grade the
   same property into one property-named file carrying the incident numbers in its
   docstring. Expected shape after: well under half the current 2,143 tests, every
   survivor naming its property.
3. **Test-architect function stands up** as the owner of the standard and the reviewer of
   any PR adding a test.

Nothing is deleted before the word. Say **COMMIT** to run the prune as one PR wave, or
name what to change first.

## The script

```python
import pathlib, re
ROOT = pathlib.Path("~/dev/code/idp").expanduser()
files = sorted((ROOT / "tests").glob("test_*.py"))
rows = []
for f in files:
    t = f.read_text()
    n = len(re.findall(r"^def test_", t, re.M))
    prose = [ln for ln in t.splitlines() if ln.strip().startswith("assert")
             and re.search(r"[\"'][^\"']*\S+ \S+ \S+ \S+[^\"']*[\"']", ln)]
    pin = ".read_text()" in t and bool(prose)
    behav = bool(re.search(r"subprocess\.(run|Popen)|CompletedProcess", t))
    struct = bool(re.search(r"yaml\.safe_load|json\.loads?|tomllib", t)) and not pin
    rows.append((f.name, n, pin, len(prose), behav, struct))
# totals printed as in the Headline block above
```

Heuristic, and labeled as one: "three-plus-word string on an assert line in a file that
reads repo text" over-counts a few legitimate error-message checks and under-counts pins
built by concatenation. It is directionally solid; the prune pass reads each assert before
touching it.

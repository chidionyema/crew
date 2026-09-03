# R76 — A test architect owns test strategy; the fire-to-test reflex is over

Founder, 2026-09-03 (verbatim capture:
`docs/founder/2026-09-03T1040Z-tests-are-theatre-need-test-architect.md`): the tests are
stupid and slowing us down; we need a test architect to actually understand what is useful
and what is just theatre; writing a test for every fire is reacting instead of proper
planning and reasoning; not on; we are destroying the platform this way.

## The measured ground (2026-09-03, idp `tests/`, script in the audit doc)

- 482 test files, 2,143 test functions.
- 434 of the 482 files (90%) are incident-reflex files (`test_incident_*`), holding 1,848
  of the 2,143 tests (86%).
- 374 files assert 1,939 English sentences read out of repo files — they can only fail
  when wording changes, never when behavior does.
- The same day, the estate carried 8 Flux Kustomizations that cannot reconcile and a
  standing FREEZE. Heavy testing and a broken platform, at once. That coexistence is the
  ruling's proof, not an aside.

## Tenets

1. **Test strategy is designed, not accreted.** A test-architect function owns what is
   tested and why. A test exists because reasoning says a property must hold for the
   platform or a buyer — never because a fire happened and someone wanted to look guarded.
2. **The fire-to-test reflex is over.** LAW 45 ("your mistake ends as a guard") is
   amended in practice: a mistake ends as the *smallest guard that grades the property
   that broke* — and only when that property is worth a standing test under the
   architect's standard. One property, one test; the incident number goes in the
   docstring, not in a new file per fire.
3. **Tests grade behavior, never prose.** R53 (drills grade features, never look and
   feel) extends to every code test: outcomes, contracts, parsed data shape — never
   comment sentences, doc wording, literal strings, selectors. An assert on an English
   sentence read from a repo file is theatre and is refused.
4. **Volume is a cost, not a virtue.** Every test runs on every push and every branch;
   a suite nobody can reason about slows every fix. The suite is pruned to what protects
   the platform, and the prune is a deliverable, not an aspiration.
5. **Nothing is deleted without the founder's word.** The audit names the classes and the
   plan; the prune executes on his COMMIT.

## Protocol (LAW 44: a law without a protocol is a wish)

- New test entering idp/crew: it names the property it grades in one sentence in its
  docstring; if the property is "this file contains this sentence", it does not merge.
- The test-architect function reviews any PR that adds a test file, and owns the standing
  audit (`docs/testing/TEST-THEATRE-AUDIT-2026-09-03.md` is the first).
- Related: [[R75-founder-is-enterprise-client-zero]], R53, LAW 45, LAW 51.

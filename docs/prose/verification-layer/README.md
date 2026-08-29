# Verification layer: the scenarios, before they are tests

These seven feature files are the founder's crew#628 spec turned into scenarios, one file per
rollout phase 0–6. **They are specs, not tests, and that is why they are here and not in
`features/`.**

`spec-gate` refuses a `.feature` file in `features/` that no test names, on R29 / crew#297:
*"a scenario nobody runs is prose"*. It is right. The prober, the claim envelope, the canary and
the ledger do not exist yet, so there are no steps to bind. Binding them anyway — with skips, or
with steps that assert nothing — would produce a green run that means nothing, which is the exact
defect the verification layer exists to stop. Writing the layer's first act as a lie about its own
tests is not a start any of us would defend.

## The rule

**A file moves from `docs/prose/verification-layer/` into `features/` in the same pull request
that implements its steps, and not before.** That PR binds it with `scenarios("<path>")` in a
pytest-bdd test and the gate then does its job.

| phase | file | where it is built | state |
|---|---|---|---|
| 0 | `verification_vocabulary.feature` | `chidionyema/claude-guards` | **built** — `state_vocabulary.py`, 36 tests, merged in claude-guards#228. Its steps live in that repo, so the file moves there, not into crew's `features/`. |
| 1 | `verification_prober.feature` | idp, once flag F1 is answered | spec |
| 2 | `verification_claim_envelope.feature` | crew | spec |
| 3 | `verification_prober_fleet.feature` | idp | spec |
| 4 | `verification_canary.feature` | crew | spec |
| 5 | `verification_tool_call_audit.feature` | crew | spec |
| 6 | `verification_ledger.feature` | crew + Backstage | spec |

43 scenarios in total. Requirements: `docs/requirements/2026-08-29-verification-layer.md`.
Spec: `docs/specs/verification-layer.md`. Work item: crew#656.

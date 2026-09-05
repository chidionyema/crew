# The spec-gate action was deleted under twenty-six repositories

**When.** The action was removed from idp on 2026-09-04 in the CI purge, commit `b3affcc8`
(the same purge is recorded on `7421eb47`). The breakage was found on 2026-09-05 while landing
the empirical proof rule.

**What broke.** `.github/actions/spec-gate` lived in idp and was called by name from the
`security-scan` workflow of twenty-six repositories, this one included. Deleting it did not
disable those jobs; it made them fail in about four seconds, every time, on every pull request,
because the step resolves the action before it runs anything. Nothing was wrong with the code
under review in any of them.

**Why it went unnoticed.** The job failed fast and always, so it read as background noise rather
than a regression. A check that is red on every pull request stops carrying information, which is
the shape LAW 28 forbids: an instrument nobody reads is not an instrument.

**The fix.** The purge was correct — spec-gate graded the wording of a specification rather than
the estate, which is the class of gate the founder ordered deleted. What was missing was the
second half: the callers. The canonical template now lives at
`idp/platform/github/workflows/security-scan.yml` with the job removed and a comment saying why,
and `idp/bin/estate-security-rollout` copies it into every repository that still calls the dead
action. This repository took that template in crew#872.

**The class of mistake, so it is not repeated.** Deleting a shared action, workflow or composite
step is not complete until its callers are counted and changed in the same pass. The count is
available before the deletion, not after:

```
$ bin/estate-security-rollout --report
```

It prints every repository whose workflow still names the action. Twenty-six were open when this
was written.

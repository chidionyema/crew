## What

<!-- What this changes, in one or two sentences. -->

Closes #

<!-- One line, only when this change completes a checkpoint. The crew qa
     workflow reads it and runs `crew verify` for each box named. Delete it
     otherwise: no line means nothing is ticked, which is the safe way to be
     wrong. Engineering writes the line; the runner does the ticking. -->

Verifies: #<issue> CP<n> CP<n>

## Evidence — LAW 22

- [ ] A screenshot of the green run is committed in this branch under `docs/evidence/pr-<n>/`
- [ ] `pr-evidence check --pr $(gh pr view --json number -q .number)` exits 0

## Verify

```
$ scripts/verify.sh
PASS=   FAIL=0   CANNOT RUN=0
```

## Checklist

- [ ] An issue exists and is linked above
- [ ] Tests pass, with an incident test if this fixes a bug
- [ ] Evidence attached per LAW 22
- [ ] No direct commit to main — this is a pull request
- [ ] QA will verify independently; engineering did not tick its own box

## Decision log

**Chosen:**
**Rejected:**
**Why:** <!-- LAW 23 the friction default, or another rule by number -->

## Known limitations

<!-- Survivable rough edges. In the open, not hidden. -->

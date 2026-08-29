## What

<!-- What this changes, in one or two sentences. -->

Closes #

<!-- One line, only when this change completes a checkpoint. The crew qa
     workflow reads it and runs `crew verify` for each box named. Delete it
     otherwise: no line means nothing is ticked, which is the safe way to be
     wrong. Engineering writes the line; the runner does the ticking. -->

Verifies: #<issue> CP<n> CP<n>

<!-- Peer review is off (founder, 2026-08-29: frontier models do not need to review
     each other's work). CI and pr-evidence are the gate. Name your session so the
     board can find you. -->

Author-session: <name of the session opening this PR>

## Architecture laws — docs/ARCHITECTURE_LAWS.md, each line a command or `n/a:` with the reason
- LAW 1 zero-gravity:
- LAW 2 fractal:
- LAW 3 nervous system:
- LAW 4 calibration:

## Definition of done — crew#105, each line a command run against THIS pr

- [ ] `crew qa` is green on this PR's head commit (the `crew qa` check below)
- [ ] `pr-evidence check --pr $(gh pr view --json number -q .number)` exits 0
      (screenshot committed, Options considered section, provider coupling)
- [ ] For a feature (not a fix/chore): the demo and onboarding doc named in
      the LAW 32 pre-push hook are present in this diff
- [ ] Merged only after every line above is green — not before

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

## Options considered

<!-- LAW 43: name at least one off-the-shelf option researched before building
     anything new, and say why it was or was not used. `pr-evidence check`
     parses this exact heading -- two bullets of real substance and a
     "Chosen:" line, or the check fails. Renaming the heading breaks the gate. -->

- <!-- option A, researched, with what it does not cover -->
- <!-- option B, researched, with what it does not cover -->
- Chosen: <!-- which one, and why, in one line -->

## Testing rung

<!-- Which rung from ~/AGENTS.md How-to-test each new test in this diff is
     (type, property, differential, incident, eval, judge, production oracle).
     A declarative config file with nothing to run offline says so: "none:
     declarative config, graded by its first live PR." -->

## Known limitations

<!-- Survivable rough edges. In the open, not hidden. -->

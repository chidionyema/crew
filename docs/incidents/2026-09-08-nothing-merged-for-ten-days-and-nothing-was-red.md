# Nothing merged for ten days, and nothing was red

**2026-09-08.** Two separate controls, added a day apart, each quietly required a human hand
on every crew pull request. Neither turned a check red, so the only symptom was the founder
being asked to approve or to chase, over and over, for ten days.

Founder, 2026-09-08, in his own words: *"soor this blind sop where pr fails ad founder needs
to tell agents need to stop pw, agents should be responsiblefor their own own, all this
chasing is fricion"* — record:
`~/.claude/docs/founder/2026-09-08T0736Z-soor-this-blind-sop-where-pr-fails-ad-385bc493.md`.

## What actually held the door shut

**1. The merge bot required a check that no longer exists.**
`.github/workflows/merge-when-green.yml` refuses to land a pull request unless every name in
its `REQUIRED` set is PRESENT and SUCCESS. The set was `{"qa", "review-gate"}`. The founder
deleted `.github/workflows/review-gate.yml` on 2026-08-29 — commit `9fca66c`, *"Retire the
peer-review gate: founder 2026-08-29, review is friction"*. From that commit onward nothing
in the repository could produce a `review-gate` check, so `PRESENT` was never true and the
mechanism refused every pull request. It said so only inside its own run log, which nobody
reads, so the pull requests looked green and simply sat.

**2. A ruleset put the retired review back the next day.**
The repository ruleset `founder-only-releases` was created 2026-08-30T17:18:27+01:00 with
`required_approving_review_count: 1` on `~DEFAULT_BRANCH`. The same ruleset on `idp` carries
`0`. So the day after review was retired as friction, crew alone had it reimposed by a
control that lives in GitHub's settings rather than in this repository — which is why no
file in the tree recorded it and no gate could see it. Every crew pull request has read
`MERGEABLE / BLOCKED, reviewDecision REVIEW_REQUIRED` since.

Neither of these is a failing test. That is the whole point: **a mechanism that refuses
correct work silently is worse than one that fails loudly**, because the estate reads red as
work to do and reads nothing at all as nothing to do.

## The fix

- `REQUIRED` is `{"qa"}`. The `review-gate` name is gone, with the retirement commit named in
  the comment beside it.
- The crew ruleset's `required_approving_review_count` is `0`, matching `idp` and matching the
  founder's 2026-08-29 decision. `non_fast_forward` and `deletion` are untouched — force-push
  and branch deletion are still refused.

## The guard, and why it is shaped this way

`tests/test_incident_crew_merge_bot_required_a_deleted_gate.py` reads the `REQUIRED` set out
of `merge-when-green.yml` itself — never a copy — and resolves every name in it against the
jobs actually declared in `.github/workflows/`. A required check that nothing produces fails
the suite in the pull request that introduces it, instead of ten days later in a run log.

It also refuses an empty `REQUIRED`, which is the opposite failure and the more expensive
one: **crew#105**, where a required check was absent, "not failing" read as green, and PR #111
merged unreviewed on 2026-08-24. Absent-reads-green and absent-reads-red are the same defect
— a check name written in one file and produced in another — so one guard covers both.

The ruleset half cannot be guarded from inside the repository: it is GitHub account state,
not a file. What this incident buys instead is the knowledge that it exists and that `idp`
and `crew` had drifted apart on it. `bin/estate-repo-settings` is the place to fold that in
when a second divergence appears.

## How you would notice this class again

Ask the mechanism, not the pull request. `gh run view` on the newest `Merge when green` run
prints its verdict and reason for every open pull request. A wall of `REFUSED` with the same
reason on every line is this shape of defect, whatever the reason says.

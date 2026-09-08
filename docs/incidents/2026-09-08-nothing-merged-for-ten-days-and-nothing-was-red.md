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
deleted `review-gate.yml` under `.github/workflows/` on 2026-08-29 — commit `9fca66c`, *"Retire the
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

**3. Every one of them was still a draft.**
`merge-when-green.yml` refuses a draft — correctly, since a draft means the author is still
writing. But all five finished, green pull requests were drafts, because the sessions that
opened them never came back to mark them ready. Even with the first two causes fixed, nothing
would have merged.

Neither of the first two is a failing test, and the third is not a failure at all. That is the whole point: **a mechanism that refuses
correct work silently is worse than one that fails loudly**, because the estate reads red as
work to do and reads nothing at all as nothing to do.

## The fix

- `REQUIRED` is `{"qa"}`. The `review-gate` name is gone, with the retirement commit named in
  the comment beside it.
- A draft is now judged **last**, and only on a pull request that would otherwise land: a green,
  clean, unlabelled draft is marked ready and merges on the next tick. A draft that is red,
  conflicted or labelled `hold` / `do-not-merge` / `wip` is untouched. The founder's ask —
  *"agents should be responsiblefor their own own"* — is met by the mechanism doing the
  remembering, not by asking the sessions to remember better.
- The crew ruleset's `required_approving_review_count` is `0`, matching `idp` and matching the
  founder's 2026-08-29 decision. `non_fast_forward` and `deletion` are untouched — force-push
  and branch deletion are still refused.

## The guard, and why it is shaped this way

`tests/test_incident_crew_merge_bot_required_a_deleted_gate.py` reads the `REQUIRED` set out
of `merge-when-green.yml` itself — never a copy — and resolves every name in it against the
jobs actually declared in `.github/workflows/`. A required check that nothing produces fails
the suite in the pull request that introduces it, instead of ten days later in a run log.

Four more tests lift the bot's decision step out of the workflow's own heredoc and run it
over synthetic pull requests, so the draft rule is graded as behaviour and not as prose: a
green draft returns `READY`, a red draft and a held draft both return `SKIP.`, and a ready
green pull request still returns `MERGE`.

It also refuses an empty `REQUIRED`, which is the opposite failure and the more expensive
one: **crew#105**, where a required check was absent, "not failing" read as green, and PR #111
merged unreviewed on 2026-08-24. Absent-reads-green and absent-reads-red are the same defect
— a check name written in one file and produced in another — so one guard covers both.

`incidents/GUARDS.jsonl` is also added to the `merge=union` list in `.gitattributes`. It is
the most-appended ledger in the repository — every session that fixes a defect writes a row —
and it was the only append-only file missing from that list. It conflicted for real between
PR #904 and PR #909 while this was being written.

The ruleset half cannot be guarded from inside the repository: it is GitHub account state,
not a file. What this incident buys instead is the knowledge that it exists and that `idp`
and `crew` had drifted apart on it. `bin/estate-repo-settings` is the place to fold that in
when a second divergence appears.

## How you would notice this class again

Ask the mechanism, not the pull request. `gh run view` on the newest `Merge when green` run
prints its verdict and reason for every open pull request. A wall of `REFUSED` with the same
reason on every line is this shape of defect, whatever the reason says.

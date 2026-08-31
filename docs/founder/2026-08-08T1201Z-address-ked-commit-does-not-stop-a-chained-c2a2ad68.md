---
captured: 2026-08-08T12:01:54+00:00
session: 98126deb-f470-4017-a241-472a25f2e571
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2491
source: founder prompt, verbatim (founder-doc-capture.py)
---

address ked commit does not stop a chained git push, even under set -e. That's how an empty branch reached the remote.

PR #150 was already merged — origin/main is now e99cde1. My local origin/main ref was stale and briefly made me misread the tree; git fetch fixed it.

The copy leak — confirmed, not yet fixed

Four live sites, all under src/components/marketing/ (my earlier note had them under discovery/+pack/, which is why the first greps came back empty):

┌───────────────┬───────────────────────────────────────────────────────┬────────────────────────────────────────────────┐
│     leak      │                         site                          │                    renders                     │
├───────────────┼───────────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ raw gate slug │ LiveKillCard.tsx:58,153 · AmbientKillColumn.tsx:37,76 │ "killed by value durability", "payer solvency" │
├───────────────┼───────────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ raw float     │ CheckSequence.tsx:124                                 │ · conf 0.87 — §5 P0 rule 4                     │
├───────────────┼───────────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ retired term  │ EvidenceExcerptPlate.tsx:67                           │ dossier:<id> — retired per §5.2                │
└───────────────┴───────────────────────────────────────────────────────┴────────────────────────────────────────────────┘

The fix already exists in the codebase and isn't being called: lib/checks.ts:127 checkForGate(gate)?.verdict, whose docstring says the field is verbatim the label the receipt prints, specifically so a page can't invent a fourth lexicon. The components bypass it with .replace(/_/g, ' ').

And the reason it leaked: scripts/copy_audit.sh and .vale.ini aren't tracked in git (git ls-files --error-unmatch errors on both), copy_lint.py is untracked too, and none is wired into CI, a hook, or package.json. copy_lint.py:95-108 only matches multi-word snake_case, so single-word incumbency is invisible to it regardless. A linter that can't fail a build didn't fail this one.

I'd fix the four sites and make the linter tracked-and-enforcing as one change — but that's a fresh task and this session is post-compaction, so the honest move is to bank it. Handoff written with all four line refs and the Check field vocabulary.

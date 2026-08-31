---
captured: 2026-08-13T06:38:53+00:00
session: 832df081-0a80-4679-aac6-ea8b98a7b3ed
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2692
source: founder prompt, verbatim (founder-doc-capture.py)
---

DONE: everything is shipped and pushed. Two PRs are green and waiting on you.

- #177 — restores your steering switch-on. This one matters most: main has had active_profile: "" and market_rotation: "" since 2026-08-10, so the daemon has been generating unsteered and UK-only for three days while the directive read as delivered.
- #178 — all ten Part A audit findings, the automatability_floor deletion, and the B1 design.
- #176 — commented, recommend closing unmerged.

I did not merge #176 as planned, because merging it would have been wrong. Details below.

---
Why #176 was the wrong move. PR #174 squash-merged that same head branch at 17:54Z on 2026-08-10; your switch-on commit 8edff52 landed on the branch at 18:59Z, an hour after the squash was cut. Measured by tree rather than commit list (git merge --no-commit, then git diff origin/main $(git write-tree)), the whole of #176 over current main is 2 lines of config.yaml — the other 31 files are already in main. git cherry marked all 9 commits as new only because a squash rewrites patch-ids. Merging would have re-landed 1,937 redundant lines through a conflict resolution to deliver two lines. #177 delivers those two lines clean: 3 files, +53/−6.

Two traps it cost. A config-only commit skips the POPDD gate ("no source changes staged") — the steering commit passed having run zero tests, and the full suite run by hand found a real failure. Turning the profile on made two tests red that had pinned the unsteered vocabulary (len(vocab) >= 8; steered = 6); their fix existed only in unpushed local commit a28dc70. Ported into #177. Suite with steering on: 2934 passed, 5 skipped, 0 failed.

#13, your delegated call — deleted the floor. Decided on the weights, not the invariant: weights: was re-cut because automatability "IS trivially easy to clone = no moat", and I verified live that it now sits at 0.15 against defensibility: 0.25. A hard floor hands that demoted axis an effective veto. Kept _automatability_score — sampling.typicality_score names it as the rule it mirrors.

B1 unblocked without touching Stripe. POST /v1/prices/:id lists currency_options as updatable while unit_amount/currency are absent, so the 50 live packs need no re-minted Prices and the orphan-product trap is avoided. Two things I could not prove and recorded as open: read-back needs expand[]=currency_options, and the 50-object backfill must be idempotent before it goes near live.

Three things I left alone: audit findings #14 and #20 (money rail, not started), and commit a28dc70 on your main checkout — R5 audit rows that are in no branch or PR and need a home. addresss the threee things left alone and close the loop once and for all

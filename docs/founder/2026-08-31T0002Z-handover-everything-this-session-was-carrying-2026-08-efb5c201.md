---
captured: 2026-08-31T00:02:36+00:00
session: 4a84e2ea-66e0-4aca-9ccd-df82be7a0eeb
cwd: /Users/chidionyema/dev/code
chars: 2574
source: founder prompt, verbatim (founder-doc-capture.py)
---

HANDOVER — everything this session was carrying (2026-08-31)

1. Otto — pull request 1014

What it does: gives Otto its Langfuse keys (memory/traces), plus six graded health rows.
Where it stands: all changes are committed on branch crew717-rebase (commit 5a151c2b) in the folder ~/dev/code/.wt-otto-token. All 25 local tests pass.
This week's fix folded in: the hand-kept "restart when these secrets change" list is deleted; the pod now carries reloader.stakater.com/auto: "true" — the watcher finds every secret by itself, so nothing can go stale.
What's left:
1. The upload (push) is still running its checks in the background — one test showed a failure partway through, so the upload may be refused. Whoever takes over: re-run git push --force-with-lease origin crew717-rebase:feat/crew717-otto-powers from that folder and read which test failed (it may be the known flaky quorum test — it passed solo last time after failing in the batch).
2. Once pushed and CI is green: it needs your APPROVE to merge.

2. The estate-wide restart fix (not yet started in the repo — drafts are ready)

One new pull request, branched off the Otto branch:
- Delete the three remaining hand-kept lists: platform/healthchecks/healthchecks.yaml line 29, platform/backstage/base/catalogue.yaml line 28, platform/llm/litellm.yaml line 21 → replace each with auto: "true".
- Make the watcher watch every namespace (watchGlobally: true in platform/reloader/reloader.yaml) — an annotation in an unwatched namespace does nothing, which was the crew#684 failure.
- New cluster rule platform/edge/require-auto-reload.yaml: automatically adds the restart annotation to every program, so nobody can forget it. Opting out requires writing "false" in git with a reason.
- Delete the old per-program test assertions (they're the rot); one estate-wide guard test replaces them.
- Undo the "delete and reinstall broken apps automatically" setting from #1027 on all 9 rows — your pasted advice is right that it destroys evidence; reinstall stays a manual emergency step.
- Your incident report ("three incidents, one defect") goes into docs/reference/incidents/.
- Before closing: run the new rule against the OLD broken files and show it catching them — proof the control works.

Full draft. Loose ends

- Blueprint 2 (catch wrong types before merge with kubeconform): designed, not built.
- Your rule "every infra change must ship a control or say why not" — not built yet.
- Langfuse's second sign-in hop is still red; the tailscale wedge is with lane 80471694. use parallen aganet and get this alldone

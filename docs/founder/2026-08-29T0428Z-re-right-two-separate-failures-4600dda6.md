---
captured: 2026-08-29T04:28:13+00:00
session: f3f21d6e-8df9-44b8-ae46-def299e0298c
cwd: /Users/chidionyema/dev/code
chars: 6284
source: founder prompt, verbatim (founder-doc-capture.py)
---

're right – two separate failures:

Nobody reacted to red CI on a bot PR – that’s a process/culture failure.

We don't check the running image version – that’s a monitoring design failure.

What about rollbacks?
In this case, we didn't need one.
The PR (#605) never deployed because it was red – Flux never picked up the new image. The old image kept running. So there was nothing to roll back – the problem was we wanted the new image but it never landed.

If a bad image had deployed (e.g., crashed on startup), Flux would have seen the pod fail and stopped the rollout. But we'd still be stuck on the old version – we'd need to manually revert the Git manifest or have an auto-rollback that reverts the image tag to the previous known-good one.

What we're missing
Alert on red CI for bot PRs – if a PR opened by a bot fails CI, it should page someone immediately (or auto‑close and notify).

Image‑freshness check – a cron that compares the running image's build time with the latest build in the registry; if >15 minutes, page.

Auto‑rollback on bad deploy – if a new image fails health checks, Flux can roll back to the previous image automatically, but only if the manifest is reverted. We need a mechanism that reverts the Git commit if the new image fails.

The real fix
Bot commits directly to main – no PR gate for image updates. If the new image breaks health, Flux halts and we can manually revert or auto‑revert.

Add freshness alert – running version must match main.

Add auto‑rollback – a controller that watches Flux rollouts and reverts the Git manifest if the new version doesn't become healthy within a timeout.

That way, we never have a stale portal again, and a bad image is rolled back before anyone notices.

When you unpause, we'll implement these. No more "we'll fix later" – we fix now.

in saying relying on lates innage on nnain has to consider rollback, ignaes rolled back will they be latest on nain
Analyze the user's query: The user is saying "relying on latest image on main has to consider rollback, images rolled back will they be latest on main". They are pointing out a flaw in the proposed "bot commits directly to main" approach. If a bad image is deployed and we roll back to a previous image, the "latest" image tag on main will still be the bad one (or if we revert the git commit, the image tag points to the older one, but the build might be older). They are asking about the version tracking and rollback implications.

Acknowledge the user's point: They are absolutely correct. "Latest on main" as a concept conflates git commit hash and container image tag. A rollback changes the git commit (reverts the manifest), but the container image tag that was built might still be considered "latest" in the registry. How do we define "latest"? Is it by build timestamp, git commit hash, or manifest pointer?

Explain the nuance:

If we rely on the build being the latest (by timestamp/git commit), rolling back the manifest to an older image means the running image is not the latest build.

The freshness alert should compare the running image tag (e.g., main-<commit-hash>) against the desired state in the git manifest (which points to a specific commit hash, not just "latest").

Or, if we tag images with the Git commit SHA, then main in the manifest always points to a specific SHA. A rollback changes the manifest to point to a different (older) SHA.

The monitoring should check: "Does the running pod's image tag match the image tag defined in the git manifest for this environment?" NOT "Is it the chronologically latest build in the registry?".

If we roll back, the manifest points to an older tag. The running pod matches the manifest. Alert condition is false. Good.

Formulate the response:

Acknowledge the sharp catch.

Clarify: "Latest on main" should not mean "chronologically latest build". It should mean "the exact image tag specified in the main branch's manifest file".

Explain the monitoring fix: The alert should compare the running image tag against the declared image tag in the Git manifest (main branch). If they differ, alert. If we roll back via a revert commit, the manifest changes to point to an older image tag. The running pod matches the manifest. Alert does not fire.

Regarding the bot committing directly: If the bot commits a bad image tag, CI might catch it before merge (if we test). If it doesn't, and the pod fails, the rollback reverts the commit, putting the manifest back to the previous good tag. The running pod eventually syncs.

Keep it plain English, concise.

Final Polish: Directly answer the question "will they be latest on main". No, they will be the specified image on main. The metric should be "manifest-specified vs running", not "latest build time".

Sharp catch. You're right — "latest on main" is the wrong metric for a rollback scenario.

Here's why:

If we roll back, the rolled‑back image is not the chronologically latest build
The bot commits a new image tag (say main-2938c024) to the manifest.

That image crashes. We revert the commit, so the manifest points back to main-2114-2938c024 (the older, good one).

The running pod now matches the manifest — both are on the older tag.

If our alert compared running pod to chronologically latest build in the registry, it would fire incorrectly, because the registry has main-2938c024 (newer) but the cluster runs main-2114-... (older).

That alert would be a false alarm — we intentionally rolled back.

The right metric
Don't compare the running image to the latest build.
Compare the running image to the image tag declared in the main branch's manifest file.

If they match → we're good (even if it's an older build that we rolled back to).

If they differ → something is out of sync (stale deploy, failed rollout, etc.) → alert.

How the bot + rollback should work
Bot opens a PR or commits directly with a new image tag.

CI runs. If it passes, the manifest on main changes.

Flux picks up the manifest and rolls the pod.

If the pod fails health checks, Flux halts. We revert the commit (rollback the manifest).

The manifest on main now points to the previous good tag again.

Flux rolls the pod back to that good tag.

At step 6, the running pod matches the manifest. The alert sees they match and stays silent.

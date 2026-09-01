# INC1 — Kustomization `flux-system/chaos` fails to reconcile: chaos-mesh admission webhook returns EOF on dry-run

**Founder record:** `~/.claude/docs/founder/2026-09-01T1454Z-you-re-right-i-was-queuing-another-audit-2924313b.md` ("Change nothing. Write up these four open items as incident records").
**Class note:** [admission webhook EOF class](2026-09-01-NOTE-admission-webhook-eof-class.md). **Nothing was changed.**

| Field | Value |
|---|---|
| First observed | 2026-08-29T23:57:23Z — the alert path (`flux-events.yml`) opened idp#888 "P0: Flux cannot reconcile Kustomization/chaos.flux-system" on the first failure (`Schedule/observability/langfuse-alert-drill dry-run failed … webhook "mschedule.kb.io" … EOF`). |
| Latest failure | 2026-09-01T14:16:51Z, `Schedule/backstage/backstage-pod-kill dry-run failed (InternalError): failed calling webhook "vschedule.kb.io": Post "https://chaos-mesh-controller-manager.chaos-mesh.svc:443/validate-chaos-mesh-org-v1alpha1-schedule?timeout=5s": EOF` |
| Current state (read 14:56:31Z) | **Recovered.** `Ready=True ReconciliationSucceeded 2026-09-01T14:55:44Z`, `Healthy=True`. Red for 39 minutes (14:16:51Z to 14:55:44Z). |
| Recurrence | 12 failures in 63 hours, each a different chaos-mesh webhook: `mschedule.kb.io` ×5, `vschedule.kb.io` ×2, `mworkflow.kb.io` ×1, `vauth.kb.io` ×3 (idp#888 comments: 08-30 08:20, 13:56, 19:28, 19:57, 22:32; 08-31 01:01, 05:50; 09-01 07:52, 08:02, 14:17). Every one self-recovered on the next 10-minute reconcile. |
| Blast radius | The `chaos` Kustomization holds 4 objects: Schedules `backstage-pod-kill` (cron `0 3 * * 1`, last run 2026-08-31T03:00Z) and `langfuse-alert-drill`, plus their first-run Workflows. A failed dry-run applies nothing new; the objects already in the cluster keep running their last applied spec. |
| Degraded or unavailable right now | Nothing. The Kustomization is Ready. During each red window a change to a chaos Schedule in git would not have reached the cluster; no such change was pending (revision `main@bee102db` applied before and after). |
| Alert fired? | **Yes and stuck.** `flux-events.yml` (repository_dispatch from Flux notification-controller) opened idp#888 at 23:57Z on 08-29 and commented on all 10 repeats. It never closed the issue on recovery: the recovery path (`gh issue close` on a recovered event) did not fire for `chaos` while it did for `edge` (idp#1111 opened 13:20Z, closed 13:36Z same day). The Telegram Flux Alert `broken-workload` is `suspend: true` (`platform/alerts/alert.yaml`), by design (founder DM is not an alert sink). |
| Webhook facts | `chaos-controller-manager`: 1 replica, 0 restarts, node `10.0.159.197`; 43 webhooks all `failurePolicy: Fail`, `timeoutSeconds: 5`; cert secret `chaos-mesh-webhook-certs` created 2026-08-25T22:50:39Z, never rotated. Its log at 14:16:50Z shows the mutating defaults and the Workflow validation served, and no `validate update backstage-pod-kill` line: the validating call's connection closed before it was served. |

## Evidence read
- `bin/idp-kube get kustomization chaos -n flux-system -o jsonpath=…conditions` at 14:56:31Z.
- `bin/idp-kube get events -A -o json` (store starts 13:18:00Z), filtered to `failed calling webhook`.
- `gh issue view 888 -R chidionyema/idp --json comments`; `gh run view 33518518956` (the 14:16:53Z flux-events run that commented).
- `bin/idp-kube get pods,deploy -n chaos-mesh`; `get validatingwebhookconfigurations,mutatingwebhookconfigurations -o json`; `get secret -n chaos-mesh`; `logs deploy/chaos-controller-manager --since=2h`.
- `platform/chaos/kustomization.yaml`, `clusters/oke/platform.yaml` (chaos row, path `./platform/chaos`), `platform/alerts/alert.yaml`, `.github/workflows/flux-events.yml`.

## Decision (mine, as asked)
A live, recurring incident of the webhook EOF class, not a chaos-specific fault: twelve self-healing failures in three days, every one on a single-replica webhook server behind a 5-second `Fail` policy. Owner: idp lane. Two defects to carry: the class (note), and the alert that opens but never closes (idp#888 has been "open P0" for 63 hours through eleven recoveries, which is noise, not an instrument). No remediation in this record.

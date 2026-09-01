# NOTE — The admission webhook EOF class: what INC1 and INC2 share, and what would confirm or rule out a common cause

**Founder record:** `~/.claude/docs/founder/2026-09-01T1454Z-you-re-right-i-was-queuing-another-audit-2924313b.md` ("Two in one hour on dry-run calls is a class, not two incidents"). **No remediation here.**

## What the two share
| Property | chaos-mesh ([INC1](2026-09-01-INC1-chaos-kustomization-webhook-eof.md)) | kyverno ([INC2](2026-09-01-INC2-edge-kyverno-webhook-eof.md)) |
|---|---|---|
| Error text | `Post "https://<svc>:443/<path>?timeout=5s": EOF` | `Post "https://<svc>:443/<path>?timeout=10s": EOF` |
| Caller | Flux kustomize-controller server-side dry-run (`InternalError` from the API server, which is the actual client of the webhook) | same |
| Webhook server replicas | 1 | 1 |
| Node | `10.0.159.197` | `10.0.159.197` |
| Restarts | 0 | 0 (running since 08-28) |
| failurePolicy / timeout | Fail / 5 s (43 webhooks) | Fail / 10 s (resource webhooks) |
| Server log at the moment | Neighbouring calls served; the failing call not logged | No line in the window |
| Recovery | Next reconcile, unaided | Next reconcile, unaided |
| Frequency | 12 in 63 h | 1 in 63 h |

EOF is not a timeout: the TCP connection from the API server to the webhook pod was closed before an HTTP response. Both servers are single pods on the same worker node, and neither restarted, so the close came from between the API server and the pod (node network, conntrack, the CNI, or the OKE control-plane egress), or from the server dropping an idle keep-alive connection the API server then reused.

## What would confirm a common cause
1. **Every EOF event lands on the same node.** Read the webhook pods' node over time (the pods have not moved since 08-28 / 08-25) against the timestamps in idp#888 and idp#1111; if the third webhook server in the estate (`cert-manager-webhook`, or the `temporal` one when it ran) never shows EOF and sits on `10.0.148.221`, the node is the common factor. Confirmable today from events and pod placement, no change needed.
2. **The failures cluster at the same minute of a reconcile wave.** Twelve chaos-mesh timestamps: 08:20, 13:56, 19:28, 19:57, 22:32, 01:01, 05:50, 07:52, 08:02, 14:17 (and 13:20 for kyverno). Today's only new artifact, `bee102db`, landed at 13:35:26Z; the kyverno EOF came 15 minutes before it and the chaos EOF 41 minutes after it, so neither coincides with a new revision. First pass: the pattern looks time-random, which favours a network-level close over apply load. A full pass needs the `NewArtifact` history for all twelve, which the one-hour event store no longer holds; the `flux-events` workflow runs carry it.
3. **A node-level signal at those minutes.** `kubectl get events` on the node kind is empty in the store; SigNoz holds the k8s-infra collector's node metrics and kube-proxy/CNI logs for the window. A conntrack table reset, a CNI restart, or a kube-proxy sync at 13:20Z and 14:16Z would confirm.
4. **The API server's own webhook client metrics.** OKE does not expose kube-apiserver logs; `apiserver_admission_webhook_request_total{rejected="true"}` and `…_fail_open_count` are scrapeable through the `kubernetes` service and would show whether other webhooks (cert-manager, kyverno's `Ignore`-policy monitor webhook) saw the same closes without anyone noticing.

## What would rule it out
- Chaos-mesh EOFs continue while kyverno's never recurs → not a shared path; chaos-mesh's own server (controller-runtime v0.21.0 webhook server with a 5-second budget) is the suspect, and the 14:16:50Z log showing one call served and its sibling dropped in the same 40 ms points at connection handling in that process.
- EOFs appear on a webhook pod on the other node → not node-bound.

## Why it matters beyond Flux
Both webhook sets are `failurePolicy: Fail`. A kyverno EOF refuses every create and update in the cluster for that instant, not only Flux's dry-run; a chaos-mesh EOF refuses chaos objects only. A single-replica `Fail` webhook is a cluster-wide single point of refusal. That is the class: **one pod, `Fail`, short timeout, no second replica**. Whether to add a replica, raise the timeout, or move to `Ignore` for dry-run is the remediation question, deliberately not answered here.

## Also seen, not this class
kyverno logs `Failed to parse value type doesn't match key type` on `require-priority-class` / rule `radio-room-set-is-guaranteed` for `Deployment hermes-agent-gateway` every few seconds (208 lines in an hour). A policy that errors on every evaluation is a silent-green candidate (memory: silent green is the defect class). Recorded in INC2; owner to be named on the board.

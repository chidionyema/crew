# INC3 — Kustomization `flux-system/temporal` shows `DependencyNotReady` since 2026-08-30T05:54:22Z: the row is suspended and its status is frozen, not failing

**Founder record:** `~/.claude/docs/founder/2026-09-01T1454Z-you-re-right-i-was-queuing-another-audit-2924313b.md`. **Nothing was changed.**

| Field | Value |
|---|---|
| First observed | Status `Ready=False DependencyNotReady "dependency 'flux-system/edge' is not ready"`, `lastTransitionTime 2026-08-30T05:54:22Z`. |
| Why it reads that way | `spec.suspend: true` (`clusters/oke/platform.yaml`, commit `27980b6a`, 2026-08-30, "platform: suspend the temporal Flux row (kini receipt watcher, founder 2026-08-30, crew#284)", PR idp#923). A suspended Kustomization is never reconciled again, so Flux keeps whatever status it had at the moment of suspension. At 05:54Z on 08-30 `edge` was not ready (the alert path filed idp#956 for `edge` at 06:07Z and closed it at 06:17Z that morning); the temporal row was suspended while that snapshot stood and has carried it for two days. `edge` has been Ready for most of the time since. |
| Current state | Suspended, deliberately, on the founder's word (crew#284). `observedGeneration 2`, `generation 4`: two spec edits since suspension have never been evaluated, as expected. The namespace and its volumes remain; `platform.yaml` line 440: "`suspend: false` brings it back". |
| Blast radius | What ran here was a Temporal server, its own Postgres and a worker, serving two 15-minute CronJobs writing a receipt, red since 2026-08-27 (kini-finish green=0 red=7). None of it is meant to run now. Windmill is the named replacement in infra; Temporal stays in the stack for the enterprise lane (founder 2026-08-30, crew#695). |
| Degraded or unavailable right now | Nothing that is supposed to be up. The kini receipt watcher is off by decision. |
| Alert fired? | No, and none should: a suspended row emits no events. The flux-events alert path does not distinguish "suspended" from "not ready", and neither did my 14:19Z report until the note was added, which is the defect worth carrying: a state report must render `suspended` as its own state, never as red. |

## Evidence read
`bin/idp-kube get kustomizations -A -o json` (`spec.suspend`, `status.observedGeneration`, `metadata.generation`); `git log -S"suspend: true" -- clusters/oke/platform.yaml` in idp (`27980b6a`); `clusters/oke/platform.yaml` lines 155–162 and 438–440; idp#956 for the edge state at the time of suspension.

## Decision (mine, as asked)
Not an incident. Parked on purpose, with the commit and the founder's word on record. Two actions belong elsewhere: the generated Flux report must show `suspended` as a state of its own (goes into the Reports build), and the register should carry a "parked since 2026-08-30, flips on: enterprise-lane decision" line for this row.

# INC4 — Kustomizations `commerce`, `commerce-data`, `event-bus`: suspended and never reconciled

**Founder record:** `~/.claude/docs/founder/2026-09-01T1454Z-you-re-right-i-was-queuing-another-audit-2924313b.md`. **Nothing was changed.**

| Field | Value |
|---|---|
| First observed | All three created 2026-08-29T19:32:37Z with `spec.suspend: true`; `status: {observedGeneration: -1}`, no conditions, no `lastAppliedRevision`: Flux has never evaluated them. |
| Why | `clusters/oke/commerce.yaml`, commit `c69236ee` 2026-08-29 "feat: the money leaves the application, dark (crew#623 CP1)". The file's own header: "Two rows, both SUSPENDED. Flux reads them and applies nothing. `suspend: true` is the estate's dark switch (platform/features/features.yaml: '`suspend:` is the switch, nothing is ever deleted'). The founder's word on the cutover flips it to false in its own PR, together with the prospector PR that removes the Stripe SDK from Store.Api." |
| Dependencies | `commerce` → `commerce-data`, `event-bus`; `commerce-data` → `external-secrets`, `secret-store`, `priority-classes`; `event-bus` → `priority-classes`. All dependencies are Ready today, so an unsuspend would evaluate immediately. |
| Current state | Dark by design, awaiting the founder's cutover word (crew#623). Since when: 2026-08-29T19:32Z. Until when: the cutover PR. |
| Blast radius | None. Nothing from these paths exists in the cluster; the storefront takes money through the application today, as before. |
| Degraded or unavailable right now | Nothing. |
| Alert fired? | No, and none should. The alert path is event-driven and a never-reconciled row emits no events. The 14:19Z report listed them under "Not Ready" with dashes, which is the same reporting defect as INC3. |

## Evidence read
`bin/idp-kube get kustomizations -A -o json` (spec and status of the three rows); `git log -S"suspend: true" -- clusters/oke/commerce.yaml` in idp; `clusters/oke/commerce.yaml` header lines 3–8 and lines 16–20; `platform/features/features.yaml`.

## Decision (mine, as asked)
Not an incident. Parked on purpose, with the commit, the checkpoint (crew#623 CP1) and the flip condition on record. The register row is "dark since 2026-08-29, flips on the founder's cutover word". No action.

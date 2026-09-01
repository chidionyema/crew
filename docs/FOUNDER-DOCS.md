# Founder documents — the permanent index

Every document produced on a founder order lands here, newest first, or it does not exist.
Stable path: `docs/FOUNDER-DOCS.md` — linked from the README first line and rendered on the
founder entity's Docs tab in Backstage (mkdocs has no nav block, so every page ships automatically).

| date | document | one line |
|---|---|---|
| 2026-09-01 | [INC1: chaos Kustomization, chaos-mesh webhook EOF](audit/incidents/2026-09-01-INC1-chaos-kustomization-webhook-eof.md) | 12 self-healing failures in 63 h; alert idp#888 open since 08-29 and never closes; recovered 14:55Z |
| 2026-09-01 | [INC2: edge Kustomization, kyverno webhook EOF](audit/incidents/2026-09-01-INC2-edge-kyverno-webhook-eof.md) | once, 13:20Z to 13:36Z; alert idp#1111 opened and closed correctly |
| 2026-09-01 | [INC3: temporal row suspended, status frozen](audit/incidents/2026-09-01-INC3-temporal-suspended-frozen-status.md) | suspended on the founder's word 2026-08-30 (idp#923, crew#284); not an incident; reports must show 'suspended' |
| 2026-09-01 | [INC4: commerce, commerce-data, event-bus dark](audit/incidents/2026-09-01-INC4-commerce-rows-suspended-dark.md) | suspended by design since 2026-08-29 (crew#623 CP1); flips on the cutover word; not an incident |
| 2026-09-01 | [NOTE: admission webhook EOF class](audit/incidents/2026-09-01-NOTE-admission-webhook-eof-class.md) | one pod, failurePolicy Fail, short timeout, same node; four checks that confirm or rule out a common cause |
| 2026-09-01 | [Flux state of the cluster, read-only, 14:19Z](audit/2026-09-01-flux-state.md) | 73 Flux objects: 68 Ready, 1 live failure (chaos: chaos-mesh webhook EOF), 4 suspended; 370 events in the hour, 2 warnings |
| 2026-09-01 | [First-time success of agent builds and releases across infra](audit/2026-09-01-first-time-success.md) | idp pull requests green on first push 29%, prospector 61%; oke-check on main 0 of 6; script and output verbatim |
| 2026-09-01 | [Research department design: boundary, contract, requesters, gut-or-keep, guard review](research-engine/DESIGN-2026-09-01-research-department-contract.md) | for his review; §7 holds the amendments from the review he pasted; index: [FOUNDATIONS.md](FOUNDATIONS.md) |
| 2026-09-01 | [Research Engine v2 reset — walking skeleton first](research-engine/RESET-2026-09-01-research-engine-v2.md) | founder verbatim; supersedes crew#659 CP1–CP5; four rulings requested in §6 |
| 2026-09-01 | [Research department charter (reworded, linked to the reset)](research-engine/CHARTER.md) | "for any subject we register — a product, a service, a market, a company, or the estate itself" |
| 2026-08-31 | [crew vs crewAI capability map](plans/2026-08-31-crew-vs-crewai-capability-map.md) | every capability, sources both sides, stays/goes column is the founder's |
| 2026-08-31 | [crew surface map](plans/2026-08-31-crew-surface-map.md) | everything the crew and the sessions use today, measured, with work plan W0–W20 |
| 2026-08-31 | [audit 1: custom builds](audit/2026-08-31-custom-builds.md) | every hand-rolled thing vs the mature tool that does the job |
| 2026-08-31 | [audit 2: tools at full potential](audit/2026-08-31-tools-full-potential.md) | what each adopted tool ships that we leave switched off |
| 2026-08-31 | [crewAI redesign plan (superseded by the two maps above)](plans/2026-08-31-crew-redesign-on-crewai.md) | first draft, kept for the record |

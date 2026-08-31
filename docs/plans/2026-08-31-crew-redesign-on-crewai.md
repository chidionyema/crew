# The crew, redesigned on crewAI — for founder verification

Date: 2026-08-31. Status: PLAN — nothing here is built; every step below starts only on the founder's word, and the how of each step is what his word covers.

Founder's framing, verbatim: "it solves all our issues one shot", "its not lift and shift, it a total redesign of the crew", "your plan needs to show the gap being addressed".

## The gaps, measured

| # | Gap | The receipt that proves it |
|---|---|---|
| G1 | No shared durable memory: the founder repeats rulings; sessions each keep private notes; compaction loses decisions | R2 (say-once-all-ack) violated again 2026-08-31 ("i dont like repeating"); incident class summary-over-source, 2 on the ledger |
| G2 | Orchestration is hand-rolled: a 543-line plan/claim/evidence/verify loop (`crew/crew/cli.py`), goal-graph files, idle-guard choreography | Audit 1 row 6; incident class gate-landed-after-branch, 16 on the ledger — sessions race each other to main |
| G3 | No manager: sessions self-organise and the founder is the integration point; asks go to the void | 2026-08-31: two ordered audits sat undelivered in a ticket while the asker waited |
| G4 | No knowledge layer: laws and runbooks live as prompt files re-read ad hoc; nothing retrieves them at need | AGENTS.md is pasted into every context; audit docs land in tickets nobody re-reads |
| G5 | Nothing grades agent runs from outside: self-scoring is banned (founder, NOT NEGOTIABLE) but no external grader replaced it | Langfuse evaluations sit unused (Audit 2, Langfuse row); no replay of any crew run exists |
| G6 | No security department: security logs sat unread through a 3-day outage | tailscale operator crashloop 2026-08-28→31; the fatal line was in the pod log the whole time (idp#586) |
| G7 | Scattered config: the zone literal appears in 39 idp files + 8 crew files outside the one config | `git grep -l mumchimp` 2026-08-31, printed in-session; founder: "we must be able to migrate anywhere seamlessly. ONE SHOT" |
| G8 | Adopted tools below potential; two ruled tools not deployed at all | Audit 2: MLflow — no config anywhere; Windmill — ruled (crew#695) yet Temporal+Dagster still run; 5 config-only wins listed |

## The design — every element names its gap

| Element | Closes | How |
|---|---|---|
| D1 Otto is the manager | G3, G2 | crewAI hierarchical process; Otto delegates to department crews (engineering, security, research, operations, audit). The GitHub board stays the human-visible ledger; task state lives in crewAI, not in claim files. Otto's superpowers plan (crew#717) is unchanged — this is his hands. |
| D2 One memory | G1 | crewAI long-term + entity memory on the cluster Postgres that already runs (no new infra). A founder ruling is ingested once and every agent recalls it. Say-once-all-ack becomes mechanical, not disciplinary. |
| D3 One knowledge base | G4 | crewAI Knowledge over: the laws, standards page, runbooks, incident corpus, audit docs. Embedded through the router's embed lane; retrieved at need; compaction can no longer lose them. |
| D4 Security crew first | G6 | A scheduled crew whose tools read SigNoz, the Tailscale audit API and OCI Audit; findings filed as issues, loud ones push-notified. The department that would have read the log on day one. |
| D5 External grading | G5 | Every crew run traces to Langfuse via the router (already true for LLM calls). Langfuse evaluations + `crewai replay`/`crewai test` grade runs from outside the lane — satisfying the self-scoring ban with machinery, not promises. |
| D6 Deletions | G2 | `crew/crew/cli.py` loop, the research worker/grader hand-off and the idle-guard choreography fold into crewAI. Every deletion is a listed line on crew#729 and waits for CONFIRM. |
| D7 Single config | G7 | One estate config (the zone and every endpoint derived from it) read by agents, scripts and manifests. One scripted pass replaces the 47 stray literals; a gate refuses any new literal. Migration anywhere = change one value. |
| D8 Tools to potential | G8 | The five config-only wins from Audit 2 ride the redesign where it touches them (LiteLLM cache, strict status checks, Flux alert to a group channel, Backstage search+notifications, SigNoz alert rules). MLflow-vs-science and Windmill-vs-Temporal are founder decisions, surfaced, not assumed. |

## The how (what approval covers)

- LLM access only through the router at `llm.<ESTATE_ZONE>`; traces to Langfuse; no vendor key anywhere (LAW 34, LAW 50).
- Runs on GitHub runners and cluster jobs, never the Mac (R31).
- All code, config, docs in git (LAW 24); memory and knowledge stores on cluster Postgres, never local files.
- Secrets via ESO/OCI Vault; the router key the science lane already holds; no new vendors, no new spend.

## Build order — each step starts on the founder's word, with its acceptance test

| Step | Builds | Accept when |
|---|---|---|
| 1 | Foundation: config module (D7 core), router+Langfuse wiring, memory+knowledge backends | one crew of two agents completes a real task; its trace, memory write and knowledge retrieval are each queryable in the backend |
| 2 | Security crew (D4) on schedule | it independently reports a seeded finding from SigNoz + the Tailscale audit log within one cycle |
| 3 | Research crew port + Otto as manager over both (D1, D5) | the research lane's next graded report is produced by the crewAI crew, replayable, with an external eval score |
| 4 | Deletions (D6) + the estate-wide literal sweep (D7) | CONFIRM-listed files deleted; `git grep` for the zone literal outside the one config returns zero |

## What this plan does NOT do
No product code is touched (prospector, hermes-v2 stay as they are). No platform layer is duplicated. Nothing is deleted before its replacement is proved and CONFIRMed.

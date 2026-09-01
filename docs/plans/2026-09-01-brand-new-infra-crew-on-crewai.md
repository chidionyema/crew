# A brand-new infra crew on crewAI — decision record for the founder's word

Date: 2026-09-01. Status: PLAN. Nothing is built until the founder writes CONFIRM on crew#729.

Founder, 2026-09-01, verbatim: "now there is a tickte on the board for crew.ai your goal is toset up
new crew , no claude code this tine,new crew to take over infra work" — "no nigration. just brnde new
crew" — "NNew crew starting tonorrw who wil obey ny laws".

Read as: a new crew, built from nothing on crewAI, runs without Claude Code, takes over the infra
work (the `idp` platform: clusters, edge, identity, drills, incidents), and obeys the laws
mechanically. Nothing from the old crew is ported. The old crew's access is being revoked by the
founder tonight; this crew gets its own identity, so nothing it does ever rides his.

This record supersedes `docs/plans/2026-08-31-crew-redesign-on-crewai.md`, which was a migration.

## What it is

| Element | Decision | Why |
|---|---|---|
| Name and home | `infra-crew`, a brand-new repository `chidionyema/infra-crew` | nothing copied, nothing inherited |
| Runtime | crewAI 1.9.3 (installed and verified: `crewai version` prints `1.9.3`), Python 3.11, in a container, running as a cluster workload | crew#763 decision record: crew agents run in pods like Otto; never on the Mac |
| Brain | any model, only through the estate router (`llm.<zone>`, OpenAI-compatible; crewAI `LLM(base_url=…)`) | LAW 34 provider-agnostic; no vendor key, no Claude Code, nothing Anthropic-specific |
| Identity | its own GitHub App `infra-crew`, minimum rights: read and write its own branches, open pull requests, write issue comments, read Actions logs. No admin, no merge, no workflow dispatch, no secrets | it can never use the founder's login; a buyer's engineer can read the permission list in one screen |
| Sign-in | the read-only estate account from crew#767 for the portal and Langfuse | reads everything, configures nothing |
| Cluster | none, ever. It reads the estate from the `flux-events` runs and the estate-state snapshot | founder 2026-09-01: no agent touches the cluster again |
| Kill switch | three independent one-action switches, all the founder's: suspend the App installation (every token dies at once); the crew#767 `agents_enabled` toggle; the pod's replica count in git, merged by him | crew#767, the switch he already asked for |

## How it obeys the laws — by construction, not by promise

- **The laws are its knowledge.** crewAI Knowledge over `AGENTS.md`, `AGENTS-FULL.md`, `crew/docs/STANDARDS.md`, the runbooks and the incident ledger, embedded through the router's embed lane and retrieved on every task. Not a pasted prompt.
- **No hand, no breach.** The crew has no merge tool, no deploy tool, no cluster tool. It cannot break the release ruling because the tool does not exist (remove the bad input, never guard it). A test in its repo proves the tool list, forever.
- **Every task ends at green.** Plan comment with an `Optimised:` line (LAW 51), branch, pull request with the ten Definition-of-done rows, verification evidence, then stop. The founder merges and deploys (founder-only releases).
- **Verified from outside.** A separate verifier agent on its own model lane grades every builder output as a crewAI task guardrail; verdicts also land as Langfuse evaluations. Self-scoring stays banned.
- **One memory.** crewAI long-term memory on the cluster Postgres that already runs: a founder ruling ingested once, recalled every run (say-once-all-ack). No `~/.claude`, no local files.
- **Everything emits.** OTEL traces to the estate collector and Langfuse; coverage proved by querying the backend, never by scanning files (LAW 50). The crew refuses to boot dark.
- **Plain English on every surface.** Board comments, feed handoffs and `FOUNDER ACTION:` lines are emitted by tools, so the format is mechanical.

## Roles — five, infra only

manager (a crewAI manager agent in the hierarchical process; Otto takes the chair later per crew#717) · planner · builder · verifier · watcher (reads `flux-events`, drills and SigNoz alerts, files incident issues, never touches the cluster).

## Build order — the founder's word once, at the top; each step accepted by a command

| Step | Builds | Accept when |
|---|---|---|
| 1 Foundation (~4h machine) | `crewai create crew infra-crew`; router LLM; Langfuse + OTEL; knowledge from the law files; tools: read issues, read repo, open branch and pull request, comment, read Actions logs | `pytest tests/test_no_deploy_hands.py` proves no merge, deploy or cluster tool exists; a seeded issue produces a pull request and a plan comment; the trace is returned by a Langfuse query printed in the run log |
| 2 Identity + kill switch (~3h, in parallel with 1) | GitHub App minted on the `bin/idp-bootstrap-github-app` road (one root, then code); the crew#767 read-only account | suspend the App: the next run fails to sign in and says so on the board; unsuspend: it runs |
| 3 Cluster workload (~3h) | the five artefacts in `idp`: manifests, Flux row with a health check, catalogue Component, drill row, runbook. The founder deploys | the drill row is green from the estate clock; the first real `lane:infra` ticket goes end to end to a green pull request with zero agent merges |

## Optimised (LAW 51)

Naive: 31 steps, 9 pull-request waves, a founder word per step. Bottleneck: founder words and identity minting. Cut: one word at the top; step 2 runs beside step 1 (no dependency); the skeleton comes from `crewai create`, not by hand; law knowledge is ingested in one batch job from git, not per run; three pull-request waves, one per step. **31 → 12 steps, 9 → 3 waves, 3 words → 1.**

## Not doing

No migration of `crew/`, its roles, `crew/crew/cli.py`, the science lane or any script. No product code touched. No second scheduler, router or tracer. No cluster access from any agent, this crew included.

## Decisions made so the founder does not have to

Name `infra-crew`; a new repository; hierarchical process with a manager agent; one GitHub App per crew, not per agent. Risk in a sentence: crewAI is a young framework (1.x), so the crew's own tools carry the estate-specific behaviour and the framework is replaceable behind them.

**The one word: CONFIRM on crew#729 starts step 1.**

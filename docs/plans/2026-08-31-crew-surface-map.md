# Every surface the crew uses today — measured 2026-08-31, and what happens to each

Founder order: "dig deeper and map all surfaces ... audit yourselves and audit the crew ... the whole
repo ... whatever crew is using now we need to know." Every number below is from a command run this
session against the live repo and machine, not memory.

## A. The crew repo itself (543 tracked files)

| surface | measured | disposition | work item |
|---|---|---|---|
| `crew/` package: cli.py 543 + board/bdd/config/errors/gh/thread = 1,088 lines, entry `bin/crew` | the whole plan/claim/evidence/verify loop | REPLACE with crewAI Crew/Process/Task | W1 |
| `roles/` 4 charters, 301 lines (engineering, pm, qa, science) | prose role definitions | BECOME crewAI Agent definitions; add Otto (manager) + security agent | W2 |
| `integrations/claude-code/` crew-engineer.py, crew-listener.py hook, 2 agent defs | how a Claude session becomes a crew worker | REPLACE with the crewAI runtime entrypoint, then delete | W3 |
| GitHub issues (the board) | task queue + founder surface | KEEP; crewAI task ↔ issue sync adapter; evidence posting becomes a task-output callback | W4 |
| `science/` 103 files, 18,110 lines (collect 1,220; outcomes 627; law_enforcement 579; showcase 524; producers 514; datamap 509; research_grade 381; foresight 269; + shapes.json 4,433) | the analytics/grading warehouse | KEEP as crewAI Tools; two ruled cuts: read_rows→duckdb (crew#74/#104), foresight tracking→MLflow | W5 W6 W7 |
| `science/scheduler/` Dagster code-location, ONE schedule `build_warehouse_hourly` | | folds into the one-scheduler decision | W8 |
| `.github/workflows/` 11 (5 on cron: ci-runs, datamap-tickets, revenue, self-grade weekly, stale hourly, merge-when-green every 10 min) | CI + robot chores | KEEP gates; merge-when-green → GitHub native auto-merge (config-only); crons become rows under the one scheduler | W8 W9 |
| `scripts/` 37 files 5,526 lines incl. verify.d 19 rungs, pr-evidence.py, estate-snapshot, crew-triage | local verify ladder + board glue | KEEP; static-predicate rungs fold into OPA with the idp gates | W10 |
| `deploy/launchd/` 4 plists + `ops/launchd/` 1 (guard-selftest, bundlepush, estatesnapshot, sciencecollect, estatelander) | Mac clock jobs | RETIRE to the one scheduler (infra-never-Mac-bound ruling) | W15 |
| root: 29 files, ~14 overlapping prose docs (STATE.md, ESTATE_STATE.md, RITUALS.md, VISIBILITY-COMMUNICATION.md, MULTI-AGENT-COORDINATION.md, CREW_ORCHESTRATION_SPEC.md …) | duplicated operating prose | DEDUPE to one operating doc + the laws; rest deleted with CONFIRM | W18 |
| `docs/` 240 files (154 evidence, 26 onboarding, 26 demo) | receipts + tutorials | KEEP; evidence keeps accruing via W4 callback | — |

## B. The self-audit — what the sessions themselves run on (the harness)

| surface | measured | disposition | work item |
|---|---|---|---|
| `~/.claude/scripts/` 113 Python files, 30,328 lines; 33 hook wires (8 SessionStart, 10 Stop, 4 UserPromptSubmit, 10 PreToolUse, 1 PostToolUse) | guards (rule/credential/dod/scope/close/blocker/assertion/ticket/pr-cap/dupe/secret-scrub/opa-hook…), relays (friction, estate-state, feed, board-deliver, founder-deliver, doc-capture, directive-capture), daemons (consultd, kimi_bridge, board_serve, session-timeout, goal_graph) | EXTRACT the rules into one policy set (OPA — opa-hook.py already exists); crewAI guardrails read the same set. One rule source, two enforcement points. Relays become crewAI task-output handlers. Bridges retire — LiteLLM lanes already route those models. | W11 W12 W13 |
| 45 `test_incident_*` files in the same dir | every past mistake pinned | CARRY as the regression suite over the policy set — mistakes survive the migration | W14 |
| launchd: 8 `ai.estate.*` jobs (cockpit, consultd, kimi-bridge x2, scheduler→Dagster, session-timeout, sovereign-worker, temporal) + com.founder.boardserve/estate-awake | the Mac is running Dagster AND Temporal AND 5 GitHub crons — three scheduler engines at once, while Windmill is ruled (crew#695) but exists nowhere on disk | ONE scheduler. Founder decision W8 picks it; the other engines and every launchd clock job are deleted behind it | W8 W15 |
| state stores: `~/.estate/` (feed.md 12,341 lines, knowledge/, guards/, registry.jsonl, estate-state.json), 99 memory files, checkpoints/LATEST.md, `.swarm_memory.txt`, goal_graph, `.crew-state/` mirror of crew root docs | six overlapping memories | crewAI memory + knowledge store (cluster Postgres + embed lane) becomes the agent memory; feed.md and the board stay founder surfaces; .crew-state mirror and .swarm_memory deleted with CONFIRM | W16 W17 |
| config scatter: `.crew.json`, `estate.toml`, `mumchimp` literal in 39 idp + 8 crew files | | ONE estate config (seed: `idp/clusters/oke/estate-config.yaml`); sweep all 47 in one pass; gate refuses new literals | W0 W19 |
| reply style / delivery habits (jargon, work lost to the void, self-scoring) | ruled junk | NOT carried: Vale estate-style grades every founder-facing message; delivery = git doc + board post is machinery (W4/W12), not discipline | W20 |

## C. The exact work plan (order, each with its proof)

| # | what gets done | proof it is done | deletes |
|---|---|---|---|
| W0 | one estate config file; crew + idp read zone/repos/lanes from it | change zone in a test env, everything follows | .crew.json scatter |
| W8 | founder decides the one scheduler (Windmill per crew#695, or keep Dagster) | one engine answers `schedules list`; the others gone | Temporal launchd, Dagster-or-Windmill loser, 5 workflow crons, 15 Mac clock jobs (with W15) |
| W16 | knowledge store up: rulings + memories + runbooks ingested, embed lane | an agent recalls a ruling never shown in its context | — |
| W1+W2 | crewAI Crew with Agent defs from roles/ + Otto manager + security agent | one board issue executed end-to-end by the crew, trace in Langfuse | crew/cli.py (543) |
| W4+W12 | task↔issue sync; task-output callback posts evidence + doc to git every time | a finished task's doc is on the board without a human step | feed choreography scripts' delivery role |
| W3 | sessions enter through the crewAI runtime | crew-listener removed, crew still works | integrations/claude-code |
| W5 W6 W7 | duckdb cutover (drill exists), MLflow deployed then foresight tracking moved, science modules registered as Tools | duckdb_differential drill green; MLflow run page shows foresight model | ~300 lines read_rows |
| W11+W14 | rules extracted to OPA policy set; 45 incident tests run against it | same command corpus blocked/allowed identically pre/post | ~half of 30,328 harness lines |
| W13 | bridges retired onto LiteLLM lanes | kimi/deepseek answer via router, daemons unloaded | 2 launchd daemons |
| W9 W10 | auto-merge native; static gates → conftest | branch protection shows required checks; conftest green on the estate | merge-when-green cron, ~1,200–1,500 gate lines |
| W15 W17 W18 W19 W20 | launchd retirement, store consolidation, root-doc dedupe, literal sweep, Vale output gate | each is one PR with its own Verify line | mirrors, dup docs, 47 literals |

Every deletion lands only behind a CONFIRM on the board. No W starts before the founder approves this
map and the HOW of the W he greenlights.

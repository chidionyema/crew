# Science lane showcase

Generated 2026-09-02T05:07Z by `python3 science/showcase.py`. Every number is read at generation
time; the command under each heading reproduces it. A section that cannot see its source says BLIND.

## Progress since the previous run

Previous run: 2026-09-02T03:05Z.

No number changed.

## Capabilities

`python3 science/showcase.py  (reads science/*.py, scripts/science-collect, scripts/verify.d, launchd)`

| Capability | What it answers | Run | Scheduled by |
|---|---|---|---|
| capa | Did the fix actually stop him having to say it again | `python3 science/capa.py` | hand-run |
| collect | Collect every estate data store into one queryable table | `python3 science/collect.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| datamap | The estate's data dictionary, generated rather than written | `python3 science/datamap.py` | CI: scripts/verify.d/26-datamap-register.sh |
| dbt_build | Generate the dbt project's `facts` model from the one registry | `python3 science/dbt_build.py` | hand-run |
| decisions_intake | Decision intake from merged pull requests (crew#366, act/agent_decisions) | `python3 science/decisions_intake.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| docsmap | Inventory every document this estate owns, and say which ones fail the standard | `python3 science/docsmap.py` | CI: scripts/verify.d/95-docs.sh |
| dora | DORA four keys for the estate, measured from GitHub, never from memory (crew#495 CP9) | `python3 science/dora.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| duckdb_differential | Does DuckDB's `read_json_auto` read this estate's stores the same way collect.py does? | `python3 science/duckdb_differential.py` | hand-run |
| emit | Emit every collected science row to the estate collector as an OTLP log (LAW 50) | `python3 science/emit.py` | hand-run |
| export_drill | crew#74 row 1: the warehouse exit drill | `python3 science/export_drill.py` | hand-run |
| false_success | False-success rate: how often an agent's "resolved" claim on the board was rejected by the prover (crew#631 CP | `python3 science/false_success.py` | hand-run |
| foresight | Foresight: predict a red CI run before the push, and score the prediction after (crew#405) | `python3 science/foresight.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| friction | What the founder has had to say twice, measured over every transcript on this machine | `python3 science/friction.py` | hand-run |
| law_enforcement | Law enforcement coverage: which laws are machine-enforced, which are prose | `python3 science/law_enforcement.py` | launchd com.founder.lawenforcement |
| ledger | Writer for the research ledger (crew#72 row 1) | `python3 science/ledger.py` | hand-run |
| map_covers_laws | Every law in AGENTS.md has a check written for it in enforcement-map.json | `python3 science/map_covers_laws.py` | hand-run |
| outcomes | Collect what the estate produced, so spend can be divided by something | `python3 science/outcomes.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| producers | Every producer of data in the estate, discovered by class rather than typed by hand | `python3 science/producers.py` | hand-run |
| research_grade | Grade the general-purpose research capability from its own ledger (crew#508) | `python3 science/research_grade.py` | hand-run |
| research_inspect_grade | crew#701 CP1: the Inspect grader, run by science/research_run.py in its own interpreter | `python3 science/research_inspect_grade.py` | hand-run |
| research_intake | Scheduled outward research intake (crew#508 CP8) | `python3 science/research_intake.py` | hand-run |
| research_run | crew#701 CP1: one graded research report, end to end, on a GitHub runner | `python3 science/research_run.py` | hand-run |
| research_worker | The research worker: GPT Researcher through the router, every report graded by Inspect, every | `python3 science/research_worker.py` | hand-run |
| self_grade | Weekly self-grade of the research loop (LAW 35, crew#72 row 4) | `python3 science/self_grade.py` | hand-run |
| transcripts | Read Claude Code session transcripts incrementally, by byte offset (crew#319, crew#74 row 4) | `python3 science/transcripts.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| velocity | Velocity per lane, measured from the board, never felt (crew#527 CP1) | `python3 science/velocity.py` | hand-run |


## Lanes

`sqlite3 science/warehouse.db "select source, count(*) from facts where ingested_at >= datetime('now','-24 hours') group by source"`

BLIND: science/warehouse.db has no readable facts table (no such table: facts)

## Warehouse

`sqlite3 science/warehouse.db "select count(*), count(distinct source), max(ingested_at) from facts"`

BLIND: science/warehouse.db has no readable facts table (no such table: facts)

## Data map (LAW 50)

`python3 science/datamap.py --check`

- 60 register entries (COLLECTED 35, EXCLUDED 9, NEVER_EMITTED 4, WIRED_NEVER 11, WRITER_DEAD 1); 4198 producers discovered at the last census
- shape walk: BLIND (science/shapes.json empty or absent; no walk has landed)
- domains blind at the last census: cluster_live
- contract violations now: 1

## Datasets collected from the estate

`python3 -m json.tool science/sources.json`

Every dataset the science lane copies out of the estate, from the register the
collector enforces (science/sources.json). A store the machine crawl finds that sits
in neither table fails `python3 science/collect.py --check`, so an omission here is
red in CI, never silent.

| Dataset | Lane | Where it lives | Written by | How | Sensitivity | Kept, days | Fresh within, h | Newest row |
|---|---|---|---|---|---|---:|---:|---|
| bundle_push | code | `~/.claude/state/estate-bundle-push.jsonl` | `~/.claude/scripts/estate/estate_bundle_push.sh` | poll | internal | 180 | 48 | - |
| ci_reach | code | `~/.claude/state/ci-reach.jsonl` | `~/.claude/scripts/estate/estate_audit.py` | poll | internal | 180 | 48 | - |
| ci_runs | code | `science/ci-runs.jsonl` | `science/outcomes.py` | poll | internal | 365 | 30 | - |
| close_guard | code | `~/.claude/state/close-guard-observe.jsonl` | `~/.claude/scripts/close-guard.py` | push | internal | 90 | 48 | - |
| dora | code | `science/dora.jsonl` | `scripts/science-collect` | poll | internal | 3650 | 26 | - |
| estate_push | code | `~/.claude/state/estate-push.jsonl` | `~/.claude/scripts/estate/estate_push.sh` | poll | internal | 180 | 48 | - |
| hook_outcomes | code | `~/.claude/state/hook-outcomes.jsonl` | `~/.claude/scripts/hook-run.py` | push | internal | 180 | 24 | - |
| lane.code.pr-hygiene | code | `science/pr-hygiene.jsonl` | `science/outcomes.py` | poll | internal | 365 | 30 | - |
| ships | code | `science/ships.jsonl` | `scripts/science-collect` | poll | internal | 3650 | 26 | - |
| worktree_cleanup | code | `~/.claude/state/estate-worktree-cleanup.jsonl` | `~/.claude/scripts/estate/estate_worktree_cleanup.sh` | poll | internal | 180 | 720 | - |
| attention | crew | `science/attention.jsonl` | `science/outcomes.py` | poll | restricted | 365 | 26 | - |
| board | crew | `~/.claude/ESTATE_BOARD.jsonl` | `~/.claude/scripts/board-deliver.py` | push | internal | 365 | 48 | - |
| board_deadletter | crew | `~/.claude/state/board-deadletter.jsonl` | `~/.claude/scripts/estate-broadcast.py` | push | internal | 90 | 48 | - |
| decisions | crew | `~/.claude/DECISIONS.jsonl` | `scripts/science-collect` | poll | internal | 3650 | 48 | - |
| directives | crew | `~/.claude/directives` | `~/.claude/scripts/directives.py` | push | restricted | 3650 | 48 | - |
| founder_actions | crew | `~/.claude/state/founder-actions.jsonl` | `~/.claude/scripts/founder_actions.py` | push | internal | 3650 | 720 | - |
| goal_net | crew | `~/.claude/state/goal-net.jsonl` | `~/.claude/scripts/goal_graph.py` | push | internal | 180 | 48 | - |
| ledger | crew | `~/.claude/state/ledger.jsonl` | `~/.claude/scripts/goal-guard.py` | push | internal | 180 | 48 | - |
| prompt_ledger | crew | `~/.claude/state/prompt-ledger` | `~/.claude/scripts/prompt-ledger.py` | push | restricted | 365 | 48 | - |
| tickets | crew | `~/.claude/state/tickets` | `~/.claude/scripts/aiden/aiden.py` | push | internal | 365 | 48 | - |
| dagster-runs | data-ml | `$ESTATE_CODE/idp/run/dagster/history/runs.db` | `~/dev/code/idp/bin/scheduler-up` | poll | internal | 90 | 24 | - |
| dagster-ticks | data-ml | `$ESTATE_CODE/idp/run/dagster/schedules/schedules.db` | `~/dev/code/idp/bin/scheduler-up` | poll | internal | 90 | 2 | - |
| job_timelines | data-ml | `~/.claude/jobs` | `scripts/admit` | push | internal | 90 | 48 | - |
| temporal_dev_executions | data-ml | `~/.estate/temporal/dev.db` | `~/.claude/scripts/launchagents/ai.estate.temporal.plist` | poll | internal | 90 | 48 | - |
| agent_cert | hermes-v2 | `~/.claude/agent-cert/history.jsonl` | `~/.claude/scripts/statusline-context.py` | push | internal | 180 | 48 | - |
| aiden_ticks | hermes-v2 | `~/.claude/state/aiden-ticks.jsonl` | `~/.claude/scripts/aiden/tick.py` | poll | internal | 90 | 48 | - |
| alerts_inbox | hermes-v2 | `~/.estate/alerts/inbox.jsonl` | `~/.claude/scripts/founder-deliver.py` | push | internal | 180 | 6 | - |
| revenue | hermes-v2 | `science/revenue.jsonl` | `science/outcomes.py` | hand | restricted | 3650 | 24 | - |
| runaway-reaper | hermes-v2 | `~/.estate/logs/maintenance/runaway-reaper.jsonl` | `~/.claude/scripts/estate/runaway-reaper.sh` | poll | internal | 90 | 168 | - |
| sovereign_budget | hermes-v2 | `~/.estate/sovereign/budget.db` | `~/dev/code/idp/sovereign/engine/budget.py` | push | internal | 30 | 48 | - |
| sovereign_receipts | hermes-v2 | `~/.estate/sovereign/receipts.jsonl` | `~/.claude/scripts/estate/launchd_receipt.py` | poll | internal | 365 | 48 | - |
| stuck_detector | hermes-v2 | `~/.claude/state/logs/stuck-detector.jsonl` | `~/.claude/scripts/stuck_detector_tick.sh` | poll | internal | 30 | 48 | - |
| capability_receipts | portal | `~/.estate/state/capability_receipts.jsonl` | `~/.claude/scripts/estate/launchd_receipt.py` | push | internal | 365 | 48 | - |
| drills | portal | `~/.claude/state/drills.jsonl` | `~/.claude/scripts/drills/run.py` | poll | internal | 365 | 48 | - |
| drills_scripts | portal | `~/.claude/scripts/state/drills.jsonl` | `~/.claude/scripts/drills/run.py` | poll | internal | 365 | 48 | - |
| enforcement_map | portal | `science/enforcement-map.json` | `science/law_enforcement.py` | poll | internal | 365 | 48 | - |
| estate_registry | portal | `~/.estate/registry.jsonl` | `~/.estate/registry.jsonl` | hand | internal | 3650 | 48 | - |
| history | science | `~/.claude/history.jsonl` | `~/.claude/scripts/secret-scrub.py` | push | restricted | 365 | 48 | - |
| method_metrics | science | `~/Documents/code/prospector/store/ops/method_metrics.json` | `~/.claude/scripts/reflect.py` | poll | internal | 180 | 12 | - |
| predictions | science | `science/predictions.jsonl` | `science/outcomes.py` | hand | internal | 3650 | 48 | - |
| research_ledger | science | `science/RESEARCH-LEDGER.jsonl` | `science/ledger.py` | hand | internal | 3650 | 168 | - |
| spend | science | `~/.claude/estate-spend-history.jsonl` | `~/.claude/scripts/estate/estate_cost_sentinel.py` | poll | internal | 365 | 6 | - |
| hindsight_recall | unmapped | `~/.claude/hindsight-recall-history.jsonl` | `~/.claude/settings.json` | push | internal | 180 | 24 | - |
| pi_bridge_runs | unmapped | `~/.claude/state/pi-bridge-runs.jsonl` | `~/.claude/mcp/pi_bridge.py` | push | internal | 365 | 48 | - |

### Declined: found by the crawl, deliberately not collected (24)

| Store | Why not |
|---|---|
| transcripts | 6.5 GB of raw session text, so never a facts source: copying it would double the largest thing on the disk. Read instead by science/transcripts.py (crew#319), every byte once by offset, into science/transcripts.db: tool calls, results, errors, sessions. |
| telemetry | The CLI vendor's own failed event uploads. Not the estate's data, and it tells us nothing about the estate that spend and the ledgers do not say better. |
| toolguard-decisions | One file per tool decision, 28.5 MB of them. The rollup is already collected as the `toolguard` source, which is the same information joined. |
| prospector-dossiers | Product data belonging to the prospector domain, not estate telemetry. Fowler's point stands: centralising another domain's store here would make this the monolith the split is meant to avoid. |
| prospector-dossiers-worktree | The same product data, stranded in an abandoned agent worktree. That it holds 130.9 MB while the live store holds 0.0 MB is a real finding, and it belongs to prospector to fix rather than to this warehouse to absorb. |
| maestro-intents | Maestro's own working memory, one file per cycle. Another domain's store. |
| .claude/state/coord/jobs.sqlite | SQLite, not append-only rows. Ingesting it needs a reader that understands its schema; the generic jsonl path would produce garbage rows that look like data. |
| .estate/healthchecks/data/hc.sqlite | Healthchecks' own database, same reason. The estate reads its verdicts through the Healthchecks API, not by copying its tables. |
| dev/code/crew/science/warehouse.db | This is the sink. Collecting the warehouse into the warehouse is the loop LAW 30 warns about, and the row count would grow without bound. |
| crew-issues | Not a file. It is a GitHub API count, and it already reaches the estate through the inventory's own ledger row. |
| .maestro/experience_graph.db | SQLite, and one half of a duplicate the crawl reports in its own findings: the same graph exists at ~/.estate/knowledge/maestro/experience_graph.db. Which one is authoritative is maestro's call, not this warehouse's, and collecting both would make the duplicate look like twice the evidence. |
| .estate/knowledge/maestro/experience_graph.db | The other half of that duplicate. Declined for the same reason and named separately so neither disappears from the registry while the question is open. |
| .claude/state/one-branch/would-have-fired.jsonl | Producer (~/.claude/quarantine/2026-08-21-pipeline-workarounds/one-branch-fence.py) was quarantined 2026-08-21 22:42 -- not in ~/.claude/settings.json hooks, mode file ~/.claude/one-branch-fence.mode still reads 'refuse' but nothing calls it. Last write to would-have-fired.jsonl is 2026-08-21 22:38, the same window. This is a decommissioned guard, not a live source going quiet: it will never write again unless someone restores the hook. Declined 2026-08-24 by the on-call attribution (LAW 29) rather than left as a stale-source alert that can never clear itself. If the fence is restored, move this back to sources. |
| dagster-run-store | Dagster's own run history and schedule state, one SQLite file per run. It is the orchestrator's bookkeeping about the jobs, not a fact about the estate -- what those jobs produced is already collected as the sources they write. Declined as a directory rather than 14 ids because the run store names each file after a fresh UUID, so an id list would be stale the next time Dagster runs. 2026-08-27 (crew#376): the tick and run tables are now collected as dagster-ticks and dagster-runs from the live store under the idp checkout (run/dagster); this ~/.estate/dagster copy is stale since 2026-08-24 and stays declined. |
| .estate/REQUIREMENTS.jsonl | The id is relative to the 'home' root, so the file is ~/.estate/REQUIREMENTS.jsonl -- not a path inside this repo. A reviewer probed ~/dev/code/crew/.estate/REQUIREMENTS.jsonl, found nothing, and reasonably read that as the row describing a file that does not exist. hermes-v2's monitoring requirements, and a specification rather than an event stream: 5 MON-* rows of id, phase, statement and acceptance_cmd, rewritten in place, carrying no timestamp. Ingesting it would append the same 5 undated rows on every run and grow without bound while saying nothing new. The signal worth having is how many of them currently pass, and that is produced by hermes-v2/bin/check-requirements.py against the live estate, not by copying the statements. Owner: hermes-v2 (templates/REQUIREMENTS.jsonl.tmpl, bin/verify). If hermes wants the pass/fail verdicts in the warehouse, that is a source pointing at its verify output, not at this file. |
| crew-snapshot-worktree | A git worktree of this repo kept by com.founder.estatesnapshot so the hourly STATE.md rebuild reads a clean checkout. Every jsonl under it (science/ships, science/attention, science/RESEARCH-LEDGER, risk/REGISTER, science/predictions) is a copy of a file tracked in crew and already collected from the science root. Collecting the copies would double-count every row. Declined as a directory because the worktree is re-created whenever the snapshot job resets it. |
| .estate/temporal/dev.db | The Temporal dev server's own persistence (SQLite), written by temporal CLI, schema owned upstream and rewritten on upgrade. It holds workflow history for the orchestrator, not a fact about the estate; what the workflows produce is collected from their outputs. Owner: the scheduler row of STANDARDS. When Temporal moves to the cluster (crew#78) this file goes with it. |
| .estate/sovereign/budget.db | The sovereign runner's budget counter, a SQLite file it locks and rewrites in place; it carries no rows with a time. The fact stream beside it, .estate/sovereign/receipts.jsonl, is collected as source sovereign_receipts and holds budget_remaining on every receipt, so the counter's history is already in the warehouse. |
| toolguard | emitter tool-drip-guard.py is wired to no hook and no launchd job since 2026-08-23; decommissioned by omission (crew#265) |
| consult | ai.estate.consultd runs with no backend configured, every consult returns 503, nothing written since 2026-08-23 (crew#265) |
| founder_actions | written only by estate_audit.py, which stopped reaching that write on 2026-08-23; no owner job (crew#265) |
| worktree_cleanup | estate_worktree_cleanup.sh is scheduled by nothing since 2026-08-23 (crew#265) |
| .estate/healthchecks/hc.sqlite | a 0-byte file at the directory root, created 2026-08-27 01:14 beside the real database data/hc.sqlite (declined above); nothing writes it, so there is nothing to collect (crew#465) |
| transcripts-index | science/transcripts.py's own index of the declined transcripts (every byte read once by offset). A derived store of a declined source, rebuilt four times a day by scripts/science-collect (crew#432); its tool-call and error rows already reach the warehouse through that reader, so collecting the index again would count them twice. crew#90. |

## Research ledger

`python3 -c "import json; print(sum(1 for l in open('science/RESEARCH-LEDGER.jsonl')))"`

- 31 entries, 2026-08-23 to 2026-08-28; 31 record the decision they fed

- **2026-08-24** Which of the estate's hand-written Claude Code guard hooks (rule-guard, goal-guard, tracked, jargon-guard, context-guard-hook) can be expres
  - decision: Replace one, split one, delete half of one, keep two. (1) jargon-guard.py -> Vale 3.17.1, already installed, already configured in 10+ repos: highest-value swap
  - metric: 269 lines (jargon-guard.py) duplicating Vale 3.17.1, which is installed and used in 10+ repos and referenced 0 times by the guard; plus an unmeasured share of rule-guard.py's 1362 lines duplicating 41 existing permissions.deny rules. -> None
- **2026-08-24** Is there a proven tool for 'prove this system can be rebuilt from nothing', to replace the hand-written nightly drill runner at ~/.claude/sc
  - decision: KEEP ~/.claude/scripts/drills/run.py. It is a drill REGISTER - 13 entries, 5 named as not yet written, with an orphan check - and no product on the market is th
  - metric: 13 registered, 8 with a command, 5 NOT WRITTEN; ai.estate.drills last exit = 1; its plist is in no git repo. -> None
- **2026-08-28** Would this market pay at least twice the price of an idea dossier for a five-year survival probability conditioned on industry code and regi
  - decision: Whether prospector's next price test sells a survival rating beside the dossier (SCALE_market hypothesis 7 test: two checkout pages, 200 visitors each, pass if 
  - metric: 0 ideas on the ledger; three contract rows FAIL (no data) -> None

## Delivery outcomes

`python3 science/outcomes.py ship --days 7; python3 science/outcomes.py attention --days 7`

- last 7 days: 77 commits across 4 repos
- founder messages 799, complaints 20 (2.5%)
- spend: BLIND (warehouse absent)
- machine learning: none. Nothing here trains a model; every number is a count or a ratio.

## Predictions

`python3 science/outcomes.py rate`

- 13 recorded before a repair, 2 scored after, hit rate 50%

## Ideas: the prospector contract (crew#537)

`python3 -c "import json; print(sum(1 for l in open('science/RESEARCH-LEDGER.jsonl') if json.loads(l).get('kind')=='idea'))"`

| Row | Value | Grade |
|---|---|---|
| ideas generated per week | 1 | ok |
| ideas graded (forecast with source) | 1 | ok |
| ideas resolved with Brier | 0 | FAIL (no data) |

- 1 idea rows in the ledger (`kind: idea`, written by `python3 science/ledger.py add --kind idea --forecast P`); resolved with `--outcome 0|1`. Red until the first business idea lands (CP5).

## Foresight: will this PR go red?

`python3 science/foresight.py report`

BLIND: science/foresight-state.json absent (python3 science/foresight.py train)

## False success: claims the prover rejected

`python3 science/false_success.py --days 30`

- false-success rate n/a (no claim decided yet): 0 rejected of 0 decided claims, 1 pending, last 30d
- a claim is an agent labelling a ticket RESOLVED_PENDING_VERIFICATION; the verdict of the moment is the prover App's next move on it (idp ticket-verification.yml)
  - pending #636 ticket-verify canary (crew#631 CP5): an agent-set VERIFIED must be rev

## Roadmap

`git log -1 --format=%cs -- science/PLAN.md`

Read from `science/PLAN.md` (last changed 2026-08-23) each run, so this page and the
plan cannot say different things. A goal is on the roadmap only if a command can
grade it; the grading command is printed beside each one.

- **G1 — a law that can be a check, is a check**
  - now: 2 of 31 laws named by a live guard
  - target: 12 of 31 by 2026-09-23
  - graded by: `science/law_enforcement.py`
- **G2 — every instrument has a named reader**
  - now: 0 live readers of the estate's main metrics file
  - target: every live instrument has a named reader by 2026-09-06
  - graded by: `an instrument with no reader on that date is deleted, not kept`
- **G3 — the estate can say what caused a failure**
  - now: n = 0, hit rate unmeasurable
  - target: 20 predictions logged and scored by 2026-09-30
  - graded by: `the hit rate itself, whatever it is`
- **G4 — the complaint rate falls**
  - now: 1.95 stops per 100 messages, 601 complaints over 2605 messages
  - target: 1.2 by 30 days, 0.8 by 60 days
  - graded by: `no grading command named in PLAN.md yet`

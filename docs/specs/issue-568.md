# crew#568 — One model stack: the migration plan

Status: PLAN, waiting on the founder's examination. Nothing below this line has been executed
except the two inventory PRs named in Phase 0. Ticket: crew#568 (P1). ADR: idp `docs/adr/0010-one-model-router.md`, written in Phase 1.

## What was decided, and what is true today

Decided (crew#119 R8, #122, #284 §3.3/§4.2, #293, #400, #506, #533, #576, #579): one provider-agnostic
router, every agent behind it, Claude one lane among many, keys minted by the pipeline, models
picked in a console not a PR, OpenCode as the harness that reads `AGENTS.md` on any vendor.

Measured 2026-08-29 (commands in crew#568 comment 5461152598):

| Fact | Number |
|---|---|
| Router lanes live at `llm.mumchimp.com` | 11 (`idp/platform/llm/config.yaml`), no `anthropic` lane |
| Router lifetime spend / calls | $0.0037 / 351 (consumers: sovereign-kernel, k8sgpt) |
| Claude Code spend today, direct to Anthropic | $850.35 / 4,965 requests |
| Agents defined outside the router | 13 `~/.claude/agents/**/*.md`, `consultd.py` daemon, hermes-v2 primary, prospector chain |
| Vendor key stores on the Mac | 6 (`~/.pi/models.json`, `~/.config/pi/config.json`, `~/.config/llm/secrets.sh`, `~/.config/wave/secrets.sh`, `~/.zshrc`, launchd env) |
| Idle credit: Cursor, 6 Ollama models | 0 calls routed |
| Boxes ticked across the nine tickets | 0 |

Verdict: the router exists and nobody uses it. Not operational.

## Target (one paragraph)

Every model call on the estate — Claude Code, OpenCode, hermes-v2, prospector, `bin/consult`, pi,
k8sgpt, Dagster jobs — goes to `llm.mumchimp.com` with a per-consumer virtual key. The router holds
the vendor keys (OCI vault → `litellm-upstream`), the lanes, the budgets, the fallbacks and the spend
ledger. Anthropic is lane `claude` beside `minimax`, `deepseek`, `gemini`, `groq`, `openrouter`, and a
`local` lane for Ollama on the Mac. A model is changed in the LiteLLM UI or `config.yaml`, never in
an agent file. The harness on the Mac is OpenCode; Claude Code stays installed as one client of the
same router, not the default. Spend is one query: `oke-check.yml -f mode=break-glass -f playbook=router-spend`.

## Phases

Each phase: what changes, exact command that proves it, what can break, and the way back.

### Phase 0 — Measure and hand the Mac a key (built, unmerged)
- idp#745 `router-spend` playbook (spend by consumer × lane, per day, keys). Proof: the run prints three tables.
- CP2 branch `feat/crew568-laptop-on-the-spine`: `vault-seed.yml -f entry=laptop` mints one virtual key across all lanes, sops-encrypts it into `estate-secrets/secrets/dev/LITELLM_LAPTOP_KEY.yaml` via a `vault-writer` App lane; `bin/litellm-status` fails on any vendor key still on the Mac (4 FAIL rows today).
- Back: delete the key row in the LiteLLM UI; `git revert`.

### Phase 1 — Claude becomes a lane; ADR 0010
- `platform/llm/config.yaml`: lanes `claude` (`anthropic/claude-fable-5`), `claude-fast` (`anthropic/claude-sonnet-5`), `local` (`ollama/…` reached over Tailscale to the Mac; off when the Mac is off, fallback `minimax`). Vault entry `litellm-upstream` gains `ANTHROPIC_API_KEY` from the existing `SEED_*` root (R52: pipeline mints, no console).
- `docs/adr/0010-one-model-router.md`: the decision, the nine tickets, what does not port (crew#122: tool schemas, thinking blocks, prompt cache) and the rule that agent files name a lane, never a vendor.
- Proof: `curl -s llm.mumchimp.com/v1/models -H "Authorization: Bearer $LITELLM_API_KEY" | jq -r '.data[].id'` lists 14 lanes; one `claude` call shows in `router-spend`.
- Break: Anthropic prompt caching through LiteLLM needs `cache_control` passthrough; measured in Phase 3 before anything is enforced (crew#533).

### Phase 2 — The Mac holds one key
- `~/.pi/models.json` → one provider `estate` (`https://llm.mumchimp.com/v1`, `$LITELLM_API_KEY`); `~/.config/pi/config.json` same; `~/.zshrc` exports `LITELLM_API_KEY` through `estate-secrets/scripts/secret-load`; `~/.config/llm/secrets.sh` and `~/.config/wave/secrets.sh` renamed `*.retired` (not deleted, LAW 16); launchd `ai.estate.consultd` and `ai.estate.kimi-bridge` unloaded; hermes `bin/consult` and `~/.claude/scripts/consultd.py` call the router (`bin/consult` becomes a 20-line client, consultd's cascade is the router's fallback list).
- Proof: `bin/litellm-status` prints `ok none`; `grep -rl 'api.anthropic.com\|api.deepseek.com\|api.minimax.io\|openrouter.ai' ~/.pi ~/.config ~/.zshrc` is empty.
- Back: rename `*.retired` back, `launchctl load`.

### Phase 3 — OpenCode is the harness, measured before enforced
- OpenCode 1.18.20 is already installed (`/usr/local/bin/opencode`). `~/.config/opencode/opencode.json`: provider `estate` = the router, models = the lanes, default `minimax`, `claude` on request. `AGENTS.md` is read as-is.
- Run one real ticket end to end on `minimax` via `opencode run --dir ~/dev/code/idp -m estate/minimax --auto` (crew#533's "measure MiniMax before enforcing"): the ticket is a small idp incident test. Record on crew#568: tokens, cost, wall time, pass/fail on the rungs, versus the same ticket on `claude`. That number decides the default lane; the founder picks it.
- Proof: `router-spend` shows consumer `laptop`, lanes `minimax` and `claude`, and the PR merged.
- Break: MiniMax may fail the rungs on a hard ticket; then `claude` stays default and `minimax` takes review/lint/test lanes (the cheaper lane still absorbs the bulk).

### Phase 4 — Agents, scripts and rules files move to the estate
Measured 2026-08-29: `~/.claude/scripts` holds 158 scripts (119 Python, 76 naming Claude or Anthropic), git-held in the `claude-guards` repo; `~/.claude/agents` holds 13 agent files; the rules exist as five top-level copies (`~/.claude.md`, `~/.claude/CLAUDE.md`, `~/.claude/AGENTS.md`, two `.snapshot.md`, `~/AGENTS-FULL.md`) plus 13 `AGENTS.md` and 4 `CLAUDE.md` across the repos.
- Agents: 13 `~/.claude/agents/**/*.md` → `~/.estate/agents/<role>.md` (git-held, LAW 24), each with `lane:` in front matter and no vendor name. Claude Code and OpenCode both read them (symlink for Claude Code, `agent` config for OpenCode). A guard refuses an agent file naming a vendor.
- Scripts: the `claude-guards` repo is renamed `estate-guards` and checked out at `~/.estate/scripts`; `~/.claude/scripts` becomes a symlink to it. Scripts that call a model directly (`consultd.py`, `kimi-bridge`, any `anthropic`/`openai` import: `grep -l 'import anthropic\|api.anthropic.com' ~/.claude/scripts/*.py`) are rewritten to call the router with the laptop key. Scripts that exist only as Claude Code hooks (`hook-run.py` and the guards it runs) get the same guard registered as an OpenCode plugin (`~/.config/opencode/plugin/`), one runner, two harnesses. A script OpenCode already does natively (session feed, compaction handoff) is retired with `git mv` to `retired/`.
- Rules: one `AGENTS.md` per repo is the file both harnesses read. The five top-level copies collapse to `~/.estate/AGENTS.md` (`~/.claude/AGENTS.md` and `~/.claude.md` become symlinks; the two `.snapshot.md` are deleted from the tree, they are in git history). Each repo `CLAUDE.md` becomes the one line `@AGENTS.md`.
- Proof: `find ~/.claude/agents -type f -name '*.md' | wc -l` → 0; `readlink ~/.claude/scripts` → `~/.estate/scripts`; `grep -rl 'api.anthropic.com' ~/.estate/scripts` → empty; `wc -l */CLAUDE.md` in `~/dev/code` → every file 1 line; guard tests green in both harnesses (`opencode run --dir idp "run the rungs"` and the Claude Code hook both refuse a bare `kubectl`).
- Break: a hook that only fires in Claude Code protects nothing in OpenCode until its plugin exists; the plugin lands in the same PR as the move, never after.

### Phase 5 — Products onto the router
- hermes-v2 primary `anthropic` → lane `claude` via router (its own virtual key `hermes`); prospector chain (`prospector`); Dagster jobs (`dagster`); k8sgpt already there. Each consumer = one `bin/idp-router-key` row in `vault-seed.yml`, each with a monthly budget.
- Proof: `router-spend` lists ≥5 consumers; `grep -rn api.anthropic.com hermes-v2 prospector-main` → 0 outside `platform/llm`.

### Phase 6 — Enforce and forget
- `bin/litellm-status` in the estate snapshot; a laptop guard refuses a `*_API_KEY` export for a vendor; STANDARDS.md LLM row points at ADR 0010; crew#119/#122/#284/#293/#400/#506/#533/#576/#579 closed with the box ticked by qa-agent against this spec.

## Rollback — one word from the founder, back in minutes

Every phase is built so that the way back is one command, and the founder never runs it: he says **`ROLLBACK <phase>`** (or `ROLLBACK ALL`) on crew#568, and the session on the lane runs `bin/estate-rollback <phase>` and posts the proof. No phase ships until its rollback line has been run once against a copy and shown green (LAW 3: the way back is tested before the way forward is trusted).

| Phase | What comes back | Command | Proof |
|---|---|---|---|
| 0 | Laptop router key withdrawn | delete the `laptop` key in the LiteLLM UI, `git revert` of the vault-seed PR | `router-spend` lists no `laptop` key |
| 1 | Claude lanes removed from the router | `git revert` of the config PR; Flux reconciles in one cycle | `/v1/models` lists 11 lanes again |
| 2 | Mac back on vendor keys | `mv *.retired` back, `launchctl load` consultd and kimi-bridge, `git checkout` of `~/.pi/models.json` | `bin/litellm-status` shows the 4 FAIL rows again, `bin/consult` answers |
| 3 | Claude Code back as the harness | nothing to undo: Claude Code was never removed; `~/.config/opencode` is left in place unused | a Claude Code session runs the rungs |
| 4 | Agents, scripts, rules back under `~/.claude` | `git checkout <tag>` of `claude-guards` at the pre-move tag `pre-568-phase4`, symlinks replaced by the directories | `find ~/.claude/agents -type f | wc -l` → 13; every hook fires |
| 5 | A product back on its own vendor key | per product `git revert`; the vendor key was never deleted from that product's vault entry | product health check green, its calls gone from `router-spend` |
| 6 | Guards off | `git revert` of the guard PR | snapshot green without the rows |

Rules of the rollback:
- Nothing is deleted on the way forward. Files are renamed or moved with `git mv`; keys and vault entries are kept until phase 6 is signed off by the founder; each repo is tagged `pre-568-phase<N>` before its phase merges.
- `ROLLBACK` outranks every open piece of work on the lane: the session stops what it is doing, rolls back, posts the proof, then asks nothing.
- Target time: phases 0–4 back in under 15 minutes of machine time; phase 5 within one Flux cycle per product. The measured time from the rehearsal goes in the PR body.
- After a rollback the plan does not retry silently: the phase reopens on crew#568 with the reason the founder gave, and waits for `go`.

## Order and effort
0 → 1 → 2 and 3 in parallel → 4 → 5 → 6. Phases 0–3 are one session's work in machine hours; 5 is the only one that touches a product and lands one product per PR.

## What the founder decides
1. Default lane for the harness after the Phase 3 measurement (`minimax` or `claude`).
2. Whether Claude Code stays installed as a client (plan says yes, as a client only).
Nothing else needs him.

## Optimised
Naive: 9 tickets re-read × 6 phases × per-tool key = 54 steps, 9 round trips. Bottleneck: key delivery to the Mac. Cut: one virtual key for the Mac (Phase 0), vendor keys only in the router; ADR replaces re-reading nine tickets. 54 → 18 steps, 9 → 3 round trips.

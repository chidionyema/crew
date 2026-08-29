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

### Phase 4 — Agents move to the estate
- 13 `~/.claude/agents/**/*.md` → `~/.estate/agents/<role>.md` (the claude-estate repo, git-held, LAW 24), each with `lane:` in front matter and no vendor name (`grep -L` gate). Claude Code and OpenCode both read them via symlink/config. A gate in claude-guards refuses an agent file naming a vendor.
- Proof: `ls ~/.claude/agents/**/*.md` → 0 regular files, 13 symlinks; guard test green.

### Phase 5 — Products onto the router
- hermes-v2 primary `anthropic` → lane `claude` via router (its own virtual key `hermes`); prospector chain (`prospector`); Dagster jobs (`dagster`); k8sgpt already there. Each consumer = one `bin/idp-router-key` row in `vault-seed.yml`, each with a monthly budget.
- Proof: `router-spend` lists ≥5 consumers; `grep -rn api.anthropic.com hermes-v2 prospector-main` → 0 outside `platform/llm`.

### Phase 6 — Enforce and forget
- `bin/litellm-status` in the estate snapshot; a laptop guard refuses a `*_API_KEY` export for a vendor; STANDARDS.md LLM row points at ADR 0010; crew#119/#122/#284/#293/#400/#506/#533/#576/#579 closed with the box ticked by qa-agent against this spec.

## Order and effort
0 → 1 → 2 and 3 in parallel → 4 → 5 → 6. Phases 0–3 are one session's work in machine hours; 5 is the only one that touches a product and lands one product per PR.

## What the founder decides
1. Default lane for the harness after the Phase 3 measurement (`minimax` or `claude`).
2. Whether Claude Code stays installed as a client (plan says yes, as a client only).
Nothing else needs him.

## Optimised
Naive: 9 tickets re-read × 6 phases × per-tool key = 54 steps, 9 round trips. Bottleneck: key delivery to the Mac. Cut: one virtual key for the Mac (Phase 0), vendor keys only in the router; ADR replaces re-reading nine tickets. 54 → 18 steps, 9 → 3 round trips.

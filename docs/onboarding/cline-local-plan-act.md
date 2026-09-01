# Cline on the laptop: the R67 pattern as a local option

Founder, 2026-09-01: "lets set this up also as an option for working locally, we not using it yet."
His research document (the record): `~/.claude/docs/founder/2026-09-01T1838Z-ook-lets-set-this-up-also-as-an-f8bef917.md`
in the claude-estate repo. Ruling this implements locally: R67 (plan strong, execute cheap, review strong).

## What is installed

- Cline CLI 3.0.60, installed with `npm i -g cline` (node 22.13.1 via nvm). Verified against
  Cline's own docs 2026-09-01 (docs.cline.bot): the terminal CLI is real, the Claude Code
  provider is real, and it bills the Claude subscription, not an API key.
- Two providers stored in `~/.cline/data/settings/providers.json`:
  - `claude-code` → the local `claude` binary (`~/.local/bin/claude`), model `claude-opus-5`.
    Subscription auth; no Anthropic key on the Mac.
  - `openai-compatible` → the estate router `https://llm.mumchimp.com/v1`, model `minimax`.
    The key is the laptop's existing `LITELLM_API_KEY`; no vendor key on the Mac (ADR 0011).

## How to use it (not in use yet — an option)

```
cline -p -P claude-code "design the change"          # planner: Opus on the subscription
cline -P openai-compatible -m minimax "do the steps" # executor: MiniMax through the router
```

The CLI has no persistent per-mode model binding (checked in the docs and the settings file),
so the mode-to-model mapping is these two flags, not a wrapper script.

## Two deliberate deviations from the pasted research

1. **The executor key stays off the Mac.** The paste says paste DeepSeek/MiniMax keys into
   Cline; here Act mode points at the estate router, which owns the vendor credential, the
   fall-backs and the spend ledger. One routing layer (the platform headline), and R67's
   chains apply unchanged.
2. **The pi bridge is not dismantled.** The founder said "we not using it yet"; nothing is
   deleted for an option.

## Caveats measured on 2026-09-01

- The `claude-code` provider runs the full local Claude Code harness: global hooks fire, so a
  nested session appears on the estate feed (entry `session 804722d4 · lane scratchpad`) and
  Cline's `--auto-approve false` does not gate tools inside that subprocess — the claude
  binary applies its own permission mode. Treat plan mode as a full agent, not a bare model.
- Cline's docs: responses through claude-code "may not stream token-by-token"; images and
  prompt caching are limited in that mode.
- Anthropic's terms treat the CLI as the product surface; driving it from another harness
  leans on the subscription in a way Anthropic may throttle or break at any release. This is
  an experiment lane, never a platform layer (R67's platform lanes stay on the router).

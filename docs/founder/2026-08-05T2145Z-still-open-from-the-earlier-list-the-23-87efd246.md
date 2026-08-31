---
captured: 2026-08-05T21:45:38+00:00
session: 57cc3775-f443-423e-8ad4-00d2fca188ce
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2298
source: founder prompt, verbatim (founder-doc-capture.py)
---

Still open from the earlier list: the 23:00 cron verification for self-improve-hourly and hermes-config-auto-push, the 3 fence-violation backfills before PR-1 becomes required, and the log brainstorm write-up. need to get this done lso and we need to     , 
Answer to "there must be a way round this Claude Code CLI": yes, and it's now proven and committed.

The route is ACP + MCP, not token borrowing:

- Token borrowing is dead — HTTP 400: Third-party apps now draw from your extra usage, not your plan limits, using the verified Claude Code OAuth credential (auth.json pool id 6e97cc, auth_type=oauth, source=claude_code). That is a billing verdict; no header fixes it.
- The binary is first-party — driving claude-agent-acp over the fork's own JSON-RPC sequence (agent/copilot_acp_client.py:543-586) returned stopReason end_turn, totalTokens 104691, no 400, and ran a live web search.
- The toolless caveat I gave you earlier was wrong. hermes mcp serve was already in the CLI and unused: it answers initialize in 5.9s and exposes 10 tools. Passed through ACP session/new mcpServers, Claude Code listed all ten as mcp__hermes__* in its real tool list.
- What can never work: the shim's prose <tool_call> contract (:128 / :227). Claude Code refuses to fabricate calls for tools it doesn't have, and emits real calls as ACP session/update events — so the text regex structurally cannot see them.

Committed: 2f06b90 (OpenRouter purged — the three stacked faults, with the verified-clean log after restart) and 0107e65 (~/.hermes/docs/CLAUDE_CLI_BRAIN.md).

Memory written: claude-code-as-a-brain-via-acp-plus-mcp.md (new), a-usable-openai-api-key-forces-provider-openrouter.md (new), claude-code-oauth-token-no-longer-spends-the-plan.md (updated to point at the ACP route), all three indexed in MEMORY.md.

Not started (design only, awaiting your go-ahead): the build order in CLAUDE_CLI_BRAIN.md:128-137 — Design B, Claude Code as the agent. One blocking fork change: copilot_acp_client.py:563 hardcodes "mcpServers": []. Step 3 (hold one ACP session open across turns) is not optional — spawn-per-turn pays the ~30s async MCP registration every turn and will intermittently run with no tools.

Safe point — type /clear (state saved, nothing will be lost).
 ok lets keep going until all perfect

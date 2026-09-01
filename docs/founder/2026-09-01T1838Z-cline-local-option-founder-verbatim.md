---
captured: 2026-09-01T18:38:51+00:00
session: 54539261-20a7-4289-a144-e9265f1b0c43
cwd: /Users/chidionyema/dev/code/.wt-r67-plan-execute-review
chars: 4165
source: founder prompt, verbatim (founder-doc-capture.py)
---

ook lets set this up also as an option for working locally, we not using it yet but as an ai reseaching and toolng conpany we need to be pusing the barrier of whats possible I have deep-researched the 2026 terminal agent ecosystem specifically for this exact constraint. The reason you have had so much friction is that Anthropic deliberately designed Claude Code as a walled garden. They enforce this by blocking Max subscription OAuth tokens from standard API access, forcing you to use their CLI for everything so that execution burns through your Max rate limits.

You don't need a custom proxy, and you don't need an IDE. The clean, native, future-proof solution is Cline CLI.

Here is exactly how it solves your problem today.

The Architecture: Cline CLI's "Dual-Provider" Strategy

Cline is an open-source agent that runs natively as a terminal CLI (no VS Code required). It has two specific features built exactly for your situation:

1. The Brain: The Native "Claude Code" Provider

You don't need an API bridge because the Cline community already built a native wrapper into the tool. In Cline's configuration, there is a provider specifically called "Claude Code". When you select this, Cline does not make an HTTP API call. Instead, it silently spawns a subprocess running your local Anthropic claude binary (claude -p --output-format stream-json).

The Result: You extract Claude Max's top-tier reasoning for your architecture and planning phase.
The Cost: $0 extra. It seamlessly uses your Max subscription authentication.
2. The Hands: Plan Mode vs. Act Mode

Cline natively separates its workflow into two distinct phases: Plan Mode and Act Mode. You configure Cline so that the two modes use different engines:

Plan Mode (The Architect): Set this to use the Claude Code Provider. When you ask it to design a system, read your CLAUDE.md, or solve a complex bug, it uses your Max subscription.
Act Mode (The Executor): Set this to use your direct DeepSeek API key or your MiniMax API key (via the OpenAI-compatible endpoint).
How the Workflow Actually Looks in Your Terminal

You initiate a task in Cline CLI.
Claude Thinks: Cline boots up the local claude binary in the background. Claude reads your Agent.md and CLAUDE.md, analyzes the codebase, and writes a step-by-step architectural plan.
You Approve the Plan.
DeepSeek/MiniMax Executes: Cline seamlessly drops the Claude subprocess and switches to your direct MiniMax or DeepSeek API key. The cheap executor takes Claude's exact blueprint and runs the 50-step loop of writing files, running terminal commands, and fixing compiler errors.
Why this is the ultimate "Bang for Buck" (Â£50/month)

Massive Token Savings on Max: Because Claude is only doing the initial reasoning and planning, you stop burning your Claude Max rate limits on trivial file-writing and syntax-fixing loops. You will rarely hit your Claude rate limits again.
Maximum Compute for your Â£50: Your Â£50 cash budget goes directly to MiniMax and DeepSeek. Because execution tasks are highly repetitive (reading the same files over and over to fix small errors), DeepSeek V3 and MiniMax's native prompt caching will reduce your execution costs to literal pennies per day.
Zero Wasted Effort: Your custom markdown files (CLAUDE.md, Agent.md) are natively ingested by Cline, meaning your entire existing framework carries over instantly without modification.
Your Setup Steps for Today

Dismantle the Bridge: Delete your Pi bridge completely.
Install Cline CLI: Run npm install -g @cline/cli (or the equivalent 2026 global install command for your environment).
Ensure Anthropic's CLI is logged in: Run claude once to ensure your Max subscription is authenticated.
Configure Cline:
Set the Planning/Primary Provider to Claude Code and point it to the path of your claude binary (usually just claude).
Set the Execution/Act Provider to DeepSeek (direct) or OpenAI-compatible (for MiniMax) and paste your Â£50-funded API keys.
This setup locks you into the best of both worlds: Anthropic's billion-dollar reasoning engine for free, backed by the fastest, cheapest execution models on the market, running purely in your terminal.

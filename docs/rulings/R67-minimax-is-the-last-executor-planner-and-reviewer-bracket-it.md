# R67: MiniMax is the last lane of execution; a planner and a reviewer bracket it

Founder, 2026-09-01, verbatim: "MiniMax needs to be the last chain of execution really cheap and
fast but need planner and reviewer."

Said while reading the routing facts: Otto's Telegram brain is the router lane `claude`
(`anthropic/claude-sonnet-5`, `hermes-v2/config.yaml:6-9`, `idp/platform/llm/config.yaml:92-99`),
every fall-back chain ends in MiniMax then DeepSeek (`idp/platform/llm/config.yaml:169-189`), the
coding jobs run on `claude-haiku-4-5` (`idp/platform/hermes-agent/estate.yaml:55`), and no lane
anywhere turns on deep reasoning.

## Meaning

- **Three roles, not one model.** Every agent turn that changes the world is a chain of three
  calls with three named router lanes: `plan` (a strong reasoning model writes the steps and the
  checks), `execute` (a cheap, fast model carries the steps out), `review` (a strong model grades
  the result against the plan before anything is sent, merged or replied). The lanes are names
  on the router; the vendor behind each name is the router's business (LAW 34).
- **MiniMax is the executor and the last hop.** `execute` is MiniMax first, DeepSeek behind it.
  MiniMax is also where every chain still ends when a stronger lane is down. It is never the
  planner and never the reviewer.
- **Planner and reviewer are strong.** `plan` is the reasoning lane (Claude Opus 5 with extended
  thinking, Sonnet 5 behind it); `review` is Sonnet 5 with Opus behind it. A reviewer that is the
  same model as the executor is self-scoring, which is banned (founder 2026-08-31).
- **The plan and the review are DSPy programs, not prose prompts** (R64). Each is a compiled
  module with a verifier, versioned in git, traced in Langfuse.
- **This is the founder's own Verified Scaffold** (crew#513: the top model compiles the method,
  weak models execute, every step is verified). R67 is the routing rule that makes it real.

## Where it lands

| surface | today | under R67 |
|---|---|---|
| router `idp/platform/llm/config.yaml` | `claude`, `claude-fast`, `minimax`, `deepseek` … | adds `plan`, `execute`, `review` lanes with the chains above; existing names stay |
| Otto's Telegram brain `hermes-v2/config.yaml` | `model.default: claude` | plan step on `plan`; tool turns on `execute`; `review` before the reply |
| Otto's coding jobs `platform/hermes-agent/estate.yaml` | `work: claude-haiku-4-5` | plan on `plan`; the work itself by Cursor's hosted agent (crew#751 redesign) or `execute`; the PR reviewed on `review` before Otto posts it |
| Crew sessions | one model per session | the same three roles; the planner writes the `Optimised:` plan (LAW 51), the reviewer grades the diff (receipt-auditor) |

Mature tool for the Hermes side, already named in `docs/THE-ARCHITECT.md:204` and not yet
installed: `oh-my-hermes` `ralplan` (Planner → Architect → Critic consensus) and `ralph`
(execute → verify → iterate). They are the procedure; the three lanes are what they call.

## Not started

No file outside this ruling changes until the founder says GO on the board (crew#568). Cost is
the risk: a reasoning planner on long Telegram sessions is the most expensive call in the estate,
against spend already at $866 a day on a $120 cap (crew#26). The executor being MiniMax is what
pays for it; the reviewer being Sonnet, not Opus, is the second saving.

## Tracked item

crew#568 (the model stack); crew#751 (Cursor as the coding executor); crew#513 (Verified Scaffold).

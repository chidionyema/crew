# DSPy and Instructor, for every agent

Ordered by the founder on 2026-08-31, in his words:

> **DSPy** — The Value: We currently spend hours tweaking "prompts" to get LLMs to do what we
> want. DSPy treats prompts like machine learning weights. You define the inputs and the desired
> outputs, and DSPy automatically compiles, tests, and optimizes the prompts for you. It turns
> brittle prompt engineering into rigorous software engineering.
>
> **Instructor** — The Value: Getting an LLM to reliably output structured data (like JSON) used
> to be a nightmare of parsing errors. Instructor patches your LLM client (OpenAI, Anthropic,
> etc.) to guarantee that the output matches a predefined Python data structure (using Pydantic).
> It is the single most valuable tool for extracting exact data points from messy text.

## What is installed, and where

Both packages are pinned in `requirements-dev.txt`, which `scripts/install-crew` installs into
the shared agent environment. Proved live on 2026-08-31: Instructor extracted a typed record and
DSPy answered a prediction, both through the estate model router on the `groq-fast` lane.

## How any agent uses them

Everything goes through the estate model router — never a vendor address, never a vendor key.

- `ROUTER_URL` — the router address. If unset, it is `https://llm.` followed by the estate zone
  (the zone lives in the cluster configuration, never in code).
- `ROUTER_KEY` (or a file named by `ROUTER_KEY_FILE`) — the one router credential. Its value is
  never printed and never pasted anywhere.
- Model names are router lanes (for example `groq-fast`, `minimax`, `deepseek`), listed in the
  platform's model routing configuration.

Run the proof yourself:

    .venv/bin/python scripts/dspy-instructor-smoke.py

It prints one `MEASURED_OK` line per tool, or a refusal naming exactly what is missing.

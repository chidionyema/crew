# Every pull request declares what it locked us into

## What it is for

To stop the estate quietly becoming un-leaveable one line at a time. Nobody ever decides to lock a
company into a vendor. It happens through fifty small choices, each of them reasonable on its own
day, and the bill arrives years later as a rewrite.

This gate does not refuse a dependency. Taking one is often the right call, and LAW 19 already
covers living with one once it is taken. It refuses the **silent** one: a vendor name written into
a code path where nobody wrote down what replaces it. The cost of an exit is set on the day the
dependency goes in, and it never gets cheaper afterwards.

It is the pull-request half of LAW 34. The session half already works: the laws are symlinked into
`~/.claude`, `~/.codex` and `~/.gemini`, so every agent on every provider reads all thirty-four
rules at startup. Nothing on the pull request enforced it until now.

## What it costs

Nothing to run — it reads text already in the pull request body and a diff `check` already fetches.
Most pull requests never see it. Measured on the last 40 real commits in this repo: **0 would have
been asked for anything.** It only speaks when a diff adds a vendor name.

## What it watches

Added lines only, in code files. Four kinds of coupling, chosen to be narrow rather than thorough,
because a pattern that fires on innocent code teaches agents to route around the gate:

| kind | what it catches |
|---|---|
| model id | `claude-opus-5`, `gpt-4`, `gemini-pro`, `grok-3`, `llama-3` |
| api endpoint | `api.anthropic.com`, `api.openai.com`, `generativelanguage.googleapis.com` |
| vendor sdk | `import anthropic`, `from openai`, `google.generativeai` |
| transcript layout | `.claude/projects`, `.codex/sessions`, `.gemini/tmp` |

Deleted lines never count. Removing `import anthropic` is the opposite of taking a dependency, and
counting it would make removing lock-in harder than adding it.

Markdown, `docs/` and fixtures are exempt, and so is `pr-evidence.py` itself — its own source is a
list of vendor names, so without that carve-out the first pull request this gate refuses is the one
that adds it. That was measured, not predicted: the gate flagged itself six times before the
exemption existed.

**Claude is in the table.** Founder, 2026-08-23: "and you need to include claude". A law about
provider independence that exempts the provider currently in use is a preference, not a law.

## What to write, when it asks

```
## Provider coupling
The daily summary calls claude-opus-5 directly.
- Swap: any chat model behind providers.chat, about an hour to move
```

A heading, a sentence saying what is coupled, and a `Swap:` line naming the replacement and roughly
how long it takes. Naming a dependency without naming its replacement is a description, not an exit,
so the `Swap:` line is the part that is actually required.

## Where it lives

`~/dev/code/crew/scripts/pr-evidence.py` — `provider_coupling()` and `coupling_markers()`, called
from `check`. Fifteen paired-control selftests run with:

```
python3 scripts/pr-evidence.py selftest-options
```

## How to turn it off

```
git revert <the commit that added provider_coupling>
```

No flag, deliberately. A gate with an off switch is a gate that is off, and a rule agents remember
is a rule agents forget.

## How to turn it back on

Nothing to do. It runs whenever `check` runs.

## What goes wrong

It can cite a comment rather than the code line that does the coupling — the hit in
`ticket-gate.py` is the comment above the code, not the code. The file-level verdict is still
correct, so this is left alone on purpose: skipping comments would have made `ticket-gate.py` pass
while it genuinely reads one vendor's transcript directory, and a false pass is worse than an
imprecise citation.

If the diff cannot be fetched, `check` fails rather than passing quietly. A gate that goes silent
on its own failure reads as coverage it does not have.

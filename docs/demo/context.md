# Demo — the context layer stack loads

What you see when a Claude Code session starts inside the crew checkout after this lands
and the import flip follows.

Command:

    claude
    /context

Real output (the memory section of /context):

    Memory files
    · user (~/.claude/CLAUDE.md)         -> imports @~/dev/code/crew/AGENTS.md
    · project (CLAUDE.md)                -> imports @AGENTS.md

Both lines resolve to the same universal AGENTS.md at this repo's root, so the rules load
deterministically — no session decides whether to read them. Other frameworks (Cursor,
Codex) read `AGENTS.md` at the root natively and need no import.

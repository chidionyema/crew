# Onboarding — the context layer stack

**What it is for.** One layered answer to "what rules does a session load": `AGENTS.md`
(how work happens, universal) at this repo's root, `CLAUDE.md` (one line, imports it, because
Claude Code reads only CLAUDE.md), and `depts/CHARTER-TEMPLATE.md` (the 400-word template a
department charter is poured into). Higher layer wins on conflict; the template says so.

**What it costs.** Nothing at runtime — three static files, under 20 KB, read once at
session start.

**Where it lives.** Repo root (`AGENTS.md`, `CLAUDE.md`) and `depts/`. The founder's design
record is the captured document named in the pull request.

**How to stop it.** Delete `CLAUDE.md` and Claude Code stops loading the repo layer; other
frameworks stop when `AGENTS.md` is removed. The universal layer's old home under `~/.claude`
is deleted only at crew#760 step 6.

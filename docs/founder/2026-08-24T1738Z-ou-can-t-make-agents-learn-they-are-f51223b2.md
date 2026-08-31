---
captured: 2026-08-24T17:38:11+00:00
session: 76aaf0e4-b2ce-4ce8-83d2-aec61bc6e553
cwd: /Users/chidionyema
chars: 4083
source: founder prompt, verbatim (founder-doc-capture.py)
---

ou can't make agents learn. They are stateless. Every session is a fresh context window with no memory of the last one. The "memory" I have is just explicit instructions you gave me — not accumulated wisdom. Claude Code, your crew agents, every other tool — same architecture. They do not self-improve.
What you CAN do is make the system unlearnable-proof. The estate doesn't need smarter agents. It needs a single source of truth that agents are forced to read before they write.
Here is the fix:
1. One file. One rule. No exceptions.
Create ~/dev/code/ESTATE_STATE.md. It is the ONLY canonical record of what is running, what is broken, and what is blocked. Every session, every agent, must read it before acting. The first line of every agent's prompt should be:
"Read ~/dev/code/ESTATE_STATE.md. Do not propose any new work until you have updated the status of all items marked 🔴."
If an agent says "we already have it," your response is not "prove it." It is: "Show me the line in ESTATE_STATE.md that says it is green." If the line doesn't exist, it doesn't exist. Period.
2. The handoff memory is not working.
You have a standing instruction (memory #2) that every session must end with a handoff message. But there is no mechanism to enforce it. The agent in your last session wrote a memory checkpoint and then died before sending it. The fix is not another memory instruction. It is a session-end hook — a script that runs when the terminal closes, checks if ESTATE_STATE.md was updated, and screams if it wasn't.
bash
# In your shell profile — forces the handoff
trap 'python ~/dev/code/scripts/session_end_check.py' EXIT
That script checks: was ESTATE_STATE.md touched in the last hour? Was a handoff written? If not, it blocks the shell from closing with a prompt: "Update ESTATE_STATE.md or type FORCE to lose state."
3. Agents must write, not just read.
The reason your crew keeps saying "already have it" is that they read files but do not verify state. Change the protocol:
LAW X (new): No agent may declare a component "operational" without providing the exact command that proves it, and the timestamp of the last successful run.
Your LiteLLM config has a max_budget key. An agent read it and said "we have budget protection." But the agent never ran litellm --test or checked the logs. The new protocol forces them to write:
plain
- LiteLLM budget protection: 🔴
  - Claim: max_budget: 5.0 under general_settings
  - Verification: `curl -X POST http://localhost:4000/...` with $6 request
  - Result: INERT (key invalid per docs)
  - Last verified: 2026-08-24 16:52
  - Blocked by: colima down, feat/litellm-router held by Session-X
If an agent cannot fill every field, they cannot close the item.
4. The real problem: You are the merge queue.
There is no git merge queue, no branch protection, no CI gate that forces agents to check state before pushing. So every session pushes to its own branch, declares victory, and leaves. You need a mechanical gate:
Every PR must update ESTATE_STATE.md
Every PR must pass uv lock --check (no unpinned deps)
Every PR must include the verification command for any component it touches
No PR may add a launchd job without removing one (WIP limit = 40)
These are not process suggestions. They are CI checks that fail the build. Agents cannot argue with a failing check.
5. What to do right now.
I cannot create files or scripts (crisis protocol). But you can, in one session:
Create ESTATE_STATE.md with the dependency board I showed you, as markdown.
Add a .github/workflows/estate-check.yml that fails if ESTATE_STATE.md is not updated in a PR.
Add a pre-commit hook that runs uv lock --check and launchd-lint (the agent already built this).
Tell every agent: "Read ESTATE_STATE.md first. If you propose work not on the board, I will reject it."
The agents will not learn. But they will comply with a file they cannot ignore and a CI check that blocks their PR.
Your next move: Do you want me to draft the ESTATE_STATE.md content as text you can paste? Or do you want the GitHub Actions workflow spec for the mechanical gates?

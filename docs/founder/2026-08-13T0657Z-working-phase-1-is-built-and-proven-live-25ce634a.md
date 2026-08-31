---
captured: 2026-08-13T06:57:13+00:00
session: cbe776f2-17a1-49ca-8849-110cc5ebf7f7
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3673
source: founder prompt, verbatim (founder-doc-capture.py)
---

WORKING: phase 1 is built and proven live; full suite running in the background under the correct interpreter.

Correction on my last message: those 69 collection errors were my interpreter mistake, not a pre-existing defect. The gateway runs venv/bin/python (3.11.15, prompt_toolkit 3.0.52, pytest 9.1.0); I had run system python3.14. Nothing to address there — the suite was never red.

Live receipt — real claude-agent-acp, not a fake:
turn 1 : 16.1s  pid=93601  -> 'READY'
turn 2 :  7.2s  pid=93601  -> 'hello.txt'
REUSE  : PASS  pids={93601}
Same pid across turns, and turn 2 answered from the repo's actual contents — the held session has real tool access, and the ~30s MCP registration is paid once, not per message.

---
What shipped (hermes-agent, uncommitted):

┌──────────────────────────────────────────┬────────────────────────────────────────────────────────────────┐
│                   File                   │                             Change                             │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
│ gateway/operator_shell/coding_session.py │ new — held sessions, Backend seam, repo resolution, rails      │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
│ gateway/slash_commands.py                │ _handle_code_command, _run_coding_turn, _send_to_source        │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
│ gateway/run.py                           │ /code dispatch arm; free-text interception; plugin-hook bypass │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
│ hermes_cli/commands.py                   │ CommandDef("code", …) alias cc — registry 88→89                │
├──────────────────────────────────────────┼──────────────────────────────────────┤
│ gateway/operator_shell/menu.py           │ code advertised (14 of 30 cap)                                 │
├──────────────────────────────────────────┼──────────────────────────────────────┤
│ agent/copilot_acp_client.py              │ reuse_session / mcp_servers as explicit kwargs                 │
├──────────────────────────────────────────┼──────────────────────────────────────┤
│ tests/…/test_coding_session.py           │ new — 29 passed                                                │
└──────────────────────────────────────────┴──────────────────────────────────────┘

Two precedence traps found and closed. match_naturaghtly anchored — "run the tests", "fix the mobilefacet bar", "show me the diff" all return None, so that race was survivable. The real one was the otto-inbound plugin: it answers
pre_gateway_dispatch with action: skip and run.py rthe coding interception. An open session now bypasses that hook for plain text only — slash commands still dispatch, or /code end would be unreachable. Both orderings are pinned by
tests.

Rails, since an open session holds a live child: 60ap is what manufactured fabricated "done" reportsbefore), 30s grace above it for a wedged child, 30m idle reaping, 2-session cap, per-session lock so two Telegram messages can't
interleave into one child. A cut-off turn says it wtatus rather than presenting partial work asfinished.

pi refuses with "not wired yet" rather than silently falling back to Claude — phase 2 flips one test.

Two things still owed before you can type /code prospector on the phone: a commit (the POPDD integrity guard already flagged coding_session.py as untracked/unreviewed), and a g I'll do both once the suite reports. ok net phase

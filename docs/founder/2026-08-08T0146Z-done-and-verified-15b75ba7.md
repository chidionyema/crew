---
captured: 2026-08-08T01:46:39+00:00
session: 245221b7-b308-462b-8e1d-5fa399817b21
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2896
source: founder prompt, verbatim (founder-doc-capture.py)
---

Done and verified

- P0 is complete and green — but a concurrent session had already implemented it. I found it staged and verified rather than redoing it: menu is 14 entries with both agent_model and model, the hardcoded 12 in telegram_menu_commands is now min(max_commands, MAX_COMMANDS_PER_SCOPE), and both tests assert the new contract instead of going vacuous. 16 passed and 8 passed.
- Fixed a false comment in menu.py that claimed the agent panel renders a role table. It renders a model+provider chip grid; switches is four hardcoded toggles. That is the programme's own defect class appearing inside the programme's own P0, so I corrected it in place with the correction visible rather than quietly deleting it.
- Spec updated with two findings that change the remaining work, plus 12 ledger rows.

Two findings worth more than the code I wrote

1. P2 is far cheaper than specced. web_server.py:3159-3171 already serves a per-role model picker via /api/model/options + /api/model/set, shape-matched to the TUI's JSON-RPC. The capability the founder asked for exists, on the web dashboard he doesn't use from a phone. P2 becomes a third renderer, and this is the strongest argument yet for doing P4 rather than three bespoke doors.
2. A blocker: the role count is 11 or 13. _AUX_TASK_SLOTS has 11; the spec says 13. tts_audio_tags and monitor are in no renderer anywhere. P2 can't render a count until that's settled.

Not done: six phases — P1, P2+L3, L1, L2, P3, P4. That's the bulk of the programme. Two honest reasons: I'm past the resident-context threshold where each turn costs multiples of the floor, and this is a multi-session build in an unfamiliar submodule with a live gateway and a concurrent session editing the same tree. Starting P1 here would produce exactly the asserted-not-proven work the spec exists to prevent. Tasks #1–#8 carry the full context, with #2 blocked on #7 and #3 blocked on #2.

Two things needing you:
- P0 is not live. The menu push is startup-only and the gateway is pid 96348. A restart drops your Telegram session, so I didn't do it unasked — that's task #8.
- Nothing is committed. The ~/.hermes autosync will bare-commit the spec within the hour; the hermes-agent changes are MM on top of a concurrent session's staged work.

Handoff written to checkpoints/2026-08-08-operator-ux-programme.md, with a pointer inserted into LATEST.md rather than overwriting it — it held another session's in-flight PR 134 merge.

Safe point — type /clear (state saved, nothing will be lost).

✻ Churned for 8m 3s

  8 tasks (0 done, 8 open)
  ◻ P1 — Persistent reply keyboard as the primary Telegram door
  ◻ L2 — Six plain-text alert sites carry inline actions
  ◻ P3 — Inventory gate and reachability budget
  ◻ P4 — One intent tree, three renderers
  ◻ Resolve the 11-vs-13 auxiliary role discrepancy
   … +3 pending need to do all quickly and  prove it works

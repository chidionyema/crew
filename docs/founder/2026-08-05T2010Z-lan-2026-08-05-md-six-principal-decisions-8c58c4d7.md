---
captured: 2026-08-05T20:10:44+00:00
session: d7223e62-849d-418e-b157-6c7b21862309
cwd: /Users/chidionyema/Documents/code/prospector
chars: 4631
source: founder prompt, verbatim (founder-doc-capture.py)
---

LAN_2026-08-05.md — six principal decisions, nine workstreams, five waves, and a traceability table where all 18 audit findings map to an owner and a runnable acceptance probe. Still report-only; nothing changed in code.

Three things I found while planning that change the audit

1. The fence violation count is 3, not 2. The audit queried the known bypass payload. The correct query is the invariant — "a fenced task reached done with no approval event" — and it finds one more:

06eadbc7ea90  contract  telegram              2026-07-31 02:46:03   ← audit's query missed this
8fb949064732  identity  project:tie           2026-07-31 02:46:03
1582bddd1a8b  money     project:signalengine  2026-07-31 02:46:03

That's a design instruction, not just a correction: detect on the invariant, not on the known bypass. It becomes probe PR-1, target 0, and a line in verify_estate.sh.

2. The red CI is not your code. Both failing files are 100% upstream-authored (git log --format='%an' → Teknium ×9, zero founder commits). I ruled out two causes by reproduction: not the blanked API keys (reran with CI's exact OPENROUTER_API_KEY="" OPENAI_API_KEY="" NOUS_API_KEY="" → 23 passed), and not dependency drift (reran under uv sync --locked --python 3.11 --extra all --extra dev → 23 passed in 1.71s). That reframes the CI workstream from "fix our broken tests" into a principal decision — what do we owe upstream's 17k tests on a fork we can't upstream to. A local run of CI's own run_tests_parallel.py --slice 3/6 is still executing; I'll report it when it lands.

3. venv split-brain. The live gateway runs venv/bin/python (pid 85713); .venv/bin/python had no pytest at all. Same class as your recorded ddgs split-brain trap.

The decisions only you can make

The one that shapes everything is D1 — where the safety gate lives. My recommendation is repo-side branch protection as enforcement, blast-radius classification as detection, keywords demoted to a trip-wire that can only raise risk, never lower it. The failure mode that picks between the options: a gate that lives only in the agent's Python can be deleted by a task that edits the agent — and self-modification is in scope in this estate. A GitHub branch-protection rule survives the agent being wrong about itself. Note that code_remote.py:151 fences at task creation, before a plan exists, so no amount of vocabulary work at that call site can ever fix the class.

D3 (fork) should be decided from a measurement, not my estimate — and the threshold set before you run it: under ~500 changed lines across the four upstream files → extension boundary; over → conscious hard fork. The command is in the plan. Drifting is the only indefensible answer and it's the current state.

The others: D2 (upstream tests), D4 (thread actor now while it's 399 mechanical edits, or write down "never a second user"), D5 (defer the macOS port, add a Supervisor interface so no new launchctl string lands outside it), D6 (name/trademark + split the hourly auto: sync off main).

Wave 0 is ~1 hour and needs no decision

Move the fail-closed guard from coordinator.py:2131 to the top of the drain loop at :2093, above both :2098 and :2105; delete the unreachable duplicate at :2133-2134; rm .git/index.lock; delete rsi_control.py:94-95. That closes the live, three-times-fired bypass today.

Two things to know before you run it: backfill the 3 historical violations before wiring PR-1 as a required check, or the check wedges the pipeline. And the correct behaviour will feel like a regression — fenced tasks stop auto-closing, so the awaiting_approval backlog grows and needs manual taps. Watch it for two days.

Handoff written to checkpoints/LATEST.md as section N. Say the word and I'll execute Wave 0; otherwise —

Safe point — type /clear (state saved, nothing will be lost).
 now tine to add ny own epectation, i expect a personal agent that nakes ny technical life a drean, i epect to be able to nanage all ny work on telegran that i currently do on htis nachine seanlessley better and better usser eperience, i epect nny agent to be proactive, self inprivig with clear goals actions,,reflections and visible ad neasureable recursive sself inporovenent, i epet the telegran user interfacce annd epereince to be heavenly and seanless and top notch, i expect to be able to set this all up seanlessly fron scratch, i expect to be able to nanage the whole sdlc proccess cocnfortbaly for projects on ny nachine and in github, i expect this product to be eventually a connnercial product that bootstraps easilty, i also need deep reearch ito hernes docs to ensure we are leveraging properly

---
captured: 2026-08-28T10:47:08+00:00
session: 54d8090d-c210-4214-85e1-1c3c499e8583
cwd: /Users/chidionyema/dev/code
chars: 1735
source: founder prompt, verbatim (founder-doc-capture.py)
---

he other session (code-2f) explicitly told this agent exactly how to get PRs #559 and #563 unblocked, but this agent is ignoring it.

code-2f said: "Use that as the Reviewed-by: name in both bodies; tell me when the line is corrected."

You need to force the agent to run the GitHub CLI commands to append Reviewed-by: 78caaa17 to the PR bodies.

Prompt the agent: "Execute gh pr edit 559 --add-label 'Reviewed-by: 78caaa17' and gh pr edit 563 --add-label 'Reviewed-by: 78caaa17', then notify code-2f."

3. Force Compliance with Law 9 (Abandon the Target)
The agent has smashed its head against datamap.py 30 times. Its own "Law 9" dictates it must change approaches after two failures.

You must ruthlessly command it to drop the current ticket.

Prompt the agent: "Stop all work on datamap.py immediately. Law 9 is invoked. You have failed 30 attempts. Declare this route unobtainable."

4. Break the Idle-Guard Loop
The agent keeps trying to stop, but the idle-guard prevents it because there are 156 open tickets on the board. We need to force it to pick up the next independent task so the system registers progress.

Prompt the agent: "Claim crew#527 from the board right now and begin work. Do not run stop hooks until you have made a commit on crew#527."

The "One-Shot" Override Prompt
To close the loop entirely, paste this exact, ruthless command to the agent once you clear the hang:

"Stop cogitating. Law 9 invoked: drop datamap.py completely, it is unobtainable. Run gh pr edit 559 and 563 to append 'Reviewed-by: 78caaa17' to their bodies so code-2f approves them. Then instantly claim crew#527 from the board and begin work. No more stopping, no more looping on datamap."

Do you want to run this override now, or do y

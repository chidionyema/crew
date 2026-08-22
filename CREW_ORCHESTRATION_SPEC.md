# THE CREW: Conversation → Delivery
## Natural chat becomes tracked, verified builds
### 2026-08-22 | GitHub Issues + BDD

---

## 1. The pattern

```
YOU (casual chat):
  "I need to not lose sleep. My app is on Fly. I want failover to another
   provider. And I want to cold start from my phone. And no bash scripts."

PM AGENT (listens, distills):
  "Got it. Writing the spec and the work items."
        ↓
  Opens GitHub Issue #N: "Build: multi-provider survival stack"
  Body: checklist CP1–CP5, extracted from the conversation
        ↓
ENGINEERING AGENT (picks up the issue):
  Builds CP1 … CP5. Posts evidence to the issue after each one.
        ↓
QA AGENT (verifies independently):
  Runs behave. Ticks the box only on a real green run.
        ↓
YOU (phone buzzes):
  "CP2 VERIFIED. 3 scenarios passed."
        ↓
  Later: every box ticked, issue closed.
```

You never write a spec document. You never check status. The GitHub app buzzes
your phone. You only reply when something is wrong.

---

## 2. The roles

| Role | Agent | Surface | Job |
|------|-------|---------|-----|
| **PM / scribe** | `pm-agent` | Your laptop chat | Listens, writes the spec, opens the issue, writes the feature files |
| **Engineer** | `engineering` | Laptop + issue | Builds, runs the suite, posts evidence |
| **QA / verifier** | `qa-agent` | Laptop | Runs `behave` independently, ticks or blocks |
| **Ops** | `operations` | Laptop | Degraded mode, shadow tests, failure injection |
| **Hermes** | `hermes` | Your phone (Telegram) | Same crew, different surface. Reads the same issue |

---

## 3. The GitHub issue is the shared brain

Every agent reads and writes one issue, through one tool (`crew`), in one shape.

```markdown
## Origin
Distilled from conversation with @founder on 2026-08-22.
Spec: `docs/specs/issue-44.md`

## Checklist

- [ ] CP1: Worker and Telegram bot responding
- [ ] CP2: Primary and standby healthy, auto-failover works
- [ ] CP3: Cold start from the phone, with the data
- [ ] CP4: Degraded mode queues orders and recovers
- [ ] CP5: Exit drill runs, the data comes back

## Verification Log

| CP | BDD | Evidence | When |
|----|-----|----------|------|

## Blockers

None.

## Crew Thread

Every agent posts here.
```

Nothing patches that body with a regex. `crew` parses it into a value, changes
the value, and renders the whole body back. A property test proves the round
trip, because a lossy write means one agent deleting another's state.

---

## 4. The gate: an agent cannot mark its own homework

Three mechanical refusals, not three conventions:

1. **`crew evidence` never ticks a box.** It posts a build report. That is all
   engineering can do.
2. **`crew verify` refuses when the caller posted the evidence.** The role that
   built it is not the role that passes it.
3. **Zero scenarios is a FAIL.** `behave` exits 0 when a tag matches nothing.
   A tick from an empty run is the worst outcome available, so the runner counts
   scenarios and refuses to call it a pass.

A tick on the checklist therefore means: a suite ran, at this commit, on this
machine, and at least one scenario passed.

---

## 5. BDD: the executable Monday test

Your sentence becomes the scenario.

```gherkin
@cp2
Feature: Auto-failover
  As a solo founder
  I want the standby to take over without me
  So that I sleep through an outage

  Scenario: the primary dies and the edge keeps serving
    Given the lab is up
    And a primary box is registered and healthy
    And a standby box is registered and healthy
    When the primary box is destroyed
    Then the control plane serves the standby within 60 seconds
```

The PM agent writes these from your words. The QA agent runs them. The tag
`@cp2` is the link between the checkbox and the test.

---

## 6. Hermes is a surface, not a second system

| Surface | What you see | What the crew sees |
|---|---|---|
| Laptop chat | You talk to `pm-agent` | `pm-agent` opens the issue |
| GitHub app | Notifications on your phone | Engineering posts evidence |
| Telegram (Hermes) | `/status` | Hermes runs `crew status --format telegram` on the same issue |

Hermes reads the board and posts requests into the thread. It never verifies —
verification runs where the repository and the lab are.

---

## 7. The command surface

```
crew init                       configure a repo (writes .crew.json)
crew plan brief.md              pm-agent: spec + issue + checklist
crew use N                      set the active issue
crew status [--format json|telegram]
crew claim CP2                  engineering: starting this one
crew evidence CP2 --result pass --summary "…" --log run.log
crew verify CP2                 qa-agent: run the suite, tick or block
crew block "CP2: standby 502"   put it on the board
crew comment "…"                post to the crew thread
crew close                      only when every box is ticked
crew doctor                     prove the wiring, before you trust any of it
```

---

## 8. What you prompt, once

```
I need a survival stack for my app. Auto-failover between providers, cold start
from my phone, no bash scripts, stack agnostic, TOTP on everything, about £15/mo.

pm-agent: open the issue and write the features.
engineering: build per spec, post evidence per checkpoint.
qa-agent: verify each one independently.
Notify me through the GitHub app. Do not ask me questions.
```

---

## 9. The verdict

| What you wanted | What this delivers |
|---|---|
| Casual chat → deliverables | `pm-agent` distils the conversation into an issue |
| No spec documents | The spec is generated, and the issue is the live copy |
| Status without asking | GitHub pushes to your phone; Hermes answers `/status` |
| Verify without trusting the agent | QA runs the suite; three refusals stop a false tick |
| Hermes on the phone | Same issue, one skill, no second system |

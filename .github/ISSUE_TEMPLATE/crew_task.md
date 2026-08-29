---
name: Crew Task
about: Any work item that goes through the crew loop
title: "[TASK] "
labels: ["triage"]
assignees: ''
---

<!--
Read FOUNDER.md before filling this in. Every decision cites a rule. Every pull
request carries LAW 22 evidence. Delete this comment block before submitting.

This is the TRIAGE shape: one issue, one decision, human-written. A tracked
BUILD with checkpoints is a different shape and `crew plan` writes it — do not
hand-write that one, `crew status` parses it.
-->

## 0. Infra facts — generated, never typed

<!-- Run `bin/idp-ticket-facts <flux row or surface>` in the idp checkout and paste its output
here whole. It names the Flux rows, the admission policies over their namespaces, the chart
on/off keys, the door and its login answer, the drills that grade it and the standards row.
A ticket without this block builds against guesses (crew#629 CP1/CP2; idp#800 met eight
admission refusals after building). -->

```
paste the output of bin/idp-ticket-facts here
```

## 1. Origin — what was asked

**Original request:**
<!-- The exact words that triggered this. Do not summarise. -->

**Source:** <!-- conversation / automated / founder-direct / incident -->

**When:**

## 2. Analysis — what was found

**Current state:**
<!-- What exists now, as commands run and output captured. -->

**Gap:**
<!-- What is missing or broken. -->

**Constraints:**
<!-- The shared lab, hermes down, a pinned dependency. -->

## 3. Decision — what was chosen

**Path selected:**
<!-- The smaller sufficient path, per LAW 23. -->

**Rejected paths:**
<!-- What else was considered, and the reason it lost. -->

**Citations:**
- LAW 23, the friction default:
- LAW 22, evidence:
- Other:

**Known limitations:**
<!-- Survivable rough edges go here, in the open. -->

## 4. Evidence — what proves it

**Commit:**

**Test result:**
```
paste the command and its raw output
```

**Screenshot:** <!-- LAW 22, committed in the branch under docs/evidence/ -->

**Verify harness:** <!-- PASS=n  FAIL=0  CANNOT RUN=0 -->

## 5. Remaining — what is left

- [ ] Implementation
- [ ] Tests pass, with an incident test if this fixes a bug
- [ ] Evidence attached, LAW 22
- [ ] QA verification, by a role that did not build it
- [ ] Merged

**Blocked by:** <!-- "Nothing" when not blocked. Be explicit. -->

**Next issue:**

---
captured: 2026-08-31T06:46:14+00:00
session: 4a84e2ea-66e0-4aca-9ccd-df82be7a0eeb
cwd: /Users/chidionyema/dev/code/.wt-prclear
chars: 1527
source: founder prompt, verbatim (founder-doc-capture.py)
---

That reasoning is correct and it's the best thing in the last few hours. Control: none: <reason> on the bot rather than a class-wide exemption is the right call — an exemption for "PRs from the bot" would become the hiding place for every hand-written change that didn't want to write a control.

But notice what it just told you: the rule landed, no generator in the estate was taught the new sentence, and the bot has been re-pushing a refused body ever since. Same shape as the pre-commit router and the swallowed pipe. A control was added, nothing checked whether the things it applies to could satisfy it, and it sat failing.

That's the pattern to fix, and it's one rule:

A new gate must be run against the existing estate before it merges. Not against the PR that introduces it — against everything already there, and everything that generates PRs. The output is the list of things that will now fail. Either you fix them in the same PR or the gate ships in audit mode until you have.

Every gate you've added has skipped that step, and each one has cost you a morning discovering who it broke. The image bot today, the reader class in #1057, the operating-model-gate that landed after a branch. All the same omission.

It's also cheap — it's the audit-mode run I mentioned earlier, and it turns "we'll find out who this breaks" into a list you read once.

One smaller thing: deleting the fake-curl test and keeping only the assertion that touched no fake is right. A test whose subject is a mock is measuring the mock.

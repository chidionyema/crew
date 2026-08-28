# Onboarding — the corrective action register

Owner: the data science lane (crew#105)
Last true: 2026-08-24

## What this is for

You said it on 2026-08-24: *"we dotjustneed lways we need prootccols that all agebnt
folow"*, and *"in tired of repearting instructino that are fucking autibantabkle and
enforcable yet dday by fucjig day"*.

Both halves of that are correct and the second half explains the first. The estate has
forty-two laws. What it has never had is anything that goes back afterwards and checks
whether a law actually stopped you having to say the thing. So laws accumulate, each one
feels like progress on the day it is written, and the number of times you repeat yourself
does not move. That is not a discipline problem. It is a missing step in the loop.

## Where the missing step comes from

It is not invented here. 21 CFR 820.100 is the corrective and preventive action
requirement that regulated manufacturers are audited against, and it asks for exactly the
two things we were missing:

> **(a)(1)** Analyzing processes, work operations, concessions, quality audit reports,
> quality records, service records, **complaints**, returned product, and other sources of
> quality data to identify existing and potential causes of nonconforming product … using
> appropriate statistical methodology

> **(a)(4)** **Verifying or validating the corrective and preventive action to ensure that
> such action is effective** and does not adversely affect the finished device

Read against this estate: your complaints are the quality data. A law is a corrective
action. `(a)(4)` is the step nobody has ever taken.

The Google SRE postmortem chapter, which is the usual place an engineer would look, does
not solve this. It says postmortems should carry "the follow-up actions to prevent the
incident from recurring" and then names nobody to track them and no way to tell whether
they worked. The regulated answer is the stronger one and it is the one we took.

## What a record is

One GitHub issue on `chidionyema/crew`, labelled `capa`. Not a file on this laptop.
You ordered on 2026-08-24 that the board is issues and that nothing gets reinvented
badly, so the register is issues, readable from your phone, with no new store behind it.

The body carries an HTML comment that the machine reads:

```
<!-- capa
complaint: "your words, verbatim, not a paraphrase"
first_said: 2026-08-21
phrase: reinvet the wheel
action: what was actually done, and where it lives
landed: 2026-08-21
-->
```

`phrase` is what the check searches your transcripts for. `landed` is the date the action
took effect, and the check only looks at what you said after it.

## What it costs

Nothing that bills. It calls no model. It runs `gh` to read the register and then reads
the transcript files already on this disk. The transcripts are 4.4 GB, so a full pass
takes minutes rather than seconds; that is why it is a command you run rather than a hook
on every prompt.

## What the verdicts mean

**REPEATED** — you said it again after the action landed. The action did not hold.

**NO RECURRENCE** — you have not said it in those words for at least seven days.

**TOO SOON** — quiet, but not for long enough to mean anything yet.

**MALFORMED** — the issue carries the label and nothing a machine can check. That is a
corrective action with no effectiveness check, which is the thing this exists to stop.

It is deliberately never called EFFECTIVE. The check matches your exact phrasing, and you
type fast and do not go back to fix typos, so the same complaint spelled a second way
reads to it as silence. Every number it prints therefore under-reports the repetition, and
the real figure is worse than the one on screen. That is the safe direction for a number
that accuses, but you should know the bias is there.

## What is enforced, and what deliberately is not

Enforced: **a record cannot be closed while the complaint is still recurring.**
`capa.py --check` exits 1 on that, and only on that, plus on records nobody can check.

Not enforced: a record that is open and recurring does not fail anything. That is a live
problem for someone to fix, not a reason to block an unrelated pull request. A guard that
refuses correct work gets switched off inside a day, and then nothing is enforced at all.

## How to run it

```
python3 ~/dev/code/crew/science/capa.py           # the register and every verdict
python3 ~/dev/code/crew/science/capa.py --check   # exit 1 if a record was closed too early
python3 ~/dev/code/crew/science/capa.py --post    # write each verdict onto its issue
```

## How to turn it off

Delete the `capa` label, or close the issues. Nothing is scheduled yet, so there is no
daemon to stop. Removing `science/capa.py` removes the checker and leaves the issues,
which then become ordinary issues that nobody verifies — which is where we were before.

## What goes wrong

**A phrase that is too common.** `phrase: research` would match half of what you say and
report a repeat every day. Pick the distinctive words of the complaint, not its subject.

**A phrase that is too rare.** The opposite failure and the more dangerous one, because it
reports NO RECURRENCE while you are still saying the thing weekly in different words. When
a record reads quiet and you know it is not, the phrase is the thing to change.

**The register is empty.** That reads as a clean estate and is not one. It means no
complaint has ever been turned into a tracked action, which is where this started.
`capa.py` says so in those words rather than printing nothing.

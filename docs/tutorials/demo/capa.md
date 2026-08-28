# Demo — science/capa.py

Owner: the data science lane (crew#105)
Last true: 2026-08-24

What it does: takes a complaint the founder made, the law that was written to fix it, and
goes back to the transcripts to ask whether he has said it again since. The estate has
never once performed that check.

## The register, before anything was filed

    $ python3 science/capa.py --check

    no CAPA records on chidionyema/crew labelled `capa`.
    An empty register is not a clean estate. It means no complaint has ever been turned
    into a tracked corrective action with a check on it.

That is the finding, and it is why this was built.

## The first record, and its verdict

Filed as crew#103. The complaint is *"never reinvet the wheel and do worse job"*. The
corrective action already existed: THE FOUR HARD RULES, rule 3, in `~/AGENTS.md`, written
2026-08-21. Nobody had ever asked whether it worked.

    $ python3 science/capa.py

    register : chidionyema/crew, label `capa`, 1 record(s)
    a record is believed quiet only after 7 days

      REPEATED       #103  CAPA: pre-work lookup landed 2026-08-21 and he repeated the
                     his words : "never reinvet the wheel and do worse job"
                     action    : THE FOUR HARD RULES rule 3, ~/AGENTS.md
                     landed    : 2026-08-21  (3.1 days ago)
                     he said it again 1x since:
                       2026-08-24 03:23  session ema-dev-code  "what are we doing about fouder conplaint and frutartis ll command ❯ never reinve"

    REPEATED after a fix : 1
    no recurrence yet    : 0
    too soon to say      : 0
    unmeasurable         : 0

Nobody told it about the 03:23 message. It found the repeat by reading the corpus, matched
it to a law written three days earlier, and returned the verdict on its own. A law that has
been in force for three days, and the complaint it was written for came back anyway.

## It writes the verdict where he will see it

    $ python3 science/capa.py --post
    $ gh issue view 103 --repo chidionyema/crew --json comments -q '.comments[-1].body'

    **Effectiveness check — REPEATED**

    Action `THE FOUR HARD RULES rule 3, ~/AGENTS.md` landed 2026-08-21, 3.1 days ago.
    He has said it again 1 time(s) since:
    - `2026-08-24 03:23` session ema-dev-code — what are we doing about fouder conplaint and frutartis ll command ❯ never reinvet the wheel and do worse job ❯ also not seein evidence of autonouse online research without ne asking ❯ in tired of repe

    The corrective action did not hold. This record does not close.

## The gate, watched in both directions

A gate nobody has watched refuse is a gate nobody has tested. A gate nobody has watched
*accept* is worse, because the first time it refuses correct work it gets switched off.

**It says yes while the record is open and recurring.** That is a live problem for someone
to fix, not a reason to fail an unrelated pull request.

    $ python3 science/capa.py --check
    rc=0

**It says no the moment the record is closed while the complaint is still recurring.**

    $ gh issue close 103 --repo chidionyema/crew
    $ python3 science/capa.py --check

    CLOSED WHILE STILL RECURRING: #103
    A corrective action is closed when the complaint stops, not when somebody decides it
    is finished (21 CFR 820.100(a)(4)).
    rc=1

**And back.**

    $ gh issue reopen 103 --repo chidionyema/crew
    $ python3 science/capa.py --check
    rc=0

That is the whole enforcement surface. One move is refused: declaring a thing fixed while
the person who complained is still complaining.

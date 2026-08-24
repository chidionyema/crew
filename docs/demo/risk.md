# Demo — the risk register

Eleven risks, each one a JSON row with a command attached. Captured 2026-08-24
from a real run.

## What is in it

```
$ jq -r '"\(.id)  \(.status)\t\(.title)"' risk/REGISTER.jsonl
R1  open	Every agent on this estate runs on one provider
R2  open	Five exits have never been drilled once
R3  open	17 of 23 repositories carry no licence file
R4  open	Work is recorded in 73 ledgers that do not join
R5  open	Uncommitted work exists only on this Mac
R6  open	The estate runs on one machine
R7  open	16 of 43 scheduled jobs report a non-clean exit and nobody has triaged which matter
R8  mitigated	There is no buyer-facing surface
R9  open	One database exists in two places with no stated authority
R10  open	~/dev/code is itself a git repository with no remote, and no inventory row
R11  open	Licence detection is implemented twice and can disagree with itself
```

These are not comfortable, and that is the point. A register that lists only
risks somebody has already handled is a marketing page.

## Every row carries the command that proves it

The difference between a risk register and a worry list is the `evidence`
field. It is a command, so a stranger can check the claim without believing
anybody.

```
$ jq -r 'select(.id=="R1") | .evidence' risk/REGISTER.jsonl
python3 ~/.claude/scripts/drills/run.py --id no-anthropic
```

Each row also carries `residual` — what is still true after the mitigation.
R1's mitigation is a passing drill; its residual says what that drill does not
prove:

```
$ jq -r 'select(.id=="R1") | .residual' risk/REGISTER.jsonl
113 of 194 catalogued assets still carry an Anthropic-specific path, name or format. The drill proves an agent can work without Anthropic; it does not prove the estate's machinery can.
```

## The check

`scripts/verify.d/85-risk-register.sh` runs with the rest of the crew
verifiers.

```
$ bash scripts/verify.d/85-risk-register.sh; echo "exit=$?"
$ python3 - /Users/chidionyema/dev/code/crew/risk/REGISTER.jsonl
PASS: 11 risks, 1 mitigated or closed, every receipt runnable
exit=0
```

"Every receipt runnable" is the part that does work. It expands `~`, takes the
first token of each evidence command and requires it to be on PATH or to be a
real file, because a receipt nobody can run is the same as no receipt.

## Seeing it refuse

A check only ever seen passing is not a check. One row was given a receipt
pointing at a program that does not exist:

```
$ jq -c 'if .id=="R3" then .evidence="/usr/bin/definitely-not-here --count" else . end' \
    risk/REGISTER.jsonl > $SP/fake/risk/REGISTER.jsonl
$ CREW_ROOT=$SP/fake bash scripts/verify.d/85-risk-register.sh; echo "exit=$?"
$ python3 - .../fake/risk/REGISTER.jsonl
FAIL: R3 evidence starts with '/usr/bin/definitely-not-here', which is not on PATH and is not a file -- nobody can run this receipt
exit=1
```

The copy under `$SP` is a throwaway; the real register was never edited to
produce that failure.

It also refuses a register where every row is still open, because a register
that only ever grows is a list of complaints.

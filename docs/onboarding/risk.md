# Onboarding — the risk register

## What it is for

When somebody decides whether to buy this platform, invest in it, or depend on
it, the first thing they look for is what is wrong with it. If you cannot hand
them that list, they build their own, and theirs is worse: it is guessed from
what they can see, it has no mitigations attached, and every gap in it counts
against you.

So the register exists to be handed over. Eleven rows today, each naming a
thing that could hurt the estate, what it would cost, what has been done about
it, and what is still true afterwards.

It is also the honest answer to "how is the platform doing". A feature list
says what was built. This says what it is standing on.

## What it costs

Nothing to run. It is one JSONL file and one shell check that takes under a
second. The cost is discipline: a risk you find and do not write down is a risk
the register now implies does not exist, which is worse than having no
register.

## What it watches and what it changes

It changes nothing. It is a record. The check reads the file, validates the
shape of every row, and confirms each row's evidence command could be run by
somebody who has never seen this estate.

It deliberately does not execute those commands. Some of them are drills that
take minutes and touch credentials, and a verifier expensive enough to be
skipped is a verifier that does not exist.

## Where it lives

```
risk/REGISTER.jsonl                   one JSON object per line, one risk each
scripts/verify.d/85-risk-register.sh  the check, run with the other verifiers
```

Each row has: `id`, `opened`, `title`, `what_goes_wrong`, `likelihood`, `cost`,
`mitigation`, `residual`, `owner`, `evidence`, `status`, and the laws it hangs
off. `status` is one of open, mitigated, closed or accepted.

The two fields that carry the weight are `evidence` and `residual`. Evidence is
a command, so nobody has to take the row on trust. Residual is what is still
true after the mitigation, which is the field that stops a register turning
into a list of things somebody feels are handled.

## How to turn it off

```
rm scripts/verify.d/85-risk-register.sh
```

That stops the check running with the rest of the verifiers. The register file
stays where it is and is still readable. There is nothing scheduled, nothing
listening and nothing to unload.

## How to turn it back on

Restore the file from git and make it executable:

```
git checkout scripts/verify.d/85-risk-register.sh && chmod +x scripts/verify.d/85-risk-register.sh
```

## What goes wrong

**The check fails on a row you just added.** Almost always a missing field or a
`status` that is not one of the four allowed words. It names the row and the
field.

**The check fails on `evidence`.** The first word of your evidence command is
not on PATH and is not a file, and the directory it names is here. Write the
receipt as something a stranger could paste, with a full path or a program that
actually exists.

**The check passes but says a receipt was not checked.** The row names a
directory this machine does not have, so it is not the estate — a CI runner, a
fresh clone. The shape was checked and the existence was not, and the count is
printed rather than hidden, so a green run on CI cannot be read as the full
check having run.

**The check fails saying every risk is open.** That is intentional. A register
where nothing has ever moved to mitigated is a list of complaints, and it
refuses rather than reporting a clean run over it.

**The register drifts from reality.** The real failure mode, and no check
catches it. The defence is that closing a risk requires evidence, so a row
cannot be marked mitigated by anyone simply asserting it.

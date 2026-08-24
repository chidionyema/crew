# Onboarding — the risk register, checked by Open Policy Agent

## What it is for

Two reasons, and the second is the one that matters.

The first is that we were writing our own rule engine. The risk register's check
was eighty lines of Python, written here, understood only here. Every rule in it
is the kind of rule a policy engine already does: required fields, allowed
values, a claim that needs a receipt.

The second is who reads this repository. Somebody buying this platform, or
investing in it, opens the checks to see whether the standards are real. A file
called `policy/risk_register.rego` is a thing their own engineers already read.
Eighty lines of our Python is a thing they have to take on trust, and they will
not.

## What it costs

Nothing. Conftest and OPA are Apache-2.0, installed from Homebrew, run locally.
No account, no server, no network call, no free tier that expires.

OPA has been CNCF Graduated since 2021-01-29 — the foundation's top maturity
tier, the same one Kubernetes sits in. That is the sentence this whole change
buys, and it is the sentence a diligence questionnaire asks for.

One thing to know before anyone claims otherwise: conftest's own LICENSE file is
Apache-2.0, but GitHub's licence detector reports it as `NOASSERTION` because the
file carries a custom preamble. A scanner will flag it. The text itself is
Apache-2.0.

## What it watches and what it changes

It changes nothing. It reads `risk/REGISTER.jsonl` and refuses seven things:

- a row missing any required field
- two rows sharing one id
- a status that is not open, mitigated, closed or accepted
- a row claiming mitigated or closed with no evidence command
- a receipt whose first word is a path inside somebody's home directory
- an empty register
- a register where no row has ever moved off open

It does not run the evidence commands. Some are drills that take minutes and
touch credentials, and a check expensive enough to be skipped is a check that
does not exist.

## The old check is still there, and that is deliberate

`scripts/verify.d/85-risk-register.sh` has not been deleted and will not be. It
is the fallback. It runs on any machine with python3 and needs nothing else, so
the register is still checked on a box where conftest was never installed.

It also keeps one rule the policy cannot have: whether the program a receipt
names actually exists on this machine. Rego cannot read the filesystem, by
design — that is what makes it safe to run untrusted policy. So the split is
real rather than tidy: seven structural rules moved, one filesystem rule stayed.

Both run. If they ever disagree, that disagreement is the finding.

## Where it lives

```
policy/risk_register.rego              the seven rules
scripts/verify.d/86-risk-policy.sh     runs them with the other verifiers
scripts/verify.d/85-risk-register.sh   the fallback, unchanged
```

## How to turn it off

```
rm scripts/verify.d/86-risk-policy.sh
```

The register is still checked afterwards, by the fallback. Nothing else changes,
nothing is scheduled, and there is nothing to unload.

## How to turn it back on

```
git checkout scripts/verify.d/86-risk-policy.sh && chmod +x scripts/verify.d/86-risk-policy.sh
```

If conftest is missing on that machine, `brew install conftest` — or leave it,
and the check reports CANNOT RUN rather than failing.

## What goes wrong

**It says CANNOT RUN.** Conftest or jq is not installed. That is exit 2 and it
is not a failure. A check that goes red because a machine lacks a tool is
grading the machine, not the register.

**Eleven identical failures from a register that is fine.** The wrapper is
missing. Conftest splits a top-level JSON array into one document per element,
so a bare array makes `input` a single row and every whole-register rule fires
once per row. `jq -s '{risks: .}'` is what stops it. Measured here on
2026-08-24, and it is the one trap in this setup that looks like a real bug.

**A receipt is refused for being a home-directory path.** That is the rule
working. Write the receipt as a program on PATH — curl the surface, or call the
checked-in script by its repo-relative path — so a stranger can run it from
their own machine.

**The two checks disagree.** Nothing has caused this yet. If it happens, neither
is automatically right: read both messages and find which rule drifted.

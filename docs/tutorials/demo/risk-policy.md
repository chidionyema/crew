# Demo — the risk register, checked by Open Policy Agent

The register already had a check. It was eighty lines of Python written here, for
this estate, that nobody outside this estate has ever seen. This replaces the
rules inside it with a policy file that a recognised engine reads.

Captured 2026-08-24 from real runs.

## The tool, and what it costs

```
$ conftest --version
Conftest: dev
OPA: 1.19.0
```

Conftest is a subproject of Open Policy Agent. OPA is CNCF Graduated (since
2021-01-29) and Apache-2.0. Installed with `brew install conftest`. Nothing is
paid, nothing phones home, and no account exists.

## The check passing

```
$ bash scripts/verify.d/86-risk-policy.sh; echo "exit=$?"
Conftest: dev OPA: 1.19.0
$ jq -s '{risks: .}' .../risk/REGISTER.jsonl | conftest test --parser json -p policy -

7 tests, 7 passed, 0 warnings, 0 failures, 0 exceptions
exit=0
```

Seven rules, one policy file, `policy/risk_register.rego`.

## The check refusing

Three registers were broken on purpose, in a throwaway copy. The real register
was never edited to produce these.

```
$ jq -c 'if .id=="R8" then .evidence="~/dev/code/idp/bin/idp-verify" else . end' risk/REGISTER.jsonl \
    | jq -s '{risks: .}' | conftest test --parser json -p policy -; echo "exit=$?"
FAIL - - main - R8 evidence starts with "~/dev/code/idp/bin/idp-verify", a path inside one person's home directory -- nobody else can run it. Write a receipt whose first word is a program on PATH, or a repo-relative path.

7 tests, 6 passed, 0 warnings, 1 failure, 0 exceptions
exit=1
```

```
$ jq -c 'if .id=="R3" then .status="probably fine" else . end' risk/REGISTER.jsonl \
    | jq -s '{risks: .}' | conftest test --parser json -p policy -; echo "exit=$?"
FAIL - - main - R3 has status "probably fine", expected one of ["accepted", "closed", "mitigated", "open"]
exit=1
```

```
$ jq -c '.status="open"' risk/REGISTER.jsonl | jq -s '{risks: .}' \
    | conftest test --parser json -p policy -; echo "exit=$?"
FAIL - - main - all risks are still open -- a register that only grows is a list of complaints, not a register
exit=1
```

## The two checks agree

The Python check stays. It is the fallback, and it keeps the one rule a policy
engine cannot express. So the honest question is whether the two ever disagree.
Three more registers were broken and both were run over each:

```
$ for case in missing-field duplicate-id mitigated-no-evidence; do ... done
  missing-field          script=1 policy=1  AGREE
      FAIL: R5 lacks ['residual']
      FAIL - - main - R5 lacks ["residual"]
  duplicate-id           script=1 policy=1  AGREE
      FAIL: R5 appears twice
      FAIL - - main - R5 appears twice
  mitigated-no-evidence  script=1 policy=1  AGREE
      FAIL: R8 claims mitigated with no evidence command
      FAIL - - main - R8 claims mitigated with no evidence command
```

Same verdict, same row, near enough the same sentence, in both directions.

## It says CANNOT RUN, not FAIL, when the tool is missing

A check that goes red because a machine lacks a tool is grading the machine.

```
$ env PATH=/usr/bin:/bin bash scripts/verify.d/86-risk-policy.sh; echo "exit=$?"
conftest is not installed -- brew install conftest
exit=2
```

Exit 2 is the harness's CANNOT RUN. The register is still checked on that
machine, by the Python fallback, which needs nothing but python3.

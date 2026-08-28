# Demo — scripts/verify.d/15-code-standard.sh

Owner: the data science lane (crew#105)
Last true: 2026-08-24

What it does: every language this repo writes gets a checker in front of it, and the
checker runs on the diff. Founder, 2026-08-24: *"sort it out once so this class of
problems never occurs again"*.

## What the estate looked like before it

    $ git ls-files | grep -c '\.py$'
    34
    $ git ls-files | grep '\.py$' | xargs cat | wc -l
    6173
    $ grep -rIl -e ruff -e mypy -e pyright . --exclude-dir=.git --exclude-dir=.venv
    science/RESEARCH-LEDGER.jsonl
    $ ls pyproject.toml
    ls: pyproject.toml: No such file or directory

Six thousand lines of Python, and the only mention of a linter anywhere in the repo was
a research note about one. Nothing had ever been run.

    $ .venv/bin/ruff check --statistics .
    Found 121 errors.

    $ .venv/bin/pyright .
    24 errors, 0 warnings, 34 files

Twenty-four of those are pyright in *basic* mode, not strict. Thirteen are the same
shape:

    crew/cli.py:233:            "title" is not a known attribute of "None"
    crew/cli.py:454:            "splitlines" is not a known attribute of "None"
    science/outcomes.py:323:    "split" is not a known attribute of "None"
    scripts/pr-evidence.py:339: "end" is not a known attribute of "None"

Each is a crash waiting for the input that makes the value None. Not one test failed,
because nothing was looking.

The single most common lint finding is the one that matters most here:

    26  PLW1510  `subprocess.run` without explicit `check` argument

Twenty-six places where `gh` or `git` can fail and the script carries on with an empty
string and reports success. That is the same defect as PR #129, in a different costume.

## The shell was in better shape than the Python

Worth printing, because the assumption ran the other way:

    $ shellcheck -f gcc -S warning <17 files, 1081 lines>
    (no output)
    $ shellcheck -f gcc -S style <same>
    2

## The gate accepts correct work

    $ bash scripts/verify.d/15-code-standard.sh
    repo-wide ruff findings on all Python: 121   (reported, not enforced)
    changed on this branch: 0 python, 1 shell, 1 workflow

    --- shellcheck, on 1 changed shell file(s) ---
    clean at severity warning.

    --- actionlint, on 1 changed workflow(s) ---
    clean.

    PASS: every file this branch touched meets the standard.
    rc=0

## And refuses, in each language, separately

**Python, a lint defect.** One new file calling `subprocess.run` the way 26 existing
lines already do:

    --- ruff, on 1 changed python file(s) ---
    science/_probe.py:1:1: I001 Import block is un-sorted or un-formatted
    science/_probe.py:3:9: PLW1510 `subprocess.run` without explicit `check` argument
    Found 2 errors.
    rc=1

**Python, a type defect ruff cannot see.** `def width(s: str | None) -> int: return len(s.strip())`:

    --- pyright, on the same file(s) ---
    science/_probe.py:6: "strip" is not a known attribute of "None"
    1 error(s) over 1 file(s).
    rc=1

**Shell.**

    --- shellcheck, on 2 changed shell file(s) ---
    scripts/_probe.sh:2:8: warning: Use "${var:?}" to ensure this never expands to / . [SC2115]
    rc=1

**A workflow.**

    --- actionlint, on 1 changed workflow(s) ---
    .github/workflows/crew-qa.yml:33:14: label "not-a-real-runner-label-xyz" is unknown [runner-label]
    rc=1

## It found three defects in itself before it found any in anyone else

That is the part worth reporting.

1. Run from a worktree it reported BLIND, because it looked for `./.venv/bin/ruff` and a
   worktree has no venv of its own. It now searches the checkout it was cut from.
2. When ruff failed **and** pyright was missing, it printed BLIND — a genuine failure
   softened into "could not tell". A real failure now outranks a blind spot.
3. Its own source had a comment line beginning `# shellcheck's ...`, which the analyser
   read as a malformed directive:

       scripts/verify.d/15-code-standard.sh:171:3: error: Couldn't parse this shellcheck
       directive. Fix to allow more checks. [SC1073]

   Caught by running the gate over the gate.

A fourth was caught by design review rather than by the gate: the first draft's fallback,
when it could not find a merge base, was to treat every tracked file as changed. On a
shallow CI checkout that would have failed every branch in the estate on 121 pre-existing
findings. It reports BLIND and names `fetch-depth: 0` instead.

## Where it runs

`scripts/verify.sh` runs every check in `verify.d` and exits 1 if any failed, and
`crew-qa.yml` already calls it on every pull request with no `continue-on-error`. So this
gate became a required CI check the moment the file landed. The only thing that needed
adding was the tools themselves — `ruff` and `pyright` in `requirements-dev.txt`,
`actionlint` in the workflow, `shellcheck` already on `ubuntu-latest`.

# Onboarding — the code standard, and the machine that holds it

Owner: the data science lane (crew#105)
Last true: 2026-08-24

## What this is for

Founder, 2026-08-24: *"almost every python script we write has defects, we need stricter
code reviews"*, then *"we burn time fixing and refixing these script issues"*, then
*"we don't have engineering standards at all"*, then *"sort it out once so this class of
problems never occurs again"*.

Every one of those is correct, and the last one names the only acceptable answer. Asking
agents to review more carefully is not a fix; it is the same hope that has been failing
daily. The fix is that a machine reads every line before it merges and refuses the ones
that break the standard.

## The standard, and who enforces it

One config, one gate, three checkers. Nothing here is hand-rolled — each is the mature
tool for its language, which is LAW 43 and R6.

| Language | Tool | Configured in |
|---|---|---|
| Python, lint | `ruff` | `pyproject.toml` |
| Python, types | `pyright` | `pyproject.toml` |
| Shell | `shellcheck` | severity `warning`, in the gate |
| GitHub Actions | `actionlint` | the gate, with the same shell severity |

Not covered, said plainly so nobody assumes otherwise: the single `.rego` file (`opa
check` is the tool when a second appears), Markdown, and JSON.

The gate is `scripts/verify.d/15-code-standard.sh`. It is picked up by
`scripts/verify.sh`, which `crew-qa.yml` runs on every pull request with no
`continue-on-error` — so it is a blocking CI check, not a local convenience.

## The one thing to understand: it checks the diff, not the repo

Measured the day it was written, `origin/main` carried 121 ruff findings and 24 pyright
errors. A gate that failed on those would fail every branch in the estate from the moment
it merged, including branches that touched none of them. Within a day every session would
have learned to ignore a red check, and then nothing is enforced at all — which is
exactly where we already were.

So the line is the diff. Code you wrote or edited on this branch meets the standard. Code
you did not touch is counted and printed on every run, so the debt is visible and goes
down in the lane that owns each file. Untouched debt never blocks unrelated work.

The base is the merge base with `main`, not `main`'s tip: a file someone else changed
after you branched is not yours to answer for.

## Running it

```
bash scripts/verify.d/15-code-standard.sh      # just this gate
scripts/verify.sh 15                           # the same, through the harness
scripts/verify.sh                              # every gate, the way CI does
```

You need the tools. On this laptop:

```
.venv/bin/pip install -r requirements-dev.txt   # ruff, pyright
brew install shellcheck actionlint
```

Without them the gate prints `BLIND` and exits 2. It does not print PASS. A check that
cannot see its subject reports that it cannot see, never a verdict.

## What the exit codes mean

**0** — every file this branch touched meets the standard.

**1** — this branch adds or edits code that breaks it. The output names file, line and
rule.

**2** — a checker could not run. Not a pass. Install it and run again. The three ways
this happens: a tool is missing, there is no merge base with `main` (on a runner that
means a shallow checkout — set `fetch-depth: 0`), or pyright analysed zero files because
it was handed paths it did not accept.

That last one is worth knowing about. `pyright` exits 0 having looked at nothing when the
paths are wrong, which reads as a clean pass. The gate asserts `filesAnalyzed > 0` and
calls the alternative BLIND. It is the same trap as the `kyverno test` false-pass already
in `RESEARCH-LEDGER.jsonl`: never grade a tool by its exit code alone.

## When a rule is wrong for your line

Fix it first. `ruff check --fix` handles the mechanical ones on its own.

If a rule is genuinely wrong for a specific line, `# noqa: RULE` with the reason beside
it. Silencing a whole file or a whole rule needs a line in `pyproject.toml` and the
reason in the commit — that is a change to the standard, and it gets read as one.

## Why the rule list is shorter than it could be

Two rules govern what was selected, both learned from watching linters get switched off:

**A rule earns its place by catching a defect, not a preference.** `os.path.join` instead
of `pathlib` is taste. `subprocess.run` without `check=` is a script that carries on
after `gh` failed and reports success over nothing — there were 26 of those. Only the
second kind is selected.

**A guard that refuses correct work is an outage (LAW 38).** Line length, statement
layout and exception-message wording are deliberately absent. Selecting the `E7` prefix
whole would have failed 71 correct lines on day one; the E7 rules that describe a defect
(`== None`, bare `except:`, `l` as a name) are named individually instead.

## What goes wrong

**It reports BLIND from a worktree.** It should not any more — it searches the checkout
it was cut from. If it still does, set `CREW_VENV` to the venv you want it to use.

**It passes locally and fails in CI.** It counts uncommitted and untracked files
deliberately, so this should not happen. If it does, the branch is behind `origin/main`
and the merge base moved: `git fetch origin`.

**The repo-wide number goes up and nobody notices.** It is printed on every run, passing
or failing. That is the whole instrument (LAW 28). If it climbs, a lane merged debt into
files it did not touch, and the number is the only thing that will say so.

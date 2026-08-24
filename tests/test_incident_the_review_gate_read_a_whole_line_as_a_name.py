"""Incident: review-gate read a whole line as a session name.

Measured 2026-08-24 on PR #156. The body carried the reviewer's name and then some
prose about the review on the same line:

    Reviewed-by: chidionyema-03 -- KEEP, non-author, comment 5393770837. They ...

    FAIL: no issue comment or review contains 'REVIEW:' together with 'session
    chidionyema-03 -- KEEP, non-author, comment 5393770837. They reproduced the'

`grep -Po '^Reviewed-by:\\s*\\K\\S.*$'` takes the whole rest of the line, so the gate
went looking for a session whose name was that entire sentence. A trailing comma does
the same thing, and nothing in the failure message tells the author that the field
takes one token -- it prints the name it invented and asks for a comment naming it.

LAW 38: a guard that refuses correct work is an outage. The review was done and posted;
the gate could not read who did it.

The class: **a field that holds a name must parse a name.** `\\S.*$` is "the rest of the
line", which is a different thing that happens to start with the name.

Not in scope, and refused with a case rather than left unsaid: the same PR's REVIEW:
comment wrote `Reviewed-by: chidionyema-03` where the gate wants `session <name>`.
chidionyema-03 reviewed the proposal to accept both spellings and rejected it, and the
rejection holds -- review-gate.yml documents `REVIEW: <findings> - session <name>` in
its own header and prints that exact example in the failure message, so refusing a
comment that ignores the printed contract is the gate working. Two accepted shapes for
one thing is how the next session gets it wrong.

These tests do not re-implement the gate. They read the two `grep -Po` patterns and the
`bad_name()` patterns out of `.github/workflows/review-gate.yml` and run them, so a
workflow edit that breaks them fails here instead of passing against a stale copy.

Rung 4.
"""
import pathlib
import re
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "review-gate.yml"

#: The runner is ubuntu-latest, where `grep -P` is PCRE. This machine's /usr/bin/grep is
#: BSD and has no -P at all, so a test that shelled out to `grep -P` would skip on every
#: developer machine and run only in CI -- which is the defect #154 was opened for, one
#: level up. perl is the same PCRE engine and is present in both places, so the pattern
#: is executed rather than approximated.
#:
#: Residual, stated rather than hidden: perl and GNU grep -P are the same engine but not
#: the same binary. A pattern that behaved differently between them would pass here and
#: fail on the runner. The patterns in this workflow are `^field:\s*\K\S+` and two
#: anchored literals, which is the part of PCRE where that cannot happen.
_PERL = shutil.which("perl")
needs_perl = pytest.mark.skipif(
    not _PERL,
    reason=("no perl on this machine, so the gate's own PCRE cannot be executed here. "
            "The gate is unmeasured, not green."))


def _perl() -> str:
    """The perl binary, or an error naming why there is none.

    A function rather than a bare `str | None` module constant: every caller is behind
    `@needs_perl`, and this states that invariant where a reader and a type checker can
    both see it instead of leaving `None` to reach `subprocess.run`.
    """
    assert _PERL, "called without perl; every caller must carry @needs_perl"
    return _PERL


def _workflow_text() -> str:
    assert WORKFLOW.is_file(), f"the workflow this file tests is not at {WORKFLOW}"
    return WORKFLOW.read_text()


def _name_pattern(field: str) -> str:
    """The PCRE the workflow uses to pull one name out of the PR body."""
    m = re.search(rf"{field}=\$\(printf .*grep -Po '([^']+)'", _workflow_text())
    assert m, f"no `grep -Po` pattern for {field} in {WORKFLOW.name}"
    return m.group(1)


def _extract(field: str, body: str) -> str:
    """Run the workflow's own pattern over a PR body and return what it calls the name."""
    r = subprocess.run([_perl(), "-ne", f'print "$&\\n" if /{_name_pattern(field)}/'],
                       input=body, capture_output=True, text=True, check=True)
    lines = r.stdout.splitlines()
    return lines[0] if lines else ""


def _rejected_by_bad_name(name: str) -> bool:
    """True if any pattern inside the workflow's `bad_name()` rejects this name."""
    body = _workflow_text().split("bad_name() {", 1)[1].split("\n          }", 1)[0]
    found = re.findall(r"grep -([A-Za-z]*)q '([^']+)'", body)
    assert found, "no grep patterns inside bad_name()"
    for flags, pat in found:
        #: `i` is the flag that matters here -- it is what makes `^author$` reject
        #: `Author`. The rest of the flags do not change whether a line matches.
        opts = "i" if "i" in flags else ""
        #: The verdict is a printed mark, not the exit status. `perl -e 'END{exit 1}'`
        #: runs its END block on the way out of an `exit 0`, so an exit-code version of
        #: this reads 1 for every input and the function returns False always -- a
        #: checker that cannot tell "no pattern matched" from "I never looked", which
        #: is the family of defect this repo keeps filing.
        r = subprocess.run([_perl(), "-ne", f'print "M" if /{pat}/{opts}'],
                           input=name, capture_output=True, text=True, check=True)
        if "M" in r.stdout:
            return True
    return False


@needs_perl
def test_incident_a_reviewed_by_line_may_carry_prose_after_the_name():
    """PR #156's body, unchanged. The name is `chidionyema-03` and nothing more."""
    body = ("Author-session: code-3a\n"
            "Reviewed-by: chidionyema-03 -- KEEP, non-author, comment 5393770837.\n")

    assert _extract("reviewed_by", body) == "chidionyema-03", (
        "the gate still reads the rest of the line as part of the session name, which "
        "is the #156 failure unchanged")
    assert _extract("author_session", body) == "code-3a"


@needs_perl
def test_a_bare_name_on_the_line_is_unchanged():
    """The other direction, in the same run. Narrowing the pattern must not have
    broken the shape that already worked -- every merged PR on this repo has one."""
    body = "Author-session: code-3a\nReviewed-by: chidionyema-03\n"

    assert _extract("reviewed_by", body) == "chidionyema-03"
    assert _extract("author_session", body) == "code-3a"


@needs_perl
def test_the_unfilled_template_placeholder_is_still_not_a_name():
    """The regression taking one token introduces if nothing else changes.

    `<your session name>` arrives as `<your` once the first token is taken, and the old
    check `^<.*>$` does not match that -- it would have waved an unfilled template
    through as a session called `<your`. This is why `bad_name()` moved to `^<`.
    """
    name = _extract("reviewed_by", "Reviewed-by: <your session name>\n")

    assert name.startswith("<"), f"the body parse produced no placeholder at all: {name!r}"
    assert _rejected_by_bad_name(name), (
        f"bad_name() does not reject {name!r}, so a PR body with the template still "
        "unfilled now names a reviewer")


@needs_perl
def test_a_real_name_is_not_rejected_by_bad_name():
    """The paired control for the test above. A check only ever seen refusing has not
    been shown to permit, and `^<` must not have become "reject everything"."""
    assert not _rejected_by_bad_name("chidionyema-03")
    assert not _rejected_by_bad_name("code-3a")

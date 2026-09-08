"""The merge bot's required-check list must name checks that something still produces.

INCIDENT, 2026-09-08. `.github/workflows/merge-when-green.yml` is the mechanism that lands
a finished pull request without a person. It refuses to merge unless every name in its
`REQUIRED` set is PRESENT and SUCCESS in the check rollup. One of those names was
`review-gate`, and the founder deleted `review-gate.yml` under `.github/workflows/` on 2026-08-29
(commit 9fca66c, "Retire the peer-review gate: founder 2026-08-29, review is friction").

From that day no run could ever produce a `review-gate` check, so the mechanism refused
every pull request in the repository and recorded the refusal only inside its own run log.
Nothing was red on the pull requests themselves; they simply never merged, and each one
went back to the founder by hand. Founder, 2026-09-08: "this blind sop where pr fails ad
founder needs to tell agents ... agents should be responsiblefor their own own, all this
chasing is fricion" (record:
~/.claude/docs/founder/2026-09-08T0736Z-soor-this-blind-sop-where-pr-fails-ad-385bc493.md).

THE CLASS. A check name written in one file and produced in another drifts the moment
either side moves. crew#105 was the same split in the opposite direction: a required check
that was absent read as GREEN and an unreviewed pull request merged. Absent-reads-green and
absent-reads-red are one defect, and the guard for both is that the name has to resolve to
a job that exists on disk.
"""

from __future__ import annotations

import ast
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
MERGE_BOT = WORKFLOWS / "merge-when-green.yml"


def required_checks() -> set[str]:
    """The REQUIRED set as the merge bot's inlined python actually defines it.

    Read out of the file rather than duplicated here: a copy in the test is a third
    place for the same name to drift, which is the defect this guards.
    """
    line = re.search(r"^\s*REQUIRED = (\{[^}]*\})", MERGE_BOT.read_text(), re.M)
    assert line, "merge-when-green.yml no longer defines a REQUIRED set on one line"
    return set(ast.literal_eval(line.group(1)))


def produced_check_names() -> set[str]:
    """Every check name a workflow in this repository can put on a commit.

    GitHub names a check run after the job's `name:` when it has one and after the job
    id otherwise, so both are collected.
    """
    names: set[str] = set()
    for path in sorted(WORKFLOWS.glob("*.y*ml")):
        doc = yaml.safe_load(path.read_text()) or {}
        for job_id, job in (doc.get("jobs") or {}).items():
            names.add(str(job_id))
            if isinstance(job, dict) and job.get("name"):
                names.add(str(job["name"]))
    return names


def test_every_required_check_is_produced_by_a_workflow_on_disk() -> None:
    missing = sorted(required_checks() - produced_check_names())
    assert not missing, (
        f"merge-when-green.yml requires {missing}, and no workflow in {WORKFLOWS} has a job "
        "that produces it. A required check nothing produces can never be PRESENT, so the "
        "merge bot refuses every pull request and only its own run log says why. Either "
        "restore the workflow or take the name out of REQUIRED."
    )


def test_the_required_set_is_not_empty() -> None:
    """The opposite failure: an empty set merges anything, including a red branch."""
    assert required_checks(), (
        "REQUIRED is empty, so merge-when-green.yml would land a pull request with no "
        "proof at all. crew#105 is what that costs."
    )


def test_the_guard_catches_a_name_nothing_produces() -> None:
    """Prove the check both ways, on the real data rather than on a fixture."""
    produced = produced_check_names()
    assert "qa" in produced, "crew-qa.yml no longer defines a job named qa"
    assert "review-gate" not in produced, (
        "review-gate is producible again. If the founder un-retired peer review, put it "
        "back in REQUIRED; until then this assertion is what proves the guard would fire."
    )


def decision_program() -> str:
    """The merge bot's decision step, lifted out of the workflow's heredoc.

    Run rather than read: R76 says a test grades behaviour, and the thing that went wrong
    here was a decision, not a sentence. Lifting it keeps one copy -- the workflow's -- so
    the test cannot pass against code the workflow does not run.
    """
    body = MERGE_BOT.read_text()
    start = body.index("python3 - <<'PY' > todo.txt\n") + len("python3 - <<'PY' > todo.txt\n")
    end = body.index("\n          PY\n", start)
    return "\n".join(line[10:] for line in body[start:end].split("\n"))


def verdicts_for(prs: list[dict]) -> dict[int, str]:
    """Run the real decision step over synthetic pull requests and read its verdicts."""
    import json
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        pathlib.Path(d, "prs.json").write_text(json.dumps(prs))
        out = subprocess.run(
            ["python3", "-c", decision_program()],
            cwd=d,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    return {int(line.split()[1]): line.split()[0] for line in out.splitlines() if line.strip()}


def _pr(number: int, **over: object) -> dict:
    pr = {
        "number": number,
        "isDraft": False,
        "mergeStateStatus": "CLEAN",
        "labels": [],
        "title": "t",
        "statusCheckRollup": [{"name": "qa", "status": "COMPLETED", "conclusion": "SUCCESS"}],
    }
    pr.update(over)
    return pr


def test_a_green_draft_is_marked_ready_rather_than_left_to_rot() -> None:
    """Five green drafts sat unmerged on 2026-09-08 because nobody came back for them."""
    assert verdicts_for([_pr(1, isDraft=True)])[1] == "READY"


def test_a_red_draft_is_never_touched() -> None:
    """Un-drafting is only ever the last step on a pull request that would otherwise land."""
    red = _pr(
        2,
        isDraft=True,
        statusCheckRollup=[{"name": "qa", "status": "COMPLETED", "conclusion": "FAILURE"}],
    )
    assert verdicts_for([red])[2] == "SKIP."


def test_a_held_draft_stays_a_draft() -> None:
    """The one-word escape still stops the mechanism, which is what makes it safe."""
    held = _pr(3, isDraft=True, labels=[{"name": "hold"}])
    assert verdicts_for([held])[3] == "SKIP."


def test_a_ready_green_pull_request_still_merges() -> None:
    assert verdicts_for([_pr(4)])[4] == "MERGE"

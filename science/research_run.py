"""crew#701 CP1: one graded research report, end to end, on a GitHub runner.

Founder document 2026-08-30 04:11Z (`docs/founder/...bootstrapping-the-science-dept...`):
GPT Researcher is the worker, not the manager; a frontier model through the router key, never a
local model; Inspect scores the report the moment it finishes and a failed score drops the run;
MLflow keeps the question, the report and the score; Langfuse catches tokens and traces.

    python3 science/research_run.py --row 0            # one intake row of RESEARCH-INTAKE.jsonl
    python3 science/research_run.py --question "..."   # or a question of your own

Exit 0 with `ok research-run ... inspect <score> ... langfuse trace <id>`; exit 1 with
`REFUSED research-run <why>`. The MLflow file store lands in `mlruns/` beside the report so the
workflow attaches both as the run artefact. Runs from the Mac fail on search (crew#659: the
Tailscale resolver); the runner is the place, and that is the point of the workflow.
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import json
import os
import pathlib
import sys
import uuid

SCIENCE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCIENCE))
import research_worker as rw  # noqa: E402

INTAKE = SCIENCE / "RESEARCH-INTAKE.jsonl"
#: Below this Inspect score the run is a failure and nothing is kept (founder: "dropped").
PASS_SCORE = float(os.environ.get("RESEARCH_PASS_SCORE", "0.5"))


def question_for(row: dict) -> str:
    return (
        f"{row['repo']} released {row['tag']} on {row['published_at'][:10]} ({row['url']}). "
        f"For a platform team running it as their '{row['row']}' layer: what changed, what breaks "
        f"on upgrade, and should they upgrade now? Cite the release notes and any incident reports."
    )


def intake_row(i: int, path: pathlib.Path = INTAKE) -> dict:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not 0 <= i < len(rows):
        raise rw.Refused(f"intake has {len(rows)} rows; --row {i} does not exist")
    return rows[i]


def research(question: str, run_id: str) -> dict:
    """GPT Researcher through the router, every call stamped with the run id as its trace id."""
    os.environ["LLM_KWARGS"] = json.dumps({"extra_body": {"litellm_trace_id": run_id}})
    return asyncio.run(rw._research(question, deep=False))


def grade(question: str, report: str, lane: str, run_id: str, log_dir: pathlib.Path) -> float:
    """Inspect model_graded_qa over the one report. Returns the score in [0, 1]."""
    from inspect_ai import Task
    from inspect_ai import eval as inspect_eval
    from inspect_ai.dataset import Sample
    from inspect_ai.model import GenerateConfig, get_model
    from inspect_ai.scorer import model_graded_qa
    from inspect_ai.solver import generate

    grader = get_model(
        f"openai/{lane}", config=GenerateConfig(extra_body={"litellm_trace_id": run_id})
    )
    task = Task(
        dataset=[
            Sample(
                input=f"Question: {question}\n\nReport:\n{report}",
                target=(
                    "A report that answers the question directly, cites at least three real "
                    "sources by URL, separates what changed from what it means for the reader, "
                    "and states a recommendation with its conditions."
                ),
            )
        ],
        solver=[generate()],
        scorer=model_graded_qa(
            model=grader,
            partial_credit=True,
            instructions=(
                "Grade the Report against the Criterion. Answer with GRADE: C when it meets "
                "every part, GRADE: P when it meets most, GRADE: I when it does not."
            ),
        ),
    )
    (log,) = inspect_eval(task, model=grader, log_dir=str(log_dir), display="none")
    if log.status != "success" or not log.results:
        raise rw.Refused(f"inspect eval {log.status}: {log.error}")
    return float(log.results.scores[0].metrics["accuracy"].value)


def record(
    mlruns: pathlib.Path, run_id: str, question: str, report: str, score: float, passed: bool
) -> str:
    import mlflow

    mlflow.set_tracking_uri(mlruns.resolve().as_uri())
    mlflow.set_experiment("research")
    with mlflow.start_run(run_name=run_id) as run:
        mlflow.log_param("question", question[:500])
        mlflow.log_param("langfuse_trace_id", run_id)
        mlflow.log_metric("inspect_score", score)
        mlflow.log_metric("passed", float(passed))
        mlflow.log_text(report, "report.md")
        return run.info.run_id


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--row", type=int, default=0, help="index into science/RESEARCH-INTAKE.jsonl")
    g.add_argument("--question")
    ap.add_argument("--worker", default=os.environ.get("RESEARCH_WORKER_LANE", "minimax"))
    ap.add_argument("--grader", default=os.environ.get("RESEARCH_GRADER_LANE", "groq"))
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("research-run"))
    a = ap.parse_args(argv)
    run_id = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    try:
        question = a.question or question_for(intake_row(a.row))
        rw.configure(a.worker, a.grader)
        out = research(question, run_id)
        if not out["sources"]:
            raise rw.Refused("the worker returned a report with no sources")
        a.out.mkdir(parents=True, exist_ok=True)
        (a.out / "report.md").write_text(
            f"# {question}\n\nrun {run_id}, worker {a.worker}, grader {a.grader}\n\n{out['report']}\n\n"
            "## Sources\n\n" + "\n".join(f"- {s}" for s in out["sources"]) + "\n"
        )
        score = grade(question, out["report"], a.grader, run_id, a.out / "inspect-logs")
        passed = score >= PASS_SCORE
        ml = record(a.out / "mlruns", run_id, question, out["report"], score, passed)
    except rw.Refused as e:
        print(f"REFUSED research-run   {e}", file=sys.stderr)
        return 1
    line = (
        f"research-run   run {run_id}: inspect {score:.2f} (pass at {PASS_SCORE}), "
        f"{len(out['sources'])} sources, mlflow run {ml}, langfuse trace {run_id}"
    )
    if not passed:
        print(f"FAILED  {line}: the report is dropped", file=sys.stderr)
        (a.out / "report.md").unlink()
        return 1
    print(f"ok      {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

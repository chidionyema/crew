"""crew#701 CP1: one graded research report, end to end, on a GitHub runner.

Founder document 2026-08-30 04:11Z (`docs/founder/...bootstrapping-the-science-dept...`):
GPT Researcher is the worker, not the manager; a frontier model through the router key, never a
local model; Inspect scores the report the moment it finishes and a failed score drops the run;
MLflow keeps the question, the report and the score; Langfuse catches tokens and traces.

    python3 science/research_run.py --row 0            # one intake row of RESEARCH-INTAKE.jsonl
    python3 science/research_run.py --question "..."   # or a question of your own

Exit 0 with `ok research-run ... inspect <score> ... langfuse trace <id>`; exit 1 with
`REFUSED research-run <why>`. The MLflow SQLite store lands in `mlruns/mlflow.db` beside the report so the
workflow attaches both as the run artefact. Runs from the Mac fail on search (crew#659: the
Tailscale resolver); the runner is the place, and that is the point of the workflow.
"""
# Rejected: GPT Researcher's own CLI/REST server (gptr.dev) -- it can run the research but it cannot
#   score the report with Inspect, drop a failed one, or log the run to MLflow; this file is only
#   that glue around the library, no research logic of its own.
# Standard: docs/STANDARDS.md rows "Experiments" (MLflow) and "Agent traces" (Langfuse via the router).
# Deviation: none -- worker, grader and store are all the named rows.

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import json
import os
import pathlib
import subprocess
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
    """Inspect model_graded_qa over the one report, in the grader's own interpreter. Returns [0, 1].

    Inspect's openai provider demands openai>=3.1 and litellm (GPT Researcher's dependency) demands
    openai<3 (crew#712, runs 33304930630 and 33305540921), so the two cannot share one environment:
    RESEARCH_GRADER_PYTHON names the interpreter that holds requirements-grade.txt; the default is
    this one, for a machine that installed both by hand."""
    py = os.environ.get("RESEARCH_GRADER_PYTHON", sys.executable)
    grader = pathlib.Path(__file__).with_name("research_inspect_grade.py")
    r = subprocess.run(
        [py, str(grader), "--lane", lane, "--run-id", run_id, "--log-dir", str(log_dir)],
        input=json.dumps({"question": question, "report": report}),
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        raise rw.Refused(f"inspect grade failed: {r.stderr.strip()[-400:]}")
    return float(json.loads(r.stdout.strip().splitlines()[-1])["score"])


def tracking_uri(mlruns: pathlib.Path) -> str:
    return f"sqlite:///{(mlruns / 'mlflow.db').resolve()}"


def record(
    mlruns: pathlib.Path, run_id: str, question: str, report: str, score: float, passed: bool
) -> str:
    import mlflow

    # MLflow 3.x refuses the `./mlruns` file store ("maintenance mode"; crew#701, five runs on
    # 2026-08-30). A SQLite database in the same folder is the backend both lines accept, and
    # the artifacts stay beside it so the whole folder is one workflow artifact.
    mlruns.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(tracking_uri(mlruns))
    if mlflow.get_experiment_by_name("research") is None:
        mlflow.create_experiment("research", artifact_location=(mlruns / "artifacts").resolve().as_uri())
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
    ap.add_argument("--worker", default=os.environ.get("RESEARCH_WORKER_LANE", "claude"))
    ap.add_argument("--grader", default=os.environ.get("RESEARCH_GRADER_LANE", "claude-fast"))
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

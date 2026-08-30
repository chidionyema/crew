"""crew#701 CP1: the Inspect grader, run by science/research_run.py in its own interpreter.

Reads {"question", "report"} on stdin, prints {"score": <0..1>} on stdout. Exit 1 on a failed eval.
Its own environment is requirements-grade.txt (Inspect wants openai>=3.1; the worker's litellm
wants openai<3, so the two never share a venv: crew#712).
"""

# Rejected: grading inside research_run.py -- one venv cannot hold openai>=3.1 and openai<3.
# Standard: docs/STANDARDS.md row "Experiments" (the score lands in MLflow via research_run.py).
# Deviation: none.
from __future__ import annotations

import argparse
import json
import pathlib
import sys


class Refused(RuntimeError):
    pass


def grade(question: str, report: str, lane: str, run_id: str, log_dir: pathlib.Path) -> float:
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
        raise Refused(f"inspect eval {log.status}: {log.error}")
    return float(log.results.scores[0].metrics["accuracy"].value)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--log-dir", required=True, type=pathlib.Path)
    a = ap.parse_args(argv)
    doc = json.load(sys.stdin)
    try:
        score = grade(doc["question"], doc["report"], a.lane, a.run_id, a.log_dir)
    except Refused as e:
        print(f"REFUSED research-grade {e}", file=sys.stderr)
        return 1
    print(json.dumps({"score": score}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

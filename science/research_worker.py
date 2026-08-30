#!/usr/bin/env python3
# Rejected: GPT Researcher's own CLI / multi_agents runner -- it can research, but it cannot refuse a
#   non-frontier lane, cannot grade its own report, and cannot write a ledger row the scoreboard counts;
#   this file is the 200 lines of glue around GPT Researcher (worker) and Inspect (grader), not a rival.
# Standard: docs/STANDARDS.md row "LLM providers" (LiteLLM router, the only door to a model) and
#   docs/RESEARCH_PLATFORM_CAPABILITY.md "The research worker" (GPT Researcher, crew#672).
# Deviation: none -- MLflow (blueprint memory) is not running in the estate yet; the ledger is the memory
#   until the MLflow row exists (crew#659).
"""The research worker: GPT Researcher through the router, every report graded by Inspect, every
idea a scored row on the ledger (crew#659 CP3, crew#221, founder 2026-08-30).

Founder, 2026-08-30, verbatim: "GPT Researcher is the worker, not the manager ... The moment GPT
Researcher finishes, Inspect scores the answer. If a run produces a report but fails the Inspect
score, the run is marked as a failure and dropped." And, from his note of 2026-08-30 00:55Z: "Run
them against a frontier API rather than a local model, or you've automated the problem."

One run, one brief, N scored ideas:

    python3 science/research_worker.py run --brief "AI tooling a two-person agency would pay for" \
        [--market "UK SME"] [--ideas 3] [--worker claude] [--grader gemini] [--deep]

1. GPT Researcher (Apache-2.0, docs/RESEARCH_PLATFORM_CAPABILITY.md "The research worker") reads
   the open web and writes a report with its sources. It reaches a model only through the estate
   router (LAW 34): OPENAI_BASE_URL is the router, the key is a router virtual key, and the lane
   must be a frontier lane (FRONTIER_LANES). A local lane is refused before any call is made.
2. A second call to the router turns the report into N ideas, each with a falsifiable claim, a
   price hypothesis and the sources from the report that back it.
3. Inspect (MIT, the eval harness on the same standards row) grades every idea with
   model_graded_qa on a second frontier lane. C = 1.0, P = 0.5, I = 0.0. The eval log is a file
   under science/inspect-logs/.
4. Every idea lands on science/RESEARCH-LEDGER.jsonl through science/ledger.py with kind=idea and
   its score. An idea with no score is never written: a report nobody graded is the failure mode
   this exists to stop. research_grade.py counts these rows (crew#659 CP2).

The router traces every call to Langfuse and the collector on its own (docs/STANDARDS.md,
Observability row), so this file carries no tracing SDK.

Rejected (LAW 43): a hand-written crawler (that is what GPT Researcher is); STORM (cold repo,
article synthesis, not a brief); a local model for the worker or the grader (the founder's note
above); a config file that names a vendor key (the router is the only door).
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import json
import os
import pathlib
import re
import sys
import uuid
from collections.abc import Callable

SCIENCE = pathlib.Path(__file__).resolve().parent
ROOT = SCIENCE.parent
sys.path.insert(0, str(SCIENCE))
import ledger  # noqa: E402

REPORTS = SCIENCE / "research-reports"
INSPECT_LOGS = SCIENCE / "inspect-logs"
#: Router lanes (platform/llm/config.yaml model_name rows) that are frontier models. The worker and
#: the grader must both be one of these; anything else is refused before a single request.
FRONTIER_LANES = frozenset({"claude", "claude-fast", "gemini", "gemini-or"})
#: The router lane that serves embeddings; gpt-researcher ranks scraped context with it.
EMBED_LANE = "embed"
SCORE = {"C": 1.0, "P": 0.5, "I": 0.0}
GRADER_INSTRUCTIONS = (
    "You are grading a business idea produced by a research run. Grade C (correct) only when the "
    "claim is falsifiable, the price hypothesis is a number a buyer could accept or reject, and "
    "the cited sources plausibly support the claim. Grade P when one of the three is weak. Grade "
    "I when the claim is unfalsifiable, unsourced, or contradicted by the report."
)


class Refused(RuntimeError):
    """The run cannot proceed and must not write anything."""


# --- the router ---------------------------------------------------------------------------------
def zone() -> str:
    """ESTATE_ZONE from the environment, else the estate config in the idp checkout beside this
    repo (LAW 46: no file names the zone)."""
    z = os.environ.get("ESTATE_ZONE", "").strip()
    if z:
        return z
    cfg = (
        pathlib.Path(os.environ.get("ESTATE_CODE", ROOT.parent))
        / "idp/clusters/oke/estate-config.yaml"
    )
    if cfg.exists():
        m = re.search(r"ESTATE_ZONE:\s*(\S+)", cfg.read_text())
        if m:
            return m.group(1)
    raise Refused(
        "no ESTATE_ZONE in the environment and no idp/clusters/oke/estate-config.yaml beside this repo"
    )


def router() -> tuple[str, str]:
    """(base_url, key). The key comes from ROUTER_KEY_FILE (a file, the way the cluster mounts
    secrets) or ROUTER_KEY; it is never printed and never a vendor key."""
    url = os.environ.get("ROUTER_URL", "").rstrip("/") or f"https://llm.{zone()}"
    key_file = os.environ.get("ROUTER_KEY_FILE", "")
    key = (
        pathlib.Path(key_file).read_text().strip() if key_file else os.environ.get("ROUTER_KEY", "")
    )
    if not key:
        raise Refused("no router key: set ROUTER_KEY_FILE (a file) or ROUTER_KEY")
    return url, key


def require_frontier(lane: str, role: str) -> str:
    if lane not in FRONTIER_LANES:
        raise Refused(
            f"{role} lane {lane!r} is not a frontier lane {sorted(FRONTIER_LANES)}: "
            "a local or small model here automates unverified claims (founder note 2026-08-30)"
        )
    return lane


#: The router walks a dead frontier lane to a fallback (claude -> minimax) and answers 200; on
#: 2026-08-30 05:3xZ every `claude` and `gemini` call came back as MiniMax-M2 because both vendor
#: accounts were empty. A frontier lane that answers from another vendor is not a frontier lane.
NO_FALLBACK = {"fallbacks": []}
#: The probe asks for as many tokens as gpt-researcher's largest single call (its default
#: SMART_TOKEN_LIMIT is 4000). OpenRouter refuses up front with 402 when the account cannot afford
#: `max_tokens`, so a 1-token probe passed at 05:5xZ on 2026-08-30 and the run then died on
#: "can only afford 2272" nine retries later. Asking for 4096 and generating two costs nothing more.
PROBE_MAX_TOKENS = 4096


def probe_lane(lane: str, role: str, ask=None) -> str:
    """One tiny call with fallbacks off. Returns the upstream model that answered, or raises
    Refused carrying the vendor's own words (an empty account is a founder action, not a retry)."""
    if ask is None:

        def _ask(lane: str) -> str:
            from openai import OpenAI

            url, key = router()
            client = OpenAI(base_url=f"{url}/v1", api_key=key)
            out = client.chat.completions.create(
                model=lane,
                max_tokens=PROBE_MAX_TOKENS,
                messages=[{"role": "user", "content": "Reply with the single word ok."}],
                extra_body=NO_FALLBACK,
            )
            return out.model or lane

        ask = _ask

    try:
        return ask(lane)
    except Exception as e:
        raise Refused(
            f"{role} lane {lane!r} does not answer from its own vendor: {str(e)[:300]}"
        ) from e


def configure(worker: str, grader: str) -> dict:
    """The environment gpt-researcher and Inspect read. Returns what was set (values redacted)."""
    url, key = router()
    require_frontier(worker, "worker")
    require_frontier(grader, "grader")
    probe_lane(worker, "worker")
    probe_lane(grader, "grader")
    env = {
        "OPENAI_BASE_URL": f"{url}/v1",
        "OPENAI_API_KEY": key,
        "FAST_LLM": f"openai:{worker}",
        "SMART_LLM": f"openai:{worker}",
        "STRATEGIC_LLM": f"openai:{worker}",
        "EMBEDDING": f"openai:{EMBED_LANE}",
        "RETRIEVER": os.environ.get("RETRIEVER", "duckduckgo"),
        "VERBOSE": os.environ.get("VERBOSE", "false"),
    }
    os.environ.update(env)
    return {k: ("<redacted>" if k == "OPENAI_API_KEY" else v) for k, v in env.items()}


# --- 1. the worker ------------------------------------------------------------------------------
async def _research(brief: str, deep: bool) -> dict:
    from gpt_researcher import GPTResearcher

    r = GPTResearcher(query=brief, report_type="deep" if deep else "research_report", verbose=False)
    await r.conduct_research()
    report = await r.write_report()
    return {
        "report": report,
        "sources": list(dict.fromkeys(r.get_source_urls())),
        "costs_usd": float(r.get_costs() or 0.0),
    }


def research(brief: str, deep: bool = False) -> dict:
    return asyncio.run(_research(brief, deep))


# --- 2. ideas out of the report -----------------------------------------------------------------
def _chat(lane: str, system: str, user: str) -> str:
    from openai import OpenAI

    url, key = router()
    client = OpenAI(base_url=f"{url}/v1", api_key=key)
    out = client.chat.completions.create(
        model=lane,
        temperature=0.2,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        extra_body=NO_FALLBACK,
    )
    return out.choices[0].message.content or ""


def parse_ideas(text: str) -> list[dict]:
    """The first JSON array in the model's answer; every idea must carry the four fields."""
    m = re.search(r"\[.*\]", text, re.S)
    if not m:
        raise Refused("the extraction step returned no JSON array")
    ideas = json.loads(m.group(0))
    for i in ideas:
        for k in ("title", "claim", "price_hypothesis", "sources"):
            if not i.get(k):
                raise Refused(f"idea {i.get('title', '?')!r} has no {k}")
    return ideas


def extract_ideas(report: dict, brief: str, n: int, lane: str, market: str = "") -> list[dict]:
    system = (
        "You turn a research report into sellable product ideas for a store front. Answer with "
        'a JSON array only. Each item: {"title": str, "claim": one falsifiable sentence, '
        '"price_hypothesis": str with a number and a unit, "sources": [urls from the report]}'
    )
    user = (
        f"Brief: {brief}\nMarket: {market or 'unspecified'}\nIdeas wanted: {n}\n\nReport:\n"
        f"{report['report']}\n\nSources available:\n" + "\n".join(report["sources"])
    )
    ideas = parse_ideas(_chat(lane, system, user))
    allowed = set(report["sources"])
    for i in ideas:
        i["sources"] = [s for s in i["sources"] if s in allowed] or i["sources"][:3]
    return ideas[:n]


# --- 3. the grade -------------------------------------------------------------------------------
def grade_ideas(
    ideas: list[dict], report: dict, grader: str, run_id: str, log_dir: pathlib.Path = INSPECT_LOGS
) -> list[dict]:
    """Inspect model_graded_qa over one sample per idea. Returns ideas with score, grade, log."""
    from inspect_ai import Task
    from inspect_ai import eval as inspect_eval
    from inspect_ai.dataset import Sample
    from inspect_ai.scorer import model_graded_qa

    samples = [
        Sample(
            id=str(k),
            input=(
                f"Idea: {i['title']}\nClaim: {i['claim']}\nPrice hypothesis: "
                f"{i['price_hypothesis']}\nSources: {', '.join(i['sources'])}\n\n"
                f"Report the idea came from:\n{report['report'][:12000]}"
            ),
            target="A falsifiable, priced, sourced idea consistent with the report.",
        )
        for k, i in enumerate(ideas)
    ]
    task = Task(
        dataset=samples,
        scorer=model_graded_qa(
            instructions=GRADER_INSTRUCTIONS, partial_credit=True, model=f"openai/{grader}"
        ),
    )
    log_dir.mkdir(parents=True, exist_ok=True)
    logs = inspect_eval(
        task,
        model=f"openai/{grader}",
        log_dir=str(log_dir),
        display="none",
        log_level="warning",
        task_args={},
        tags=[run_id],
    )
    log = logs[0]
    if log.status != "success" or not log.samples:
        raise Refused(
            f"Inspect eval {log.status}: no grade, so no idea is written ({log.location})"
        )
    by_id = {str(s.id): s for s in log.samples}
    for k, i in enumerate(ideas):
        s = by_id.get(str(k))
        value = None if s is None or not s.scores else next(iter(s.scores.values())).value
        if value not in SCORE:
            raise Refused(f"idea {i['title']!r} came back without a grade ({value!r}); dropped")
        i.update(grade=value, score=SCORE[value], grader=grader, inspect_log=str(log.location))
    return ideas


# --- 4. the ledger ------------------------------------------------------------------------------
def _rel(p: pathlib.Path) -> str:
    """Repo-relative when the path is inside the repo (the ledger is git), else as given."""
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def rows_for(
    ideas: list[dict],
    brief: str,
    market: str,
    worker: str,
    run_id: str,
    report_path: str,
    asked_at: str,
    costs_usd: float,
) -> list[dict]:
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    rows = []
    for i in ideas:
        if not isinstance(i.get("score"), int | float):
            raise Refused(
                f"idea {i.get('title')!r} has no score: an unscored idea never reaches the ledger"
            )
        rows.append(
            {
                "kind": "idea",
                "title": i["title"],
                "claim": i["claim"],
                "price_hypothesis": i["price_hypothesis"],
                "market": market,
                "score": i["score"],
                "grade": i["grade"],
                "grader": i["grader"],
                "worker": worker,
                "run_id": run_id,
                "report": report_path,
                "inspect_log": i.get("inspect_log", ""),
                "question": brief,
                "why": "crew#659 CP3: an idea for the store front, generated by the research worker",
                "decision_fed": f"candidate for the store front, graded {i['grade']} ({i['score']}) by Inspect on {i['grader']}",
                "sources": i["sources"],
                "findings": [f"Claim: {i['claim']}", f"Price hypothesis: {i['price_hypothesis']}"],
                "metric": "Inspect model_graded_qa score, 0 to 1",
                "metric_before": str(i["score"]),
                "what_this_costs": f"router spend {costs_usd:.4f} USD for the run, shared by {len(ideas)} ideas",
                "ticket": "https://github.com/chidionyema/crew/issues/659",
                "asked_at": asked_at,
                "decided_at": now,
            }
        )
    return rows


def run(
    brief: str,
    market: str = "",
    n: int = 3,
    worker: str = "claude",
    grader: str = "gemini",
    deep: bool = False,
    ledger_path: pathlib.Path = ledger.LEDGER,
    reports: pathlib.Path = REPORTS,
    researcher: Callable[..., dict] | None = None,
    extractor: Callable[..., list[dict]] | None = None,
    grader_fn: Callable[..., list[dict]] | None = None,
    dry_run: bool = False,
) -> dict:
    """The whole run. The three callables exist so a test can run it with no network."""
    require_frontier(worker, "worker")
    require_frontier(grader, "grader")
    if researcher is None:
        configure(worker, grader)
    run_id = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    asked_at = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    report = (
        (researcher or research)(brief, deep) if researcher is None else researcher(brief, deep)
    )
    if not report.get("sources"):
        raise Refused("the worker returned a report with no sources; nothing is written")
    ideas = (extractor or extract_ideas)(report, brief, n, worker, market)
    if not ideas:
        raise Refused("no idea came out of the report; nothing is written")
    ideas = (grader_fn or grade_ideas)(ideas, report, grader, run_id)
    reports.mkdir(parents=True, exist_ok=True)
    report_path = reports / f"{run_id}.md"
    rows = rows_for(
        ideas,
        brief,
        market,
        worker,
        run_id,
        _rel(report_path),
        asked_at,
        report.get("costs_usd", 0.0),
    )
    if not dry_run:
        report_path.write_text(
            f"# {brief}\n\nrun {run_id}, worker {worker}, grader {grader}\n\n"
            f"{report['report']}\n\n## Sources\n\n"
            + "\n".join(f"- {s}" for s in report["sources"])
            + "\n"
        )
        for r in rows:
            ledger.append(r, ledger_path)
    return {
        "run_id": run_id,
        "ideas": len(rows),
        "scored": sum(1 for r in rows if r["score"] >= 0.5),
        "mean_score": round(sum(r["score"] for r in rows) / len(rows), 2),
        "report": str(report_path),
        "costs_usd": report.get("costs_usd", 0.0),
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=(__doc__ or "").split("\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="one brief in, N scored ideas on the ledger")
    r.add_argument("--brief", required=True)
    r.add_argument("--market", default="")
    r.add_argument("--ideas", type=int, default=3)
    r.add_argument(
        "--worker", default="claude", help=f"router lane, one of {sorted(FRONTIER_LANES)}"
    )
    r.add_argument(
        "--grader", default="gemini", help="router lane that grades; keep it a different one"
    )
    r.add_argument(
        "--deep", action="store_true", help="report_type=deep: recursive breadth/depth research"
    )
    r.add_argument("--dry-run", action="store_true", help="run everything, write nothing")
    r.add_argument("--ledger", type=pathlib.Path, default=ledger.LEDGER)
    a = ap.parse_args(argv)
    try:
        out = run(
            a.brief, a.market, a.ideas, a.worker, a.grader, a.deep, a.ledger, dry_run=a.dry_run
        )
    except Refused as e:
        print(f"REFUSED research-worker   {e}", file=sys.stderr)
        return 1
    print(
        f"ok      research-worker   run {out['run_id']}: {out['ideas']} ideas, {out['scored']} graded C or P, "
        f"mean {out['mean_score']}, {out['costs_usd']:.4f} USD, report {out['report']}"
    )
    for row in out["rows"]:
        print(
            f"        {row['grade']} {row['score']:.1f}  {row['title']}  ({row['price_hypothesis']})"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())

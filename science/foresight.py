#!/usr/bin/env python3
"""Foresight: predict a red CI run before the push, and score the prediction after (crew#405).

Founder, 2026-08-27: "lets get to Self-aware estate now asap". A self-aware estate is one that
writes down what it expects to happen, then grades itself. This is the first prediction with
free labels: every pull request in the estate already carries a first CI run, red or green.

    python3 science/foresight.py pull      # workflow runs + pull requests, four repos, to science/ci/
    python3 science/foresight.py train     # logistic regression, time-ordered holdout, honest metrics
    python3 science/foresight.py predict   # one row per open PR into science/predictions.jsonl
    python3 science/foresight.py score     # grade every unscored foresight row against the real run
    python3 science/foresight.py report    # what the model knows, and how often it was right

Every row it writes is in the same ledger outcomes.py keeps, so `outcomes.py rate` and the
showcase page count it with everything else. A model that cannot beat the base rate says so in
science/foresight-state.json and the page prints that sentence; it never prints a hit rate
without the base rate beside it. No history on disk is BLIND (exit 2), never a model.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import pathlib
import subprocess
import sys

SCIENCE = pathlib.Path(__file__).resolve().parent
CI = SCIENCE / "ci"
STATE = SCIENCE / "foresight-state.json"
PREDICTIONS = SCIENCE / "predictions.jsonl"
REPOS = ("crew", "idp", "claude-guards", "prospector")
OWNER = "chidionyema"
# Gates that grade the PR body or the review, not the code. A red one says nothing about the diff.
BODY_GATES = ("review-gate", "operating-model-gate", "spec-gate", "merge when green", "dupe", "evidence")
MODEL = "foresight"
MIN_ROWS = 40


def _jsonl(path: pathlib.Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _gh(args: list[str]) -> str:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


# ----------------------------------------------------------------------------- data

def cmd_pull(_args) -> int:
    CI.mkdir(exist_ok=True)
    for repo in REPOS:
        runs = _gh(["api", "--paginate", f"repos/{OWNER}/{repo}/actions/runs?per_page=100",
                    "-q", '.workflow_runs[] | {name, head_branch, conclusion, created_at, sha: .head_sha, event, id}'])
        (CI / f"runs-{repo}.jsonl").write_text(runs)
        prs = _gh(["pr", "list", "--repo", f"{OWNER}/{repo}", "--state", "all", "--limit", "1000", "--json",
                   "number,headRefName,changedFiles,additions,deletions,createdAt,mergedAt,closedAt,title,body,files"])
        rows = [dict(p, repo=repo) for p in json.loads(prs)]
        (CI / f"prs-{repo}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        print(f"{repo}: {runs.count(chr(10))} runs, {len(rows)} prs")
    return 0


def _history() -> tuple[list[dict], list[dict]]:
    runs, prs = [], []
    for repo in REPOS:
        r, p = CI / f"runs-{repo}.jsonl", CI / f"prs-{repo}.jsonl"
        if not r.exists() or not p.exists():
            continue
        runs += [dict(x, repo=repo) for x in _jsonl(r)]
        prs += _jsonl(p)
    return runs, prs


def label(pr: dict, runs: list[dict]) -> bool | None:
    """True if the first sha CI saw on this PR's branch had a code check go red.

    Body gates are excluded: a red review-gate is about the PR body, not the diff. None when no
    completed code run exists yet, so an open PR is never labelled by its absence of runs.
    """
    mine = [r for r in runs if r["repo"] == pr["repo"] and r["head_branch"] == pr["headRefName"]
            and r["event"] == "pull_request" and not any(g in (r["name"] or "").lower() for g in BODY_GATES)]
    if not mine:
        return None
    first_sha = min(mine, key=lambda r: r["created_at"])["sha"]
    first = [r for r in mine if r["sha"] == first_sha]
    if any(r["conclusion"] in (None, "") for r in first):
        return None
    return any(r["conclusion"] == "failure" for r in first)


FEATURES = ("log_files", "log_add", "log_del", "hour", "weekday", "f_test", "f_docs", "f_py", "f_yaml",
            "f_workflow", "t_fix", "t_test", "t_docs", "log_body", "has_session",
            "r_crew", "r_idp", "r_claude-guards", "r_prospector")


def features(pr: dict) -> list[float]:
    files = [f.get("path", "") for f in (pr.get("files") or [])]
    n = max(len(files), 1)
    frac = lambda pred: sum(1 for f in files if pred(f)) / n  # noqa: E731
    at = dt.datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))
    title = (pr.get("title") or "").lower()
    body = pr.get("body") or ""
    return [math.log1p(pr.get("changedFiles") or 0), math.log1p(pr.get("additions") or 0),
            math.log1p(pr.get("deletions") or 0), at.hour / 23, at.weekday() / 6,
            frac(lambda f: "/test" in f or f.startswith("tests/")), frac(lambda f: f.endswith(".md")),
            frac(lambda f: f.endswith(".py")), frac(lambda f: f.endswith((".yaml", ".yml"))),
            frac(lambda f: ".github/workflows" in f), float("fix" in title), float("test" in title),
            float("doc" in title), math.log1p(len(body)), float("author-session" in body.lower()),
            *[float(pr["repo"] == r) for r in REPOS]]


def dataset() -> tuple[list[list[float]], list[bool], list[dict]]:
    runs, prs = _history()
    X, y, keep = [], [], []
    for pr in sorted(prs, key=lambda p: p["createdAt"]):
        lab = label(pr, runs)
        if lab is None:
            continue
        X.append(features(pr)); y.append(lab); keep.append(pr)
    return X, y, keep


# ----------------------------------------------------------------------------- model

def _fit(X, y):
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, C=0.5)).fit(X, y)


def cmd_train(_args) -> int:
    runs, prs = _history()
    if not runs or not prs:
        print(f"BLIND: no history in {CI}; run `python3 science/foresight.py pull`", file=sys.stderr)
        return 2
    X, y, _ = dataset()
    if len(y) < MIN_ROWS:
        print(f"BLIND: {len(y)} labelled PRs, under the {MIN_ROWS} floor", file=sys.stderr)
        return 2
    cut = int(len(y) * 0.8)                       # time-ordered: the newest fifth is unseen
    model = _fit(X[:cut], y[:cut])
    probs = model.predict_proba(X[cut:])[:, 1]
    truth = y[cut:]
    pred = [p >= 0.5 for p in probs]
    acc = sum(p == t for p, t in zip(pred, truth, strict=True)) / len(truth)
    base = max(sum(truth), len(truth) - sum(truth)) / len(truth)
    brier = sum((p - float(t)) ** 2 for p, t in zip(probs, truth, strict=True)) / len(truth)
    tp = sum(p and t for p, t in zip(pred, truth, strict=True)); fp = sum(p and not t for p, t in zip(pred, truth, strict=True))
    fn = sum((not p) and t for p, t in zip(pred, truth, strict=True))
    coef = model.named_steps["logisticregression"].coef_[0]
    top = sorted(zip(FEATURES, coef, strict=True), key=lambda kv: -abs(kv[1]))[:5]
    state = {"trained_at": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%MZ"), "labelled_prs": len(y),
             "red_rate": round(sum(y) / len(y), 3), "holdout": len(truth), "holdout_accuracy": round(float(acc), 3),
             "holdout_base_rate": round(base, 3), "brier": round(float(brier), 3),
             "red_precision": round(float(tp) / (tp + fp), 3) if tp + fp else None,
             "red_recall": round(float(tp) / (tp + fn), 3) if tp + fn else None,
             "beats_base_rate": bool(acc > base), "top_features": [[k, round(float(v), 3)] for k, v in top],
             "verdict": ("model beats the base rate on unseen PRs" if acc > base else
                         "model does NOT beat the base rate; predictions are recorded but carry no claim")}
    STATE.write_text(json.dumps(state, indent=1) + "\n")
    for k, v in state.items():
        print(f"{k:<20} {v}")
    return 0


def _predictions() -> list[dict]:
    if not PREDICTIONS.exists():
        return []
    latest: dict = {}
    for r in _jsonl(PREDICTIONS):
        latest[r["id"]] = r
    return list(latest.values())


def cmd_predict(_args) -> int:
    runs, prs = _history()
    X, y, _ = dataset()
    if len(y) < MIN_ROWS:
        print(f"BLIND: {len(y)} labelled PRs, under the {MIN_ROWS} floor", file=sys.stderr)
        return 2
    model = _fit(X, y)
    done = {(r.get("repo"), r.get("pr")) for r in _predictions() if r.get("model") == MODEL}
    coef = model.named_steps["logisticregression"].coef_[0]
    scaler = model.named_steps["standardscaler"]
    rows = _predictions(); pid = max([r["id"] for r in rows], default=0)
    n = 0
    for pr in prs:
        if pr.get("closedAt") or pr.get("mergedAt") or (pr["repo"], pr["number"]) in done:
            continue
        if label(pr, runs) is not None:
            continue                              # CI already answered; a prediction now is hindsight
        x = features(pr)
        p = float(model.predict_proba([x])[0][1])
        z = (x - scaler.mean_) / scaler.scale_
        why = sorted(zip(FEATURES, z * coef, strict=True), key=lambda kv: -abs(kv[1]))[:3]
        pid += 1
        rec = {"id": pid, "at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
               "issue": f"{pr['repo']}#{pr['number']}",
               "step": f"first CI run goes {'RED' if p >= 0.5 else 'GREEN'} (p_red={p:.2f})",
               "because": "; ".join(f"{k} {'+' if v > 0 else '-'}{abs(v):.2f}" for k, v in why),
               "scored_at": None, "correct": None, "model": MODEL, "repo": pr["repo"], "pr": pr["number"],
               "p_red": round(p, 3), "predicted_red": p >= 0.5}
        with PREDICTIONS.open("a") as fh:
            fh.write(json.dumps(rec, separators=(",", ":")) + "\n")
        n += 1
        print(f"#{pid} {rec['issue']}: {rec['step']}  because {rec['because']}")
    print(f"{n} prediction(s) recorded, unscored")
    return 0


def cmd_score(_args) -> int:
    runs, prs = _history()
    by_key = {(p["repo"], p["number"]): p for p in prs}
    n = 0
    for r in _predictions():
        if r.get("model") != MODEL or r.get("scored_at"):
            continue
        pr = by_key.get((r["repo"], r["pr"]))
        actual = label(pr, runs) if pr else None
        if actual is None:
            continue
        rec = dict(r, scored_at=dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
                   correct=(actual == r["predicted_red"]), note=f"first run {'red' if actual else 'green'}")
        with PREDICTIONS.open("a") as fh:
            fh.write(json.dumps(rec, separators=(",", ":")) + "\n")
        n += 1
        print(f"#{r['id']} {r['issue']}: predicted {'red' if r['predicted_red'] else 'green'}, "
              f"was {'red' if actual else 'green'} -> {'CORRECT' if rec['correct'] else 'WRONG'}")
    print(f"{n} prediction(s) scored")
    return 0


def summary() -> dict:
    """What the showcase prints. BLIND fields are strings, never zeros."""
    state = json.load(STATE.open()) if STATE.exists() else None
    mine = [r for r in _predictions() if r.get("model") == MODEL]
    scored = [r for r in mine if r.get("scored_at")]
    hits = sum(1 for r in scored if r.get("correct"))
    return {"state": state, "recorded": len(mine), "scored": len(scored), "hits": hits,
            "hit_rate": round(100 * hits / len(scored)) if scored else None}


def cmd_report(_args) -> int:
    s = summary()
    if not s["state"]:
        print(f"BLIND: {STATE} absent; run train first", file=sys.stderr)
        return 2
    for k, v in s["state"].items():
        print(f"{k:<20} {v}")
    print(f"{'live predictions':<20} {s['recorded']} recorded, {s['scored']} scored, hit rate "
          f"{s['hit_rate'] if s['hit_rate'] is not None else 'n/a'}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("pull", cmd_pull), ("train", cmd_train), ("predict", cmd_predict),
                     ("score", cmd_score), ("report", cmd_report)):
        sub.add_parser(name).set_defaults(fn=fn)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())

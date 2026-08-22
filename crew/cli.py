"""crew — a conversation becomes a tracked, verified build.

The GitHub issue is the crew's shared memory. The PM writes it, engineering
posts evidence to it, QA runs the BDD suite and is the only role that can tick
a box. Hermes reads the same issue from your phone.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import __version__, bdd, board as B, config as C, gh
from .errors import CrewError
from .thread import Entry, latest, marker, parse_comments

EVIDENCE_TAIL = 6000


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def say(msg: str) -> None:
    print(msg)


def head(cfg: C.Config) -> str:
    p = subprocess.run(["git", "-C", str(cfg.root), "rev-parse", "--short", "HEAD"],
                       capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else "unknown"


def load_issue(cfg: C.Config, number: int) -> tuple[dict, B.Board, list[Entry]]:
    data = gh.issue_view(cfg.repo, number)
    return data, B.parse(data.get("body", "")), parse_comments(data.get("comments", []))


def details(title: str, text: str) -> str:
    tail = text[-EVIDENCE_TAIL:]
    if len(text) > EVIDENCE_TAIL:
        tail = "…(trimmed to the last %d characters)…\n%s" % (EVIDENCE_TAIL, tail)
    return f"<details><summary>{title}</summary>\n\n```\n{tail}\n```\n\n</details>"


# --------------------------------------------------------------------- init

def cmd_init(a) -> int:
    root = Path(a.path or os.getcwd()).resolve()
    if not (root / ".git").exists():
        raise CrewError(f"{root} is not a git repository")
    repo = a.repo or C.repo_from_git(root)
    data = {
        "repo": repo,
        "features_dir": a.features_dir,
        "specs_dir": a.specs_dir,
        "bdd_command": a.bdd_command,
        "bdd_cwd": a.bdd_cwd,
        "default_role": a.role or "engineering",
    }
    f = C.write(root, data)
    gitignore = root / ".gitignore"
    line = f"{C.STATE_DIR}/"
    existing = gitignore.read_text() if gitignore.exists() else ""
    if line not in existing:
        gitignore.write_text(existing + ("" if existing.endswith("\n") or not existing else "\n") + line + "\n")
    say(f"crew configured for {repo}\n  {f}")
    return 0


# --------------------------------------------------------------------- plan

def parse_brief(text: str) -> tuple[str, str, list[tuple[str, str]]]:
    """A brief is markdown: `# Title`, prose, then `- CP1: ...` lines."""
    title, cps, body = "", [], []
    for line in text.splitlines():
        s = line.strip()
        if not title and s.startswith("# "):
            title = s[2:].strip()
            continue
        if s.startswith("- CP") and ":" in s:
            cid, _, rest = s[2:].partition(":")
            cps.append((cid.strip(), rest.strip()))
            continue
        body.append(line)
    if not title:
        raise CrewError("the brief needs a `# Title` line")
    if not cps:
        raise CrewError("the brief needs at least one `- CP1: ...` checkpoint line")
    return title, "\n".join(body).strip(), cps


def cmd_plan(a) -> int:
    cfg = C.load()
    text = Path(a.brief).read_text() if a.brief != "-" else sys.stdin.read()
    title, prose, cps = parse_brief(text)

    spec_dir = cfg.root / cfg.specs_dir
    spec_dir.mkdir(parents=True, exist_ok=True)

    origin = (
        f"Distilled from conversation with @{a.author} on {datetime.now().date()}.\n"
        f"Spec: `{cfg.specs_dir}/SPEC.md` (replaced with the issue path once the number is known)."
    )
    board = B.Board(
        origin=origin,
        checkpoints=[B.Checkpoint(id=c, title=t) for c, t in cps],
    )
    for label, colour, desc in [
        ("crew", "5319e7", "Managed by the crew"),
        ("crew:blocked", "b60205", "The crew is blocked on this issue"),
    ]:
        gh.ensure_label(cfg.repo, label, colour, desc)

    number = gh.issue_create(cfg.repo, title, B.render(board), labels=["crew"])

    spec_path = spec_dir / f"issue-{number}.md"
    spec_path.write_text(
        f"# {title}\n\n"
        f"Issue: https://github.com/{cfg.repo}/issues/{number}\n"
        f"Written by pm-agent on {datetime.now().date()} from conversation with @{a.author}.\n\n"
        f"## What the founder asked for\n\n{prose}\n\n"
        f"## Checkpoints\n\n"
        + "\n".join(f"### {c}: {t}\n\nVerified by `{bdd.tag_for(c)}` in `{cfg.features_dir}/`.\n"
                    for c, t in cps)
        + "\n"
    )
    board = B.Board(
        origin=f"Distilled from conversation with @{a.author} on {datetime.now().date()}.\n"
               f"Spec: `{spec_path.relative_to(cfg.root)}`",
        checkpoints=board.checkpoints,
    )
    gh.issue_set_body(cfg.repo, number, B.render(board))

    C.write_state(cfg, {**C.read_state(cfg), "issue": number})
    if a.assignee:
        subprocess.run(["gh", "issue", "edit", str(number), "--repo", cfg.repo,
                        "--add-assignee", a.assignee], capture_output=True, text=True)
    gh.issue_comment(cfg.repo, number, (
        f"{marker(role='pm-agent', kind='opened')}\n"
        f"**pm-agent** ({now()}): issue opened from conversation. "
        f"{len(cps)} checkpoints. Spec at `{spec_path.relative_to(cfg.root)}`. "
        f"Engineering builds; qa-agent is the only role that can tick a box."
    ))
    say(f"issue #{number}: https://github.com/{cfg.repo}/issues/{number}")
    say(f"spec: {spec_path}")
    return 0


# --------------------------------------------------------------------- use

def cmd_use(a) -> int:
    cfg = C.load()
    data = gh.issue_view(cfg.repo, a.issue)
    C.write_state(cfg, {**C.read_state(cfg), "issue": int(a.issue)})
    say(f"active issue: #{data['number']} {data['title']}")
    return 0


# ------------------------------------------------------------------ status

def cmd_status(a) -> int:
    cfg = C.load()
    n = C.active_issue(cfg, a.issue)
    data, board, entries = load_issue(cfg, n)

    if a.format == "json":
        print(json.dumps({
            "issue": data["number"], "title": data["title"], "state": data["state"],
            "url": data["url"], "complete": board.complete,
            "done": board.done_count, "total": len(board.checkpoints),
            "checkpoints": [{"id": c.id, "title": c.title, "done": c.done} for c in board.checkpoints],
            "blockers": board.blockers,
            "verification": [r.__dict__ for r in board.rows],
        }, indent=2))
        return 0

    marks = []
    for c in board.checkpoints:
        if c.done:
            marks.append(f"{c.id}: DONE")
        elif latest(entries, kind="claim", cp=c.id):
            marks.append(f"{c.id}: BUILDING")
        else:
            marks.append(f"{c.id}: TODO")

    if a.format == "telegram":
        icon = {"DONE": "✅", "BUILDING": "\U0001f504", "TODO": "⏳"}
        line = " ".join(f"{m.split(':')[0]} {icon[m.split(': ')[1]]}" for m in marks)
        state = "BLOCKED" if board.blockers else ("DONE" if board.complete else "WORKING")
        print(f"*#{data['number']} {data['title']}*\n{state} — {board.done_count}/{len(board.checkpoints)}\n{line}"
              + ("\n⛔ " + "; ".join(board.blockers) if board.blockers else ""))
        return 0

    say(f"#{data['number']} {data['title']}  [{data['state']}]  {data['url']}")
    say(f"{board.done_count}/{len(board.checkpoints)} checkpoints verified")
    for m in marks:
        say("  " + m)
    if board.rows:
        say("verification log:")
        for r in board.rows[-8:]:
            say(f"  {r.cp}  {r.result}  {r.when}")
    if board.blockers:
        say("BLOCKED:")
        for b in board.blockers:
            say("  - " + b)
    return 0


# ------------------------------------------------------------------- claim

def cmd_claim(a) -> int:
    cfg = C.load()
    n = C.active_issue(cfg, a.issue)
    role = C.role(a.role, cfg)
    _, board, _ = load_issue(cfg, n)
    cp = a.cp.upper()
    if board.get(cp) is None:
        raise CrewError(f"{cp} is not on the checklist of #{n}")
    gh.issue_comment(cfg.repo, n, (
        f"{marker(role=role, kind='claim', cp=cp)}\n"
        f"**{role}** ({now()}): starting {cp} — {board.get(cp).title}. HEAD `{head(cfg)}`."
    ))
    say(f"{role} claimed {cp} on #{n}")
    return 0


# ---------------------------------------------------------------- evidence

def cmd_evidence(a) -> int:
    cfg = C.load()
    n = C.active_issue(cfg, a.issue)
    role = C.role(a.role, cfg)
    _, board, _ = load_issue(cfg, n)
    cp = a.cp.upper()
    if board.get(cp) is None:
        raise CrewError(f"{cp} is not on the checklist of #{n}")
    log = ""
    if a.log:
        p = Path(a.log)
        if not p.exists():
            raise CrewError(f"no such log file: {p}")
        log = p.read_text(errors="replace")
    body = (
        f"{marker(role=role, kind='evidence', cp=cp, result=a.result)}\n"
        f"**{role}** ({now()}): {cp} build {a.result.upper()}. {a.summary}\n\n"
        f"HEAD `{head(cfg)}`. This is a build report, not a verification — "
        f"the box stays unticked until qa-agent runs the suite.\n"
    )
    if log:
        body += "\n" + details(f"{cp} build log", log)
    gh.issue_comment(cfg.repo, n, body)
    say(f"{role} posted {a.result} evidence for {cp} on #{n} (box unchanged)")
    return 0


# ------------------------------------------------------------------ verify

def cmd_verify(a) -> int:
    cfg = C.load()
    n = C.active_issue(cfg, a.issue)
    role = C.role(a.role, cfg) if (a.role or os.environ.get("CREW_ROLE")) else "qa-agent"
    _, board, entries = load_issue(cfg, n)
    cp = a.cp.upper()
    if board.get(cp) is None:
        raise CrewError(f"{cp} is not on the checklist of #{n}")

    ev = latest(entries, kind="evidence", cp=cp)
    if ev is None and not a.force:
        raise CrewError(
            f"no build evidence for {cp} on #{n} — engineering runs `crew evidence {cp} …` first.\n"
            f"(`--force` verifies anyway; it is recorded in the log.)"
        )
    if ev is not None and ev.role == role and not a.force:
        raise CrewError(
            f"{role} posted the evidence for {cp} and cannot also verify it.\n"
            f"Run this as qa-agent (CREW_ROLE=qa-agent), or pass --force and own it."
        )

    features = cfg.root / cfg.features_dir
    tag = bdd.tag_for(cp)
    if bdd.find_feature(features, tag) is None:
        raise CrewError(f"no feature file under {features} carries the tag {tag}")

    say(f"running the suite for {cp} … (tag {tag})")
    res = bdd.run(cfg.root, cfg.bdd_command, cfg.bdd_cwd, cp, timeout=a.timeout)
    say(res.output[-2000:])

    sha = head(cfg)
    row = B.Row(cp=cp, result=res.verdict,
                evidence=f"{res.scenarios_passed} passed / {res.scenarios_failed} failed @ `{sha}`",
                when=now())
    board = board.add_row(row)

    if res.passed:
        board = board.tick(cp, True)
        board = board.with_blockers([b for b in board.blockers if not b.startswith(f"{cp}:")])
        verdict_line = f"**{role}** ({now()}): {cp} **VERIFIED**. {res.scenarios_passed} scenario(s) passed."
    else:
        reason = "the suite matched no scenarios" if res.ran_nothing else f"{res.scenarios_failed} scenario(s) failed"
        board = board.tick(cp, False)
        board = board.with_blockers(sorted(set(board.blockers) | {f"{cp}: {reason}"}))
        verdict_line = (f"**{role}** ({now()}): {cp} **NOT VERIFIED** — {reason}. "
                        f"Evidence insufficient, retry required. The box stays unticked.")

    gh.issue_set_body(cfg.repo, n, B.render(board))
    gh.issue_comment(cfg.repo, n, (
        f"{marker(role=role, kind='verdict', cp=cp, result='pass' if res.passed else 'fail')}\n"
        f"{verdict_line}\n\n`{res.command}` exit {res.exit_code}, HEAD `{sha}`.\n\n"
        + details(f"{cp} BDD output", res.output)
    ))

    if board.blockers:
        subprocess.run(["gh", "issue", "edit", str(n), "--repo", cfg.repo, "--add-label", "crew:blocked"],
                       capture_output=True, text=True)
    else:
        subprocess.run(["gh", "issue", "edit", str(n), "--repo", cfg.repo, "--remove-label", "crew:blocked"],
                       capture_output=True, text=True)

    say(f"{cp}: {res.verdict} — issue #{n} updated")
    if board.complete:
        say("every checkpoint is verified — `crew close` will close the issue")
    return 0 if res.passed else 1


# ------------------------------------------------------- block / comment

def cmd_block(a) -> int:
    cfg = C.load()
    n = C.active_issue(cfg, a.issue)
    role = C.role(a.role, cfg)
    _, board, _ = load_issue(cfg, n)
    board = board.with_blockers(sorted(set(board.blockers) | {a.reason}))
    gh.issue_set_body(cfg.repo, n, B.render(board))
    gh.issue_comment(cfg.repo, n, f"{marker(role=role, kind='blocked')}\n**{role}** ({now()}): BLOCKED — {a.reason}")
    subprocess.run(["gh", "issue", "edit", str(n), "--repo", cfg.repo, "--add-label", "crew:blocked"],
                   capture_output=True, text=True)
    say(f"#{n} blocked: {a.reason}")
    return 0


def cmd_unblock(a) -> int:
    cfg = C.load()
    n = C.active_issue(cfg, a.issue)
    role = C.role(a.role, cfg)
    _, board, _ = load_issue(cfg, n)
    kept = [b for b in board.blockers if a.match.lower() not in b.lower()] if a.match else []
    board = board.with_blockers(kept)
    gh.issue_set_body(cfg.repo, n, B.render(board))
    gh.issue_comment(cfg.repo, n, f"{marker(role=role, kind='unblocked')}\n**{role}** ({now()}): blocker cleared.")
    if not kept:
        subprocess.run(["gh", "issue", "edit", str(n), "--repo", cfg.repo, "--remove-label", "crew:blocked"],
                       capture_output=True, text=True)
    say(f"#{n} blockers now: {kept or 'none'}")
    return 0


def cmd_comment(a) -> int:
    cfg = C.load()
    n = C.active_issue(cfg, a.issue)
    role = C.role(a.role, cfg)
    gh.issue_comment(cfg.repo, n, f"{marker(role=role, kind='note')}\n**{role}** ({now()}): {a.text}")
    say(f"{role} commented on #{n}")
    return 0


def cmd_close(a) -> int:
    cfg = C.load()
    n = C.active_issue(cfg, a.issue)
    _, board, _ = load_issue(cfg, n)
    if not board.complete and not a.force:
        missing = [c.id for c in board.checkpoints if not c.done]
        raise CrewError(f"#{n} still has unverified checkpoints: {', '.join(missing)} (--force to close anyway)")
    gh.issue_close(cfg.repo, n, comment=(
        f"{marker(role='qa-agent', kind='closed')}\n"
        f"**qa-agent** ({now()}): every checkpoint verified by the suite. Closing."
    ))
    say(f"#{n} closed")
    return 0


# ------------------------------------------------------------------ doctor

def cmd_doctor(a) -> int:
    checks: list[tuple[str, bool, str]] = []

    p = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    checks.append(("gh authenticated", p.returncode == 0, (p.stdout + p.stderr).strip().splitlines()[-1] if (p.stdout or p.stderr) else ""))

    try:
        cfg = C.load()
        checks.append((f"config for {cfg.repo}", True, str(cfg.root / C.CONFIG_NAME)))
    except CrewError as e:
        checks.append(("config", False, str(e)))
        cfg = None

    if cfg:
        cmd = cfg.bdd_command.format(tag="@none", cp="none", CP="NONE").split()[0]
        exe = (cfg.root / cfg.bdd_cwd / cmd).resolve()
        found = exe.exists() or subprocess.run(["which", cmd], capture_output=True).returncode == 0
        checks.append((f"bdd runner `{cmd}`", bool(found), str(exe) if exe.exists() else cmd))

        feats = cfg.root / cfg.features_dir
        n_feats = len(list(feats.rglob("*.feature"))) if feats.is_dir() else 0
        checks.append((f"feature files in {cfg.features_dir}", n_feats > 0, f"{n_feats} found"))

        try:
            n = C.active_issue(cfg)
            data, board, _ = load_issue(cfg, n)
            checks.append((f"issue #{n} reachable", True,
                           f"{board.done_count}/{len(board.checkpoints)} verified — {data['url']}"))
        except CrewError as e:
            checks.append(("active issue", False, str(e)))

    width = max(len(c[0]) for c in checks)
    ok = True
    for name, good, detail in checks:
        ok = ok and good
        say(f"{'PASS' if good else 'FAIL'}  {name.ljust(width)}  {detail}")
    return 0 if ok else 1


# --------------------------------------------------------------------- main

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="crew", description=__doc__.splitlines()[0])
    p.add_argument("--version", action="version", version=f"crew {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    def issue_arg(sp):
        sp.add_argument("--issue", type=int, help="issue number (default: the active one)")
        sp.add_argument("--as", dest="role", help="role to post as (default $CREW_ROLE)")

    s = sub.add_parser("init", help="configure the crew for this repo")
    s.add_argument("--path")
    s.add_argument("--repo")
    s.add_argument("--features-dir", default="features")
    s.add_argument("--specs-dir", default="docs/specs")
    s.add_argument("--bdd-command", default=C.Config.bdd_command)
    s.add_argument("--bdd-cwd", default=".")
    s.add_argument("--role")
    s.set_defaults(fn=cmd_init)

    s = sub.add_parser("plan", help="pm-agent: turn a brief into a spec and a GitHub issue")
    s.add_argument("brief", help="path to the brief markdown, or - for stdin")
    s.add_argument("--author", default=os.environ.get("CREW_FOUNDER", "founder"))
    s.add_argument("--assignee")
    s.set_defaults(fn=cmd_plan)

    s = sub.add_parser("use", help="set the active issue for this repo")
    s.add_argument("issue", type=int)
    s.set_defaults(fn=cmd_use)

    s = sub.add_parser("status", help="read the board")
    s.add_argument("--issue", type=int)
    s.add_argument("--format", choices=["text", "json", "telegram"], default="text")
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("claim", help="engineering: say you are starting a checkpoint")
    s.add_argument("cp")
    issue_arg(s)
    s.set_defaults(fn=cmd_claim)

    s = sub.add_parser("evidence", help="engineering: post a build report (never ticks a box)")
    s.add_argument("cp")
    s.add_argument("--result", choices=["pass", "fail"], required=True)
    s.add_argument("--summary", required=True)
    s.add_argument("--log")
    issue_arg(s)
    s.set_defaults(fn=cmd_evidence)

    s = sub.add_parser("verify", help="qa-agent: run the suite and tick the box only if it passes")
    s.add_argument("cp")
    s.add_argument("--timeout", type=int, default=3600)
    s.add_argument("--force", action="store_true", help="verify without engineering evidence")
    issue_arg(s)
    s.set_defaults(fn=cmd_verify)

    s = sub.add_parser("block", help="record a blocker on the board")
    s.add_argument("reason")
    issue_arg(s)
    s.set_defaults(fn=cmd_block)

    s = sub.add_parser("unblock", help="clear blockers")
    s.add_argument("match", nargs="?")
    issue_arg(s)
    s.set_defaults(fn=cmd_unblock)

    s = sub.add_parser("comment", help="post a note to the crew thread")
    s.add_argument("text")
    issue_arg(s)
    s.set_defaults(fn=cmd_comment)

    s = sub.add_parser("close", help="close the issue once every box is ticked")
    s.add_argument("--force", action="store_true")
    issue_arg(s)
    s.set_defaults(fn=cmd_close)

    s = sub.add_parser("doctor", help="prove the crew is wired up")
    s.set_defaults(fn=cmd_doctor)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args)
    except CrewError as e:
        print(f"crew: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

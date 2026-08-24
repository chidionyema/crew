#!/usr/bin/env python3
"""Did the fix actually stop him having to say it again.

WHY THIS EXISTS. Founder, 2026-08-24: "we dotjustneed lways we need prootccols that all
agebnt folow", and "in tired of repearting instructino that are fucking autibantabkle and
enforcable yet dday by fucjig day".

He is right that a law is not a protocol, and the missing piece has a name outside this
estate. 21 CFR 820.100, the corrective and preventive action requirement, is the audited
standard for exactly this problem and it asks for two things this estate has never done:

  820.100(a)(1) -- "Analyzing processes, work operations, concessions, quality audit
  reports, quality records, service records, COMPLAINTS, returned product, and other
  sources of quality data to identify existing and potential causes of nonconforming
  product", using "appropriate statistical methodology".

  820.100(a)(4) -- "Verifying or validating the corrective and preventive action to
  ensure that such action IS EFFECTIVE and does not adversely affect the finished device".

  820.100(b) -- "All activities required under this section, and their results, shall be
  documented."

Read against this estate: his complaints are the quality data, and science/friction.py is
the statistical analysis of them. A law is a corrective action. What has never existed is
(a)(4). The estate writes a law, declares the matter closed, and never once goes back to
the data to ask whether the complaint stopped. So laws accumulate and the complaint rate
does not move, which is precisely what he is describing.

Notably, the Google SRE book's postmortem chapter does NOT answer this. Fetched
2026-08-24: it defines blamelessness well -- "you can't 'fix' people, but you can fix
systems and processes" -- and says postmortems carry "the follow-up actions to prevent
the incident from recurring", but it specifies nobody to track them and no verification
that they worked. The regulated-industry answer is the stronger one here.

WHAT THIS IS. The register is GitHub issues labelled `capa` on chidionyema/crew, because
the founder ordered on 2026-08-24 that the board is issues and nothing is to be reinvented
badly. Nothing new is stored on this laptop. Each record names his words, the date he
first said them, the action taken, and the date that action landed. This then goes back to
the transcripts and asks whether he has said it since.

    python3 science/capa.py                 # the register and every verdict
    python3 science/capa.py --check         # exit 1 if any action is proven ineffective
    python3 science/capa.py --post          # write each verdict back onto its issue

WHAT A PASS DOES NOT MEAN, SAID HERE RATHER THAN DISCOVERED LATER. The check can only
ever report that he has not repeated a complaint IN THOSE WORDS. He types fast and does
not correct typos, so a phrase spelled a second way reads as silence. The verdict is
therefore named NO RECURRENCE and never EFFECTIVE, because the first is what was measured
and the second is a claim about the world. A record that has never recurred is evidence,
not proof, and it stays open until the window is wide enough to mean something.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

SCRIPTS = os.path.expanduser("~/.claude/scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
try:
    from founder_board import _founder_messages, _walk_transcripts
except ImportError as exc:                                   # pragma: no cover
    sys.exit(f"cannot import the founder-message parsers from {SCRIPTS}/founder_board.py: {exc}")

REPO = os.environ.get("CAPA_REPO", "chidionyema/crew")
LABEL = os.environ.get("CAPA_LABEL", "capa")

#: How long a record has to sit quiet before its silence is worth anything. Seven days is
#: the estate's own cadence: he works every day, so a week with no repeat is a week of
#: chances not taken. Anything shorter reads as proof after one quiet afternoon.
QUIET_DAYS = float(os.environ.get("CAPA_QUIET_DAYS", "7"))

BLOCK = re.compile(r"<!--\s*capa\s*(.*?)-->", re.S)


def parse_record(issue: dict) -> dict | None:
    """The machine-readable block inside a CAPA issue body.

    An issue carrying the label but no block is a real finding, not a thing to skip
    quietly: somebody filed a corrective action with nothing to check it against.
    """
    m = BLOCK.search(issue.get("body") or "")
    if not m:
        return {"number": issue["number"], "title": issue["title"],
                "state": (issue.get("state") or "").upper(), "malformed": True}
    rec: dict = {"number": issue["number"], "title": issue["title"],
                 "state": (issue.get("state") or "").upper(), "malformed": False}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        rec[k.strip()] = v.strip().strip('"')
    missing = [k for k in ("complaint", "phrase", "action", "landed") if not rec.get(k)]
    if missing:
        rec["malformed"] = True
        rec["missing"] = missing
    return rec


def issues() -> list[dict]:
    """Every CAPA record. A network failure is said out loud, never rendered as an empty register."""
    try:
        out = subprocess.run(
            ["gh", "issue", "list", "--repo", REPO, "--label", LABEL, "--state", "all",
             "--limit", "200", "--json", "number,title,body,state"],
            capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as exc:
        sys.exit(f"cannot reach the register on {REPO}: {exc}")
    if out.returncode != 0:
        sys.exit(f"cannot read the register on {REPO}: {out.stderr.strip()}")
    return json.loads(out.stdout or "[]")


def said_since(phrases: list[str], since_epoch: float) -> list[dict]:
    """Every founder message since `since_epoch` containing any of these phrases.

    One pass over the transcripts answers every record at once. Walking the corpus once
    per record would multiply a four-gigabyte read by the size of the register.
    """
    now = time.time()
    hits: list[dict] = []
    low_phrases = [p.lower() for p in phrases if p]
    for path, mtime in _walk_transcripts():
        if mtime < since_epoch:
            continue
        session = os.path.basename(os.path.dirname(path))[-12:]
        for ts, text in _founder_messages(path):
            if not ts or ts < since_epoch or ts > now:
                continue
            low = " ".join(text.split()).lower()
            for p in low_phrases:
                if p in low:
                    hits.append({"at": ts, "phrase": p, "session": session,
                                 "text": " ".join(text.split())})
    return hits


def iso(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%d %H:%M")


def epoch_of(stamp: str) -> float:
    """A `landed:` date, as epoch. A record whose date will not parse is malformed, not old."""
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
        try:
            d = datetime.strptime(stamp, fmt)
            return d.replace(tzinfo=d.tzinfo or timezone.utc).timestamp()
        except ValueError:
            continue
    return 0.0


def judge(records: list[dict]) -> list[dict]:
    """Each record's verdict, from one pass over the transcripts."""
    live = [r for r in records if not r.get("malformed")]
    for r in live:
        r["landed_at"] = epoch_of(r.get("landed", ""))
    dated = [r for r in live if r["landed_at"]]
    for r in live:
        if not r["landed_at"]:
            r["malformed"], r["missing"] = True, ["landed (will not parse)"]

    if dated:
        floor = min(r["landed_at"] for r in dated)
        all_hits = said_since([r["phrase"] for r in dated], floor)
    else:
        all_hits = []

    now = time.time()
    for r in dated:
        mine = [h for h in all_hits
                if h["phrase"] == r["phrase"].lower() and h["at"] >= r["landed_at"]]
        quiet_days = (now - r["landed_at"]) / 86400
        r["repeats"] = sorted(mine, key=lambda h: h["at"])
        if mine:
            r["verdict"] = "REPEATED"
        elif quiet_days >= QUIET_DAYS:
            r["verdict"] = "NO RECURRENCE"
        else:
            r["verdict"] = "TOO SOON"
        r["quiet_days"] = quiet_days
    return records


def render(r: dict) -> str:
    if r.get("malformed"):
        return (f"  MALFORMED      #{r['number']}  {r['title'][:60]}\n"
                f"                 missing {', '.join(r.get('missing', ['the capa block']))}, "
                f"so nothing can check it")
    body = [f"  {r['verdict']:<14} #{r['number']}  {r['title'][:60]}",
            f"                 his words : \"{r['complaint'][:90]}\"",
            f"                 action    : {r['action']}",
            f"                 landed    : {r['landed']}  ({r['quiet_days']:.1f} days ago)"]
    if r["verdict"] == "REPEATED":
        body.append(f"                 he said it again {len(r['repeats'])}x since:")
        for h in r["repeats"][:3]:
            body.append(f"                   {iso(h['at'])}  session {h['session']}  "
                        f"\"{h['text'][:80]}\"")
    elif r["verdict"] == "TOO SOON":
        body.append(f"                 quiet, but {QUIET_DAYS - r['quiet_days']:.1f} days short of "
                    f"a window worth believing")
    else:
        body.append(f"                 not said again in these words since it landed")
    return "\n".join(body)


def post(r: dict) -> None:
    if r.get("malformed"):
        return
    lines = [f"**Effectiveness check — {r['verdict']}**", "",
             f"Action `{r['action']}` landed {r['landed']}, {r['quiet_days']:.1f} days ago."]
    if r["verdict"] == "REPEATED":
        lines.append(f"He has said it again {len(r['repeats'])} time(s) since:")
        lines += [f"- `{iso(h['at'])}` session {h['session']} — {h['text'][:200]}"
                  for h in r["repeats"][:5]]
        lines.append("")
        lines.append("The corrective action did not hold. This record does not close.")
    elif r["verdict"] == "NO RECURRENCE":
        lines.append(f"He has not repeated it in these words in {r['quiet_days']:.0f} days. "
                     f"That is evidence, not proof: the check matches his exact phrasing and "
                     f"he does not correct typos, so a second spelling reads as silence.")
    else:
        lines.append(f"Quiet so far, {QUIET_DAYS - r['quiet_days']:.1f} days short of the "
                     f"{QUIET_DAYS:.0f}-day window. No verdict yet.")
    subprocess.run(["gh", "issue", "comment", str(r["number"]), "--repo", REPO,
                    "--body", "\n".join(lines)], check=False, timeout=60)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any corrective action has been proven ineffective")
    ap.add_argument("--post", action="store_true", help="write each verdict onto its issue")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = issues()
    if not raw:
        print(f"no CAPA records on {REPO} labelled `{LABEL}`.")
        print("An empty register is not a clean estate. It means no complaint has ever been "
              "turned into a tracked corrective action with a check on it.")
        return 1 if args.check else 0

    records = judge([parse_record(i) for i in raw])
    if args.json:
        print(json.dumps(records, indent=2, default=str))
        return 0

    print(f"register : {REPO}, label `{LABEL}`, {len(records)} record(s)")
    print(f"a record is believed quiet only after {QUIET_DAYS:.0f} days\n")
    for r in records:
        print(render(r))
        print()
        if args.post:
            post(r)

    repeated = [r for r in records if r.get("verdict") == "REPEATED"]
    malformed = [r for r in records if r.get("malformed")]
    #: THE enforcement point, and deliberately the only one. A repeated complaint is not
    #: made false by somebody clicking Close, so closing a record whose complaint is still
    #: recurring is the one move this refuses. It is narrow on purpose (LAW 38): failing
    #: every unrelated pull request because the founder is still annoyed would be a guard
    #: that refuses correct work, and it would be switched off within a day.
    closed_but_repeating = [r for r in repeated if r.get("state") == "CLOSED"]
    print(f"REPEATED after a fix : {len(repeated)}")
    print(f"no recurrence yet    : {sum(1 for r in records if r.get('verdict') == 'NO RECURRENCE')}")
    print(f"too soon to say      : {sum(1 for r in records if r.get('verdict') == 'TOO SOON')}")
    print(f"unmeasurable         : {len(malformed)}")
    if closed_but_repeating:
        print(f"\nCLOSED WHILE STILL RECURRING: "
              f"{', '.join('#' + str(r['number']) for r in closed_but_repeating)}")
        print("A corrective action is closed when the complaint stops, not when somebody "
              "decides it is finished (21 CFR 820.100(a)(4)).")
    if malformed:
        print(f"\nUNMEASURABLE: {', '.join('#' + str(r['number']) for r in malformed)} carry the "
              f"label with nothing to check them against, which is a corrective action with "
              f"no effectiveness check and therefore not a CAPA record at all.")
    return 1 if (args.check and (closed_but_repeating or malformed)) else 0


if __name__ == "__main__":
    sys.exit(main())

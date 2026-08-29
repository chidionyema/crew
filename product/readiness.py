"""crew#609 CP2: the product readiness scorecard, generated from what runs.

Founder, 2026-08-28: a product function like science; "a needle and lens through the whole
estate for commercial and also product readiness, especially from 2 lenses: selling to a
founder or engineer or team, and also the customer/public facing angle: prospector and the
personal agents"; "we also need to be prepared for glasses and robots, always forward looking";
"needs collab with science and research".

Every row is graded from a file or a tree the grader can read. A source it cannot read is
BLIND with the path it looked for, never green and never silently amber (memory
`silent-green-is-the-defect-class`). Hermes rows print first whatever their colour: the founder
called the agent the future of the business. No path is a literal: the estate root comes from
ESTATE_ROOT or the parent of this checkout (LAW 46).
"""
# Rejected: Backstage Tech Insights / scorecard plugins -- they grade catalog entities from
#   fact retrievers over HTTP, not files and trees on the estate root, and cannot read hermes,
#   prospector or science proofs that live only on disk; SonarQube/Allure grade code, not readiness.
# Standard: docs/STANDARDS.md row "Observability" (one query surface) and row "GitOps" -- this
#   grader reads the trees those rows name and writes two Markdown pages, no store of its own.
# Deviation: none -- it is a report generator over existing artefacts, not a platform layer.
from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import sys
from email.utils import parsedate_to_datetime

HERE = pathlib.Path(__file__).resolve().parent
CREW = HERE.parent
STALE_DAYS = 30
BAND_USD = (20, 50)  # personal-agent price band, CHARTER.md market facts
COMMERCIAL = re.compile(r"stripe|billing|checkout|signup|sign-up|subscription", re.I)

HORIZONS = [
    ("consumer smart glasses", "voice-only walk of the ten hermes tasks (proxy: no screen)"),
    ("voice-first wearables", "same ten tasks over a voice adapter, completion rate"),
    ("home and workplace robots", "one tool call from the agent core to a robot SDK stub"),
    ("in-car agents", "hands-free surface: the ten tasks by voice with no confirmation taps"),
]


def estate_root() -> pathlib.Path:
    return pathlib.Path(os.environ.get("ESTATE_ROOT") or CREW.parent).resolve()


def research_ids(ledger: pathlib.Path) -> set[str]:
    """R-row and horizon ids that a science ledger row cites; the handshake with science."""
    if not ledger.exists():
        return set()
    out: set[str] = set()
    for line in ledger.read_text().splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        blob = json.dumps(row)
        out.update(re.findall(r"\bR-[A-Z]\d\b", blob))
        out.update(h for h, _ in HORIZONS if h in blob)
    return out


def authority_clock(run=subprocess.run) -> dt.date | None:
    """Today's date from GitHub's own `Date` header, never from this machine (crew#583, idp#669).

    A proof's **Date:** line was stamped by a person on the day they ran the checkout; the age
    graded here is that stamp against a clock the estate trusts. This Mac's clock is not one
    (RTC reset to 1970 on 2026-08-27; founder 2026-08-28: "eliminate absolute trust in the local
    machine's clock"). No header is None, and the caller grades BLIND -- never a fall back.
    """
    try:
        out = run(["gh", "api", "-i", "-X", "GET", "rate_limit"], capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    for line in out.splitlines():
        name, _, value = line.partition(":")
        if name.strip().lower() == "date" and value.strip():
            try:
                return parsedate_to_datetime(value.strip()).date()
            except (TypeError, ValueError):
                return None
    return None


def _proof_age(path: pathlib.Path, today: dt.date | None) -> tuple[str | None, int | None]:
    """(verdict, age in days). Age is None when the proof has no date, the estate has no clock,
    or the stamp lies in the future of that clock -- each of those is unmeasured, not fresh."""
    text = path.read_text()
    m = re.search(r"\*\*Verdict:\*\*\s*(.+)", text)
    d = re.search(r"\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})", text)
    verdict = m.group(1).strip() if m else None
    age = (today - dt.date.fromisoformat(d.group(1))).days if (d and today) else None
    if age is not None and age < 0:
        age = None
    return verdict, age


def grade_prospector(root: pathlib.Path, today: dt.date | None) -> list[dict]:
    base = root / "prospector-main"
    proof = base / "store/launch/checkout-proof.md"
    cfg = base / "config.yaml"
    if not base.is_dir():
        return [_row("prospector", "B", "pay path", "BLIND", f"looked for {_rel(base)}")]
    rows = []
    if not proof.exists():
        rows.append(_row("prospector", "B", "pay path", "BLIND", f"looked for {_rel(proof)}"))
    else:
        verdict, age = _proof_age(proof, today)
        if not verdict or "ALL" not in verdict.upper():
            rows.append(_row("prospector", "B", "pay path", "red", f"verdict: {verdict}"))
        elif age is None:
            rows.append(_row("prospector", "B", "pay path", "BLIND",
                             f"{verdict}, but its age is unmeasured (no trusted clock, no **Date:** line, or a stamp in the future)"))
        elif age > STALE_DAYS:
            rows.append(_row("prospector", "B", "pay path", "amber",
                             f"{verdict}, but proof is {age} days old (> {STALE_DAYS})"))
        else:
            rows.append(_row("prospector", "B", "pay path", "green", f"{verdict}, {age} days old"))
    if not cfg.exists():
        rows.append(_row("prospector", "B", "price", "BLIND", f"looked for {_rel(cfg)}"))
    else:
        text = cfg.read_text()
        rungs = re.search(r"^\s*rungs:\s*\[([\d, ]+)\]", text, re.M)
        hypo = re.search(r"rungs.*HYPOTHESIS|HYPOTHESIS.*rungs", text, re.S | re.I)
        if not rungs:
            rows.append(_row("prospector", "B", "price", "red", "no rungs in config.yaml"))
        elif hypo:
            rows.append(_row("prospector", "B", "price", "amber",
                             f"rungs [{rungs.group(1).strip()}] pence, config says HYPOTHESIS (R-P1)"))
        else:
            rows.append(_row("prospector", "B", "price", "green", f"rungs [{rungs.group(1).strip()}]"))
    rows.append(_row("prospector", "B", "help and cancel path", "red", "no walk recorded (R-P2, CP5)"))
    return rows


def grade_hermes(root: pathlib.Path) -> list[dict]:
    base = root / "hermes-v2"
    if not base.is_dir():
        return [_row("hermes", "B", "pay path", "BLIND", f"looked for {_rel(base)}")]
    hits = []
    for p in list(base.glob("*.md")) + list(base.glob("docs/**/*.md")) + list(base.glob("*.yaml")):
        try:
            if COMMERCIAL.search(p.read_text()):
                hits.append(str(p.relative_to(base)))
        except (UnicodeDecodeError, OSError):
            continue
    rows = []
    real = [h for h in hits if "billing" in h.lower() or "signup" in h.lower() or "pricing" in h.lower()]
    if real:
        rows.append(_row("hermes", "B", "pay path", "amber", "commercial files exist, unwalked: " + ", ".join(real[:3])))
    else:
        rows.append(_row("hermes", "B", "pay path", "red",
                         f"no signup, billing or pricing file in hermes-v2 ({len(hits)} incidental mentions) (R-H3)"))
    readme = base / "README.md"
    cost = re.search(r"\*\*\$([\d.]+)/month\*\*", readme.read_text()) if readme.exists() else None
    if cost:
        usd = float(cost.group(1))
        inside = BAND_USD[0] <= usd <= BAND_USD[1]
        rows.append(_row("hermes", "B", "price vs run cost", "amber" if inside else "red",
                         f"run cost ${usd}/month {'inside' if inside else 'outside'} the ${BAND_USD[0]}-{BAND_USD[1]} band; no price named (R-H1)"))
    else:
        rows.append(_row("hermes", "B", "price vs run cost", "BLIND", f"no **$N/month** cost line in {_rel(readme)}"))
    rows.append(_row("hermes", "B", "surface-agnostic core", "red", "one surface (Telegram); no screenless walk (R-H4)"))
    rows.append(_row("hermes", "B", "second tenant", "red", "gateway is a launchd job on one Mac (R-H2)"))
    return rows


def grade_idp(root: pathlib.Path) -> list[dict]:
    base = root / "idp"
    if not base.is_dir():
        return [_row("idp", "A", "install path", "BLIND", f"looked for {_rel(base)}")]
    n = sum(1 for _ in base.rglob("catalog-info.yaml") if "node_modules" not in _.parts)
    rows = [_row("idp", "A", "catalog", "green" if n else "red", f"{n} catalog entities")]
    sku = base / "docs/product/SKU.md"
    rows.append(_row("idp", "A", "SKU, licence, support tier",
                     "amber" if sku.exists() else "red",
                     f"{sku.relative_to(base)} {'exists, ungraded' if sku.exists() else 'absent'} (R-A1)"))
    floor = base / "drills/portability-floor.txt"
    rows.append(_row("idp", "A", "install path (portability drill)",
                     "amber" if floor.exists() else "BLIND",
                     f"floor file {'present' if floor.exists() else 'absent'}: {_rel(floor)}; green only on a green run (R-A2)"))
    return rows


def _rel(p: pathlib.Path) -> str:
    """Never print a home directory (LAW 46): paths in reasons are relative to the estate root."""
    try:
        return str(p.relative_to(estate_root()))
    except ValueError:
        return str(p.relative_to(p.parents[2])) if len(p.parents) > 2 else p.name


def _row(asset: str, lens: str, step: str, status: str, reason: str) -> dict:
    return {"asset": asset, "lens": lens, "step": step, "status": status, "reason": reason}


def grade(root: pathlib.Path, today: dt.date | None = None) -> dict:
    # `today` is the authority's clock or None; never dt.date.today() (crew#583).
    rows = grade_hermes(root) + grade_prospector(root, today) + grade_idp(root)
    ids = research_ids(CREW / "science/RESEARCH-LEDGER.jsonl")
    for r in rows:
        m = re.search(r"\((R-[A-Z]\d)", r["reason"])
        r["research"] = ("linked" if m.group(1) in ids else "BLIND") if m else "-"
    horizons = [{"surface": h, "experiment": e, "research": "linked" if h in ids else "BLIND"}
                for h, e in HORIZONS]
    return {"date": today.isoformat() if today else "BLIND", "root": str(root), "rows": rows, "horizons": horizons}


def render(g: dict) -> str:
    out = [f"# Product readiness (generated {g['date']} by `bin/product-readiness`; do not edit)", "",
           "Stealth until `bootstrap` on crew#609. Hermes first: the founder called the personal agent",
           "the future of the business. BLIND = the grader could not read the source it names.", "",
           "| Asset | Lens | Step | Status | Why | Science |", "|---|---|---|---|---|---|"]
    for r in g["rows"]:
        out.append(f"| {r['asset']} | {r['lens']} | {r['step']} | **{r['status']}** | {r['reason']} | {r['research']} |")
    counts = {}
    for r in g["rows"]:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    out += ["", "Totals: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())), ""]
    return "\n".join(out)


def render_horizons(g: dict) -> str:
    out = [f"# Horizons (generated {g['date']}; do not edit)", "",
           "Founder, 2026-08-28: glasses, robots, always forward looking. One science experiment per",
           "surface; a horizon with no experiment is a wish (LAW 44). `Science` is linked when a",
           "research-ledger row names the surface.", "",
           "| Surface | Experiment | Science |", "|---|---|---|"]
    out += [f"| {h['surface']} | {h['experiment']} | {h['research']} |" for h in g["horizons"]]
    return "\n".join(out) + "\n"


def check(g: dict) -> list[str]:
    errs = []
    if len({r["asset"] for r in g["rows"]}) < 3:
        errs.append("fewer than 3 assets graded")
    if not g["rows"] or g["rows"][0]["asset"] != "hermes":
        errs.append("hermes is not the first row")
    if g["rows"] and all(r["status"] == "BLIND" for r in g["rows"]):
        errs.append(f"every row is BLIND: the grader read nothing under {g['root']}")
    if g["date"] == "BLIND":
        errs.append("no trusted clock: GitHub's Date header did not come back, so no age was measured")
    for r in g["rows"]:
        if r["status"] not in {"green", "amber", "red", "BLIND", "stealth-held"} or not r["reason"]:
            errs.append(f"malformed row: {r}")
    return errs


def main(argv: list[str]) -> int:
    g = grade(estate_root(), authority_clock())
    if "--json" in argv:
        print(json.dumps(g, indent=1))
        return 0
    errs = check(g)
    if "--check" in argv:
        for e in errs:
            print("FAIL", e)
        print(f"product-readiness: {len(g['rows'])} rows, {sum(r['status']=='BLIND' for r in g['rows'])} BLIND, {len(errs)} errors")
        return 1 if errs else 0
    if g["date"] == "BLIND":
        # No trusted clock: exit rather than replace yesterday's measured page with an unmeasured one
        # (idp#623 served_now rule; crew#610 review).
        print("BLIND product-readiness: no trusted clock, pages left as they were")
        return 1
    (CREW / "docs/product/READINESS.md").write_text(render(g))
    (CREW / "docs/product/HORIZONS.md").write_text(render_horizons(g))
    print(render(g))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

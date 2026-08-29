"""The docs named 47 files that exist nowhere in the estate, and nothing had ever checked.

Measured 2026-08-29 across 297 tracked markdown files in `crew` and `idp`: relative markdown
links were clean (0 broken in either repo), but 63 backticked file paths written in prose pointed
at nothing. Most were not typos -- they were cross-repo references written as if the reader were
standing in the other repo (`drills/catalogue.yaml` from crew, meaning `idp/drills/catalogue.yaml`),
so a founder or a buyer's engineer following the sentence lands nowhere and cannot tell whether
the file moved, was deleted, or never existed.

Rung 3, incident test. The trap this closes is that prose is unexecutable: a path in a sentence
is a claim about the repository, and until something reads it back, it decays silently the moment
a file moves. Every other claim in this estate has to carry a receipt; this one did not.

The ratchet is `ALLOWED` below. A path is allowed only with a reason on the line, and the reason
has to say why the file is legitimately absent -- not "we have not got to it yet". Adding a name
here is a decision someone can read; leaving a dead path in the prose was not.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Every repo in `~/dev/code` a doc may point into. A path starting with one of these names is a
#: cross-repo reference, and CI checks out one repo, so it cannot be resolved here. Repointing the
#: 34 bare paths into this form was most of the fix; a prefix at least tells the reader WHERE.
SIBLINGS = {"crew", "idp", "prospector", "prospector-main", "hermes-v2", "hermes-audit",
            "survival-stack", "maestro", "agent-guard", "ebookStore", "ecommerce-clean",
            "QAlgo", "mumchimp-medusa", "e26-rescue", "forex_trend_prediction"}

#: A backticked token with a slash and a source-file extension. Deliberately narrow: prose is full
#: of bare words in backticks, and grading those would be grading English.
TICK = re.compile(r'`([A-Za-z0-9_./-]+\.(?:py|sh|tf|ya?ml|md|rego|json|ts|go))`')

#: Placeholders in templates (`docs/decisions/NNNN-title.md`) name a shape, not a file.
PLACEHOLDER = re.compile(r"NNNN|issue-N\.|<[a-z]+>|\.\.\.")

#: path -> why it is legitimately absent. Read this as a list of things the estate has NOT got.
ALLOWED = {
    # The finding IS that nothing writes it. Repointing this would delete the finding.
    "store/ops/method_metrics.json":
        "science/FINDINGS-01: the file has no live writer, which is the finding itself",
    # Deliverables ROAD-TO-9D commits to, named before they are written, on purpose.
    "docs/DECISION-RIGHTS.md": "a ROAD-TO-9D deliverable, not yet written",
    "docs/MANIFESTO.md": "a ROAD-TO-9D deliverable, not yet written",
    "docs/product/LEDGER.md": "a CHARTER deliverable, not yet written",
    "docs/specs/issue-44.md": "the spec for crew#44 was never written; the sentence records that",
    # Things that were removed, in docs whose subject is the removal.
    "./deploy/fly/finish-cutover.sh":
        "MAC-EXIT describes leaving Fly (R1-no-fly-revival); the script is gone with it",
    ".github/workflows/deadman.yml":
        "crew#163: the deadman is a Healthchecks ping, never a workflow -- this names the thing "
        "that was rejected",
    "policy/feed.rego": "the feed rules moved into feed-guard.py; LANES.md still names the old file",
    "agent/monitoring/otlp_exporter.py": "the hermes agent tree it belonged to is retired",
    "scheduler/run_scheduled.py": "superseded by the Dagster schedules (crew#247)",
    # A dated research note quoting an artefact from a worktree that no longer exists.
    ".claude/worktrees/agent-aaecfffaa54620133/store/dossiers/79e36b3878b6d081.kill.json":
        "a 2026-08-25 research step quoting a worktree artefact, kept verbatim as evidence",
}


def _tracked_markdown() -> list[str]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "*.md", "**/*.md"],
                         capture_output=True, text=True, check=True).stdout
    return sorted(set(out.split()))


def _is_generated(rel: str) -> bool:
    """A path .gitignore covers is written by a run, so it is absent in a clean checkout and
    present after one. `science/foresight-state.json` is real; refusing it would be a guard that
    refuses correct work (LAW 38)."""
    return subprocess.run(["git", "-C", str(ROOT), "check-ignore", "-q", rel]).returncode == 0


def dead_paths() -> dict[str, list[str]]:
    """{doc: [paths it names that resolve to nothing]}."""
    dead: dict[str, list[str]] = {}
    for doc in _tracked_markdown():
        p = ROOT / doc
        for m in TICK.finditer(p.read_text(errors="replace")):
            t = m.group(1)
            if "/" not in t or PLACEHOLDER.search(t):
                continue
            if t.startswith(("http", "//")) or "github.com/" in t:
                continue                              # a URL that happens to end in .md
            if t.split("/")[0] in SIBLINGS:
                continue                              # another repo; not checked out here
            if (ROOT / t).exists() or (p.parent / t).exists():
                continue
            if _is_generated(t):
                continue
            dead.setdefault(doc, []).append(t)
    return dead


def test_no_doc_names_a_file_that_does_not_exist():
    unexplained = {doc: [t for t in ts if t not in ALLOWED]
                   for doc, ts in dead_paths().items()}
    unexplained = {d: ts for d, ts in unexplained.items() if ts}
    assert not unexplained, (
        "these docs name paths that resolve to nothing. Repoint the path (a cross-repo reference "
        "needs its repo prefix: `idp/drills/catalogue.yaml`, not `drills/catalogue.yaml`), delete "
        "the sentence, or add the path to ALLOWED with the reason it is legitimately absent:\n"
        + "\n".join(f"  {d}: {', '.join(ts)}" for d, ts in sorted(unexplained.items())))


def test_the_allowlist_does_not_outlive_the_paths_it_excuses():
    """An excuse for a path nobody names any more is dead weight that hides the next one."""
    named = {t for ts in dead_paths().values() for t in ts}
    stale = sorted(set(ALLOWED) - named)
    assert not stale, ("ALLOWED still excuses paths no doc names. Delete these entries:\n  "
                       + "\n  ".join(stale))


def test_every_excuse_says_why_the_file_is_absent():
    thin = sorted(k for k, v in ALLOWED.items() if len(v) < 25)
    assert not thin, f"an entry with no real reason is not a decision anyone can review: {thin}"


def test_a_cross_repo_path_is_recognised_by_its_prefix():
    """The fix's whole shape in one assertion: the prefix is what makes the sentence followable."""
    assert "idp" in SIBLINGS and "hermes-v2" in SIBLINGS and "survival-stack" in SIBLINGS
    assert "drills/catalogue.yaml".split("/")[0] not in SIBLINGS
    assert "idp/drills/catalogue.yaml".split("/")[0] in SIBLINGS

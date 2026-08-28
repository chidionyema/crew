# Platform requirements: documentation and dependencies

Written 2026-08-24. Every number below was measured on this machine on this date, by a command
whose output is in the session transcript. Nothing here is quoted from a doc, a memory or a
previous session's claim.

Scope is two layers only: how we write documentation, and how we manage dependencies. It is
deliberately not the whole platform. These two were chosen because they are the two that are
currently unmeasured and unowned, and every other layer inherits from them.

---

## 1. The baseline, measured

### Documentation

**Measured 2026-08-24T22:27Z.** Every row carries the command that produced it. This estate moves
by the hour -- `hermes-v2` alone gained 32 markdown files between two readings four hours apart --
so re-run the command rather than trusting the figure. Where a number here disagrees with
`docs/explanation/ESTATE_STATE.md`, neither is authoritative: the command is.

| Measurement | Value | Command |
|---|---|---|
| Markdown files under `~/dev/code` | 2,644 | `find … -name '*.md' -not -path '*/node_modules/*' \| wc -l` |
| Modified in 2026-08 | 2,480 of 2,497 | `stat -f %Sm` grouped by month |
| Modified before 2026-06 | 7 | same |
| Architecture decision records | **15** (3 idp, 12 prospector-main) | `find … -type d \( -iname 'adr' -o -iname 'decisions' \)` |
| …plus RFCs, which crew#183 counts and this doc does not | 2, in `hermes-v2/hermes-agent/docs/rfcs/` | `ls hermes-v2/hermes-agent/docs/rfcs/` |
| …carrying a `Sources` section | 3 of 15 (all three in idp; prospector-main's 12 carry none) | `grep -LiE '^#{1,4}\s*sources' docs/decisions/*.md` |
| `docs/` directories | 6 (crew, hermes-v2, idp, maestro, prospector-main, survival-stack) | `find . -maxdepth 2 -type d -name docs` |
| `mkdocs.yml` files | **1** (`idp/mkdocs.yml`, added by `2fe28c2`) | `find … -maxdepth 3 -name mkdocs.yml` |
| Backstage TechDocs referenced in idp config | yes (`app-config.yaml`, `catalog-info.yaml`) | `grep -rl techdocs idp` |
| Markdown on disk but **not in git** | **2,111** | `git ls-files '*.md'` vs `find` per repo |

Per repo, tracked versus on disk:

```
crew             tracked=63     onDisk=91       <--    28 untracked
idp              tracked=43     onDisk=59       <--    16 untracked
hermes-v2        tracked=25     onDisk=2090     <-- 2,065 untracked
prospector-main  tracked=303    onDisk=304      <--     1 untracked
maestro          tracked=9      onDisk=10       <--     1 untracked
```

Two things follow directly. TechDocs renders MkDocs, and until `2fe28c2` there was no
`mkdocs.yml` anywhere, so the portal had a documentation plugin configured and **zero pages to
serve**. There is now exactly one, in idp, which makes the count 1 of 6 repos rather than 0 --
the plugin has something to render and nothing to render it *from* for the other five. And 2,111
of our markdown files are invisible to every session, because they are not in git -- 2,065 of them
in `hermes-v2`, which DOC-4 classifies as vendor, leaving 46 that are ours and untracked.

### Dependencies

| Measurement | Value |
|---|---|
| Python manifests (`requirements.txt` / `pyproject.toml`) | 8 |
| Python **lockfiles** | **1** (`hermes-v2/hermes-agent/uv.lock`) |
| Pinned versions (`==`), the five repos this doc covers | **0 of 43 versioned lines** |
| Pinned versions (`==`), estate-wide | 52 lines, all in survival-stack and QAlgo |
| Distinct Python versions across 6 venvs | **5** (3.10.9 ×3, 3.11, 3.11.15, 3.14.6) |
| Dependabot / Renovate configs | **1** (`hermes-v2/hermes-agent/.github/dependabot.yml`) |
| SBOM files in `idp/reports/` | 4 (spdx, spdx3, syft, cyclonedx) |
| `uv` installed | yes, 0.12.5 |
| poetry / pipenv / pip-compile installed | none |

**How 43 is arrived at, because two earlier figures in this estate disagree.** The pattern matches
53 lines across `crew`, `.crew-state`, `prospector-main`, `hermes-v2` and `forex_trend_prediction`.
Seven of those are `.crew-state/requirements-dev.txt`, which is a git worktree of `crew` and
therefore the same file counted twice. Three are `@ file:` local path references in
`prospector-main/requirements-local.txt`, which carry no version at all. That leaves **43 versioned
dependency lines, 0 pinned**. An earlier draft said 44 and `docs/explanation/ESTATE_STATE.md` says 49; both counted
the worktree, and they differ from each other because the estate moved between the two readings.

Every runtime dependency we have is a floating range. `prospector-main/requirements.txt`, verbatim:

```
anthropic>=0.40
google-genai>=0.3
pyyaml>=6.0
pydantic>=2.6
requests>=2.31
json_repair>=0.63
```

Thirty lines, thirty ranges, no lock. Two provisions a week apart install different software. That
is the definition of running blind, and it is also why "it worked yesterday" is not evidence here.

Note the shape of it: we generate **four SBOM formats** describing a dependency set that has **one
lockfile**. An SBOM taken from an unlocked environment is a photograph of one machine at one
moment. It is the sophisticated artifact sitting on top of the missing foundation.

---

## 2. Requirements

Each is numbered, testable, and has an acceptance command. A requirement without a command that
returns 0 is not a requirement, it is a preference.

### Documentation

**DOC-1 — One documentation tree per repo, rendered by the portal we already run.**
Every repo in the catalog has `docs/` and a `mkdocs.yml`, published through Backstage TechDocs.
No second doc site, no wiki, no Notion.
*Accept:* `find ~/dev/code -maxdepth 2 -name mkdocs.yml | wc -l` equals the number of catalog
components, and the TechDocs tab renders for each.

**DOC-2 — Diátaxis structure, four folders, no free-form.**
`docs/tutorials/`, `docs/how-to/`, `docs/reference/`, `docs/explanation/`. A page that fits none of
the four does not belong in `docs/`.
*Accept:* every `docs/` contains exactly those four directories.

**DOC-3 — Decisions are ADRs, not prose in a README.**
MADR format in `docs/decisions/NNNN-title.md`. Every row of `crew/docs/STANDARDS.md` cites the ADR
that chose it. The gap is not that we write no ADRs -- 15 exist, 3 in idp and 12 in
prospector-main. It is that crew, which owns the 16 standards rows, has none, so 16 decisions
are recorded as a table cell with no reasoning behind it; and 12 of the 15 carry no `Sources`
section, which makes them prose in a numbered file. The three that comply are all in idp.

The test is the one crew#183 defines for this layer -- MADR with a mandatory `Sources` section --
not a looser search for any URL in the body. An earlier draft of this row used
`grep -rLE 'http|\.py:[0-9]|\$ '` and reported 3 of 12, because a record that mentions a link
in passing passes that test while citing nothing for its actual decision.
*Accept:* `ls docs/decisions/*.md | wc -l` > 0 in crew, every STANDARDS row carries an ADR id,
and `grep -LiE '^#{1,4}\s*sources' docs/decisions/*.md` returns nothing.

**DOC-4 — No untracked markdown.**
The gap between `git ls-files '*.md'` and `find -name '*.md'` is zero in every repo we own.
Vendored upstream trees are either gitignored or moved under a `vendor/` path and excluded from
the count — they are not ours to document.
*Accept:* the tracked-vs-on-disk table shows 0 difference for crew, idp, maestro,
prospector-main; hermes-v2's 2,065 are classified as vendor and excluded explicitly. The
remaining 46 are ours: 28 in crew, 16 in idp, 1 each in prospector-main and maestro.

**DOC-5 — One standards document.**
`crew/docs/STANDARDS.md` is the only one. No repo carries a competing copy.

The accept command in the first draft of this doc was `find ~/dev/code -name STANDARDS.md
-not -path '*/node_modules/*'` returning exactly one path, and it returns **two**:

```
~/dev/code/.crew-state/docs/STANDARDS.md
~/dev/code/crew/docs/STANDARDS.md
```

The second is not a competing copy. `~/dev/code/.crew-state/.git` reads
`gitdir: /Users/chidionyema/dev/code/crew/.git/worktrees/-crew-state`, and the two files are
byte-identical -- it is one file in one repo, checked out twice. A `find` over a filesystem counts
checkouts, and this estate has 39 crew worktrees. The requirement is about repositories, so the
command has to ask git, not the filesystem.

*Accept:* every `STANDARDS.md` under `~/dev/code` resolves to the same repository and the same
blob -- one distinct `(git dir, blob hash)` pair:

```sh
find ~/dev/code -name STANDARDS.md -not -path '*/node_modules/*' | while read -r f; do
  d=$(dirname "$f")
  printf '%s %s\n' "$(git -C "$d" rev-parse --path-format=absolute --git-common-dir)" \
                    "$(git -C "$d" hash-object "$f")"
done | sort -u | wc -l
```

returns 1. Run 2026-08-24T22:34Z, both ways, because a check only ever seen passing has not been
shown to refuse:

```
MUST FAIL (two repos, two different files): 2   (want 2)
still 2 (same bytes, two real repos):       2   (want 2 -- a real second copy)
MUST PASS (one repo checked out twice):     1   (want 1)
real estate now:                            1   (want 1)
```

The middle row is the one that matters: two separate repos holding byte-identical content still
count as two, so the check has not been weakened into "compare the bytes".

**DOC-6 — Docs are migrated once, then the old location is deleted, not left behind.**
A migration that leaves both copies has doubled the problem.
*Accept:* after each migration, the source path returns no `.md`.

### Dependencies

**DEP-1 — `uv` is the Python dependency tool, estate-wide.**
It is already installed (0.12.5) and already the only one present. One `pyproject.toml` and one
committed `uv.lock` per Python repo. No `requirements.txt` as a source of truth.
*Accept:* `uv lock --check` exits 0 in crew, idp, prospector-main, maestro, agent-guard.

**DEP-2 — Zero floating specifiers in any runtime manifest.**
Ranges belong in a library's published metadata. An application resolves and commits the result.
*Accept:* no `requirements*.txt` remains and `uv.lock` carries exact versions and hashes. Test the
absence of the files, not the absence of grep output -- a `grep --include` glob that matches no
file exits 1, so under `set -e` the check fails, and under `|| true` it passes for the wrong
reason. Either way it grades its own error:

```sh
[ "$(find ~/dev/code -name 'requirements*.txt' -not -path '*/node_modules/*' | wc -l)" -eq 0 ]
```

**DEP-3 — One declared Python version per repo, and the venv matches it.**
We are on five versions across six venvs, including a directory literally named
`crew/.venv.py310-was-out-of-spec`.
*Accept:* every Python repo has `.python-version`; `python -V` inside its venv matches it.

**DEP-4 — Dependency updates arrive as pull requests, not as a session's decision at 03:00.**
**Dependabot, not Renovate, and the decision is already made.** `hermes-v2/hermes-agent` carries
a `.github/dependabot.yml` that scopes updates to `github-actions` only and says why in the file:
source dependencies are pinned exactly in `uv.lock`, and scheduled bump PRs against a pin would
undermine the pin. That is the posture DEP-1 and DEP-2 ask for, already reasoned and already
running in one repo. Proposing Renovate here would be reinventing a wheel we have (LAW 43) and
would put two update tools in one estate. The work is to copy that config to the other repos and
promote its reasoning to an ADR, not to choose a tool.
*Accept:* every Python repo has `.github/dependabot.yml` scoped to `github-actions`; at least one
Dependabot PR open or merged; an ADR records the pin-plus-actions-only decision.

**DEP-5 — The SBOM is generated in CI from the lockfile, not on a laptop from a live venv.**
*Accept:* a clean checkout regenerates the SBOM identically; the CI job that produces it is green.

**DEP-6 — A declared dependency that nothing imports is removed.**
This has already happened once here (`tenacity`, removed 2026-08-15, imported by nothing).
*Accept:* an unused-dependency check runs in CI and is green.

---

## 3. Non-goals

- Not adopting the proposed fortress-stack compose file. Its Langfuse cannot boot (v3 with one of
  four required backing services), and its LiteLLM budget, fallback and callback keys are not real
  keys. Verified against `docs.litellm.ai` and the Langfuse repo compose file on 2026-08-24.
- Not adding another background job. There are 51 LaunchAgents and 0 of them in git; a new
  scheduled guard is the thing to stop doing, not the fix.
- Not writing a second standards document. This one becomes ADRs plus rows in the existing
  `crew/docs/STANDARDS.md`.

---

## 4. Order of work

Cheapest first, and each step is provable before the next starts.

1. **DEP-2 + DEP-1** — convert one repo (crew) to `pyproject.toml` + `uv.lock`, prove `uv lock
   --check` returns 0, then repeat. This is the single largest risk on the list and the cheapest
   to close.
2. **DEP-3** — declare `.python-version`, delete `crew/.venv.py310-was-out-of-spec`.
3. **DOC-4** — classify hermes-v2's 2,033 untracked files as vendor, and commit the rest.
4. **DOC-1 + DOC-2** — one `mkdocs.yml` in crew with the four Diátaxis folders, rendered in
   TechDocs. Prove the page loads before doing the other five repos.
5. **DOC-3** — write the 16 ADRs for the standards rows that already exist.
6. **DEP-4, DEP-5, DEP-6** — automation, once the foundation under it is real.

---

## 5. Two defects this measurement already found

Both are live, both are in our own code, and neither is in the proposal that started this.

**The spend ceiling does not exist.** `idp/llm/config.yaml` line 90 puts `max_budget: 5.0` and
`budget_duration: 1d` under `general_settings`. That section has no budget keys — confirmed against
`docs.litellm.ai/docs/proxy/config_settings` and independently against the documented key list. The
comment above it says it is "the thing that refuses a runaway loop at 03:00". It refuses nothing.

**The SBOM is not reproducible.** Four SBOM formats in `idp/reports/`, one lockfile in the estate.
Closing DEP-1 is what makes DEP-5 mean anything.

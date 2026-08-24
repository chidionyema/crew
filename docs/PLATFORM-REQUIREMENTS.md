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

| Measurement | Value | Command |
|---|---|---|
| Markdown files under `~/dev/code` | 2,497 | `find … -name '*.md' \| wc -l` |
| Modified in 2026-08 | 2,480 of 2,497 | `stat -f %Sm` grouped by month |
| Modified before 2026-06 | 7 | same |
| Architecture decision records | **0** | `find … -type d -iname 'adr*' -o -iname 'decisions'` |
| `docs/` directories | 6 (crew, hermes-v2, idp, maestro, prospector-main, survival-stack) | `find . -maxdepth 2 -type d -name docs` |
| `mkdocs.yml` files | **0** | `find … -name mkdocs.yml` |
| Backstage TechDocs referenced in idp config | yes (`app-config.yaml`, `catalog-info.yaml`) | `grep -rl techdocs idp` |
| Markdown on disk but **not in git** | **2,034** | `git ls-files '*.md'` vs `find` per repo |

Per repo, tracked versus on disk:

```
crew             tracked=63     onDisk=64
idp              tracked=13     onDisk=13
hermes-v2        tracked=25     onDisk=2058     <-- 2,033 untracked
prospector-main  tracked=303    onDisk=304
maestro          tracked=9      onDisk=10
```

Two things follow directly. The portal has a documentation plugin configured and **zero pages to
serve**, because TechDocs renders MkDocs and there is no `mkdocs.yml` anywhere. And 2,033 of our
markdown files are invisible to every session, because they are not in git.

### Dependencies

| Measurement | Value |
|---|---|
| Python manifests (`requirements.txt` / `pyproject.toml`) | 8 |
| Python **lockfiles** | **1** (`hermes-v2/hermes-agent/uv.lock`) |
| Pinned versions (`==`) across platform `requirements*.txt` | **0 of 49 lines** |
| Distinct Python versions across 6 venvs | **5** (3.10.9 ×3, 3.11, 3.11.15, 3.14.6) |
| Dependabot / Renovate configs | **0** |
| SBOM files in `idp/reports/` | 4 (spdx, spdx3, syft, cyclonedx) |
| `uv` installed | yes, 0.12.5 |
| poetry / pipenv / pip-compile installed | none |

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
that chose it. We currently have 0 ADRs and 16 standards rows, so 16 decisions exist with no
recorded reasoning.
*Accept:* `ls docs/decisions/*.md | wc -l` > 0 in crew, and every STANDARDS row carries an ADR id.

**DOC-4 — No untracked markdown.**
The gap between `git ls-files '*.md'` and `find -name '*.md'` is zero in every repo we own.
Vendored upstream trees are either gitignored or moved under a `vendor/` path and excluded from
the count — they are not ours to document.
*Accept:* the tracked-vs-on-disk table shows 0 difference for crew, idp, maestro,
prospector-main; hermes-v2's 2,033 are classified as vendor and excluded explicitly.

**DOC-5 — One standards document.**
`crew/docs/STANDARDS.md` is the only one. No repo carries a competing copy.
*Accept:* `find ~/dev/code -name STANDARDS.md -not -path '*/node_modules/*'` returns exactly one path.

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
*Accept:* `grep -rE '>=|~=|\*' --include='requirements*.txt' ~/dev/code` returns nothing, because
those files no longer exist; `uv.lock` carries exact versions and hashes.

**DEP-3 — One declared Python version per repo, and the venv matches it.**
We are on five versions across six venvs, including a directory literally named
`crew/.venv.py310-was-out-of-spec`.
*Accept:* every Python repo has `.python-version`; `python -V` inside its venv matches it.

**DEP-4 — Dependency updates arrive as pull requests, not as a session's decision at 03:00.**
Renovate, configured once, per repo. It is the mature tool and it replaces every hand-rolled
update script.
*Accept:* `renovate.json` present; at least one Renovate PR open or merged.

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

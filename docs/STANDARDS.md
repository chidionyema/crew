# The estate standard stack

Owner: crew (all sessions). Date: 2026-08-24. Ruling: R7 ("we need standardisation today")
and R9 ("the review includes getting it fully operational — add to acceptance criteria").

This page names ONE standard per layer. A component not on this page needs a one-line stated
deviation in its PR, and the review grades the deviation. Every choice below was researched
online with sources on the record in `science/RESEARCH-LEDGER.jsonl` (entries dated
2026-08-24); nothing here is a recollection.

## The stack, one line per layer

| Layer | Standard | Status today | Why this one (ledger receipt) |
|---|---|---|---|
| Substrate | Laptop + launchd until free-tier managed k8s (Oracle Always Free OKE — free control plane and Always Free ARM shapes; any paid tier waits on R14 sign-off) | live | Founder ruling: laptop is the substrate until k8s; the exit is MANAGED k8s — operating your own control plane is the wheel LAW 43 says not to reinvent. (A "~70% fail within 18 months" figure stood here; removed 2026-08-24, no source found — see crew#135.) R14 (2026-08-24) sharpens the exit: zero cost until proof is done. Manifests, policies and drills are proved locally (k3d/k3s on this machine, GitHub-hosted runners, free tiers); only a completed proof can reopen the spend question, and paid infra needs explicit founder sign-off first. |
| GitOps (at k8s time) | Flux | not yet | Recommended for solo-operator clusters; CNCF Graduated, Apache-2.0. Argo CD is the reviewed deviation (97% of surveyed users run it in production, up from 93% in 2023 — [CNCF 2025 Argo CD End User Survey](https://www.cncf.io/announcements/2025/07/24/cncf-end-user-survey-finds-argo-cd-as-majority-adopted-gitops-solution-for-kubernetes/) — but it is a UI service to run) |
| Admission policy | Kyverno, CEL ValidatingPolicy API only | migrating | CNCF Graduated 2026-03-24; legacy ClusterPolicy is REMOVED at v1.20 (Oct 2026) — new policies on the legacy API grade REWORK on sight |
| Policy proof | `kustomize build \| kyverno apply/test`, grading the JSON REASON field | live in prospector | `kyverno test`'s summary has an open false-pass bug class (#11519); the REASON field is the truth |
| Data | DuckDB 1.4 LTS + dbt-core (Apache-2.0), DuckLake v1.0 when data outgrows one file | live | Licence survives resale; DuckLake is plain Parquet + a catalog file, portable by construction (LAW 19) |
| Documentation structure | Diataxis — `docs/tutorials/`, `docs/how-to/`, `docs/reference/`, `docs/explanation/` | adopted in idp, 0 of 6 repos migrated | The framework itself is [diataxis.fr](https://diataxis.fr/); the adoption bar is an organisation that migrated a large corpus and published how it went, which is [Canonical](https://ubuntu.com/blog/diataxis-a-new-foundation-for-canonical-documentation) and the [Python documentation community](https://discuss.python.org/t/adopting-the-diataxis-framework-for-python-documentation/15072). A page that fits none of the four does not belong in `docs/`. ADR 0002 |
| Documentation delivery | docs-as-code rendered by Backstage TechDocs — one `mkdocs.yml` per repo, `backstage.io/techdocs-ref: dir:.` on the entity | live in idp only | Backstage's own guidance is [`dir:.`](https://backstage.io/docs/features/techdocs/how-to-guides/), because the docs are authored beside the source they describe. The estate had **0** `mkdocs.yml` files on 2026-08-24 while TechDocs was configured and had nothing to build. Proof is a build, not a config: `spotify/techdocs build --strict` finishes in 6.37s on idp. No wiki, no Notion, no second doc site. ADR 0002 |
| Decision records | MADR, `docs/decisions/NNNN-title.md`, every record carrying a `## Sources` section with dated URLs | 2 of 15 records comply | [MADR](https://adr.github.io/madr/) is maintained under the [`adr` organisation](https://github.com/adr) alongside the original Nygard format. R18: "alway research, it pays off all the tine". Enforced, not intended — `adr-sources-guard.py` refuses a record with no Sources heading or fewer than two distinct URLs, and its `--sweep` printed the damage: 15 records in the estate, 13 citing nothing. Every row on this page should cite the ADR that chose it; today two do. claude-guards#41 |
| Architecture diagrams | C4, modelled in Structurizr DSL, rendered to Mermaid and committed | live in idp | The model is one file; every diagram is a view of it, so views cannot disagree the way four hand-drawn pictures do — [Simon Brown, who wrote C4](https://dev.to/simonbrown/software-architecture-diagrams-which-tool-should-we-use-29e), and the [2026 tool comparison](https://infrasketch.net/blog/best-diagram-as-code-tools-2026). Mermaid is the OUTPUT because GitHub and TechDocs render it with nothing installed; hand-written Mermaid as the source is rejected. `structurizr/cli` is EOL and exits 0 while writing no files — use `structurizr/structurizr`. The estate had **0** architecture diagrams of any kind before 2026-08-24. ADR 0002 |
| Agent instructions | `~/AGENTS.md`, one file, symlinked into every vendor's CLI directory | live | Not a documentation standard and not adopted as one. It is a community convention in plain Markdown with no schema, no required fields and no versioned specification — [the convention](https://agents.md), [what it actually specifies](https://asdlc.io/practices/agents-md-spec/) — which is the right shape for telling an agent how to work in a repo and the wrong shape for how a platform documents itself. Read natively by Claude Code, Codex CLI, Cursor, Copilot and Gemini CLI. The [Agentic AI Foundation](https://blog.agentailor.com/posts/top-ai-agent-standards-2026) (Anthropic, OpenAI, Google, AWS, Microsoft, Salesforce, March 2026) governs agent-facing standards and publishes nothing about platform documentation, so it is not an option for this layer. ADR 0002 |
| Data registry | `science/sources.json` — every store declared or declined with a reason | live, gated | Gate 25 reconciles the registry against the hourly crawl both ways |
| Job monitoring | Healthchecks (self-hosted, BSD-3) dead-man switch wrapping launchd jobs | to adopt | The only surveyed OSS that tells PASS from NOT RUN — the estate's biggest gap; reachability tools (Uptime Kuma, Gatus) cannot |
| Notifications | Apprise (BSD-2) | to adopt | Provider-agnostic send path (~100 services incl. Telegram); delivery proof stays on the caller (LAW 28) |
| Backups | restic, with a monthly restore drill | to adopt | Closest 1:1 for the custom backup scripts; `restic check` is the drill |
| Secrets | sops+age directory vault (founder ruling 2026-08-24, crew#119 comment 5393502867): one file per secret, env-segregated `secrets/<env>/<name>.yaml`, ingress `secret-add` reading the value from stdin — never argv — egress `secret-load`, k8s path via secrets-as-files with rotation-safe precedence (file wins); the vault lives in a PRIVATE repo — crew, prospector and hermes-v2 are public and no ciphertext lands in them (default home `estate-secrets`, founder may override) | ruled; vault not yet built — migrating | Ruled the same day this row was measured adrift. The previous cell said "sops + age … live" while nothing sops-shaped existed (no `.sops.yaml` anywhere under ~/dev/code; a probe for it finds an age store never, which misled three sessions in one day) — "live" was the drift; the shape survived by founder ruling. Live today is the migration SOURCE: `prospector-main/deploy/secrets.env.age` (age X25519 whole-file, disk-local and untracked on purpose — prospector commit b5060a15 — identity `~/.config/prospector/age-key.txt` mode 600, 25 keys incl. MINIMAX_API_KEY); it stays live until the vault holds all 25, then is deleted per the ruling. Carried-over handling rulings: no private key is ever committed; any CI secret-scan ships report-mode first scoped past prospector's 152 legitimate matches (LAW 38). prospector#701 (recipients file, S5) is transitional — it protects the migration source and merges only if migration is not immediate; escrow (S1) remains founder action. Today's risk is LOSS, not exposure; residual: anything ever pushed to a public repo may stay fetchable by SHA, unenumerable from here |
| LLM providers | prospector `operator.py` factory today; LiteLLM (MIT core) is a CANDIDATE, not a component | live (factory) | Measured 2026-08-24: litellm is importable in 0 venvs and imported by 0 files on this estate — its CVE record is adoption cost, not live exposure. Routing today is one `Operator` ABC with 10 subclasses (8 in `operator.py`, plus `ClaudeCliOperator` and `GeminiCliOperator`), config-driven factory. Count: `grep -rhc '^class .*(Operator):' prospector/{operator,claude_cli,gemini_cli}.py`. Adopting LiteLLM needs its own reviewed PR; flags on record: enterprise split; open issues: `gh api repos/BerriAI/litellm --jq .open_issues_count` → 4,909 on 2026-08-24 |
| Agent traces | OpenTelemetry GenAI semconv → Langfuse (MIT core, self-hosted) | partially live | The single largest lock-in escape available; Langfuse containers already run |
| Agent board / sync | GitHub Issues (crew repo) | live | No mature OSS agent board exists (researched); do not build one |
| CI/CD | GitHub Actions; evidence gates; merge-when-green poller until required checks return with a deploy-key bypass | live | Native auto-merge cannot arm before checks pass; required checks block the hourly snapshot push until the bypass actor exists |
| Code quality | `ruff` + `pyright` (Python), `shellcheck` (shell), `actionlint` (workflows), enforced on the diff by `scripts/verify.d/15-code-standard.sh` | live, gated | Founder 2026-08-24: "we don't have engineering standards at all". Measured that morning: 6,173 lines of Python, no `pyproject.toml`, nothing ever run over it — 121 ruff findings, 24 pyright errors in basic mode. crew#134 |
| Instructions | `AGENTS.md` per repo, vendor files are symlinks | live | R8: no estate asset in a vendor-named home |

## Founder table, 2026-08-24: "custom code is a last resort — stop writing wrappers"

Founder, verbatim: "everything we write ourselves breaks." Each row of his table, evaluated
against this page and the estate as measured today. DELETE-custom is the default verdict;
a kept custom piece needs the mature tool named that was rejected, and why.

| Founder row | Verdict | Receipt |
|---|---|---|
| Custom guard scripts → pre-commit framework | ADOPT for every git-side gate (jargon, LAW 32 docs pair, ledger shape): `repo: local` hooks register the existing guards unmodified, pre-commit.ci enforces in CI. The agent-harness PreToolUse guards stay custom because pre-commit runs at commit time and cannot see an agent's tool call before it executes. Tracked crew#130 | ledger 2026-08-24 founder-table entry (15.5k stars, active 2026-08-17) |
| Custom health monitors → Uptime Kuma / Healthchecks | ALREADY THE STANDARD: Healthchecks (self-hosted, BSD-3) row above. Uptime Kuma was researched and rejected: it probes reachability and cannot tell PASS from NOT RUN for a scheduled job, which is this estate's actual failure mode | ledger 2026-08-24 monitoring entry |
| Custom secrets store → SOPS + age | THE STANDARD by founder ruling 2026-08-24 (directory vault, crew#119 comment 5393502867) — not yet live: the vault is being stood up in a private repo, the age blob store is the migration source, row above | ledger 2026-08-24 secrets entry |
| Custom scheduled jobs → systemd timers | INTENT ADOPTED, TOOL CORRECTED: systemd does not exist on macOS (`ps -p 1` → `/sbin/launchd`; `command -v systemctl` → none). launchd IS the native scheduler and is already the substrate row above. Any Python-loop scheduler grades REWORK to a launchd job; at k8s time these become CronJobs | measured this session |
| Custom alerting loops → Gotify / Telegram Bot API | Apprise row above stays: it is the mature OSS send path (BSD-2, ~100 providers incl. Telegram) and needs zero daemon; Gotify would add a server to run. Any custom polling/alerting daemon grades REWORK to a launchd job + Apprise send | ledger 2026-08-24 notifications entry |
| Custom data pipeline wrappers → Dagster native | ADOPT: Dagster used natively, wrapper layer deleted. Dagster's own docs run schedules via `dagster-daemon` supervised as a service — launchd here; `dagster dev` is development-only. Probe: the daemon must tick schedules across a reboot. Owned by the platform-engineering session as crew#126 | crew#126; ledger 2026-08-24 founder-table entry |
| Code quality gates → pre-commit + ruff + mypy | **DONE for the CI side (crew#134): ruff + pyright live and blocking, plus shellcheck and actionlint for the other two languages this estate writes.** pre-commit (the git-side half) remains open as crew#130 and must register these same three tools, not pick different ones. ADOPT pre-commit + ruff (drop-in for flake8+black+isort; PyPI Warehouse migrated to it Apr 2026). Typing gate: pyright --strict is the estate testing law's named tool for the same slot and the 2026 strict-gate consensus; mypy is the stated deviation only where a plugin no stub covers is demonstrably needed | ledger 2026-08-24 founder-table entry; measured: `ruff` installed, `pre-commit` not yet |

## What stays custom, on purpose

Researched, no mature equivalent exists — these are NOT wheels: the claim gate (DONE must
link to passing evidence; no OSS product does this), the Telegram gateway (no maintained
coding harness has a connector), the local asset inventory (Steampipe is cloud-API-shaped),
and the law-to-guard enforcement map. Everything else hand-rolled is a migration candidate
and grades REWORK when its replacement above is live.

## Licence rule (LAW 40: build it so it could be sold)

Apache-2.0 / MIT / BSD: use freely. ELv2 / FSL / Collate CCL: internal use is fine; add a
diligence note. GPL server components: flag before adopting. A dependency with NO licence
file grants nothing and is unusable. Never call a project "CNCF Graduated" without checking
`landscape.yml` — Backstage is Incubating, k3s and Velero are Sandbox, Talos is not CNCF.

## Widening a gate: report-only first, then flip

A gate that starts checking something it did not check yesterday turns branches red on
findings their authors did not write and could not have seen coming. The estate already
knows what happens then. Every session learns within a day to scroll past a red check, and
after that nothing is enforced at all — which is where the code standard found us in the
first place (crew#134). A guard that refuses correct work is an outage (LAW 38), and
"correct" here includes work that was correct under yesterday's rule.

So widening lands in two PRs, and the split is not optional.

**PR one widens the selection and reports.** The new files are checked by the same code
path the enforced files go through — not a second, simpler path, because a report produced
by a different implementation is a report about that implementation. The run prints which
files are newly visible, every finding on them, and one verdict line: `WOULD-FAIL`,
`WOULD-BE-BLIND`, or nothing. The exit code does not move. A test asserts that it does not
move, so the report-only property is a red line in a suite rather than a habit.

**Paired controls run in report mode too.** A report only ever seen complaining has not
been shown to be reading the files — it may be reacting to their existence. So the same PR
ships the permit case: a clean file in the newly-visible set produces no would-fail
verdict. And it ships the other half of the pair, an assertion that what was already
enforced still fails, because a widening that quietly turned the old check into a report
would satisfy every other assertion and delete the gate.

**PR two flips it to blocking, and quotes the count.** Its body carries the WOULD-FAIL
number that report-only has been printing, so the review is about a measured debt and not
an estimate. The flip is a diff — the report-only assertion inverts — and never a side
effect of some other change. Between the two PRs the debt is paid in the lane that owns
each file, which is what report-only buys: the number is visible to everyone who touches
those files, and it goes down before it starts blocking.

Nothing here says how long the gap is. A widening whose debt is zero flips the same week.
One with hundreds of findings flips when the lane has paid them, and the printed count is
the thing that stops it being forgotten (LAW 28).

## Stated deviations from this page

One per line, with the reason. The page's own rule is that a deviation is stated in the PR
and graded; these are the ones that have been.

**`pyright` runs in `standard` mode, not `--strict`, on the repo as a whole (crew#134).**
The testing law names `pyright --strict` and it is the right target. Strict demands an
annotation on every parameter of 6,173 lines that currently have almost none, which is a
migration and not a gate — shipped as strict it would have failed every branch on day one
and been switched off inside a day (LAW 38). Standard mode already finds 24 errors nobody
was looking at, 13 of them attribute access on a possibly-None value. A directory tightens
to strict when its owner has annotated it; that is a per-lane ratchet, not a page-wide flip.

## Review acceptance criteria (every review, every lane)

1. Grade every file KEEP / REWORK / NOT-RAISING-THE-BAR (R3).
2. Primary axis is LAW 43 / R6: hand-rolled code doing a mature platform's job grades
   REWORK with the replacement named from this page.
3. **Operational proof (R9): the review is not finished until the work is proven running
   on the live system.** The REVIEW record carries an `Operational:` line quoting the
   command and output — the scheduled job green, the service serving, the gate deciding.
   Merged-but-not-running grades REWORK.
4. Defects get a demonstrated failing input, or they are labelled "process risk:".
5. Evidence is shown, not described: screenshot on the PR (LAW 22), `Options considered`
   in the body, receipts in the commit message.
6. A PR touching infra paths (`scripts/`, `.github/`, launchd plists, this page) carries a
   `Standard:` line naming the row it uses, or a `Deviation:` line stating what and why
   (LAW 44, crew#135). `pr-evidence check` reports it on every PR — report-only today;
   flipping it to blocking is its own reviewed PR. A deviation is never refused, only graded.
7. Every ADOPT verdict names its cost tier (R14, 2026-08-24). Anything over EUR 0 — a rented
   node, a managed cluster, a paid tier — is refused with "Founder ruling R14: Mac substrate
   only", not escalated and not re-asked in different words. The available answers are free
   tiers, GitHub-hosted runners, and local k3d/k3s; "self-hosted on a small rented box" is
   not one of them. However mature the tool, a paid requirement parks it until the local
   proof is done and the founder reopens the spend question.

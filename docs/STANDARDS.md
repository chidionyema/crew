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
| Substrate | Laptop + launchd until managed k8s | live | Founder ruling: laptop is the substrate until k8s; the exit is MANAGED k8s — operating your own control plane is the wheel LAW 43 says not to reinvent. (A "~70% fail within 18 months" figure stood here; removed 2026-08-24, no source found — see crew#135.) R14 (2026-08-24) sharpens the exit: zero cost until proof is done. Manifests, policies and drills are proved locally (k3d/k3s on this machine, GitHub-hosted runners, free tiers); only a completed proof can reopen the spend question, and paid infra needs explicit founder sign-off first. |
| GitOps (at k8s time) | Flux | not yet | Recommended for solo-operator clusters; CNCF Graduated, Apache-2.0. Argo CD is the reviewed deviation (97% of surveyed users run it in production, up from 93% in 2023 — [CNCF 2025 Argo CD End User Survey](https://www.cncf.io/announcements/2025/07/24/cncf-end-user-survey-finds-argo-cd-as-majority-adopted-gitops-solution-for-kubernetes/) — but it is a UI service to run) |
| Admission policy | Kyverno, CEL ValidatingPolicy API only | migrating | CNCF Graduated 2026-03-24; legacy ClusterPolicy is REMOVED at v1.20 (Oct 2026) — new policies on the legacy API grade REWORK on sight |
| Policy proof | `kustomize build \| kyverno apply/test`, grading the JSON REASON field | live in prospector | `kyverno test`'s summary has an open false-pass bug class (#11519); the REASON field is the truth |
| Data | DuckDB 1.4 LTS + dbt-core (Apache-2.0), DuckLake v1.0 when data outgrows one file | live | Licence survives resale; DuckLake is plain Parquet + a catalog file, portable by construction (LAW 19) |
| Data registry | `science/sources.json` — every store declared or declined with a reason | live, gated | Gate 25 reconciles the registry against the hourly crawl both ways |
| Job monitoring | Healthchecks (self-hosted, BSD-3) dead-man switch wrapping launchd jobs | to adopt | The only surveyed OSS that tells PASS from NOT RUN — the estate's biggest gap; reachability tools (Uptime Kuma, Gatus) cannot |
| Notifications | Apprise (BSD-2) | to adopt | Provider-agnostic send path (~100 services incl. Telegram); delivery proof stays on the caller (LAW 28) |
| Backups | restic, with a monthly restore drill | to adopt | Closest 1:1 for the custom backup scripts; `restic check` is the drill |
| Secrets | sops + age; in-cluster later: secrets-as-files, rotation-safe precedence (file wins) | live | Research found nothing that supplants sops+age; pydantic-settings' env-over-file precedence is the wrong direction for rotation |
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
| Custom secrets store → SOPS + age | ALREADY THE STANDARD and live, row above | ledger 2026-08-24 secrets entry |
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

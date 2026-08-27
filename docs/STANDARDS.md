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
| Data registry | `science/sources.json` — every store declared or declined with a reason | live, gated | Gate 25 reconciles the registry against the hourly crawl both ways |
| Job monitoring | Healthchecks (self-hosted, BSD-3) dead-man switch wrapping launchd jobs | to adopt | The only surveyed OSS that tells PASS from NOT RUN — the estate's biggest gap; reachability tools (Uptime Kuma, Gatus) cannot |
| Notifications | Apprise (BSD-2) | to adopt | Provider-agnostic send path (~100 services incl. Telegram); delivery proof stays on the caller (LAW 28) |
| Backups | restic, with a monthly restore drill | to adopt | Closest 1:1 for the custom backup scripts; `restic check` is the drill |
| Secrets | sops+age directory vault (founder ruling 2026-08-24, crew#119 comment 5393502867): one file per secret, env-segregated `secrets/<env>/<name>.yaml`, ingress `secret-add` reading the value from stdin — never argv — egress `secret-load`, k8s path via secrets-as-files with rotation-safe precedence (file wins); the vault lives in a PRIVATE repo — crew, prospector and hermes-v2 are public and no ciphertext lands in them (default home `estate-secrets`, founder may override) | ruled; vault not yet built — migrating | Ruled the same day this row was measured adrift. The previous cell said "sops + age … live" while nothing sops-shaped existed (no `.sops.yaml` anywhere under ~/dev/code; a probe for it finds an age store never, which misled three sessions in one day) — "live" was the drift; the shape survived by founder ruling. Live today is the migration SOURCE: `prospector-main/deploy/secrets.env.age` (age X25519 whole-file, disk-local and untracked on purpose — prospector commit b5060a15 — identity `~/.config/prospector/age-key.txt` mode 600, 25 keys incl. MINIMAX_API_KEY); it stays live until the vault holds all 25, then is deleted per the ruling. Carried-over handling rulings: no private key is ever committed; any CI secret-scan ships report-mode first scoped past prospector's 152 legitimate matches (LAW 38). prospector#701 (recipients file, S5) is transitional — it protects the migration source and merges only if migration is not immediate; escrow (S1) remains founder action. Today's risk is LOSS, not exposure; residual: anything ever pushed to a public repo may stay fetchable by SHA, unenumerable from here |
| Identity | Three populations, one standard each, and a number per population that the row is graded on. **Machines in the cloud:** provider workload identity, no long-lived key — GitHub Actions OIDC → OCI IAM WIF (live, CP2), in-cluster OKE workload identity / instance principal for every pod that calls the cloud API (`instance_principal` pods vs `static_key_pods` in the cluster-state receipt). **Workloads to each other:** SPIFFE/SPIRE (CNCF Graduated 2022-09, Apache-2.0) — every service in the catalog holds an X.509 SVID from the cluster agent over the CSI socket and every service-to-service call is SVID mTLS; the number is *services holding an SVID / services in the catalog*, read from `spiffe.svids` in the cluster-state receipt against the Backstage catalog. **Humans:** WebAuthn passkeys (W3C Recommendation, FIDO2) on GitHub and the cloud console, FileVault on; graded by `gh api /user -q .two_factor_authentication` under a token with the `user` scope (a session token prints empty, reviewer 78caaa17 on crew#482), or by the account security-log export listing `passkey` sign-ins. **Third-party keys** go through the Secrets row (ESO/SOPS), never a `.env` or a keychain the gate can see: the bar is `idp/bin/static-secret-gate` = 0. | partially live: CP2 live; 12/12 OCI-calling pods instance_principal (receipt 2026-08-27 08:45Z); SVID 1 proof pod, 0 catalog services, 0 mTLS calls (receipt 09:30Z); static-secret-gate = 25; passkeys unverified | Founder 2026-08-27: "do we have these capabilities at the level of sophistication suggested" — the answer was no, and there was no row to say what the level is; this row is the level. SPIRE is the only CNCF Graduated workload-identity project and the one every mesh (Istio, Linkerd, Cilium) can consume, so the SVID is the portable identity (LAW 19); a mesh is a later deviation, not the standard. crew#227 is the tracked item; the grader is the cluster-state receipt joined to the catalog, never a file scan (LAW 50). |
| Container images | multi-arch, `linux/amd64,linux/arm64` under one tag (founder ruling R24, 2026-08-25) | gated in idp | Built by `docker buildx` in GitHub Actions, pushed as one manifest list to GHCR; the Mac pulls amd64, OKE pulls arm64. `idp/bin/build-image` is the one build path, `idp/bin/multiarch-gate` refuses a single-arch push (idp#35). Estate sweep 2026-08-25: 8 single-arch builds outside idp, crew#195 |
| LLM providers | LiteLLM proxy (MIT core) at idp platform/llm: one OpenAI-compatible router, 11 lanes in config.yaml (minimax, deepseek, openrouter, groq, gemini, vision…), Postgres-backed keys/spend, llm.<zone> at the Gateway; prospector's Operator factory calls it as one more OpenAI endpoint | live (cluster) | Measured 2026-08-27: `config.yaml` under platform/llm has 11 model_name lanes (grep -c model_name `config.yaml` under platform/llm); image ghcr.io/berriai/litellm-database:v1.98.0 (platform/llm/litellm.yaml); https://llm.<zone>/ui 200 with 45/45 assets text/css / text/javascript (crew#503 CP4 row). Superseded row of 2026-08-24 said CANDIDATE; the adoption PR was idp platform/llm (crew#66, LAW 43 row for model routing). Open issues: gh api repos/BerriAI/litellm --jq .open_issues_count |
| Observability | OpenTelemetry Collector (Apache-2.0) → SigNoz (Apache-2.0 core, self-hosted, ClickHouse) for metrics, traces and logs; GenAI traces also copied to Langfuse | absent | One collector, one store, one query surface for all five God View layers (crew#258). Pipeline: `idp/observability/otel-collector.yaml`; source registry: `science/sources.json` (crew#253). Rejected: bare ClickHouse with hand-written ingestion (stitching); Datadog, Honeycomb, Grafana Cloud (hosted run history is lock-in, LAW 19) |
| Front door | One hostname per service under the estate DNS zone, published by external-dns from the Gateway API HTTPRoute (ADR 0001) with OIDC at the gateway (ADR 0003); the portal (`catalogue.<zone>`) is the only place a URL lives, every catalogue entity carries `links:`; the gate is idp `bin/catalog-links-check` (a Component with no URL fails the PR, both ways in `bin/idp-ci`, live in `bin/idp-verify`); login is Authelia today, federated GitHub login via oauth2-proxy per ADR 0007 | live (crew#269 rows 1–3; catalogue.mumchimp.com answers behind the login) | Founder 2026-08-25: he must never ask for a URL and a migration must not change a name. `.local` rejected (mDNS, Mac-bound); `/etc/hosts` rejected (crew#247: infra is never Mac-bound, R25: the founder is not always on the laptop); a register-on-boot script rejected (headline rule 1: GitOps + external-dns already do it). Zone: founder decision, default the zone external-dns already automates |
| Agent traces | OpenTelemetry GenAI semconv → Langfuse (MIT core, self-hosted) | partially live | The single largest lock-in escape available; Langfuse containers already run |
| Experiments | MLflow (Apache-2.0, self-hosted): every research run logs params, prompt hash, sources and a Brier-scored forecast | absent | R34 names MLflow; `pgrep -f mlflow` is empty and predictions.jsonl holds 2 forecasts, 0 scored (crew#244 snapshot rows). Weights & Biases is the rejected hosted deviation: provider-hosted run history is lock-in (LAW 19) |
| Scheduling | Dagster under launchd until crew#78 (k8s), then Argo Workflows on OKE | partially live | Dagster is the data-pipeline row above and runs today; R34 names Argo on Kubernetes, which has no substrate until #78. Two schedulers at once is the stitching the headline forbids, so the switch is one cut-over at #78, not a parallel run |
| Agent board / sync | GitHub Issues (crew repo) | live | No mature OSS agent board exists (researched); do not build one |
| CI/CD | GitHub Actions; evidence gates; merge-when-green poller until required checks return with a deploy-key bypass | live | Native auto-merge cannot arm before checks pass; required checks block the hourly snapshot push until the bypass actor exists |
| Code quality | `ruff` + `pyright` (Python), `shellcheck` (shell), `actionlint` (workflows), enforced on the diff by `scripts/verify.d/15-code-standard.sh` | live, gated | Founder 2026-08-24: "we don't have engineering standards at all". Measured that morning: 6,173 lines of Python, no `pyproject.toml`, nothing ever run over it — 121 ruff findings, 24 pyright errors in basic mode. crew#134 |
| Instructions | `AGENTS.md` per repo, vendor files are symlinks | live | R8: no estate asset in a vendor-named home |
| Front end (every public surface) | One multi-brand platform: Next.js (MIT, 16.x) + Payload CMS 3 (MIT, 3.88, runs inside the same Next.js app on Postgres, `@payloadcms/plugin-multi-tenant` for one brand per tenant) + one design system with per-brand tokens; Medusa 2 (MIT core, 2.19; Enterprise Edition excluded) underneath any brand that sells. A brand is a config entry, a content collection and a domain, never a new front end. Bytesync is the parent brand (sells nothing); mumchimp/prospector, hermes-v2 and later companies are child brands | to adopt (crew#235); today three unstandardised front ends exist: prospector `store_platform/src/Store.Web`, `docs/storefront/look-engine`, `mumchimp-medusa/apps/storefront` | Founder rulings 2026-08-25 (crew#235): "we need front end capabilities", "bytesync is the ai company, mumchimp/prospector is one of our companies/products, think Alphabet/Google type", "everything needs to be configurable". Rejected: Sanity/Contentful (hosted content, LAW 19 portability); Strapi (a second Node service to run, LAW 23); Astro-only (content edits in git, LAW 31). Licences and versions checked online 2026-08-25 (ledger) |

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
| Definition of done → DoD Hard v2.1 (founder, 2026-08-25) | **live.** Done means the founder used it end to end and confirmed it; merged code, green CI and passing tests are INVENTORY. Reply line 1 is `DONE:` (carries `Founder receipt:`), `INVENTORY:` (carries exactly `Built:` `Use:` `Expect:` `Not done:` `Evidence:`), `WORKING:` or `BLOCKED:`. Evidence is a URL, commit, path or command, never a sentence. Enforced on every Claude session by `~/.claude/scripts/dod-guard.py` (Stop hook) and relayed as ruling R27; Codex, Gemini and Hermes read the same rule from `~/AGENTS.md`. Gates the policy names (security scan, coverage, demo, bootstrap, receipt) are tracked on crew#229; the security-scan gate is merge-blocking on idp since 2026-08-25 (ruleset idp-required-checks #21473806) | policy text: `idp/docs/policy/definition-of-done.md`; source PDF `~/Downloads/AGENTS_md_DoD_v2_1.pdf`; guard selftest `python3 ~/.claude/scripts/dod-guard.py --selftest` |

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

## Definition of done (every tracked item, every lane)

Founder, 2026-08-25: "what does done mean? what are the deliverables, what assets did it
produce? we need more standard." LAW 33 says define done in commands; this section says
which assets those commands must find. An item is DONE when every row below exists and its
check passes. A row that does not apply is stated as `n/a: <why>` in the PR body, never
skipped silently. `DONE:` on a reply with a missing row is the incident.

| # | Asset | Where it lives | Check |
|---|---|---|---|
| 1 | Tracked item | crew issue, `security`/lane label, owner named | `gh issue view N` shows owner and `Closes #N` on the PR |
| 2 | Code or config | a merged PR, squash, branch deleted | `git log --oneline -1 main` names the PR |
| 3 | Gate proved both ways | `bin/<name>-gate` + `tests/fixtures/<name>/{good,bad}` + a row in the repo's CI script | CI script prints `ok <name>`; in one run the good fixture exits 0 and the bad fixture exits non-zero |
| 4 | Reference doc | `docs/reference/` or an ADR, one page, Diátaxis quadrant named | page in `idp/mkdocs.yml` nav; docs build green |
| 5 | How-to and demo (LAW 32) | `docs/how-to/<verb>-<thing>.md` with a `Demo:` line naming one command | the demo command runs on main and prints its receipt |
| 6 | Catalog entity | Backstage entity or annotation generated from the source file, never typed twice | `idp/bin/catalog-refcheck` ok; entity visible in the portal |
| 7 | Operational proof (R9) | the thing running: scheduled job green, service serving, or gate deciding on a real PR | `Operational:` line in the REVIEW comment quoting command and output |
| 8 | Scheduled re-grade (LAW 28) | a Dagster job or CI schedule that re-runs the gate and notifies on red | job listed by `idp/bin/scheduler-status`; last run green |
| 9 | Standard row | `crew/docs/STANDARDS.md` names the tool, or the PR carries `Deviation:` | `crew/scripts/pr-evidence.py check --pr N` sees `Standard:` or `Deviation:` |
| 10 | Evidence block | `## Verification evidence` in the PR body with the exact commands and output | present; every number in the reply traces to a line in it |

Ten rows is the whole list. A feature that produced assets 1, 2 and 10 only is a merged
patch, not a deliverable; say `WORKING:` and name the rows still missing.

# Control plane: what to adopt, what to keep

Date 2026-08-24. Owner claude/control-plane. Ledger receipts: `science/RESEARCH-LEDGER.jsonl`,
four rows dated 2026-08-24, owner `claude/control-plane`.

Founder ruling, twice unanswered: "never reinvent the wheel and do a worse job."

## Measured first

- `estate-selftest.py` discovers **98** scripts. **53 report NO SELFTEST** and that count does
  not change the exit code. 43 PASS, 1 FAIL, 1 MISSING DEP. Run `2026-08-24T08:37:39+0100`.
- **32** estate plists in `~/Library/LaunchAgents`, 31 loaded. **28 are in no git repo.** Of the 4
  tracked, **3 have drifted** from disk.
- Healthchecks — the job-monitoring standard in `docs/STANDARDS.md` — is **down**
  (`http://127.0.0.1:8000/` returns HTTP 000). 9 of 32 jobs ping it; `hc-wrap.sh` is fail-open. So
  nothing is monitored and nothing says so.
- 13 drills registered, **8 have a command, 5 are NOT WRITTEN**.
- **Vale 3.17.1 is installed** and configured in 10+ repos. `jargon-guard.py`, 269 lines of
  hand-rolled prose linting, references it **zero** times.

`docs/STANDARDS.md` is not on `main`. It exists only on `standards/one-stack` (commit `9a11c64`).
Everything below fits it; the one addition is Vale.

## Do this first

**Bring Healthchecks back up and wrap all 32 jobs, pinging after the real work.**
[Self-hosting docs](https://healthchecks.io/docs/self_hosted/), BSD-3, £0.

A wrapper that `cd`s to a missing directory and exits 0 is judged successful by launchd, systemd,
Nomad, Kubernetes and Temporal alike. "Fails loudly" is a heartbeat property, not a scheduler
property. This is already the estate standard, already half-installed, and it protects the jobs
that stay on launchd.

Same day, one line: make `estate-selftest.py` count NO SELFTEST and exit nonzero.

## 1. Discovery — pytest + coverage.py, not a platform

coverage.py is the only surveyed tool that reports non-discovery out of the box. With
`[run] source=`, "coverage.py … can search the source tree for files that haven't been measured at
all" ([docs](https://coverage.readthedocs.io/en/latest/source.html)); `--fail-under` exits 2. With
`include=` instead, the orphan vanishes and the report reads a false 100% — this estate's bug,
inside coverage.py. Add a 15-line `conftest.py` asserting every script has one collected test;
`--collect-only` runs it in ~30ms. pytest 9.0.3 is here; **coverage.py is not installed**.

Residual: `source=` only walks importable files, and the runner globs `*/*.py`. The conftest's
`pathlib.glob` has no such limit — run both, they fail in different places.

**Chef InSpec is disqualified on measured behaviour**: a control with no describe block is dropped
from the totals and, under `--enhanced-outcomes`, reported **passed**
([inspec#849](https://github.com/inspec/inspec/issues/849), open since 2016).

## 2. Scheduling — heartbeat, then git, then systemd

Reproduced on this Mac: a plist pointing at a missing binary reports honestly (exit 78 EX_CONFIG).
The silent failure is **loaded-vs-disk drift** — `launchctl print` still shows the old program,
`launchctl list` shows exit 0, and `plutil -lint` says OK.

So: (2) commit all 32 plists with an apply script that lints, asserts `ProgramArguments[0]` is
executable, and boots out/bootstraps — plus an hourly drift check. (3) Only the
must-survive-the-Mac subset moves to **systemd v261.2 + Podman Quadlet** on an always-on Linux box
(~€3.79/mo rented, £0 owned), gated by `systemd-analyze verify`. Ban `Condition*=` — it reproduces
the silent skip; use `Assert*=`.

**Nomad is rejected**: BUSL 1.1, Licensor IBM, and no fork exists — no swap path to state.
**GitHub Actions is rejected**: "some queued jobs may be dropped", leaving no record to turn red;
also ~$138/mo Linux, ~$1,428/mo macOS for 32 hourly jobs.

Workflow engines sell observability the heartbeat already gives you: Temporal Cloud floors at
$100/mo against ~$4.50 of real use; Prefect Starter ($100/mo) caps at 20 deployments.

## 3. Guards — replace one, split one, keep two

| Guard | Verdict |
|---|---|
| `jargon-guard.py` (269 ln) | **Vale 3.17.1**, already installed — [rule types](https://docs.vale.sh/topics/styles) map one-for-one |
| `rule-guard.py` (1362 ln) | **Split.** Static bans → the 41 existing `permissions.deny` rules, which are shell-operator and env-prefix aware ([docs](https://code.claude.com/docs/en/permissions)). Law logic stays |
| `context-guard-hook.py` | Delete the token arithmetic, read the harness field — also fixes the `[1m]` threshold bug |
| `goal-guard.py`, `tracked.py` | **Keep.** Every guardrail product is a single-message content filter; none models session trajectory |

OPA/Conftest deferred: no prior art wiring Rego into Claude Code hooks exists, so it is a build,
not an adoption.

## 4. Drills — keep `run.py`

No product does "rebuild from nothing" on a Mac. Veeam SureBackup needs a hypervisor; AWS Backup
restore testing is AWS-only. Backup tools prove the archive, not the system — and none publishes a
restore-test recipe. Chaos tooling answers a different question and cannot witness its own
substrate being rebuilt.

Wire in restic 0.19.1's own commands as register entries: `check --read-data-subset=1/7` nightly
and `restore latest --dry-run --verbose=2`
([docs](https://restic.readthedocs.io/en/stable/045_working_with_repos.html)). Write the 5 missing
drills. At k8s time add one: k3d + Flux bootstrap, £0 on installed tooling. Fix `kubectl` v1.27.2
against k3s v1.35.5 first.

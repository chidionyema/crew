# The research department: boundary, contract, requesters, and the gut-or-keep test

**Status:** DESIGN FOR FOUNDER REVIEW — nothing here is built or decided. Founder, 2026-09-01: "this needs
careful design ... no quick decisions". Companion to [RESET-2026-09-01-research-engine-v2.md](RESET-2026-09-01-research-engine-v2.md).
Founder record: `~/.claude/docs/founder/` entry of 2026-09-01T12:3xZ ("this needs careful desig, the engine is general purpse").

## 0. What the founder said, in requirements form

1. The engine is general purpose. Prospector (looking for marketable business ideas) is one user of it.
2. The interface must stop prospector's demands leaking into the engine.
3. The engine is the research department: it serves every lane of the estate under a defined contract.
4. It is also the founder's tool, usable for any purpose.
5. Other departments can submit research requests.
6. The estate holds a lot of data and problems — infra, incident reports, agent behaviour — and the
   department must turn them into improvement, not leave them to the founder.
7. Departments exist, yet the founder still sets up departments, straightens out infra and crew, researches
   best practice for six lanes of agents, sources expert consultation, watches compliance, and repeats
   himself daily. Either the research department and the science lane take weight off him, measurably, or
   they are gutted. No quick decisions; no slipping back to old patterns.
8. The guards need review: they were keeping rogue agents honest, so a review may tighten and must not
   quietly weaken them.

## 1. The boundary: core, profiles, requesters

Three layers, each allowed to know only about the one below it.

| Layer | Owns | Must not know |
|---|---|---|
| **Core** (the engine) | Question → Claims → Brief. The provenance gate (a source snapshot, a locator, a verifier model different from the producer). Storage: Postgres record, R2 snapshots, ClickHouse metrics. | Any requester's vocabulary. The words "business idea", "marketable", "dossier", "verdict" do not appear in core code or schema. |
| **Profile** (one per requester kind) | Question templates, source list, output shape, grading rubric, budget. Lives in the *requester's* repository (prospector's profile in prospector; the estate's in idp). | Other profiles. Core internals beyond the contract. |
| **Requester** | Submits a request, receives a brief, and emits a delivery event when it uses it. | How the brief was made. |

**The leak test, mechanical:** the engine repository carries a test that fails if its code or schema imports
or names any profile. Profiles are data loaded by contract, never code merged into core. A prospector
need that cannot be expressed as a profile is a change request to the *contract*, reviewed by the founder,
never a special case in core.

## 2. The contract

One request shape in, one brief shape out, versioned.

**ResearchRequest** — `id` · `requester` (founder | a department role | a scheduled standing question) ·
`profile_id` · `subject` (a product, a service, a market, a company, the estate, or free text) ·
`questions[]` (the founder may leave this empty and write one sentence; the compile stage forms the
questions) · `deadline` · `budget` (tokens or money, hard stop) · `sensitivity` (public | internal |
founder-only) · `contradicts_ruling?` (checked at intake against the rulings record; a request that
contradicts a standing ruling is refused with the ruling quoted).

**ResearchBrief** — `request_id` · `claims[]` (admitted only; each with sources, locator, verifier verdict) ·
`rejected_count` and why · `artifact` (the readable brief, plain English) · `cost` · `producer` and
`verifier` models · `delivered_at`.

**DeliveryEvent** — written by the requester, never the engine: `brief_id` · `used_for` (a decision, a
merged change, a founder reply, a sale) · `by`. The department's grade is computed from these alone
(self scoring is banned, founder 2026-08-31).

**What the department promises:** every claim sourced and verified; cost inside the budget or a clean
stop; an answer or a stated failure by the deadline; no claim ever edited after admission.

## 3. Who may ask, and how

| Requester | How the request is made | How the answer comes back |
|---|---|---|
| **Founder, any purpose** | One phrase to Otto on Telegram ("research: …"), or the Backstage "Ask research" template. Jumps the queue. | Telegram, pinned, one link to the brief page. |
| **A department** (engineering, product, science, information architecture, UX, QA, PM — the role files) | A board ticket carrying the `research-request` label, or the same Backstage template. One queue, one owner per request. | A comment on the requesting ticket with the brief link; the department writes the delivery event when it acts on it. |
| **Standing questions** (nobody asks; the department owes them) | A schedule in idp. | A weekly brief page and one pinned Telegram line. |

### Standing questions — the weight the founder listed, made into work the department owes

| What the founder does today by hand | Standing question the department owns | Sources |
|---|---|---|
| Sets up departments | "What should the charter of role X be, given best practice and our own incident record?" — the department drafts, he approves. | role files, incidents, industry practice |
| Straightens out infra and crew | Weekly estate brief: the five failure classes that recurred most, each with a sourced fix and the guard that should have caught it. | hook-outcome ledger (454,143 rows since 2026-08-25), incident pages, board |
| Researches best practice for six lanes of agents | One question per lane, refreshed on a schedule, answers cited to sources. | vendor docs, papers, the intake watch list (22 repositories already watched) |
| Gets expert consultation | "Second opinion" request type: the producer drafts, a model from a different maker verifies each claim against sources; the brief names the references a human expert would. | as above |
| Watches compliance | Standing watch on the regulations touching each product (ties to the data policy row, crew#674). | regulators' pages, snapshotted |
| Repeats himself daily | Rulings are read at intake; a request or brief that contradicts one is refused with the ruling quoted. The department does not own the rulings record; it reads it. | rulings.json, founder docs |

### Estate data are sources, not lanes

Incident reports, the hook-outcome ledger, the board, the alerts inbox, agent-behaviour records
(runaway-reaper, agent certification) and the estate state snapshot are **source adapters**. The engine
asks its standing questions of them the same way it asks the web: snapshot, locate, verify. "Science facts"
folds in here as one adapter. Machine learning enters only where a grader shows a gain (charter, unchanged).

## 4. The gut-or-keep test — measured, dated, no self-scoring

Keep the department if, inside a fixed window the founder sets after the skeleton (CP1) lands, requesters
other than the lane itself have written delivery events for its briefs — a decision made, a change merged,
a founder reply citing a claim. The count and the window are his numbers to set; the measurement is
theirs to write, never the lane's.

If the test fails: the lane's scripts are archived with one commit, `roles/science.md` shrinks to the data
pipeline it actually runs, and the standing questions above go back on the founder's desk openly rather
than pretending a department holds them.

Progress counts only as: claims admitted per day, rejection rate, time to brief, delivery events per week
(reset §9). Charters, grade pages and checkpoint edits — including this page — count for nothing.

## 5. The guard review

Facts from the ledger `~/.claude/state/hook-outcomes.jsonl`, counted 2026-09-01:

- 30 guard scripts in `~/.claude/scripts`; 454,143 hook runs since 2026-08-25; 3,349 refusals.
- Refusals per day: 08-27 607 · 08-28 740 · 08-29 1,086 · 08-30 295 · 08-31 532 · 09-01 89 (partial day).
- Top refusers: rule-guard 819 of 51,659 runs (1.6%) · pre-push 622 of 3,466 (17.9%) · idle-guard 414 of 1,886
  (22.0%) · dupe-work-fence 352 of 51,537 (0.7%) · auto-objective 351 of 1,885 (18.6%) · pre-commit 239 ·
  opa-hook 105 · feed-guard 103 · jargon-guard 74 · blocker-guard 58 · repeat-guard 55 · dod-guard 44.

No guard was removed or weakened today; the fall from 1,086 to 89 refusals a day is either fewer mistakes
or fewer sessions running, and the review must say which before anyone reads it as improvement.

**Method (facts, not opinion), per guard:** refusals · refusals later overridden with an `-intended`
suffix · incidents of the guard's class that recurred after it landed · correct work it refused (the
outage class, LAW 38). Verdict per guard: **KEEP** (caught real mistakes, few overrides), **TIGHTEN**
(its class recurred anyway), **RETIRE** (only ever refused correct work). Any RETIRE needs the founder's
word; KEEP and TIGHTEN do not weaken anything.

**Dogfood:** this review is the first request through the contract in §2 — subject: the estate's guards;
sources: the ledger, the incidents file, the guard tests. If the department cannot answer this one well,
the gut-or-keep test in §4 has its first data point.

## 6. What the founder decides, after reading — not now

1. The boundary in §1 and the contract in §2: agree, or mark the lines to change.
2. The requester table in §3: who else may ask; whether founder requests jump the queue.
3. The window and the count for the gut-or-keep test in §4.
4. The four rulings in the reset (§6 there) stand as asked.
5. Whether the guard review runs first, as the dogfood request.

No timer on this page. The founder reads it when he reads it; the crew builds nothing until he answers.

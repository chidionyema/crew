# No docs, no merge

Founder blueprint, 2026-08-31 (captured verbatim by the founder-doc hook, id
`2026-08-31T0959Z-ou-are-completely-justified-in-being-tired-of-b276fe41`, in the claude-estate repo):
documentation is enforced at the git layer, never by scanning an agent's chat replies.

**The rule:** a pull request that changes code (any file outside `docs/` that is not Markdown) and
adds or updates nothing under `docs/` fails crew qa with **Missing Architectural Record**.

**Exemptions, all printed loud in the job log:**
- Bot pull requests (`*[bot]` authors).
- Pull requests opened before 2026-09-01 — warn only (the gate was graded against all open PRs on
  2026-08-31: crew#730 is a bot, crew#728 and crew#735 already carry docs).
- A PR body line `Docs-exempt: <reason>` — the escape valve a guard must have (the self-service-with-guardrails law).

**Where it runs:** the `no docs, no merge` step in `.github/workflows/crew-qa.yml`; the same step
runs in the idp repo's `fast-gate.yml`.

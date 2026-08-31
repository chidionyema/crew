---
captured: 2026-08-16T00:08:31+00:00
session: fe9d031d-11dd-41c1-8e9a-97663906df79
cwd: /Users/chidionyema/Documents/code/prospector
chars: 1664
source: founder prompt, verbatim (founder-doc-capture.py)
---

need to close the isues quickly 
DONE: confirmed your diagnosis, and found a second defect sitting behind it.

The one_liner is the culprit — store/dossiers/b94760e86e62585a.pass.json carries it verbatim: "It takes a published NHS rota and timesheet…". "It" has no antecedent except the title above it.

The closing paragraph isn't generated at all — it's hardcoded on every pack page at store_platform/src/Store.Web/src/pages/pack/[id].tsx:688. That means one edit fixes all 145 listings with no backfill and no model calls. It's also a textbook breach of the antithesis rule I landed this session: "is not having it. It is the time…".

Opener histogram across all 75 live one-liners: 55 start with "A", 7 "For", 4 "An", and one each of "Gets"/"Work"/"Printed"/"Automatically"/"It". So the bare pronoun is a single outlier, but 55-of-75 opening the same way is its own defect worth fixing while we're in there.

---
PR #224 is open with auto-merge armed (squash) — it lands when python and dotnet CI clear. It contains both commits, so #223 merges with it; no separate action needed.

Two things I deliberately did not do without your go: a live-zip probe finished but I haven't read it (it decides the real backfill scope), and nothing has touched a live product — STORE_INTERNAL_API_KEY is unset, so --apply can't fire by accident.

One trade-off you haven't been asked about yet, recorded in the handoff: the engine-info removal backfills from disk for free, but the dash and antithesis fixes are generator-side, so existing packs keep their dashes unless regenerated — and that costs model calls.

Safe point — type /clear (state saved, nothing will be lost).

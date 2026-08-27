# Onboarding — `science/dora.py`

**What it is.** The four DORA keys (deploy frequency, lead time, change failure rate, MTTR) for
any set of GitHub repositories, from the API, on demand.

**Run it.**

```
python3 science/dora.py                       # idp and crew, last 7 days
python3 science/dora.py --days 30 --json      # machine-readable
python3 science/dora.py --repo chidionyema/hermes-v2
```

**What it needs.** `gh` authenticated (any session on the estate already is). Repositories come
from `--repo`, else `DORA_REPOS` (comma-separated), else `chidionyema/idp,chidionyema/crew`; no
path or host is typed in the file (LAW 46).

**Reading it.** `change failure rate=n/a` means no merge in the window; `MTTR=n/a` means no P1
closed in the window. A P1 counts by its `P1` label, never by its title.

**Where it goes next.** CP9 on crew#495: a showcase row from this output on the daily render.
Incident test: `tests/test_incident_crew495_dora_counts_every_page_and_p1_by_label.py`.

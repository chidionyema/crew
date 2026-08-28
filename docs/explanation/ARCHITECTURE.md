# Estate architecture

Owner: claude/science
Last true: 2026-08-24

This is what is actually running, measured on 2026-08-24, not what anybody intended to
build. Every row carries the command that produced it, so a reader who does not trust
this page can re-run it rather than take its word. That is the point of the page: the
estate has six agent sessions that cannot see each other and a founder who should not
have to ask what exists.

Three labels are used throughout and they are not interchangeable.

- **Measured** means a command was run this day and its output is quoted.
- **Declared** means a document or a config file says so and nobody re-ran it. Treat
  declared rows as leads, not facts.
- **Unknown** means the question was asked and the command did not answer it. These
  rows are the most useful ones on the page.

## What this estate is

One founder, six agent sessions on interchangeable providers, and a set of machines
that must keep working when any one provider is removed. The software divides into
four layers. Nothing here is a microservice architecture and it should not become one.

1. **The laws and the guards.** `~/AGENTS.md` is one file, symlinked into each vendor's
   directory, holding forty-one rules. `scripts/verify.d/*.sh` in this repository are
   the gates that enforce the ones a machine can enforce. This layer has no runtime and
   no state; it refuses things.
2. **The coordination layer.** The crew issue board on GitHub, the estate board at
   `~/.claude/ESTATE_BOARD.jsonl`, and the prompt ledger. Sessions cannot see each
   other, so everything one session needs another to know passes through here.
3. **The measurement layer.** `science/` in this repository: collectors, a SQLite
   warehouse, a research ledger and a risk register. It answers what the estate did,
   what it cost and what it learned.
4. **The products.** Prospector, hermes-v2 and the survival stack. These are the things
   that could be sold. Everything in layers one to three exists to keep them shipping.

## Components running right now

Measured with `docker ps` and `launchctl list`.

### Containers

| name | image | reachable on | state |
|---|---|---|---|
| prospector-store-api | `prospector-store-api:local` | 127.0.0.1:5291 | up, healthy |
| prospector-store-web | `prospector-store-web:local` | 127.0.0.1:3000 | up, healthy |
| prospector-engine | `prospector-engine:local` | 127.0.0.1:8611 | up |
| prospector-edge | `caddy:2.10-alpine` | 0.0.0.0:8080, 0.0.0.0:8443 | up, healthy |
| estate-healthchecks | `healthchecks/healthchecks:latest` | 127.0.0.1:8000 | up, healthy |

All five come from one compose project, measured rather than assumed:

```
$ docker inspect prospector-store-web \
    --format '{{index .Config.Labels "com.docker.compose.project.config_files"}}'
/Users/chidionyema/dev/code/prospector-main/deploy/compose/docker-compose.yml
```

**None of these five appears in `STATE.md`.** That is live infrastructure with open
ports, absent from the page the estate treats as its snapshot. It is the largest single
gap on this document.

### Long-running agents

`launchctl list`, where a PID in column one means loaded and running and column two is
the last recorded exit code.

| label | pid | last exit | what it is |
|---|---|---|---|
| `ai.architect.gateway` | 73085 | 1 | the Telegram gateway, the founder's channel to the estate |
| `com.chidionyema.maestro` | 26915 | -15 | the overseer, cycles on `INTENT-*.json` files |
| `com.founder.boardserve` | 76247 | -15 | serves the founder board |
| `ai.estate.consultd` | 52009 | 0 | consult daemon |
| `ai.estate.friction-relay` | 78687 | 0 | carries founder complaints into every session |
| `ai.estate.deepseek-bridge` | 6722 | 0 | model bridge |
| `ai.estate.kimi-bridge` | 75615 | 0 | model bridge |

`ai.architect.gateway` is running with a last exit code of 1. That means it died badly
at least once and was restarted. Nobody has looked at why.

### Scheduled jobs

Twenty-one further launchd jobs run on a schedule and are not resident. Four of them
last exited non-zero and nobody has read the stderr:

```
com.founder.sciencecollect      1
com.founder.board               1
com.estate.costsentinel         1
com.prospector.estate-inventory 1
```

There are 47 plist files in `~/Library/LaunchAgents`, most stamped within the same
minute on 2026-08-24. Whether that was a deliberate bulk deploy or a symptom of
something rewriting them is **unknown**, and it is worth answering before trusting any
schedule on this page.

## Where the data lives

Every store, its path, and what it held when this page was written.

| store | path | rows | written by |
|---|---|---|---|
| science warehouse | `science/warehouse.db` | `facts` 6040, `ingest_log` 255 | `science/collect.py`, `science/outcomes.py` |
| estate board | `~/.claude/ESTATE_BOARD.jsonl` | 140 | ten scripts, `estate-broadcast.py` among them |
| prompt ledger | `~/.claude/state/ledger.jsonl` | 694 | `prompt-ledger.py` |
| risk register | `risk/REGISTER.jsonl` | 11, of which 1 mitigated | by hand, gated by `verify.d/85-risk-register.sh` |
| research ledger | `science/RESEARCH-LEDGER.jsonl` | 16 | by hand, gated by `verify.d/80-research-ledger.sh` |
| decisions | `~/.claude/DECISIONS.jsonl` | 118, **last written 2026-08-21 18:23** | unknown, and that is the defect |
| would-have-fired | `~/.claude/state/one-branch/would-have-fired.jsonl` | 162, **last written 2026-08-21 22:38** | unknown |
| issue board | GitHub `chidionyema/crew` | 30 open | `crew/gh.py`, via `crew-triage` |

Two of those stores stopped being written three days ago and no alarm fired. A store
that goes quiet and is still read looks like an estate with nothing to report, which is
exactly the failure LAW 28 describes.

The estate board writer count is worth stating plainly: ten different scripts append to
one JSONL file with no schema and no gate. It works today because appends are atomic at
this size. It is the thing most likely to break silently as the file grows.

## Portability

Measured, not assumed.

```
$ grep -rl '/Users/chidionyema' ~/dev/code/crew ~/dev/code/idp --include='*.py' --include='*.sh'
(no output)
```

Neither this repository nor `idp` carries a hardcoded home directory. `maestro.py` has a
single hit and it is a string inside an incident description, not a path the program
depends on.

**Declared, not re-measured:** `docs/decisions/DECISIONS.md` records that hermes-v2 cannot be moved with
a plain `mv`, because its virtualenv bakes an absolute interpreter path into the shebang
and `./bin/hermes` breaks on relocation. That is a real trap in that repository and it
belongs in any rebuild drill.

**Single points of failure visible in the configuration:** `ai.architect.gateway`,
`com.chidionyema.maestro` and `com.founder.boardserve` are each one process on one Mac
with no second instance anywhere. The Telegram gateway is the founder's only channel, so
its failure is not degraded service, it is silence.

## What is declared but not true

This section is the reason the page exists.

- Five containers are serving on open ports and appear in no snapshot.
- Two data stores have been silent since 2026-08-21 and are still treated as live.
- Four scheduled jobs last exited 1 and nobody has read why.
- `STATE.md`, the page the estate is told to read first, was last rebuilt at 01:44 on
  2026-08-24 and does not carry the container layer at all.

Open issues that corroborate this from the estate's own measurements rather than from
this page: #84 on 1064 field paths with no contracts, #74 on the absent pipeline, #69 on
32 of 59 scripts wired to nothing, #73 on 2429 warehouse rows with no timestamp, and #80
on a guard tracking a writer that stopped.

## How to check this page yourself

Nothing here should be believed because it is written down. These are the commands, and
they take under a minute.

```bash
docker ps --format '{{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'
launchctl list | grep -iE 'founder|estate|architect|maestro'
sqlite3 science/warehouse.db "select 'facts',count(*) from facts;"
wc -l ~/.claude/ESTATE_BOARD.jsonl risk/REGISTER.jsonl science/RESEARCH-LEDGER.jsonl
python3 science/docsmap.py
```

If any of them disagrees with this page, the command is right and this page is stale.
Correct it in the same turn rather than working around it.

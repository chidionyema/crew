---
captured: 2026-08-31T04:58:20+00:00
session: 14ed6c8b-f0a9-40d7-82a8-895f336f9b78
cwd: /Users/chidionyema/dev/code
chars: 2899
source: founder prompt, verbatim (founder-doc-capture.py)
---

orry — plainly.

The identity job is now tiny. One user account. Nothing to migrate. Create it in Keycloak, point the shop at it, delete the old tables. An afternoon.

But that same file holds everything else. store.db isn't just logins — it has your 202 packs, 76 price history rows, 41,035 analytics events, the orders, the entitlements. All of it, in one 5.5MB file, on one volume, with no backup.

So the risk moved. It was never the identity migration. It's that if that volume dies, you lose the shop — the products, the sales record, all of it. That's true today, before anyone touches Keycloak.

And a migration is when files get lost. Someone runs a command against the wrong path, a pod restarts mid-write, a PVC gets recreated. Doing identity work on an unbacked-up database is how a small job becomes a disaster.

So: copy that file somewhere safe before anything else. One command, one minute:

kubectl exec -n <shop-ns> <pod> -- sqlite3 /data/store.db ".backup /tmp/b.db"
kubectl cp <shop-ns>/<pod>:/tmp/b.db ./store-backup-20260831.db

Then put it in object storage and set it on a schedule.

That's the whole point. Not a new problem — the one that was already there, now that identity turned out not to be one.

so when we do get cliennt ewhat jhaopens

When an enterprise client arrives, on the design you've just settled:

Their users never get accounts in your system. You add an identity provider entry to the realm — a config file in git, applied by keycloak-config-cli — pointing at their Okta or Entra. Their staff log in with their own corporate credentials. Nothing is created per-user by you.

That's a PR, not a project. Realm config change, one client entry, their metadata URL and certificate. Hours, not weeks.

Your app needs one thing already true: users identified by Keycloak subject ID, and a tenant claim on the token that your authorization checks read. That's why the single-realm decision and the subject-ID column matter now — they're the two things that make the later change a config edit instead of a rewrite.

What they'll also ask for, and what it costs:

SCIM provisioning, so deactivating someone in their HR system removes access here. Keycloak needs a SCIM extension for this; it's not built in. Real work, but only when someone demands it.

Audit logs, exportable. Keycloak emits events; you'd need them shipped somewhere retained. A day.

Their own branding on the login page. Theme file, trivial.

What blocks the deal if it isn't done: the backup and retention story on that SQLite file, and encryption at rest. Those are the questions a security review opens with, and they're the ones you can't answer today.

So: the client arrival itself is cheap because of the decisions made tonight. The things that would stop the deal are the data ones, not the identity ones — and they're fixable now, cheaply, while there are three orders in the table.

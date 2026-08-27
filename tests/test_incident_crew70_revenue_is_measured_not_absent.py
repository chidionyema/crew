"""crew#70: every efficiency number was a cost divided by nothing.

Rule, not code: the revenue row is GREEN only when the store answered inside the
staleness bar. An unanswered store, a missing token or an old row is NOT RUN, never a
zero, so a measured zero and an absent number can never look alike on the page.
"""
import datetime as dt
import importlib.machinery
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "science"))
import outcomes  # noqa: E402

_loader = importlib.machinery.SourceFileLoader("snap", str(ROOT / "scripts" / "estate-snapshot"))
_spec = importlib.util.spec_from_loader("snap", _loader)
assert _spec is not None
snap = importlib.util.module_from_spec(_spec)
_loader.exec_module(snap)

NOW = dt.datetime(2026, 8, 27, 2, 0, tzinfo=dt.UTC)


def _row(tmp_path, row):
    p = tmp_path / "revenue.jsonl"
    p.write_text(json.dumps(row) + "\n")
    return snap.revenue_row(p, now=NOW.timestamp())[0]


def test_incident_crew70_no_token_is_not_measured(monkeypatch):
    monkeypatch.delenv("MEDUSA_ADMIN_TOKEN", raising=False)
    row = outcomes.collect_revenue(now=NOW, fetch=lambda u, t: (_ for _ in ()).throw(AssertionError("must not fetch")))
    assert row["measured"] is False and "MEDUSA_ADMIN_TOKEN" in row["reason"]


def test_incident_crew70_dead_backend_is_not_a_zero(monkeypatch, tmp_path):
    monkeypatch.setenv("MEDUSA_ADMIN_TOKEN", "x")

    def dead(url, token):
        raise OSError("connection refused")
    row = outcomes.collect_revenue(now=NOW, fetch=dead)
    assert row["measured"] is False and row["paid_orders"] == 0
    line = _row(tmp_path, row)
    assert "NOT RUN" in line and "GREEN" not in line


def test_incident_crew70_measured_zero_is_green_with_a_date(monkeypatch, tmp_path):
    monkeypatch.setenv("MEDUSA_ADMIN_TOKEN", "x")
    row = outcomes.collect_revenue(now=NOW, fetch=lambda u, t: {"orders": [], "count": 0})
    assert row["measured"] is True and row["paid_orders"] == 0
    line = _row(tmp_path, row)
    assert "GREEN" in line and "0 paid orders" in line and row["at"] in line


def test_incident_crew70_a_payment_names_who_how_much_when(monkeypatch, tmp_path):
    monkeypatch.setenv("MEDUSA_ADMIN_TOKEN", "x")
    orders = [{"id": "o1", "email": "a@x.io", "total": 12.5, "currency_code": "gbp", "created_at": "2026-08-20T10:00:00Z"},
              {"id": "o2", "email": "b@x.io", "total": 7.5, "currency_code": "gbp", "created_at": "2026-08-26T10:00:00Z"}]
    row = outcomes.collect_revenue(now=NOW, fetch=lambda u, t: {"orders": orders, "count": 2})
    assert (row["paid_orders"], row["total"], row["currency"], row["payers"]) == (2, 20.0, "gbp", ["a@x.io", "b@x.io"])
    assert (row["first_paid_at"], row["last_paid_at"]) == ("2026-08-20T10:00:00Z", "2026-08-26T10:00:00Z")
    line = _row(tmp_path, row)
    assert "GREEN" in line and "2 paid order(s)" in line and "20.0 gbp" in line


def test_incident_crew70_stale_row_is_not_run(tmp_path):
    old = {"at": "2026-08-20T00:00:00Z", "measured": True, "paid_orders": 0}
    line = _row(tmp_path, old)
    assert "NOT RUN" in line and "old" in line


def test_incident_crew70_revenue_is_a_declared_source():
    reg = json.loads((ROOT / "science" / "sources.json").read_text())
    src = {s["name"]: s for s in reg["sources"]}
    assert src["revenue"]["path"] == "revenue.jsonl" and src["revenue"]["stale_after_hours"] <= 24

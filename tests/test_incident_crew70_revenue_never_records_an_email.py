"""Incident crew#70 / crew#409 review: science/revenue.jsonl is committed to a public repository
and listed the paying customers' email addresses. The rule: a payer in the series is an opaque
identifier, and the scheduled measurement exists so the row is never older than a day. Rung 4.
"""
import importlib.util
import json
import os
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("outcomes", ROOT / "science" / "outcomes.py")
assert _spec is not None and _spec.loader is not None
outcomes = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(outcomes)
EMAIL = re.compile(r"[^@\s\"]+@[^@\s\"]+\.[a-z]{2,}", re.I)


def test_collect_revenue_records_opaque_payers():
    orders = [{"id": 1, "email": "Alice@Example.org", "total": 1000, "currency_code": "gbp", "created_at": "2026-08-01T00:00:00Z"},
              {"id": 2, "email": "alice@example.org", "total": 500, "currency_code": "gbp", "created_at": "2026-08-02T00:00:00Z"}]
    os.environ["MEDUSA_ADMIN_TOKEN"] = "x"
    row = outcomes.collect_revenue(fetch=lambda u, t: {"orders": orders, "count": 2})
    assert row["payers"] == [outcomes.payer_id("alice@example.org")] and len(row["payers"][0]) == 12
    assert not EMAIL.search(json.dumps(row))


def test_the_committed_series_holds_no_email():
    path = ROOT / "science" / "revenue.jsonl"
    if path.exists():
        assert not EMAIL.search(path.read_text()), "an email address sits in a public series"


def test_the_measurement_is_scheduled_off_the_laptop():
    wf = (ROOT / ".github" / "workflows" / "revenue.yml").read_text()
    assert "cron:" in wf and "outcomes.py revenue" in wf and "MEDUSA_ADMIN_TOKEN" in wf

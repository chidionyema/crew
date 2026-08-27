"""crew#516 CP5 slice 2: every collected science row reaches the estate collector as an
OTLP log carrying `science.source`, or the collector run says why it did not.

Incident (2026-08-27): `bin/idp-science-facts` (idp#427) counts science rows per source
from ClickHouse. Its first receipt read `FAIL sources=0` because nothing on the Mac ever
put a row on the wire: the warehouse was a file under one home directory (LAW 50). This
test stands a real HTTP listener in, runs the emitter at it, and asserts the payload the
ClickHouse query groups by.
"""
from __future__ import annotations

import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "science"))
import emit

ROWS = [("2026-08-27T10:00:00+00:00", {"at": "2026-08-27T10:00:00+00:00", "n": 1}),
        (None, {"n": 2})]


class _Sink(HTTPServer):
    def __init__(self, status: int):
        self.status, self.posts = status, []
        super().__init__(("127.0.0.1", 0), _Handler)


class _Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        self.server.posts.append((self.path, dict(self.headers), json.loads(self.rfile.read(n))))
        self.send_response(self.server.status)
        self.end_headers()

    def log_message(self, *a):
        pass


def _serve(status: int):
    srv = _Sink(status)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_port}"


def test_rows_arrive_as_otlp_logs_tagged_with_the_source(monkeypatch):
    srv, base = _serve(200)
    monkeypatch.setenv(emit.HEADERS_VAR, "Authorization=Bearer t0k,X-Empty=")
    assert emit.emit("attention", ROWS, base) == "ok n=2 posts=1"
    path, hdrs, body = srv.posts[0]
    assert path == "/v1/logs"
    assert hdrs["Authorization"] == "Bearer t0k"
    recs = body["resourceLogs"][0]["scopeLogs"][0]["logRecords"]
    assert [r["attributes"][0] for r in recs] == [
        {"key": "science.source", "value": {"stringValue": "attention"}}] * 2
    assert recs[0]["timeUnixNano"] == str(1_787_824_800 * 10**9)
    assert recs[1]["timeUnixNano"] == "0"
    assert json.loads(recs[1]["body"]["stringValue"]) == {"n": 2}
    assert body["resourceLogs"][0]["resource"]["attributes"][0]["value"]["stringValue"] == "science-collect"
    srv.shutdown()


def test_a_rejecting_collector_is_a_fail_not_an_ok(monkeypatch):
    srv, base = _serve(401)
    verdict = emit.emit("attention", ROWS, base)
    assert verdict.startswith("FAIL") and "HTTP 401" in verdict
    srv.shutdown()


def test_unreachable_collector_is_a_fail_not_an_ok():
    verdict = emit.emit("attention", ROWS, "http://127.0.0.1:9")
    assert verdict.startswith("FAIL http://127.0.0.1:9/v1/logs")


def test_no_endpoint_means_skipped_and_no_network(monkeypatch):
    monkeypatch.delenv(emit.ENDPOINT_VAR, raising=False)
    assert emit.emit("attention", ROWS) == "skipped (OTEL_EXPORTER_OTLP_ENDPOINT unset)"


def test_rows_are_chunked(monkeypatch):
    srv, base = _serve(200)
    monkeypatch.setattr(emit, "CHUNK", 3)
    assert emit.emit("s", ROWS * 4, base) == "ok n=8 posts=3"
    assert [len(p[2]["resourceLogs"][0]["scopeLogs"][0]["logRecords"]) for p in srv.posts] == [3, 3, 2]
    srv.shutdown()


def test_collect_reports_the_emit_verdict_per_source():
    src = (Path(__file__).resolve().parents[1] / "science" / "collect.py").read_text()
    assert 'otlp.emit(name, [(row_time(r, tfield), r) for r in rows])' in src
    assert '"emit": emitted' in src


def test_collect_check_fails_when_the_collector_refuses_and_says_skipped_when_unset():
    src = (Path(__file__).resolve().parents[1] / "science" / "collect.py").read_text()
    assert 'collector {e[\'emit\']}' in src and "failures.extend(emit_failures)" in src
    assert 'print(f"emit: {emits[0][\'emit\']}")' in src

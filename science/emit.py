"""Emit every collected science row to the estate collector as an OTLP log (LAW 50).

WHY THIS FILE EXISTS. The warehouse `science/facts.db` is a file under one Mac's home.
`bin/idp-science-facts` (idp, crew#516 CP5) counts science rows per source from inside the
cluster's ClickHouse, grouped by the attribute `science.source`; until something puts that
attribute on the wire its receipt reads `FAIL sources=0`. This module is the something.

Shape: one OTLP/HTTP JSON request per chunk of rows, POSTed to
`$OTEL_EXPORTER_OTLP_ENDPOINT/v1/logs`. Each log record carries the row as its body,
`science.source` as an attribute and the row's own time as `timeUnixNano`.

Mature tool rejected: `opentelemetry-sdk` + `opentelemetry-exporter-otlp-proto-http`.
`science/collect.py` is a stdlib-only program run by a scheduler tick with no dependency
install step (crew#90: the tick runs main's code, nothing else), and the SDK's value here
(batching, retry, context propagation) is not needed for one hourly push per source. The
OTLP JSON encoding is the stable wire spec, and the payload is asserted by
tests/test_incident_crew516_science_rows_reach_the_collector.py.

Provider coupling: none. Any OTLP/HTTP receiver.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime

ENDPOINT_VAR = "OTEL_EXPORTER_OTLP_ENDPOINT"
HEADERS_VAR = "OTEL_EXPORTER_OTLP_HEADERS"
SOURCE_ATTR = "science.source"
SERVICE_NAME = "science-collect"
CHUNK = 500
TIMEOUT_SEC = 20


def endpoint() -> str | None:
    v = os.environ.get(ENDPOINT_VAR, "").strip().rstrip("/")
    return v or None


def headers() -> dict[str, str]:
    """`OTEL_EXPORTER_OTLP_HEADERS` in the spec's `k=v,k=v` form; a bare token is ignored."""
    out = {"Content-Type": "application/json"}
    for part in os.environ.get(HEADERS_VAR, "").split(","):
        if "=" in part:
            k, v = part.split("=", 1)
            if k.strip():
                out[k.strip()] = v.strip()
    return out


def _nanos(at: str | None) -> str:
    if not at:
        return "0"
    try:
        dt = datetime.fromisoformat(at.replace("Z", "+00:00"))
    except ValueError:
        return "0"
    return str(int(dt.timestamp() * 1_000_000_000))


def payload(source: str, rows: list[tuple[str | None, dict]]) -> dict:
    """OTLP/JSON `ExportLogsServiceRequest` for one source. `rows` are (row_time, row)."""
    records = [
        {
            "timeUnixNano": _nanos(at),
            "body": {"stringValue": json.dumps(row, separators=(",", ":"))},
            "attributes": [{"key": SOURCE_ATTR, "value": {"stringValue": source}}],
        }
        for at, row in rows
    ]
    return {
        "resourceLogs": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": SERVICE_NAME}},
                    ]
                },
                "scopeLogs": [{"scope": {"name": "science/collect.py"}, "logRecords": records}],
            }
        ]
    }


def emit(source: str, rows: list[tuple[str | None, dict]], base: str | None = None) -> str:
    """POST the rows in chunks. Returns `ok n=<rows> posts=<k>` or `FAIL <why>`.

    Unset endpoint returns `skipped` and touches no network: the Mac tick keeps working
    on a machine that has never been told where the collector is.
    """
    base = base or endpoint()
    if not base:
        return f"skipped ({ENDPOINT_VAR} unset)"
    url = f"{base}/v1/logs"
    posts = 0
    for i in range(0, len(rows), CHUNK):
        body = json.dumps(payload(source, rows[i:i + CHUNK])).encode()
        req = urllib.request.Request(url, data=body, headers=headers(), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
                if resp.status // 100 != 2:
                    return f"FAIL {url} -> HTTP {resp.status} after {posts} post(s)"
        except urllib.error.HTTPError as exc:
            return f"FAIL {url} -> HTTP {exc.code} after {posts} post(s)"
        except (urllib.error.URLError, OSError) as exc:
            return f"FAIL {url} -> {exc.reason if hasattr(exc, 'reason') else exc} after {posts} post(s)"
        posts += 1
    return f"ok n={len(rows)} posts={posts}"

#!/usr/bin/env python3
"""POST /notify -> a desktop notification. For agents that cannot pop a window.

    curl -s -XPOST 127.0.0.1:8081/notify -d '{"title":"crew","message":"CP2 green"}'

Bound to 127.0.0.1 on purpose. It executes osascript with text from the
request, so it is never exposed to a network. GET /health says it is up.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notify import desktop  # noqa: E402

PORT = int(os.environ.get("CREW_NOTIFY_PORT", "8081"))
LIMIT = 64 * 1024


class Handler(BaseHTTPRequestHandler):
    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._json(200, {"ok": True, "port": PORT})
        else:
            self._json(404, {"error": "POST /notify"})

    def do_POST(self) -> None:
        if self.path != "/notify":
            self._json(404, {"error": "POST /notify"})
            return
        n = int(self.headers.get("Content-Length") or 0)
        if n > LIMIT:
            self._json(413, {"error": "too long"})
            return
        try:
            data = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            self._json(400, {"error": "not json"})
            return
        title = str(data.get("title", "crew"))[:100]
        message = str(data.get("message", ""))[:1000]
        print(f"[{title}] {message}", flush=True)
        self._json(200, {"ok": desktop(title, message)})

    def log_message(self, *_a) -> None:
        pass


if __name__ == "__main__":
    print(f"notify on http://127.0.0.1:{PORT}/notify", flush=True)
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
